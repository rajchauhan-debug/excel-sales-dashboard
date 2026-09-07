import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    df = pd.read_excel("data/sales_data.xlsx")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df


df = load_data()


# ==================================================
# DASHBOARD HEADER
# ==================================================

st.title("CI/CD Pipeline ")
st.caption("Sales performance overview | Updated deployment")

# ==================================================
# SIDEBAR FILTERS
# ==================================================

st.sidebar.header("🔍 Dashboard Filters")

# Date Range Filter
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

selected_dates = st.sidebar.date_input(
    "📅 Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Handle selected date range
if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date = min_date
    end_date = max_date


# Region Filter
selected_regions = st.sidebar.multiselect(
    "📍 Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)


# Category Filter
selected_categories = st.sidebar.multiselect(
    "🛒 Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)


# ==================================================
# APPLY FILTERS
# ==================================================

filtered_df = df[
    (
        df["Order Date"].dt.date >= start_date
    )
    &
    (
        df["Order Date"].dt.date <= end_date
    )
    &
    (
        df["Region"].isin(selected_regions)
    )
    &
    (
        df["Category"].isin(selected_categories)
    )
].copy()


# ==================================================
# NO DATA CHECK
# ==================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No data available for the selected filters."
    )

    st.stop()


# ==================================================
# KPI CALCULATIONS
# ==================================================

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()

profit_margin = (
    total_profit / total_sales
) * 100


# ==================================================
# KPI CARDS
# ==================================================

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Sales",
        value=f"₹{total_sales:,.2f}"
    )

with col2:
    st.metric(
        label="📈 Total Profit",
        value=f"₹{total_profit:,.2f}"
    )

with col3:
    st.metric(
        label="📦 Total Orders",
        value=f"{total_orders:,}"
    )

with col4:
    st.metric(
        label="📊 Profit Margin",
        value=f"{profit_margin:.2f}%"
    )


# ==================================================
# SALES BY REGION
# ==================================================

region_sales = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
    .sort_values(
        by="Sales",
        ascending=False
    )
)


# ==================================================
# SALES BY CATEGORY
# ==================================================

category_sales = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
    .sort_values(
        by="Sales",
        ascending=False
    )
)


# ==================================================
# CHARTS - REGION AND CATEGORY
# ==================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("📍 Sales by Region")

    fig_region = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        text_auto=".2s",
        title="Total Sales by Region"
    )

    fig_region.update_layout(
        xaxis_title="Region",
        yaxis_title="Sales (₹)"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )


with col2:

    st.subheader("🛒 Sales by Category")

    fig_category = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        title="Sales Distribution by Category",
        hole=0.4
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# ==================================================
# MONTHLY SALES TREND
# ==================================================

st.divider()

st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .set_index("Order Date")
    .resample("ME")["Sales"]
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Performance"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales (₹)"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# ==================================================
# REGION-WISE SUMMARY
# ==================================================

st.divider()

st.subheader("📊 Region-Wise Performance")

region_summary = (
    filtered_df.groupby("Region")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order ID", "nunique")
    )
    .reset_index()
)

region_summary["Profit_Margin_Percent"] = (
    region_summary["Total_Profit"]
    /
    region_summary["Total_Sales"]
    * 100
).round(2)

st.dataframe(
    region_summary,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# CATEGORY-WISE SUMMARY
# ==================================================

st.subheader("📦 Category-Wise Performance")

category_summary = (
    filtered_df.groupby("Category")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order ID", "nunique")
    )
    .reset_index()
)

category_summary["Profit_Margin_Percent"] = (
    category_summary["Total_Profit"]
    /
    category_summary["Total_Sales"]
    * 100
).round(2)

st.dataframe(
    category_summary,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# FILTERED RAW DATA
# ==================================================

st.divider()

st.subheader("📋 Filtered Sales Dataset")

st.write(
    f"Showing {len(filtered_df)} of {len(df)} total records"
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)
import pandas as pd
import random
from datetime import datetime, timedelta

# Reproducible random data
random.seed(42)

regions = ["North", "South", "East", "West"]

categories = {
    "Electronics": ["Laptop", "Smartphone", "Headphones", "Tablet"],
    "Furniture": ["Chair", "Desk", "Table", "Sofa"],
    "Office Supplies": ["Notebook", "Pen", "Printer", "Paper"]
}

rows = []

start_date = datetime(2025, 1, 1)

for i in range(1, 501):

    category = random.choice(list(categories.keys()))
    product = random.choice(categories[category])

    order_date = start_date + timedelta(
        days=random.randint(0, 365)
    )

    sales = round(random.uniform(500, 50000), 2)

    profit_percentage = random.uniform(0.05, 0.25)
    profit = round(sales * profit_percentage, 2)

    rows.append({
        "Order ID": f"ORD-{i:04d}",
        "Order Date": order_date,
        "Region": random.choice(regions),
        "Category": category,
        "Product": product,
        "Sales": sales,
        "Profit": profit
    })

df = pd.DataFrame(rows)

df.to_excel(
    "data/sales_data.xlsx",
    index=False
)

print("Excel dataset created successfully!")
print(f"Total rows: {len(df)}")

print("\nFirst 5 rows:")
print(df.head())
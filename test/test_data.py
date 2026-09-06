import pandas as pd
from pathlib import Path


def test_excel_file_exists():
    file_path = Path("data/sales_data.xlsx")
    assert file_path.exists()


def test_excel_columns():
    file_path = "data/sales_data.xlsx"
    df = pd.read_excel(file_path)

    required_columns = [
        "Order ID",
        "Order Date",
        "Region",
        "Category",
        "Product",
        "Sales",
        "Profit"
    ]

    for column in required_columns:
        assert column in df.columns


def test_excel_not_empty():
    file_path = "data/sales_data.xlsx"
    df = pd.read_excel(file_path)

    assert len(df) > 0
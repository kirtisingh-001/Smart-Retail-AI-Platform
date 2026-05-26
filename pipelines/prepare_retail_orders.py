import pandas as pd
from pathlib import Path

RAW_FILE = Path("data/raw/retail_orders.csv")
PROCESSED_FILE = Path("data/processed/retail_orders_clean.csv")


def main():
    df = pd.read_csv(RAW_FILE)

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    print("Original Columns:")
    print(df.columns.tolist())

    # Convert dates
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce",
        dayfirst=True
    )

    df["ship_date"] = pd.to_datetime(
        df["ship_date"],
        errors="coerce",
        dayfirst=True
    )

    # Convert numeric columns
    numeric_cols = [
        "sales",
        "quantity",
        "discount",
        "profit",
        "shipping_cost"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Feature engineering
    df["ship_days"] = (df["ship_date"] - df["order_date"]).dt.days
    df["order_month"] = df["order_date"].dt.month
    df["order_year"] = df["order_date"].dt.year

    # profit margin safe calculation
    df["profit_margin"] = df["profit"] / (df["sales"] + 1)

    # sales category for classification
    df["sales_class"] = df["sales"].apply(
        lambda x: "Low" if x < 100 else ("Medium" if x < 500 else "High")
    )

    # Remove invalid rows
    df = df.dropna(
        subset=[
            "order_date",
            "ship_date",
            "sales",
            "quantity",
            "discount",
            "profit",
            "shipping_cost",
            "ship_days",
            "order_month",
            "order_year",
        ]
    )

    # Keep columns available in new dataset
    keep_columns = [
        "order_id",
        "order_date",
        "ship_date",
        "ship_mode",
        "customer_name",
        "segment",
        "state",
        "country",
        "market",
        "region",
        "product_id",
        "category",
        "sub_category",
        "product_name",
        "sales",
        "quantity",
        "discount",
        "profit",
        "shipping_cost",
        "order_priority",
        "year",
        "ship_days",
        "order_month",
        "order_year",
        "profit_margin",
        "sales_class",
    ]

    df = df[keep_columns]

    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_FILE, index=False)

    print("\nCLEAN DATASET CREATED SUCCESSFULLY")
    print("Saved at:", PROCESSED_FILE)
    print("Shape:", df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nPreview:")
    print(df.head())


if __name__ == "__main__":
    main()
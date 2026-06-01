# type: ignore

"""
Databricks Retail Data Engineering Pipeline

This file is designed to run inside Azure Databricks.
Databricks automatically provides:
- spark session
- display() function

Flow:
RAW CSV -> STAGED PARQUET -> CURATED PARQUET -> SPARK SQL OUTPUT
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    when,
    to_date,
    dayofmonth,
    month,
    dayofweek,
    avg,
    max as spark_max,
    sum as spark_sum
)

# Spark Session
try:
    spark
except NameError:
    spark = SparkSession.builder.appName("SmartRetailDataPipeline").getOrCreate()


def show_data(df, title):
    print(title)
    try:
        display(df)
    except NameError:
        df.show(20, truncate=False)


# Azure Storage Configuration

storage_account = "smartstorage321"

# Use Databricks secrets in real deployment.
# Example:
# storage_key = dbutils.secrets.get(scope="retail-scope", key="storage-key")

storage_key = "PASTE_STORAGE_ACCOUNT_KEY_IN_DATABRICKS_ONLY"

spark.conf.set(
    f"fs.azure.account.key.{storage_account}.blob.core.windows.net",
    storage_key
)

raw_path = f"wasbs://raw@{storage_account}.blob.core.windows.net/retail_sales.csv"
staged_path = f"wasbs://staged@{storage_account}.blob.core.windows.net/retail_sales_staged_parquet"
curated_path = f"wasbs://curated@{storage_account}.blob.core.windows.net/retail_sales_curated_parquet"
sql_output_path = f"wasbs://curated@{storage_account}.blob.core.windows.net/sql_analytics_parquet"

# RAW Layer

raw_df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(raw_path)
)

show_data(raw_df, "========== RAW DATA ==========")

# STAGED Layer
# Cleaning + Feature Engineering


staged_df = (
    raw_df
    .dropna()
    .withColumn("date", to_date(col("date")))
    .withColumn("day", dayofmonth(col("date")))
    .withColumn("month", month(col("date")))
    .withColumn("weekday", dayofweek(col("date")))
    .withColumn(
        "discount_flag",
        when(col("discount") > 10, "High").otherwise("Normal")
    )
)

show_data(staged_df, "========== STAGED DATA ==========")

staged_df.write.mode("overwrite").parquet(staged_path)

print("Staged parquet saved successfully!")


# CURATED Layer
# Aggregated Analytics-Ready Data


curated_df = (
    staged_df
    .groupBy("product", "category", "region")
    .agg(
        spark_sum("sales").alias("total_sales"),
        avg("sales").alias("avg_sales"),
        spark_max("sales").alias("max_sales"),
        avg("price").alias("avg_price"),
        spark_sum("discount").alias("total_discount")
    )
    .orderBy(col("total_sales").desc())
)

show_data(curated_df, "========== CURATED DATA ==========")

curated_df.write.mode("overwrite").parquet(curated_path)

print("Curated parquet saved successfully!")


# Spark SQL Analytics


staged_df.createOrReplaceTempView("sales_table")

sql_result = spark.sql("""
SELECT
    product,
    category,
    ROUND(AVG(sales), 2) AS avg_sales,
    MAX(sales) AS max_sales,
    SUM(sales) AS total_sales
FROM sales_table
GROUP BY product, category
ORDER BY total_sales DESC
""")

show_data(sql_result, "========== SPARK SQL ANALYTICS ==========")

sql_result.write.mode("overwrite").parquet(sql_output_path)

print("SQL analytics parquet saved successfully!")


# Final Status


print("DATA ENGINEERING PIPELINE COMPLETED SUCCESSFULLY")
print("RAW -> STAGED -> CURATED flow completed")
print("Staged parquet path:", staged_path)
print("Curated parquet path:", curated_path)
print("SQL analytics parquet path:", sql_output_path)
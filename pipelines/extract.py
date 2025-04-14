from pyspark.sql import SparkSession
import os

# Create Spark session
spark = SparkSession.builder \
    .appName("MarketingAnalyticsExtract") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Define paths
raw_data_path = "data/raw/marketing_campaign.csv"
delta_output_path = "data/processed/raw_delta/"

# Read CSV file
df = spark.read.option("header", True).option("inferSchema", True).csv(raw_data_path)

# Show schema and preview
df.printSchema()
df.show(10)

# Write to Delta Lake
df.write.format("delta").mode("overwrite").save(delta_output_path)

print("✅ Data extraction complete and saved to Delta format.")

# Stop Spark session
spark.stop()

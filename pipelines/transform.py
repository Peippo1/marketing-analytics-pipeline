from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, year
import os

# Start Spark session
spark = (
    SparkSession.builder.appName("MarketingAnalyticsTransform")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )
    .getOrCreate()
)

# Define input and output paths
delta_input_path = "data/processed/raw_delta/"
delta_output_path = "data/processed/clean_delta/"

# Load raw Delta data
df = spark.read.format("delta").load(delta_input_path)

# Clean & transform
df_clean = df.dropna(subset=["Income", "Age"])  # Drop rows with missing critical fields
df_clean = (
    df_clean.withColumnRenamed("MntWines", "SpendWines")
    .withColumnRenamed("MntFruits", "SpendFruits")
    .withColumnRenamed("MntMeatProducts", "SpendMeat")
    .withColumnRenamed("MntFishProducts", "SpendFish")
    .withColumnRenamed("MntSweetProducts", "SpendSweets")
    .withColumnRenamed("MntGoldProds", "SpendGold")
)

# Add derived columns
df_clean = df_clean.withColumn(
    "TotalSpend",
    col("SpendWines")
    + col("SpendFruits")
    + col("SpendMeat")
    + col("SpendFish")
    + col("SpendSweets")
    + col("SpendGold"),
)

df_clean = df_clean.withColumn(
    "AgeGroup",
    when(col("Age") < 30, "Under 30")
    .when((col("Age") >= 30) & (col("Age") < 50), "30-49")
    .otherwise("50+"),
)

# Preview transformed data
df_clean.printSchema()
df_clean.show(10)

# Save cleaned and enriched data as Delta
df_clean.write.format("delta").mode("overwrite").save(delta_output_path)

print("✅ Transformation complete and saved to Delta format.")

# Stop Spark session
spark.stop()

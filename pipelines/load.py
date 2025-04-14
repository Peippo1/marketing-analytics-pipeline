from pyspark.sql import SparkSession

# Start Spark session
spark = SparkSession.builder \
    .appName("MarketingAnalyticsLoad") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Define input path
delta_input_path = "data/processed/clean_delta/"

# Load the transformed data
df = spark.read.format("delta").load(delta_input_path)

# Show sample data
df.printSchema()
df.show(10)

# Optional: write to another destination or register as a temporary table
df.createOrReplaceTempView("marketing_data_cleaned")

print("✅ Data loaded and ready for analysis or ML pipelines.")

# Stop Spark session
spark.stop()

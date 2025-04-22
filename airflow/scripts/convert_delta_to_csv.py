from pyspark.sql import SparkSession

# Start Spark with Delta Lake support
spark = SparkSession.builder \
    .appName("ConvertDeltaToCSV") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Load Delta table
df = spark.read.format("delta").load("../data/processed/clean_delta/")

# Convert and save as CSV
df.toPandas().to_csv("../data/processed/clean_delta.csv", index=False)

print("✅ Converted Delta to CSV.")

spark.stop()
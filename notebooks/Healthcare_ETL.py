# Databricks notebook source
# MAGIC %md
# MAGIC # Healthcare ETL Pipeline

# COMMAND ----------
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Note: In Databricks, the 'spark' session is already created for you automatically.
# You don't strictly need to manually build it, but keeping it won't break anything.
spark = SparkSession.builder.appName("HealthcareETL").getOrCreate()

# COMMAND ----------
df = spark.read.csv(
    "/FileStore/tables/diabetic_data.csv",
    header=True,
    inferSchema=True
)

# COMMAND ----------
clean_df = df.dropDuplicates()
clean_df = clean_df.fillna("Unknown")

# COMMAND ----------
clean_df.write.format("delta").mode("overwrite").save("/tmp/healthcare_delta")

# COMMAND ----------
display(clean_df)
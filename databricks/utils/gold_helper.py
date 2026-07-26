# Databricks notebook source
# MAGIC %run ../Utilities

# COMMAND ----------

import uuid
from pyspark.sql.window import *
from delta.tables import *

# COMMAND ----------

catalog = "insureallbi"
gold_schema = "gold"

# COMMAND ----------

def read_silver(entity_name: str) -> DataFrame:
    return spark.read.format("delta").load(f"{silver_path}/{entity_name}")
    print(f"Reading from silver: {silver_path}/{entity_name}")

# COMMAND ----------

def register_table(table_name):
    path = f"{gold_path}/{table_name}"
    spark.sql(f"""CREATE TABLE IF NOT EXISTS {catalog}.{gold_schema}.{table_name} 
              USING DELTA 
              LOCATION '{path}' """)
    print(f"Table registered: {table_name}")

# COMMAND ----------

def write_initial(df,table_name):
    path = f"{gold_path}/{table_name}"

    (df.write.format("delta")
     .mode("overwrite")
     .option("overwriteSchema", "true")
     .save(f"{path}"))
    
    print(f"Writen initial data to delta table: {path}")
    register_table(table_name)
    

# COMMAND ----------

def get_full_table_name(table_name):
    full_table_name = f"{catalog}.{gold_schema}.{table_name}"
    print(f"Full table name: {full_table_name}")
    return full_table_name

# COMMAND ----------

def validate_table(table_name):

    full_table_name = (get_full_table_name(table_name))

    df = spark.table(full_table_name)

    print("="*50)
    print("TABLE VALIDATION")
    print("="*50)
    print(f"Table : {full_table_name}")
    print(f"Count : {df.count()}")
    print("Schema:")
    df.printSchema()
    return True

# COMMAND ----------

def merge_scd1(df: DataFrame, target_table: str, business_key: str, hash_column: str):
    delta_table = DeltaTable.forName(spark, target_table)

    update_columns = {col: f"source.{col}" for col in df.columns}
    (delta_table.alias("target").merge(
          df.alias("source"),
          f"target.{business_key} = source.{business_key}")

    .whenMatchedUpdate(
          condition=f"""
          target.{hash_column} <> source.{hash_column}
          """,
          set=update_columns
        )
     .whenNotMatchedInsertAll()
     .execute())

    print(f"SCD1 merge completed for {target_table}")

# COMMAND ----------

def load_gold_table(df,table_name,business_key,hash_column):
    full_table_name = get_full_table_name(table_name)
    if not spark.catalog.tableExists(full_table_name):
        print(f"Table {table_name} does not exist. Writing initial data")
        write_initial(df,table_name)
    else:
        validate_table(table_name)
        print(f"{table_name} exists. Running SCD1 MERGE")
        merge_scd1(df,full_table_name,business_key,hash_column)


# COMMAND ----------

def merge_fact(df,target_table,business_key):
    delta_table = DeltaTable.forName(spark,target_table)

    (delta_table.alias("target")
     .merge(df.alias("source"),f"target.{business_key}=source.{business_key}")
     .whenNotMatchedInsertAll()
     .execute())

    print(f"Fact merge completed for {target_table}")

# COMMAND ----------

def load_fact(df,table_name,business_key):    
    full_table_name = get_full_table_name(table_name)
    if not spark.catalog.tableExists(full_table_name):
        print(f"Table {table_name} does not exist. Writing initial data")
        write_initial(df,table_name)
    else:
        validate_table(table_name)
        print(f"{table_name} exists. Running SCD1 MERGE")
        merge_fact(df,full_table_name,business_key)

# COMMAND ----------


# Databricks notebook source
# MAGIC %run ../Utilities

# COMMAND ----------

# MAGIC %run ./silver_helper

# COMMAND ----------

# MAGIC %run ../audit

# COMMAND ----------

dbutils.widgets.text("api_name","type entity")
entity_name = dbutils.widgets.get("api_name")

# COMMAND ----------

runid = generate_run_id()
start_audit(runid,f"silver_{entity_name}","Silver","{entity_name}")

# COMMAND ----------

df = spark.read.format("json")\
        .load(f"{bronze_path}/{entity_name}")
display(df)


# COMMAND ----------

df_raw = df.drop("_source_file","_index")
display(df_raw.limit(10))

# COMMAND ----------

clean_df = clean_dataset(df_raw)
casted_df = apply_schema(clean_df,f"{entity_name}")
display(casted_df.limit(10))


# COMMAND ----------

try:
    (casted_df.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .option("path",f"{silver_path}/{entity_name}")
        .save())
    end_audit(runid,"SUCCESS",record_count)
except Exception as e:    
    end_audit(runid,"FAILED",record_count,e)
    raise
    
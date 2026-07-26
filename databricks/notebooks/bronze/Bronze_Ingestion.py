# Databricks notebook source
dbutils.widgets.text("entity_name","")
entity_name = dbutils.widgets.get("entity_name")

print(f"Processing entity: {entity_name}")

# COMMAND ----------

# MAGIC %run ../Utilities

# COMMAND ----------

# MAGIC %run ./bronze_helper

# COMMAND ----------

# MAGIC %run ../audit

# COMMAND ----------

runid = generate_run_id()
start_audit(runid,f"bronze_{entity_name}","Bronze","{entity_name}")

# COMMAND ----------

output_path = f"abfss://bronze@{storage_account}.dfs.core.windows.net/{entity_name}"

try:
    df = fetch_rest_api_dataset(dataset_name = entity_name, per_page = 2000)
    record_count = len(df)
    df.write.format("json")\
        .mode("overwrite")\
        .save(output_path)
    end_audit(runid,"SUCCESS",record_count)
except Exception as e:
    print(e)
    end_audit(runid,"FAILED",record_count,e)
    raise


# COMMAND ----------


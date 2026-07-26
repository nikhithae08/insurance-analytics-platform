# Databricks notebook source
# MAGIC %run ../Utilities

# COMMAND ----------

# MAGIC %run ./gold_helper

# COMMAND ----------

# MAGIC %run ../audit

# COMMAND ----------

pipeline_name = "gold_dim_countries"
entity_name = "insurance_countries"
target_table = "dim_countries"
business_key = "country_id"
runid = generate_run_id()
layer = "Gold"
target_path = f"{gold_path}/{target_table}"

# COMMAND ----------

start_audit(runid,pipeline_name,layer,target_table)

# COMMAND ----------

silver_df = read_silver(entity_name)
display(silver_df.count())
display(silver_df.limit(100))

# COMMAND ----------

final_df = (silver_df
            .select("country_id","country_name")
            .withColumn("country_hash_key",sha2(concat_ws("|","country_name"),256))
            .withColumn("created_timestamp",current_timestamp())
            .withColumn("updated_timestamp",lit(None).cast("timestamp"))
            .withColumn("pipeline_name",lit(pipeline_name))
            .withColumn("record_source",lit("REST_API"))
            .withColumn("run_id",lit(runid)))

display(final_df)

# COMMAND ----------

record_count = final_df.count()

try:
    load_gold_table(final_df,target_table,"country_id","country_hash_key")
    end_audit(runid,"SUCCESS",record_count)
except Exception as e:
    end_audit(runid,"FAILED",record_count,e)
    raise

# COMMAND ----------

spark.sql("""Select * from insureallbi.gold.dim_countries""").display()

# COMMAND ----------


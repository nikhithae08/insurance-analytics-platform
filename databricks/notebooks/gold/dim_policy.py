# Databricks notebook source
# MAGIC %run ../Utilities

# COMMAND ----------

# MAGIC %run ./gold_helper

# COMMAND ----------

# MAGIC %run ../audit

# COMMAND ----------

pipeline_name = "gold_dim_policy"
entity_name = "insurance_policies"
target_table = "dim_policy"
business_key = "policy_code"
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

final_df = (silver_df.select("policy_code",col("name").alias("policy_name"),"category","base_premium_usd",
                             "coverage","currency","coverage_type","term_period","description","start_date","end_date","is_active")
                .withColumn("policy_hash_key",sha2(concat_ws("|","policy_name","category","base_premium_usd",
                            "coverage","currency","coverage_type","term_period","description",
                            "is_active"),256))
                .withColumn("created_timestamp",current_timestamp())
                .withColumn("updated_timestamp",lit(None).cast("timestamp"))
                .withColumn("pipeline_name",lit(pipeline_name))
                .withColumn("record_source",lit("REST_API"))
                .withColumn("run_id",lit(runid)))

display(final_df)

# COMMAND ----------

record_count = final_df.count()

try:
    load_gold_table(final_df,target_table,"policy_code","policy_hash_key")
    end_audit(runid,"SUCCESS",record_count)
except Exception as e:
    end_audit(runid,"FAILED",record_count,e)
    raise

# COMMAND ----------

spark.sql("""Select * from insureallbi.gold.dim_policy""").display()

# COMMAND ----------


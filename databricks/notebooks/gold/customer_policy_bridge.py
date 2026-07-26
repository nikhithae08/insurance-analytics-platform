# Databricks notebook source
# MAGIC %run ../Utilities

# COMMAND ----------

# MAGIC %run ./gold_helper

# COMMAND ----------

# MAGIC %run ../audit

# COMMAND ----------

pipeline_name = "gold_fact_customer_policy"
entity_name = "customer_policies"
target_table = "fact_customer_policy"
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
            .select("customer_id","policy_id","policy_enroll_date")
            .withColumn("customer_policy_key",sha2(concat_ws("|","customer_id","policy_id"),256))
            .withColumn("created_timestamp",current_timestamp())            
            .withColumn("pipeline_name",lit(pipeline_name))
            .withColumn("record_source",lit("REST_API"))
            .withColumn("run_id",lit(runid)))

display(final_df)

# COMMAND ----------

record_count = final_df.count()

try:
    load_fact(final_df,target_table,"customer_policy_key")
    end_audit(runid,"SUCCESS",record_count)
except Exception as e:
    end_audit(runid,"FAILED",record_count,e)
    raise

# COMMAND ----------

spark.sql("""Select * from insureallbi.gold.customer_policy""").display()
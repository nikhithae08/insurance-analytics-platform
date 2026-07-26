# Databricks notebook source
# MAGIC %run ../Utilities

# COMMAND ----------

# MAGIC %run ./gold_helper

# COMMAND ----------

# MAGIC %run ../audit

# COMMAND ----------

pipeline_name = "gold_fact_claims"
entity_name = "insurance_claims"
target_table = "fact_claims"
business_key = "claim_id"
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

final_df = (silver_df.dropDuplicates(["claim_id"])
            .select("claim_id","customer_id","policy_id","claim_date","incident_date","claim_amount",
                    "claim_status","approval_date","settlement_amount","fraud_flag","channel","reported_delay_days")
            .withColumn("created_timestamp",current_timestamp())            
            .withColumn("pipeline_name",lit(pipeline_name))
            .withColumn("record_source",lit("REST_API"))
            .withColumn("run_id",lit(runid)))

display(final_df)

# COMMAND ----------

record_count = final_df.count()

try:
    load_fact(final_df,target_table,"claim_id")
    end_audit(runid,"SUCCESS",record_count)
except Exception as e:
    end_audit(runid,"FAILED",record_count,e)
    raise

# COMMAND ----------

spark.sql("""Select * from insureallbi.gold.fact_claims""").display()

# COMMAND ----------


# Databricks notebook source
# MAGIC %run ../Utilities

# COMMAND ----------

# MAGIC %run ./gold_helper

# COMMAND ----------

# MAGIC %run ../audit

# COMMAND ----------

pipeline_name = "gold_dim_agent"
entity_name = "insurance_agents"
target_table = "dim_agent"
business_key = "agent_id"
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
            .select("agent_id","agent_name","date_of_joining","experience_years","agent_email","agent_phone",
                    "agent_gender","city","state","country","agent_type","license_number","license_expiry_date",
                    "agent_status","branch_id","branch_name","zone","sales_team","manager_agent_id")
            .withColumn("agent_hash_key",sha2(concat_ws("|","agent_name","experience_years","agent_email",
                    "agent_phone","agent_status","branch_id","zone"),256))
            .withColumn("created_timestamp",current_timestamp())
            .withColumn("updated_timestamp",lit(None).cast("timestamp"))
            .withColumn("pipeline_name",lit(pipeline_name))
            .withColumn("record_source",lit("REST_API"))
            .withColumn("run_id",lit(runid)))
display(final_df)


# COMMAND ----------

record_count = final_df.count()

try:
    load_gold_table(final_df,target_table,"agent_id","agent_hash_key")
    end_audit(runid,"SUCCESS",record_count)
except Exception as e:
    end_audit(runid,"FAILED",record_count,e)
    raise

# COMMAND ----------

spark.sql("""Select * from insureallbi.gold.dim_agent""").display()
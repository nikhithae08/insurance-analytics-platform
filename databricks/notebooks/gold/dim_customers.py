# Databricks notebook source
# MAGIC %run ../Utilities

# COMMAND ----------

# MAGIC %run ./gold_helper

# COMMAND ----------

# MAGIC %run ../audit

# COMMAND ----------

pipeline_name = "gold_dim_customers"
entity_name = "insurance_customers"
target_table = "dim_customers"
business_key = "customer_id"
runid = generate_run_id()
layer = "Gold"
target_path = f"{gold_path}/{target_table}"

# COMMAND ----------

start_audit(runid,pipeline_name,layer,target_table)

# COMMAND ----------

customer_df = read_silver(entity_name)
display(customer_df.count())
display(customer_df.limit(100))

# COMMAND ----------

cleaned_df = customer_df.filter(col("customer_id").isNotNull())\
                .filter(col("is_active")==True)

display(cleaned_df.count())

# COMMAND ----------

final_df = (cleaned_df.select("customer_id",col("name").alias("customer_name"),"gender",
                             "occupation","city","state","country","email","phone",
                             col("Channel").alias("channel"),"nominee_relation","start_date",
                             "end_date","is_active")
                #change detection hash
                .withColumn("customer_hash_key",sha2(concat_ws("|",
                        coalesce(col("customer_name"), lit("")),
                        coalesce(col("gender"), lit("")),
                        coalesce(col("occupation"), lit("")),
                        coalesce(col("city"), lit("")),
                        coalesce(col("state"), lit("")),
                        coalesce(col("country"), lit("")),
                        coalesce(col("email"), lit("")),
                        coalesce(col("phone"), lit("")),
                        coalesce(col("channel"), lit("")),
                        coalesce(col("nominee_relation"), lit(""))),256))
                .withColumn("created_timestamp",current_timestamp())
                .withColumn("updated_timestamp",lit(None).cast("timestamp"))
                .withColumn("pipeline_name",lit(pipeline_name))
                .withColumn("record_source",lit("REST_API"))
                .withColumn("run_id",lit(runid)))

display(final_df)

# COMMAND ----------

record_count = final_df.count()

try:
    load_gold_table(final_df,target_table,"customer_id","customer_hash_key")
    end_audit(runid,"SUCCESS",record_count)
except Exception as e:
    end_audit(runid,"FAILED",record_count,e)
    raise

# COMMAND ----------

spark.sql("""Select * from insureallbi.gold.dim_customers""").display()

# COMMAND ----------


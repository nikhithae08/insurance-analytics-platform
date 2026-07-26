# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import * 
from pyspark.sql import Row
from datetime import datetime
from delta.tables import DeltaTable
import uuid

# COMMAND ----------

audit_schema = StructType([
    StructField("run_id", StringType(), False),
    StructField("pipeline_name", StringType(), False),
    StructField("layer", StringType(), False),
    StructField("table_name", StringType(), False),
    StructField("start_time", TimestampType(), True),
    StructField("end_time", TimestampType(), True),
    StructField("status", StringType(), True),
    StructField("records_processed", LongType(), True),
    StructField("error_message", StringType(), True)
])

# COMMAND ----------

empty_df = spark.createDataFrame([],audit_schema)

empty_df.write.format("delta").mode("overwrite").saveAsTable("insureallbi.gold.audit")

# COMMAND ----------

def generate_run_id():
    return str(uuid.uuid4())

# COMMAND ----------

def start_audit(run_id,pipeline_name,layer,table_name):
    row = Row(run_id=run_id,pipeline_name=pipeline_name,
              layer=layer,table_name=table_name,start_time=datetime.now(),end_time=None,status="STARTED",records_processed=0,error_message=None)
    (spark.createDataFrame([row],audit_schema).write
     .mode("append")
     .saveAsTable("insureallbi.gold.audit"))

# COMMAND ----------

def end_audit(run_id,status,records_processed,error_message=None):
    audit = DeltaTable.forName(spark,"insureallbi.gold.audit")
    audit.update(
    condition=f"run_id='{run_id}'",
    set={
        "end_time": current_timestamp(),
        "status": lit(status),
        "records_processed": lit(records_processed),
        "error_message": lit(error_message)}
    )
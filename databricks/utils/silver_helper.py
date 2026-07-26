# Databricks notebook source
# MAGIC %run ./Utilities

# COMMAND ----------

def clean_dataset(df):

    # 1. Trim strings
    for c, t in df.dtypes:
        if t == "string":
            df = df.withColumn(c, trim(col(c)))

    # 2. Standardize nulls
    for c, t in df.dtypes:
        if t == "string":
            df = df.withColumn(
                c,
                when(col(c).isin("", " ", "null", "N/A"), None)
                .otherwise(col(c))
            )

    # 3. Remove duplicates
    df = df.dropDuplicates()
    return df


# COMMAND ----------

schema_registry = {
    
    "insurance_policies": {
        "policy_code": StringType(),
        "name": StringType(),
        "category": StringType(),
        "base_premium_usd": DoubleType(),
        "coverage": StringType(),
        "currency": StringType(),     
        "coverage_type": StringType(),   
        "term_period": StringType(),
        "description": StringType(),
        "start_date":TimestampType(),
        "end_date":TimestampType(),
        "is_active": BooleanType(),
        "_index": LongType()
    },

      "insurance_agents": {
        "agent_id": IntegerType(),
        "agent_name": StringType(),
        "date_of_joining":TimestampType(),
        "experience_years": IntegerType(),  
        "region_id  ": IntegerType(),
        "id_deleted":BooleanType(),
        "agent_email":StringType(),
        "agent_phone":StringType(),
        "agent_gender":StringType(),
        "date_of_birth":StringType(),
        "agent_address":StringType(),
        "city":StringType(),
        "state":StringType(),
        "country":StringType(),
        "agent_type":StringType(),
        "license_number":StringType(),
        "license_expiry_date":StringType(),
        "agent_status":StringType(),
        "total_policies_sold":IntegerType(),
        "total_commission_earned":DecimalType(),
        "rating":DecimalType(),
        "manager_agent_id":IntegerType(),
        "branch_id":IntegerType(),
        "branch_name":StringType(),
        "zone":StringType(),
        "sales_team":StringType(),
        "policies_sold_current_year":IntegerType(),
        "policies_sold_last_year":IntegerType(),
        "avg_policy_value":DecimalType(),
        "conversion_rate":DecimalType(),
        "customer_retention_rate":DecimalType(),
        "commission_rate":DecimalType(),
        "commission_paid_ytd":DecimalType(),
        "commission_pending":DecimalType(),
        "last_commission_date":StringType(),
        "kyc_verified":BooleanType(),
        "background_check_status":StringType(),
        "compliance_score":DecimalType(),
        "last_audit_date":StringType(),
        "last_login_channel":StringType(),
        "login_count_30_days":IntegerType(),
        "last_activity_timestamp":StringType(),
        "device_type":StringType(),
        "avg_response_time_minutes":IntegerType(),
        "complaints_handled":IntegerType(),
        "escalations_count":DecimalType(),
        "customer_satisfaction_score":StringType(),
        "record_created_timestamp":StringType(),
        "record_updated_timestamp":StringType(),
        "batch_id":StringType()
    },
      
    "insurance_customers": {
        "customer_id": IntegerType(),
        "name": StringType(),
        "dob": StringType(),
        "gender": StringType(),
        "occupation": StringType(),
        "address": StringType(),
        "city": StringType(),
        "state": StringType(),
        "country": StringType(),
        "pincode": IntegerType(),
        "email": StringType(),
        "phone": StringType(),
        "Channel": StringType(),
        "nominated": StringType(),
        "nominee_relation": StringType(),
        "start_date": TimestampType(),
        "end_date": TimestampType(),
        "is_active":BooleanType()
    },

    "insurance_countries": {
        "country_id": IntegerType(),
        "country_name": StringType(),
        "_index": LongType()
    },

    "payment_frequency": { 
        "customer_id": IntegerType(),
        "payment_frequency": StringType(),
        "start_date": TimestampType(),
        "end_date": TimestampType(),
        "_index": IntegerType()
    },
    
    "insurance_payments": {
        "customer_id": IntegerType(),
        "policy_id": StringType(),
        "payment_date": TimestampType(),
        "payment_amount": DoubleType(),
        "payment_frequency": StringType(),
        "payment_mode": StringType(),
        "payment_status": StringType(),
        "transaction_id": StringType(),
        "_index": LongType()
    },

    "insurance_claims": {
        "claim_id": StringType(),
        "customer_id": IntegerType(),
        "policy_id": StringType(),
        "claim_date":TimestampType(),
        "incident_date":TimestampType(),
        "claim_amount": DoubleType(),
        "claim_status": StringType(),
        "approval_date": StringType(),
        "settlement_amount": StringType(),
        "fraud_flag": StringType(),
        "channel":StringType(),
        "reported_delay_days":IntegerType(),
        "_index": LongType()
    },

     "customer_policies": {
        "customer_id": IntegerType(),
        "policy_id": StringType(),
        "policy_enroll_date": TimestampType(),
        "_index": LongType()
    },
}

# COMMAND ----------

def apply_schema(df,dataset_name):
    if dataset_name  in schema_registry:
        schema = schema_registry[dataset_name]
    else:
        raise Exception(f"Schema not found for dataset: {dataset_name}")
    cast_df = df
    for col_name, col_type in schema.items():
        if col_name in cast_df.columns:
            cast_df = cast_df.withColumn(col_name, col(col_name).try_cast(col_type))
    return cast_df

# COMMAND ----------


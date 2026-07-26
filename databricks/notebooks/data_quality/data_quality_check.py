# Databricks notebook source
# DBTITLE 1,Cell 1
from pyspark.sql.functions import *

# COMMAND ----------

import uuid
run_id = str(uuid.uuid4())

# COMMAND ----------

# MAGIC %run ./audit

# COMMAND ----------

run_id = generate_run_id()
start_audit(run_id,"data_quality","DQ","All Tables")


# COMMAND ----------

dim_customers = spark.table(
    "insureallbi.gold.dim_customers"
)

dim_policy = spark.table(
    "insureallbi.gold.dim_policy"
)

dim_agent = spark.table(
    "insureallbi.gold.dim_agent"
)

dim_countries = spark.table(
    "insureallbi.gold.dim_countries"
)

fact_claims = spark.table(
    "insureallbi.gold.fact_claims"
)

fact_payments = spark.table(
    "insureallbi.gold.fact_payments"
)

fact_customer_policy = spark.table(
    "insureallbi.gold.fact_customer_policy"
)

# COMMAND ----------

print("Running dim_customer quality checks")

customer_count = dim_customers.count()
print(f"Total customer records: {customer_count}")

null_customer_id = dim_customers.filter(col("customer_id").isNull()).count()
null_customer_name = dim_customers.filter(col("customer_name").isNull()).count()
duplicate_customer = dim_customers.groupBy("customer_id").count().filter(col("count") > 1).count()

if null_customer_id > 0 or null_customer_name > 0 or duplicate_customer > 0:
    raise Exception(f"""dim_customer Data Quality Failed
    NULL customer_id: {null_customer_id}
    NULL customer_name: {null_customer_name}
    Duplicate customer_id: {duplicate_customer}
    """)
else:
    print("dim_customer Data Quality Passed")


# COMMAND ----------

print("Running dim_policy quality checks")

policy_count = dim_policy.count()
print(f"Total policy records: {policy_count}")

null_policy_code = dim_policy.filter(col("policy_code").isNull()).count()
duplicate_policy = dim_policy.groupBy("policy_hash_key").count().filter(col("count") > 1).count()
invalid_premium = dim_policy.filter(col("base_premium_usd") < 0).count()

if null_policy_code > 0 or duplicate_policy > 0 or invalid_premium > 0:
    raise Exception(f"""dim_policy Data Quality Failed

NULL policy_code: {null_policy_code}
Duplicate policy_code: {duplicate_policy}
Negative premium: {invalid_premium}
""")
else:
    print("dim_policy Data Quality Passed")


# COMMAND ----------

print("Running dim_agent quality checks")

agent_count = dim_agent.count()
print(f"Total agent records: {agent_count}")

null_agent_id = dim_agent.filter(col("agent_id").isNull()).count()
duplicate_agent = dim_agent.groupBy("agent_id").count().filter(col("count") > 1).count()

if null_agent_id > 0 or duplicate_agent > 0:
    raise Exception(f"""dim_agent Data Quality Failed

NULL agent_id: {null_agent_id}
Duplicate agent_id: {duplicate_agent}
""")
else:
    print("dim_agent Data Quality Passed")


# COMMAND ----------

print("Running dim_country quality checks")

country_count = dim_countries.count()
print(f"Total country records: {country_count}")

null_country_id = dim_countries.filter(col("country_id").isNull()).count()
null_country_name = dim_countries.filter(col("country_name").isNull()).count()
duplicate_country = dim_countries.groupBy("country_id").count().filter(col("count") > 1).count()

if null_country_id > 0 or null_country_name > 0 or duplicate_country > 0:
    raise Exception(f"""dim_country Data Quality Failed

NULL country_id: {null_country_id}
NULL country_name: {null_country_name}
Duplicate country_id: {duplicate_country}
""")
else:
    print("dim_country Data Quality Passed")


# COMMAND ----------

print("Running fact_claims quality checks")

claim_count = fact_claims.count()
print(f"Total claims: {claim_count}")

null_claim_id = fact_claims.filter(col("claim_id").isNull()).count()
null_customer_id = fact_claims.filter(col("customer_id").isNull()).count()
null_policy_id = fact_claims.filter(col("policy_id").isNull()).count()

duplicate_claims = fact_claims.groupBy("claim_id").count().filter(col("count") > 1).count()

invalid_claim_amount = fact_claims.filter(col("claim_amount") < 0).count()
invalid_settlement_amount = fact_claims.filter(col("settlement_amount").try_cast("double") < 0).count()

invalid_customer_reference = (
    fact_claims
    .join(dim_customers,"customer_id","left")
    .filter(dim_customers.customer_id.isNull())
    .count()
)

if (null_claim_id > 0 or null_customer_id > 0 or null_policy_id > 0 or
    duplicate_claims > 0 or invalid_claim_amount > 0 or
    invalid_settlement_amount > 0 or invalid_customer_reference > 0 ):

    raise Exception(f"""fact_claims Data Quality Failed

NULL claim_id: {null_claim_id}
NULL customer_id: {null_customer_id}
NULL policy_id: {null_policy_id}
Duplicate claims: {duplicate_claims}
Negative claim amount: {invalid_claim_amount}
Negative settlement amount: {invalid_settlement_amount}
Invalid customer reference: {invalid_customer_reference}
""")
else:
    print("fact_claims Data Quality Passed")


# COMMAND ----------

print("Running fact_payments quality checks")

payment_count = fact_payments.count()
print(f"Total payments: {payment_count}")

null_transaction_id = fact_payments.filter(col("transaction_id").isNull()).count()

duplicate_transactions = fact_payments.groupBy("transaction_id").count().filter(col("count") > 1).count()

invalid_payment_amount = fact_payments.filter(col("payment_amount") < 0).count()

invalid_customer_reference = (
    fact_payments
    .join(dim_customers,"customer_id","left")
    .filter(dim_customers.customer_id.isNull())
    .count()
)
invalid_policy = (
    fact_customer_policy
    .join(dim_policy,fact_customer_policy.policy_id == dim_policy.policy_code,"left")
    .filter(dim_policy.policy_code.isNull())
    .count()
)

if null_transaction_id > 0 or duplicate_transactions > 0 or invalid_payment_amount > 0 or invalid_customer_reference > 0:
    raise Exception(f"""fact_payments Data Quality Failed

NULL transaction_id: {null_transaction_id}
Duplicate transactions: {duplicate_transactions}
Negative payment amount: {invalid_payment_amount}
Invalid customer reference: {invalid_customer_reference}
""")
else:
    print("fact_payments Data Quality Passed")


# COMMAND ----------

print("Running customer_policy_bridge quality checks")

null_bridge_key = fact_customer_policy.filter(col("customer_policy_key").isNull()).count()

invalid_customer = (
    fact_customer_policy
    .join(dim_customers,"customer_id","left")
    .filter(dim_customers.customer_id.isNull())
    .count()
)

invalid_policy = (
    fact_customer_policy
    .join(dim_policy,fact_customer_policy.policy_id == dim_policy.policy_code,"left")
    .filter(dim_policy.policy_code.isNull())
    .count()
)

if null_bridge_key > 0  or invalid_customer > 0 or invalid_policy > 0:
    raise Exception(f"""customer_policy_bridge Data Quality Failed
    NULL bridge key: {null_bridge_key}    
    Invalid customer reference: {invalid_customer}
    Invalid policy reference: {invalid_policy}
    """)
else:
    print("customer_policy_bridge Data Quality Passed")


# COMMAND ----------

total_checks = (
    dim_customers.count()
    + dim_policy.count()
    + dim_agent.count()
    + dim_countries.count()
    + fact_claims.count()
    + fact_payments.count()
    + fact_customer_policy.count()
)


# COMMAND ----------

try:
    end_audit(run_id,"SUCCESS",total_checks)
except Exception as e:
    end_audit(run_id,"FAILURE",total_checks)
    raise 

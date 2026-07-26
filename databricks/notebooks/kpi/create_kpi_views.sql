-- Databricks notebook source
-- Policy KPIs
CREATE OR REPLACE VIEW insureallbi.gold.vw_policy_kpi AS

SELECT

COUNT(DISTINCT policy_code) AS total_policies,

COUNT(
CASE 
WHEN is_active = true 
THEN policy_code 
END
) AS active_policies,

round(AVG(base_premium_usd),4) AS avg_premium,

SUM(base_premium_usd) AS total_premium

FROM insureallbi.gold.dim_policy;

-- COMMAND ----------

select * from insureallbi.gold.vw_policy_kpi

-- COMMAND ----------

-- Claim KPIs
CREATE OR REPLACE VIEW insureallbi.gold.vw_claim_kpi AS

SELECT

COUNT(claim_id) AS total_claims,

round(SUM(claim_amount),2) AS total_claim_amount,

round(SUM(settlement_amount),2) AS total_settlement_amount,


COUNT(
CASE
WHEN claim_status='Approved'
THEN claim_id
END
)
AS approved_claims,


COUNT(
CASE
WHEN fraud_flag='true'
THEN claim_id
END
)
AS fraud_claims


FROM insureallbi.gold.fact_claims; 

-- COMMAND ----------

select * from insureallbi.gold.vw_claim_kpi

-- COMMAND ----------

-- Customer KPIs
CREATE OR REPLACE VIEW insureallbi.gold.vw_customer_kpi AS

SELECT

COUNT(customer_id)
AS total_customers,


COUNT(
CASE
WHEN is_active=true
THEN customer_id
END
)
AS active_customers,


COUNT(DISTINCT city)
AS customer_locations


FROM insureallbi.gold.dim_customers;

-- COMMAND ----------

select * from insureallbi.gold.vw_customer_kpi

-- COMMAND ----------

--Payment KPI's
CREATE OR REPLACE VIEW insureallbi.gold.vw_payment_kpi AS

SELECT

COUNT(transaction_id)
AS total_transactions,


SUM(payment_amount)
AS total_payment_amount,


round(AVG(payment_amount),2)
AS average_payment_amount,


COUNT(
CASE
WHEN payment_status='Success'
THEN transaction_id
END
)
AS successful_payments


FROM insureallbi.gold.fact_payments;

-- COMMAND ----------

select * from insureallbi.gold.vw_payment_kpi

-- COMMAND ----------

--Loss Ratio
CREATE OR REPLACE VIEW insureallbi.gold.vw_loss_ratio AS


SELECT

SUM(c.settlement_amount)
/
SUM(p.payment_amount)
AS loss_ratio


FROM insureallbi.gold.fact_claims c

JOIN

insureallbi.gold.fact_payments p

ON

c.policy_id = p.policy_id;

-- COMMAND ----------

select * from insureallbi.gold.vw_loss_ratio
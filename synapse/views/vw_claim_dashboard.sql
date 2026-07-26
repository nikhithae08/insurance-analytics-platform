CREATE OR ALTER VIEW dbo.claim_dashboard
AS
WITH claims AS
(
    SELECT *,
           ROW_NUMBER() OVER(
               PARTITION BY claim_id, customer_id, policy_id
               ORDER BY claim_date DESC
           ) AS rn
    FROM dbo.fact_claims
)
SELECT
    c.customer_name,
    c.state,
    p.category,
    f.claim_status,
    f.claim_amount,
    f.settlement_amount,
    f.fraud_flag,
    f.claim_date
FROM claims f
LEFT JOIN dbo.dim_customers c
    ON f.customer_id = c.customer_id
LEFT JOIN dbo.dim_policy p
    ON f.policy_id = p.policy_code
WHERE rn = 1;


GO

select top 10 * from dbo.claim_dashboard

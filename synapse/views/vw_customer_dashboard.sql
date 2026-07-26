CREATE OR ALTER VIEW dbo.customer_dashboard
AS

SELECT
    c.customer_id,
    c.customer_name,
    c.gender,
    c.occupation,
    c.city,
    c.state,
    c.country,
    c.channel,

    COUNT(DISTINCT p.policy_code) AS total_policies,

    SUM(p.base_premium_usd) AS total_premium

FROM dbo.dim_customers c

LEFT JOIN dbo.fact_claims f
ON c.customer_id = f.customer_id

LEFT JOIN dbo.dim_policy p
ON f.policy_id = p.policy_code

GROUP BY
    c.customer_id,
    c.customer_name,
    c.gender,
    c.occupation,
    c.city,
    c.state,
    c.country,
    c.channel;
GO

select top 10 * from customer_dashboard
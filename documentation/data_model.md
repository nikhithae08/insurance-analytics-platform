                     dim_customer
                     (Customer SK)
                           │
                           │
                           │
dim_policy ─────────── fact_claims ─────────── dim_agent
 (Policy SK)             (Claim Facts)         (Agent SK)
                           │
                           │
                           │
                     dim_country
                     (Country SK)


                     fact_payments
                  (Payment Transactions)
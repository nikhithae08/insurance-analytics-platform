CREATE OR ALTER VIEW dbo.fact_payments
AS

SELECT *

FROM OPENROWSET
(
    BULK 'fact_payments/',
    DATA_SOURCE = 'GoldLake',
    FORMAT = 'DELTA'
) AS payments;
GO
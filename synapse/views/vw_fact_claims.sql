CREATE OR ALTER VIEW dbo.fact_claims
AS

SELECT *

FROM OPENROWSET
(
    BULK 'fact_claims/',
    DATA_SOURCE = 'GoldLake',
    FORMAT = 'DELTA'
) AS claims;
GO

SELECT TOP 10 * from dbo.fact_claims
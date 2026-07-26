CREATE VIEW dbo.dim_customers
AS

SELECT *

FROM OPENROWSET
(
    BULK 'dim_customers/',
    DATA_SOURCE = 'GoldLake',
    FORMAT='DELTA'
) AS customers;
GO

SELECT TOP 10 * FROM dbo.dim_customers;
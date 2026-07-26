CREATE OR ALTER VIEW dbo.dim_policy
AS

SELECT *

FROM OPENROWSET
(
    BULK 'dim_policy/',
    DATA_SOURCE = 'GoldLake',
    FORMAT = 'DELTA'
) AS policy;
GO

select top 10 * from dbo.dim_policy
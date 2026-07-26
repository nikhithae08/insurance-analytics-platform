CREATE OR ALTER VIEW dbo.dim_agent
AS

SELECT *

FROM OPENROWSET
(
    BULK 'dim_agent/',
    DATA_SOURCE = 'GoldLake',
    FORMAT = 'DELTA'
) AS policy;
GO
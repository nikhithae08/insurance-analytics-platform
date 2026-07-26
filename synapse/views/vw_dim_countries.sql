CREATE OR ALTER VIEW dbo.dim_countries
AS

SELECT *

FROM OPENROWSET
(
    BULK 'dim_countries/',
    DATA_SOURCE = 'GoldLake',
    FORMAT = 'DELTA'
) AS country;
GO
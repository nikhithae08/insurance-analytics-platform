CREATE MASTER KEY
ENCRYPTION BY PASSWORD = 'InsuranceAnalytics@12345';
GO

SELECT * FROM sys.symmetric_keys;
GO

CREATE DATABASE SCOPED CREDENTIAL SynapseManagedIdentity
WITH IDENTITY = 'Managed Identity';
GO

SELECT *
FROM sys.database_scoped_credentials;

CREATE EXTERNAL DATA SOURCE GoldLake
WITH
(
    LOCATION = 'abfss://gold@adlse2eproject.dfs.core.windows.net',
    CREDENTIAL = SynapseManagedIdentity
);
GO

SELECT *
FROM sys.external_data_sources;


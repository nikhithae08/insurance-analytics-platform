# Databricks notebook source
service_credential = dbutils.secrets.get(scope="az_secret_scope",key="client-secret-value")
storage_account = dbutils.secrets.get(scope="az_secret_scope",key="adls-name")
sp_client_id = dbutils.secrets.get(scope="az_secret_scope",key="client-id")
sp_tenant_id = dbutils.secrets.get(scope="az_secret_scope",key="tenant-id")

spark.conf.set(f"fs.azure.account.auth.type.{storage_account}.dfs.core.windows.net", "OAuth")
spark.conf.set(f"fs.azure.account.oauth.provider.type.{storage_account}.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set(f"fs.azure.account.oauth2.client.id.{storage_account}.dfs.core.windows.net", sp_client_id)
spark.conf.set(f"fs.azure.account.oauth2.client.secret.{storage_account}.dfs.core.windows.net", service_credential)
spark.conf.set(f"fs.azure.account.oauth2.client.endpoint.{storage_account}.dfs.core.windows.net", f"https://login.microsoftonline.com/{sp_tenant_id}/oauth2/token")

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

containers = {
    "bronze": f"abfss://bronze@{storage_account}.dfs.core.windows.net",
    "silver": f"abfss://silver@{storage_account}.dfs.core.windows.net",
    "gold": f"abfss://gold@{storage_account}.dfs.core.windows.net"
}

bronze_path = containers["bronze"]
silver_path = containers["silver"]
gold_path = containers["gold"]
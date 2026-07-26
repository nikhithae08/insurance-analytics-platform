# Databricks notebook source
# MAGIC %run ../Utilities

# COMMAND ----------

import requests
import json
import time

# COMMAND ----------

class RateLimitException(Exception):
        pass

# COMMAND ----------

def fetch_rest_api_dataset(dataset_name,per_page):

    #Creating Authentication token
    import base64

    username = dbutils.secrets.get(scope="az_secret_scope",key="rest-api-username")
    password = dbutils.secrets.get(scope="az_secret_scope",key="rest-api-password")
    credentials = f"{username}:{password}"
    token = base64.b64encode(credentials.encode()).decode()
    headers = {f"Authorization" : f"Basic {token}"}

    base_url = f"https://cloudanddatauniverse.com/wp-json/custom-api/datasets/{dataset_name}"
    
    #Retry logic and logging
    from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, wait_chain, before_sleep_log
    import logging
    logger = logging.getLogger(__name__)
    
    @retry(stop=stop_after_attempt(3), 
        wait=wait_chain(wait_fixed(60),wait_fixed(300)), 
        retry=retry_if_exception_type(RateLimitException),
        reraise=True,
        before_sleep=before_sleep_log(logger,logging.WARNING))

    def get_api(url):
        response = requests.get(url, headers=headers, timeout = 30)
        try:
            data = response.json()
        except:
             raise Exception(f"Invalid Response: {response.text}")
         
        if response.status_code == 200:
            return data
        if response.status_code == 429 or data.get("code") == "rate_limit_exceeded":
            print("Rate limit hit. Retrying...")
            raise RateLimitException("Rate limit exceeded")

        raise Exception(f"API Error: {data}")

    #Get Metadata
    first_url = f"{base_url}?page=1&per_page={per_page}"
    first_response = get_api(first_url)
    
    if "total_pages" in first_response:
        total_pages = int(first_response["total_pages"])
        print(f"Dataset: {dataset_name} -> Total pages: {total_pages}")
    else:
        raise Exception(f"Unexpected API response: {first_response}")

    #loop through pages
    all_recs = []
    for page in range(1,total_pages+1):
        url = f"{base_url}?page={page}&per_page={per_page}"
        print(f" Processing Page: {page}")
        response = get_api(url)
        if "data" not in response:
            raise Exception(f"Error on page {page}: {response}")
        rows = response["data"]
        all_recs.extend(rows)
        print(f"Fetched page {page}/{total_pages}")
        time.sleep(1)  

    print(f"Completed {dataset_name}. "
        f"Total records: {len(all_recs)}"
    )

    if not all_recs:
        raise Exception(f"No records returned for dataset {dataset_name}")

    #Create dataframe
    raw_df = spark.createDataFrame(all_recs)
    return raw_df 
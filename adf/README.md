# Azure Data Factory

# Metadata-Driven REST API Ingestion Framework using Azure Data Factory

## Overview

Developed a scalable REST API ingestion framework using **Azure Data Factory (ADF)** to automate data extraction from REST APIs and load data into **Azure Data Lake Storage Gen2 (ADLS)**.

The framework follows a **metadata-driven architecture**, enabling multiple API entities to be onboarded with minimal pipeline changes.

---

## Architecture

```
                 Entity Configuration
                         |
                         v
                +----------------+
                | Master Pipeline |
                | pl_master_api   |
                +----------------+
                         |
              Ingestion Type Decision
                         |
          +--------------+--------------+
          |                             |
          v                             v
 ADF Child Pipeline              Databricks Notebook
 pl_Ingest_RestAPI                Custom Processing

          |
          v

 Azure Data Lake Storage Gen2
      JSON Data Landing Zone
```

---

## Key Components

### Master Pipeline (`pl_master_api`)

- Acts as the orchestration layer for ingestion.
- Reads entity configuration dynamically.
- Determines the ingestion method based on `ingestionType`.
- Supports both:
  - Azure Data Factory pipeline execution for small to medium data.
  - Azure Databricks notebook execution for large data and custom processing.

---

### REST API Ingestion Pipeline (`pl_Ingest_RestAPI`)

- Reusable pipeline for REST API data extraction.
- Accepts dynamic parameters:
  - Entity name.
  - API endpoint path.
- Handles API pagination automatically.
- Stores API responses as JSON files in ADLS.

---

## Data Processing Flow

1. Reads API entity configuration.
2. Determines ingestion approach.
3. Retrieves total number of API pages.
4. Iterates through each page dynamically.
5. Extracts REST API data.
6. Writes JSON output files into ADLS.

Example output:

```
insurance_customers/
 |
 |-- insurance_customers_page_1.json
 |-- insurance_customers_page_2.json
 |-- insurance_customers_page_3.json
```

---

## Security Implementation

- Integrated **Azure Key Vault** for API credential management.
- Avoided storing sensitive credentials in pipeline code.
- Used secure linked services for authentication.

---

## Technology Stack

| Technology | Usage |
|---|---|
| Azure Data Factory | Pipeline orchestration and REST API ingestion |
| Azure Data Lake Storage Gen2 | Data landing and storage |
| Azure Databricks | Alternative ingestion and processing workloads for large data|
| Azure Key Vault | Secure credential management |
| REST API | Source data integration |
| JSON | Data storage format |

---

## Engineering Highlights

- Designed reusable and parameterized ADF pipelines.
- Implemented metadata-driven ingestion architecture.
- Built dynamic pagination handling for large API datasets.
- Added retry mechanisms and API throttling controls.
- Created scalable ingestion framework for multiple data entities.

---

## Skills Demonstrated

- Azure Data Factory Development
- REST API Integration
- Cloud ETL/ELT Design
- Metadata-Driven Framework Development
- Azure Data Lake Storage
- Azure Key Vault Integration
- Pipeline Parameterization
- Data Engineering Best Practices


# Azure Databricks Implementation


## Overview

This folder contains the Databricks implementation of the Insurance Analytics Platform.


## Technology

- Azure Databricks
- PySpark
- Delta Lake
- Unity Catalog


## Layers


## Bronze

Responsibilities:

- REST API ingestion
- Raw JSON processing
- Landing data into Delta tables


## Silver

Responsibilities:

- Schema enforcement
- Data cleansing
- Data type conversion
- Duplicate handling


## Gold

Responsibilities:

- Star schema creation
- Dimension loading
- Fact loading
- SCD Type 1 implementation


## Data Quality

Implemented checks:

- Null validation
- Duplicate checks
- Referential integrity


## Audit

Pipeline execution tracking using audit tables.


## Orchestration

Databricks Workflows used for:

Bronze → Silver → Gold → DQ → KPI
# Azure Databricks

# Enterprise Insurance Analytics Processing Platform using Azure Databricks

## Overview

Developed an end-to-end data processing framework using **Azure Databricks, PySpark, Delta Lake, and Unity Catalog** to transform raw insurance data into a business-ready analytics platform.

The Databricks implementation follows a **Medallion Architecture (Bronze → Silver → Gold)** and supports:

- Parameter-driven ingestion processing.
- Data cleansing and standardization.
- Dimensional data modeling.
- Incremental fact loading.
- Slowly Changing Dimension Type 1 implementation.
- Automated data quality validation.
- Pipeline execution auditing.

The framework processes insurance entities including:

- Customers
- Policies
- Agents
- Claims
- Payments
- Customer-Policy relationships

---

# Architecture

```
                         Azure Data Factory
                                |
                                |
                         Pipeline Parameters
                         Entity Name
                                |    
                                |
                                v

                    +----------------------+
                    | Bronze Layer         |
                    | Delta Lake           |
                    | Raw JSON Processing  |
                    +----------------------+

                                |
                                |
                                v

                    +----------------------+
                    | Silver Layer         |
                    | PySpark Processing   |
                    +----------------------+

                    Data Cleansing
                    Schema Enforcement
                    Standardization
                    Deduplication
                    Data Validation

                                |
                                |
                                v

                    +----------------------+
                    | Gold Layer           |
                    | Dimensional Model    |
                    +----------------------+

                    Dimensions
                    Facts
                    Bridge Tables

                                |
                                |
                                v

              +----------------+----------------+
              |                                 |
              v                                 v

      Data Quality Framework          Audit Framework

              |
              |
              v

        KPI Reporting Layer
```

---

# Key Components

## Bronze Layer

### Parameterized Data Ingestion Framework

The Bronze layer receives data from Azure Data Factory and stores raw source data in Delta format.

ADF passes dynamic parameter:

- Entity name

Example:

```
insurance_agents 
insurance_policies
insurance_customers
insurance_payments
insurance_countries
insurance_claims
customer_policies
payment_frequency
```

The same notebook framework processes multiple entities dynamically.

### Responsibilities:

- Read raw JSON files from ADLS Gen2.
- Preserve source data without business transformations.
- Maintain raw ingestion history.
- Enable data replay capability.

---

# Silver Layer

## Data Cleansing and Standardization Framework

The Silver layer transforms raw Bronze data into clean and analytics-ready Delta tables.

Separate processing notebooks were implemented to handle:

- Data ingested through Azure Data Factory.
- Data ingested directly through Databricks processing.

---

## Silver Processing Capabilities

Implemented transformations:

### Schema Enforcement

- Applied predefined schemas.
- Validated incoming columns.
- Standardized data types.

---

### Data Cleaning

Implemented:

- Null value standardization.
- String trimming.
- Date conversion.
- Numeric type casting.
- Invalid record handling.

---

### Duplicate Handling

Implemented:

- Business key-based duplicate removal.
- Latest record selection logic.

---

### Silver Files Created

```
silver

├── insurance_customers
├── insurance_policies
├── insurance_agents
├── insurance_countries
├── insurance_claims
└── insurance_payment
└── customer_policies
└── payment_frequency
```

---

# Gold Layer

## Dimensional Data Modeling

The Gold layer implements a business-ready analytics model using a **Star Schema approach**.

---

# Dimension Processing

Implemented dimension notebooks:

```
gold

├── dim_customer
├── dim_policy
├── dim_agent
└── dim_countries
```

---

## Slowly Changing Dimension Type 1 Implementation

Implemented:

- Business key-based matching.
- Hash-based change detection.
- Delta MERGE operations.
- Existing records updated when changes occur.

Example:

```
Customer Change

Old Email
    |
    |
Hash Comparison
    |
    |
Updated Dimension Record
```

---

# Fact Processing

Implemented incremental fact loading using Delta Lake MERGE.

Fact notebooks:

```
gold

├── fact_claims
└── fact_payments
└── fact_customer_policy
```

---

## Fact Processing Features

Implemented:

- Incremental loading.
- Deduplication.
- Business key validation.
- Audit column generation.

Fact tables:

```
fact_claims

fact_payments

```

---

# Bridge Table Processing

Implemented many-to-many relationship handling:

```
fact_customer_policy
```

Features:

- Customer-policy relationship mapping.
- Generated surrogate relationship key using SHA2 hashing.

---

# Data Quality Framework

Implemented centralized data quality validation using PySpark.

Notebook:

```
data_quality_check
```

---

## Validation Rules Implemented

### Dimension Checks

Examples:

- Record count validation.
- Primary key NULL checks.
- Duplicate record detection.
- Mandatory column validation.

---

### Fact Checks

Examples:

- Business key validation.
- Negative amount validation.
- Referential integrity checks.
- Duplicate transaction detection.

---

### Relationship Checks

Validated:

- Customer existence.
- Policy existence.
- Bridge table relationships.

---

# Audit Framework

Implemented pipeline execution tracking using Delta audit tables.

Notebook:

```
audit_logging
```

---

## Audit Information Captured

Tracks:

- Pipeline execution ID.
- Pipeline name.
- Layer name.
- Table name.
- Start time.
- End time.
- Execution status.
- Records processed.
- Error details.

Example:

```
Pipeline Run

Bronze
 |
Silver
 |
Gold
 |
DQ

Each step logged independently
```

---

# Reusable Utility Framework

Developed reusable PySpark utility functions to improve maintainability.

Utility modules:

```
utils

├── Utilities
├── silver_helper
├── gold_helper
└── audit_helper
```

---

## Utility Capabilities

### Schema Registry

Handles:

- Centralized schema definitions.
- Data type management.
- Schema consistency.

---

### Silver Helper Functions

Handles:

- Data cleansing.
- Standard transformations.
- Reusable processing logic.

---

### Gold Helper Functions

Handles:

- Dimension loading.
- Fact loading.
- Delta MERGE operations.
- SCD Type 1 processing.

---

### Audit Helper Functions

Handles:

- Pipeline logging.
- Execution status updates.
- Error tracking.

---

# Workflow Orchestration

Implemented Databricks Workflow Jobs for automated execution.

Workflow:

```
Bronze Ingestion

        |

Silver Transformations

        |

Gold Dimensions

        |

Gold Facts

        |

Data Quality Checks

        |

KPI Views
```

---

## Workflow Features

Implemented:

- Task dependency management.
- Parallel execution where applicable.
- Retry configuration.
- Failure handling.
- Scheduled execution.

Workflow definition:

```
workflows/

└── insurance_pipeline_job.yml
```

---

# Unity Catalog Implementation

Implemented Unity Catalog for:

- Data governance.
- Secure data access.
- Catalog and schema organization.

Catalog:

```
insureallbi
```

Schemas:

```
bronze

silver

gold
```

---

# Technology Stack

| Technology | Usage |
|---|---|
| Azure Databricks | Data processing and orchestration |
| PySpark | Data transformation framework |
| Delta Lake | Storage layer and ACID transactions |
| Unity Catalog | Data governance and security |
| Azure Data Lake Storage Gen2 | Data storage |
| Azure Data Factory | Parameter-driven ingestion orchestration |
| Python | Utility development |
| Databricks Workflows | Pipeline scheduling and execution |


---

# Engineering Highlights

- Designed scalable Medallion Architecture using Databricks.
- Implemented parameter-driven Bronze ingestion framework.
- Developed reusable PySpark transformation utilities.
- Built SCD Type 1 dimension processing using Delta MERGE.
- Implemented incremental fact loading framework.
- Designed enterprise-style data quality validation.
- Developed centralized audit logging framework.
- Implemented workflow orchestration using Databricks Jobs.
- Applied Delta Lake optimization and transactional processing.
- Used Unity Catalog for governance and security.

---

# Skills Demonstrated

- Azure Databricks Development
- PySpark Programming
- Delta Lake Architecture
- Medallion Architecture
- Data Modelling
- Star Schema Design
- SCD Type 1 Implementation
- Incremental Data Processing
- Data Quality Framework Development
- Pipeline Orchestration
- Unity Catalog Governance
- Cloud Data Engineering Best Practices
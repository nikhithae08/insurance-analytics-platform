                         ┌──────────────────────┐
                         │      REST APIs       │
                         │  External Data Source │
                         └──────────┬───────────┘
                                    │
                                    │  API Extraction
                                    │
                                    ▼
                    ┌─────────────────────────────┐
                    │     Azure Data Factory       │
                    │                              │
                    │  • Pipeline Orchestration    │
                    │  • API Ingestion             │
                    │  • Scheduling & Monitoring   │
                    └──────────────┬──────────────┘
                                   │
                                   │ Raw Data Landing
                                   │
                                   ▼
              ┌────────────────────────────────────────┐
              │        Azure Data Lake Storage Gen2    │
              │                 Bronze Layer           │
              │                                        │
              │  • Raw API JSON Responses              │
              │  • Immutable Source Data               │
              └──────────────────┬─────────────────────┘
                                 │
                                 │ Data Transformation
                                 │
                                 ▼
              ┌────────────────────────────────────────┐
              │          Azure Databricks               │
              │                                        │
              │  • Data Cleaning                       │
              │  • Transformation Logic                │
              │  • PySpark Processing                  │
              │  • Delta Lake Management               │
              └──────────────────┬─────────────────────┘
                                 │
                                 │ Curated Data
                                 │
                                 ▼
              ┌────────────────────────────────────────┐
              │             Silver Delta Lake          │
              │                                        │
              │  • Cleaned Data                        │
              │  • Standardized Schema                 │
              │  • Data Quality Applied                │
              └──────────────────┬─────────────────────┘
                                 │
                                 │ Business Aggregation
                                 │
                                 ▼
              ┌────────────────────────────────────────┐
              │              Gold Delta Lake           │
              │                                        │
              │  • Business-Level Tables               │
              │  • Aggregated Metrics                  │
              │  • Analytics Ready Data                 │
              └──────────────────┬─────────────────────┘
                                 │
                                 │ SQL Consumption
                                 │
                                 ▼
              ┌────────────────────────────────────────┐
              │      Azure Synapse Serverless SQL      │
              │                                        │
              │  • External Table Access               │
              │  • SQL Analytics Layer                 │
              │  • Ad-hoc Querying                     │
              └──────────────────┬─────────────────────┘
                                 │
                                 │ Reporting & Insights
                                 │
                                 ▼
              ┌────────────────────────────────────────┐
              │                Power BI                 │
              │                                        │
              │  • Dashboards                          │
              │  • Reports                             │
              │  • Business Intelligence               │
              └────────────────────────────────────────┘

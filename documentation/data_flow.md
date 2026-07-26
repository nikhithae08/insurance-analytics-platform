          REST API
              │
              ▼
      Extract Insurance Data
              │
              ▼
   Azure Data Factory Pipeline
              │
              ▼
 Bronze Layer (Raw JSON Files)
              │
              ▼
     Silver Transformations
──────────────────────────────────
• Schema Enforcement
• Data Type Casting
• Null Handling
• Duplicate Removal
• String Cleansing
──────────────────────────────────
              │
              ▼
 Gold Layer
──────────────────────────────────
• Dimension Tables
• Fact Tables
• SCD Type 1
• Delta MERGE
• Incremental Loading
──────────────────────────────────
              │
              ▼
 Data Quality & Audit Validation
              │
              ▼
 Synapse Serverless SQL Views
              │
              ▼
 Power BI Claims Dashboard
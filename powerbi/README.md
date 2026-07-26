# Power BI Reporting Layer

## Overview

Implemented Power BI reporting layer for the Insurance Analytics Platform.

The dashboard consumes reporting views from Azure Synapse Serverless SQL and provides business insights into insurance claims analytics.

---

## Architecture

```
Azure Databricks Gold Layer

        |

        |

Azure Synapse Serverless SQL

        |

        |

Power BI Dashboard
```

---

## Dashboard

### Claims Dashboard

Created dashboard to analyze insurance claim performance.

Includes:

- Total Claims by Year
- Total Claims by State
- Total Claims by fraud_flag
- Total Claim Amount by Category


---

## Data Source

Connected to:

Azure Synapse Serverless SQL

Reporting View:

```
dbo.claim_dashboard
```

---

## Folder Structure

```
powerbi

├── screenshots

├── dashboard_documentation

└── README.md
```

---

## Technology Stack

| Technology | Usage |
|---|---|
| Power BI | Dashboard development |
| Azure Synapse Serverless SQL | Reporting data source |
| Azure Databricks | Data processing |
| Delta Lake | Data storage |

---

## Engineering Highlights

- Built business-focused Power BI dashboard.
- Connected Power BI with Synapse Serverless SQL views.
- Created reporting layer on top of curated Gold data.
- Documented dashboard design and metrics.
# Azure Synapse Serverless SQL

## Overview

Implemented Azure Synapse Serverless SQL Pool as the serving layer for the Insurance Analytics Platform.

The Synapse layer provides SQL-based access to the Gold Delta tables stored in Azure Data Lake Storage Gen2 and prepares analytics-ready datasets for Power BI reporting.

---

## Architecture

```
Azure Databricks Gold Layer

        |

        |

Azure Data Lake Storage Gen2

        |

        |

Azure Synapse Serverless SQL Pool

        |

        |

SQL Views

        |

        |

Power BI
```

---

## Folder Structure

```
synapse

├── setup
│
├── views
│
└── README.md
```

---

## Setup

The setup folder contains Synapse configuration scripts required to connect Serverless SQL Pool with the Databricks Gold Delta layer.

Includes:

- Database creation
- Database master key configuration
- Database scoped credential
- External data source configuration

---

## Views

The views folder contains SQL views created on top of Gold Delta tables.

### Dimension Views

- vw_dim_customers
- vw_dim_policy
- vw_dim_agent
- vw_dim_countries


### Fact Views

- vw_fact_claims
- vw_fact_payments


### Reporting Views

Created simplified reporting datasets for Power BI consumption:

- vw_claim_dashboard
- vw_customer_dashboard

---

## Technology Stack

| Technology | Usage |
|---|---|
| Azure Synapse Serverless SQL | Analytics serving layer |
| Azure Data Lake Storage Gen2 | Delta data storage |
| Azure Databricks | Gold layer processing |
| Delta Lake | Data storage format |
| Power BI | Reporting layer |

---

## Engineering Highlights

- Implemented Azure Synapse Serverless SQL architecture.
- Enabled direct querying of Delta tables stored in ADLS Gen2.
- Created reusable SQL views for analytics consumption.
- Designed reporting datasets for Power BI integration.
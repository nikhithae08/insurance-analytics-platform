# Deployment Documentation

## Overview

This folder contains the deployment documentation/screenshots for the Insurance Analytics Platform.

Azure DevOps CI/CD pipelines were implemented to automate the deployment of Azure Data Factory and Azure Databricks components using GitHub source control and Azure DevOps release workflows.

The deployment process enables version-controlled, repeatable, and automated deployment of data engineering assets.

---

## CI/CD Workflow

```text
GitHub Repository
        |
        v
Azure DevOps CI Pipeline
        |
        v
Build Artifact
        |
        v
Azure DevOps CD Pipeline
        |
        v
Azure Cloud Resources
        |
        +-----------------------+
        |                       |
        v                       v
Azure Data Factory       Azure Databricks
Deployment               Deployment
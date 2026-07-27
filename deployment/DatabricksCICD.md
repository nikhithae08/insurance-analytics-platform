# Azure Databricks CI/CD Deployment

## Overview

Azure Databricks CI/CD deployment was implemented using Azure DevOps and GitHub to automate the deployment of Databricks notebooks, PySpark code, and workflow configurations.

The deployment process enables version-controlled, repeatable, and automated delivery of Databricks data processing components.

## Deployment Flow

GitHub Repository  
↓  
Azure DevOps CI Pipeline  
↓  
Build Artifact  
↓  
Azure DevOps CD Pipeline  
↓  
Azure Databricks Workspace  

## CI Pipeline

The CI pipeline performs:

- Source code checkout from GitHub
- Validation of Databricks assets
- Build artifact creation
- Publishing deployment artifacts

## CD Pipeline

The CD pipeline performs:

- Artifact retrieval
- Azure authentication using service connection
- Deployment of Databricks notebooks and configurations
- Update of Databricks workspace assets

## Deployed Components

The deployment process manages:

- Bronze layer notebooks
- Silver layer transformation notebooks
- Gold layer analytics notebooks
- PySpark utility modules
- Databricks workflow configurations

## Technologies Used

- Azure Databricks
- Azure DevOps
- GitHub
- PySpark
- Delta Lake
- Azure Service Connections

## Deployment Status

Completed:

- Databricks source code integration with GitHub
- Azure DevOps CI pipeline
- Azure DevOps CD pipeline
- Automated Databricks deployment
- Deployment of notebooks and workflow configurations
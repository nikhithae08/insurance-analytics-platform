# Azure Data Factory CI/CD Deployment

## Overview

Azure Data Factory CI/CD deployment was implemented using Azure DevOps, GitHub, and ARM templates.

The deployment process automates the release of Azure Data Factory components, enabling version-controlled and repeatable deployments.

## Deployment Flow

GitHub Repository  
↓  
Azure DevOps CI Pipeline  
↓  
ADF ARM Template Artifact  
↓  
Azure DevOps CD Release Pipeline  
↓  
Azure Data Factory  

## CI Pipeline

The CI pipeline performs:

- Source code checkout from GitHub
- ADF validation
- ARM template generation
- Artifact creation and publishing

## CD Pipeline

The CD pipeline performs:

- Artifact retrieval
- Azure authentication using service connection
- ARM template deployment
- Azure Data Factory resource updates

## Deployed Components

The deployment process manages:

- Pipelines
- Datasets
- Linked Services
- Triggers
- Parameters

## Technologies Used

- Azure Data Factory
- Azure DevOps
- GitHub
- ARM Templates
- Azure Service Connections

## Deployment Status

Completed:

- Azure Data Factory GitHub integration
- ADF publish process
- ARM template generation
- Azure DevOps CI pipeline
- Azure DevOps CD release pipeline
- Automated ADF deployment
# Databricks Assets Bundle - Sample Repository

## Description
This repository offers a template-driven approach to facilitate the deployment of Databricks Workflows. Below is an overview of the contents:

### DAB_job_definitions/<job.yml>
- Contains job definition files. To create a new job, add a new yml file with the job definitions here.

### deploy/ <environment>
- Provides a reference to yml files that need deployment. Leave it empty if all deployed resources need deletion.

### scripts/databricks_deploy_template.yml
- **Purpose:** Templated Deployment File
- **Functionality:** 
  - Structures the configuration for deploying Databricks bundles.
  - Supports various resources like notebooks, jobs, etc.
  - Offers customizable variables and deployment targets.

### scripts/databricks_job_deployment.py
- **Purpose:** Starting Point for Deployment
- **Functionality:**
  - Generates Databricks.yml file based on the template scripts/databricks_deploy_template.yml.
  - Parses command-line arguments for environment and branch name. The environment-specific deployment file is referenced based on the environment name (e.g., if environment is "development", it refers to deploy/development).
  - Deploys all jobs referred to in the environment file.

### scripts/databricks_dev_cleanup.py
- **Purpose:** Cleanup Script
- **Functionality:**
  - Generates a Databricks YAML file for cleanup using the provided branch name.
  - Validates command-line arguments and provides usage instructions.
  - Replaces placeholders in the cleanup template file with the branch name.
  - Writes the modified content to the Databricks YAML file.

### scripts/databricks_destroy_template.yml
- **Purpose:** Templated Deletion File
- **Functionality:** 
  - Forms part of the configuration for deleting resources created by Databricks bundles.

## Authors and Acknowledgments
- Danny (Databricks SA)
- Akshata Nayak (Mantel Group)

## Project Status
This repository serves as a sample project, and there are no ongoing updates or contributions.

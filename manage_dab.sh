#!/bin/bash

set -e

# Usage function to display help
usage() {
    echo "Usage: $0 {deploy|destroy} <environment>"
    exit 1
}

# Check the number of arguments
if [ "$#" -ne 2 ]; then
    usage
fi

# Assign arguments to variables
ACTION=$1
ENVIRONMENT=$2

# Paths to scripts
DEPLOY_SCRIPT="scripts/databricks_job_deployment.py"
CLEANUP_SCRIPT="scripts/databricks_dev_cleanup.py"

# Function to deploy resources
deploy() {
    echo "Starting deployment to $ENVIRONMENT environment..."
    python3 $DEPLOY_SCRIPT $ENVIRONMENT
    echo "Deployment completed successfully."
}

# Function to destroy resources
destroy() {
    echo "Starting destruction in $ENVIRONMENT environment..."
    python3 $CLEANUP_SCRIPT $ENVIRONMENT
    echo "Cleanup completed successfully."
}

# Perform the requested action
case $ACTION in
    deploy)
        deploy
        databricks bundle init 
        databricks bundle validate
        databricks bundle deploy
        ;;
    destroy)
        destroy
        databricks bundle destroy
        ;;
    *)
        usage
        ;;
esac

.PHONY: deploy destroy

# Set the environment variable (e.g., development, test, production)
ENVIRONMENT ?= development

# Path to the deployment script
DEPLOY_SCRIPT := scripts/databricks_job_deployment.py

# Path to the cleanup script
CLEANUP_SCRIPT := scripts/databricks_dev_cleanup.py

# Deployment target
deploy:
	echo "Deploying Databricks Asset Bundle to $(ENVIRONMENT) environment..."
	./manage_dab.sh deploy $(ENVIRONMENT)

# Destruction target
destroy:
	echo "Destroying Databricks Asset Bundle resources in $(ENVIRONMENT) environment..."
	./manage_dab.sh destroy $(ENVIRONMENT)

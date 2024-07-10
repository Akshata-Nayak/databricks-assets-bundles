import sys
import yaml
import os

def main():
    # Check if the correct number of command-line arguments is provided
    args = sys.argv
    if len(args) < 2:
        print("Usage: python databricks_job_deployment.py <environment> <branch_name>")
        return

    # Extract environment from command-line arguments
    environment = sys.argv[1]
    branch = sys.argv[2]
    bundle_workflow_file = f'../deploy/{environment}'
    template_file = 'databricks_deploy_template.yml'
    template_destroy_file = 'databricks_destroy_template.yml'
    databricks_write_file = '../databricks.yml'

    # Function to write content to Databricks.yml file
    def write_databricks_yml(template_text):
        with open(databricks_write_file, 'w') as databricks_bundle_file:
            databricks_bundle_file.write(template_text)
        print("Databricks Bundle file (databricks.yml) generated successfully!")

    # Check if the file '../deploy/<environment>'  is empty; if empty, delete all resources created by the Databricks bundle
    if os.stat(bundle_workflow_file).st_size == 0:
        with open(template_destroy_file, 'r') as destroy_template_file:
            template_text = destroy_template_file.read()
        if environment == "development":
            template_text = template_text.replace('{{branch_name}}', branch)
        write_databricks_yml(template_text)
        return

    # For a non-empty bundle file, read its contents for job deployment
    with open(bundle_workflow_file, 'r') as bundle_workflow_list:
        bundle_workflow_files = bundle_workflow_list.read()

    # Read the Databricks Template File (databricks_deploy_template.yml)
    with open(template_file, 'r') as template_file:
        template_text = template_file.read()

    # Update the Databricks Template File with the list of YAML files from the file  '../deploy/<environment>' 
    template_text = template_text.replace('{{bundle_resources_list}}', bundle_workflow_files)

    # Update job permissions based on the environment
    if environment == "production":
        permissions = """
        {{job_name}}:
            email_notifications:
                on_success:
                - abc@gmail.com
                on_failure:
                - abc@gmail.com
            permissions:
                - group_name: Group-Support
                  level: CAN_MANAGE_RUN
                - group_name: Group-Operations
                  level: CAN_MANAGE_RUN
        """
    elif environment == "test":
        permissions = """
        {{job_name}}:
            email_notifications:
                on_success:
                - abcde@gmail.com
                on_failure:
                - abcde@gmail.com
            permissions:
                - group_name: Group-Developers
                  level: CAN_MANAGE_RUN
                - group_name: Group-Support
                  level: CAN_MANAGE_RUN
                - group_name: Group-Operations
                  level: CAN_MANAGE_RUN
        """
    else:
        template_text = template_text.replace('{{branch_name}}', branch)
        permissions = """
        {{job_name}}:
            email_notifications:
                on_success:
                - abcde@gmail.com
                on_failure:
                - abcde@gmail.com
            permissions:
                - group_name: Group-Developers
                  level: CAN_MANAGE_RUN
                - group_name: Group-Support
                  level: CAN_MANAGE_RUN
                - group_name: Group-Operations
                  level: CAN_MANAGE_RUN
        """

    # Fetch the job names for which permissions need to be updated
    job_names_list = []
    bundle_workflow_files_list = bundle_workflow_files.split("\n")
    for yaml_file in bundle_workflow_files_list:
        yaml_file_path = yaml_file.replace('- ', '../')
        print(yaml_file_path)
        with open(yaml_file_path, 'r') as yaml_job_file:
            data = yaml.safe_load(yaml_job_file)
        job_names = [job.get('name') for job in data.get('resources', {}).get('jobs', {}).values()]
        job_names_list.extend(job_names)

    print("Job Names:", job_names_list)

    # Format the job permissions for inclusion in the template
    job_permissions_variable = "\n".join(permissions.replace('{{job_name}}', job_name) for job_name in job_names_list)
    template_text = template_text.replace('{{job_permissions}}', job_permissions_variable)
    
    # Generate the Databricks.yml file
    write_databricks_yml(template_text)

if __name__ == '__main__':
    main()

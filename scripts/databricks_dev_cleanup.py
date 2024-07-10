import sys

def main():
    # Check if the correct number of command-line arguments is provided
    args = sys.argv
    if len(args) < 2:
        print("Usage: python databricks_job_deployment.py <branch_name>")
        return

    # Extract branch from command-line arguments
    branch = sys.argv[1]
    template_destroy_file = 'databricks_dev_cleanup_template.yml'
    databricks_write_file = '../databricks.yml'

    # Function to write content to Databricks.yml file
    def write_databricks_yml(template_text):
        with open(databricks_write_file, 'w') as databricks_bundle_file:
            databricks_bundle_file.write(template_text)
        print("Databricks Bundle file (databricks.yml) generated successfully!")

    with open(template_destroy_file, 'r') as destroy_template_file:
        template_text = destroy_template_file.read()
    
    template_text = template_text.replace('{{branch_name}}', branch)
    write_databricks_yml(template_text)
 
if __name__ == '__main__':
    main()

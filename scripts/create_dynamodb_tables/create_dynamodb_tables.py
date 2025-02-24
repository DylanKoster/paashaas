import boto3
import yaml

# Configure the local DynamoDB endpoint
DYNAMODB_ENDPOINT = "http://localhost:8000"

# Initialize DynamoDB client
dynamodb = boto3.client("dynamodb", endpoint_url=DYNAMODB_ENDPOINT)

# Custom YAML tag handlers
def ref_constructor(loader, node):
    return f"REF_{node.value}"

def sub_constructor(loader, node):
    if isinstance(node, yaml.ScalarNode):
        return node.value
    return node.value[0]

def getatt_constructor(loader, node):
    return f"GETATT_{'.'.join(node.value)}"

def load_template(file_path="template.yml"):
    yaml.add_constructor('!Ref', ref_constructor)
    yaml.add_constructor('!Sub', sub_constructor)
    yaml.add_constructor('!GetAtt', getatt_constructor)
    
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def create_dynamodb_tables(template):
    """Extract table definitions and create them in local DynamoDB."""
    resources = template.get("Resources", {})

    for resource_name, resource in resources.items():
        if resource.get("Type") == "AWS::DynamoDB::Table":
            properties = resource["Properties"]

            # Prepare table creation parameters
            table_params = {
                "TableName": properties["TableName"],
                "AttributeDefinitions": properties["AttributeDefinitions"],
                "KeySchema": properties["KeySchema"],
                "BillingMode": properties.get("BillingMode", "PAY_PER_REQUEST"),
            }

            # Add Provisioned Throughput if necessary
            if table_params["BillingMode"] == "PROVISIONED":
                table_params["ProvisionedThroughput"] = properties["ProvisionedThroughput"]

            try:
                dynamodb.create_table(**table_params)
                print(f"Created table: {table_params['TableName']}")
            except dynamodb.exceptions.ResourceInUseException:
                print(f"Table {table_params['TableName']} already exists.")
            except Exception as e:
                print(f"Error creating table {table_params['TableName']}: {e}")


if __name__ == "__main__":
    template_data = load_template("paas-haas/template.yaml")
    create_dynamodb_tables(template_data)
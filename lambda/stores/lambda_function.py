import json
import boto3
import os

def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource("dynamodb", region_name=os.getenv("eu-west-1"))
        table = dynamodb.Table("Store")

        # Scan all items from the "Stores" table
        stores = table.scan()['Items']

        return {
            "statusCode": 200,
            "body": json.dumps(stores)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

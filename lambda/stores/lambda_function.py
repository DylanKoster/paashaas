import json
import boto3
import uuid
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

def lambda_handler(event, context):
    path = event.get("path", "")
    method = event.get("httpMethod", "")

    if path == "/stores" and method == "GET":
        return get_stores()
    elif path.startswith("/stores/") and method == "GET":
        store_id = path.split("/")[-1]
        return get_store(store_id)
    elif path == "/stores" and method == "POST":
        body = json.loads(event["body"])
        return create_store(body)
    elif path.startswith("/stores/") and method == "PUT":
            store_id = path.split("/")[-1]
            body = json.loads(event["body"])
            return update_store(store_id, body)
    
    return {"statusCode": 400, "body": json.dumps({"error": "Invalid request"})}

def get_stores():
    response = table.scan()
    return {"statusCode": 200, "body": json.dumps(response.get("Items", []))}

def get_store(store_id):
    response = table.get_item(Key={"id": store_id})
    if "Item" not in response:
        return {"statusCode": 404, "body": json.dumps({"error": "Store not found"})}
    return {"statusCode": 200, "body": json.dumps(response["Item"])}

def create_store(store_data):
    store_data["id"] = store_data.get("id", str(uuid.uuid4()))  # Auto-generate ID if missing
    table.put_item(Item=store_data)
    return {"statusCode": 201, "body": json.dumps(store_data)}

def update_store(store_id, store_data):
    response = table.update_item(
        Key={"id": store_id},
        UpdateExpression="SET #name = :name, #location = :location",
        ExpressionAttributeNames={"#name": "name", "#location": "location"},
        ExpressionAttributeValues={":name": store_data["name"], ":location": store_data["location"]},
        ReturnValues="ALL_NEW"
    )
    return {"statusCode": 200, "body": json.dumps(response.get("Attributes", {}))}
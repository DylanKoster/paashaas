import json
import boto3
import os
import uuid
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

def lambda_handler(event, context):
    path = event.get("path", "")
    method = event.get("httpMethod", "")

    if path.startswith("/stores/") and "/orders" in path:
        parts = path.split("/")
        store_id = parts[2]

        if len(parts) == 4 and method == "GET":
            return get_orders(store_id)
        elif len(parts) == 5 and method == "GET":
            order_id = parts[4]
            return get_order(store_id, order_id)
        elif len(parts) == 4 and method == "POST":
            body = json.loads(event["body"])
            return create_order(store_id, body)
        elif path.startswith("/stores/") and "/orders/" in path and method == "PUT":
            parts = path.split("/")
            store_id = parts[2]
            order_id = parts[4]
            body = json.loads(event["body"])
            return update_order(store_id, order_id, body)

    return {"statusCode": 400, "body": json.dumps({"error": "Invalid request"})}

def get_orders(store_id):
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("store_id").eq(store_id)
    )
    return {"statusCode": 200, "body": json.dumps(response.get("Items", []))}

def get_order(store_id, order_id):
    response = table.get_item(Key={"id": order_id, "store_id": store_id})
    if "Item" not in response:
        return {"statusCode": 404, "body": json.dumps({"error": "Order not found"})}
    return {"statusCode": 200, "body": json.dumps(response["Item"])}

def create_order(store_id, order_data):
    order_data["store_id"] = store_id
    order_data["id"] = order_data.get("id", str(uuid.uuid4()))
    order_data["status"] = "pending"
    order_data["created_at"] = datetime.now().isoformat()
    
    table.put_item(Item=order_data)
    return {"statusCode": 201, "body": json.dumps(order_data)}

def update_order(store_id, order_id, order_data):
    response = table.update_item(
        Key={"id": order_id, "store_id": store_id},
        UpdateExpression="SET #status = :status, #items = :items",
        ExpressionAttributeNames={"#status": "status", "#items": "items"},
        ExpressionAttributeValues={":status": order_data["status"], ":items": order_data["items"]},
        ReturnValues="ALL_NEW"
    )
    return {"statusCode": 200, "body": json.dumps(response.get("Attributes", {}))}


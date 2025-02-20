import json
import boto3
import os
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

def lambda_handler(event, context):
    try:
        path = event.get("path", "").strip("/")
        method = event.get("httpMethod", "")
        body = json.loads(event["body"]) if event.get("body") else None

        parts = path.split("/")
        if len(parts) < 3 or parts[1] != "stores" or parts[3] != "orders":
            return error_response(400, "Invalid request")

        store_id = parts[2]

        if len(parts) == 4 and method == "GET":
            return get_orders(store_id)
        elif len(parts) == 5:
            order_id = parts[4]
            if method == "GET":
                return get_order(store_id, order_id)
            elif method == "PUT":
                return update_order(store_id, order_id, body)
        elif len(parts) == 4 and method == "POST":
            return create_order(store_id, body)

        return error_response(400, "Invalid request")
    except Exception as e:
        return error_response(500, str(e))

def get_orders(store_id):
    try:
        response = table.query(
            IndexName="store_id-index",
            KeyConditionExpression=Key("store_id").eq(store_id)
        )
        return success_response(200, response.get("Items", []))
    except Exception as e:
        return error_response(500, str(e))

def get_order(store_id, order_id):
    try:
        response = table.get_item(Key={"id": order_id, "store_id": store_id})
        if "Item" not in response:
            return error_response(404, "Order not found")
        return success_response(200, response["Item"])
    except Exception as e:
        return error_response(500, str(e))

def create_order(store_id, order_data):
    try:
        order_data["store_id"] = store_id
        order_data["id"] = order_data.get("id", str(uuid.uuid4()))
        order_data["status"] = "pending"
        order_data["created_at"] = datetime.utcnow().isoformat()
        
        table.put_item(Item=order_data)
        return success_response(201, order_data)
    except Exception as e:
        return error_response(500, str(e))

def update_order(store_id, order_id, order_data):
    try:
        response = table.update_item(
            Key={"id": order_id, "store_id": store_id},
            UpdateExpression="SET #status = :status, #items = :items",
            ExpressionAttributeNames={"#status": "status", "#items": "items"},
            ExpressionAttributeValues={
                ":status": order_data["status"],
                ":items": order_data["items"]
            },
            ReturnValues="ALL_NEW"
        )
        return success_response(200, response.get("Attributes", {}))
    except Exception as e:
        return error_response(500, str(e))

def success_response(status_code, data):
    return {"statusCode": status_code, "body": json.dumps(data)}

def error_response(status_code, message):
    return {"statusCode": status_code, "body": json.dumps({"error": message})}

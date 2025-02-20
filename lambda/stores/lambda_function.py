import json
import boto3
import uuid
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

def lambda_handler(event, context):
    try:
        path = event.get("path", "").strip("/")
        method = event.get("httpMethod", "")
        body = json.loads(event["body"]) if event.get("body") else None

        parts = path.split("/")
        if parts[0] != "stores":
            return error_response(400, "Invalid request")

        if len(parts) == 1 and method == "GET":
            return get_stores()
        elif len(parts) == 2:
            store_id = parts[1]
            if method == "GET":
                return get_store(store_id)
            elif method == "PUT":
                return update_store(store_id, body)
        elif len(parts) == 1 and method == "POST":
            return create_store(body)

        return error_response(400, "Invalid request")
    except Exception as e:
        return error_response(500, str(e))

def get_stores():
    try:
        response = table.scan()
        return success_response(200, response.get("Items", []))
    except Exception as e:
        return error_response(500, str(e))

def get_store(store_id):
    try:
        response = table.get_item(Key={"store_id": store_id})
        if "Item" not in response:
            return error_response(404, "Store not found")
        return success_response(200, response["Item"])
    except Exception as e:
        return error_response(500, str(e))

def create_store(store_data):
    try:
        store_data["store_id"] = store_data.get("store_id", str(uuid.uuid4()))
        table.put_item(Item=store_data)
        return success_response(201, store_data)
    except Exception as e:
        return error_response(500, str(e))

def update_store(store_id, store_data):
    try:
        response = table.update_item(
            Key={"store_id": store_id},
            UpdateExpression="SET #name = :name, #location = :location",
            ExpressionAttributeNames={"#name": "name", "#location": "location"},
            ExpressionAttributeValues={
                ":name": store_data["name"],
                ":location": store_data["location"]
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

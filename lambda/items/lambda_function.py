import json
import boto3
import uuid
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

def lambda_handler(event, context):
    try:
        path = event.get("path", "")
        method = event.get("httpMethod", "")
        body = json.loads(event["body"]) if event.get("body") else None

        parts = path.strip("/").split("/")
        if len(parts) < 3 or parts[1] != "stores" or parts[3] != "items":
            return error_response(400, "Invalid request")

        store_id = parts[2]

        if len(parts) == 4 and method == "GET":
            return get_items(store_id)
        elif len(parts) == 5:
            item_id = parts[4]
            if method == "GET":
                return get_item(store_id, item_id)
            elif method == "PUT":
                return update_item(store_id, item_id, body)
        elif len(parts) == 4 and method == "POST":
            return create_item(store_id, body)

        return error_response(400, "Invalid request")
    except Exception as e:
        return error_response(500, str(e))

def get_items(store_id):
    try:
        response = table.query(
            IndexName="store_id-index",
            KeyConditionExpression=Key("store_id").eq(store_id)
        )
        return success_response(200, response.get("Items", []))
    except Exception as e:
        return error_response(500, str(e))

def get_item(store_id, item_id):
    try:
        response = table.get_item(Key={"id": item_id, "store_id": store_id})
        if "Item" not in response:
            return error_response(404, "Item not found")
        return success_response(200, response["Item"])
    except Exception as e:
        return error_response(500, str(e))

def create_item(store_id, item_data):
    try:
        item_data["store_id"] = store_id
        item_data["id"] = item_data.get("id", str(uuid.uuid4()))
        table.put_item(Item=item_data)
        return success_response(201, item_data)
    except Exception as e:
        return error_response(500, str(e))

def update_item(store_id, item_id, item_data):
    try:
        response = table.update_item(
            Key={"id": item_id, "store_id": store_id},
            UpdateExpression="SET #name = :name, #img = :img, #quantity = :quantity",
            ExpressionAttributeNames={
                "#name": "name",
                "#img": "img",
                "#quantity": "quantity"
            },
            ExpressionAttributeValues={
                ":name": item_data["name"],
                ":img": item_data["img"],
                ":quantity": item_data["quantity"]
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

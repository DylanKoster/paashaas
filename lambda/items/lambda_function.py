import json
import boto3
import uuid
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

def lambda_handler(event, context):
    path = event.get("path", "")
    method = event.get("httpMethod", "")

    if path.startswith("/stores/") and "/items" in path:
        parts = path.split("/")
        store_id = parts[2]

        if len(parts) == 4 and method == "GET":
            return get_items(store_id)
        elif len(parts) == 5 and method == "GET":
            item_id = parts[4]
            return get_item(store_id, item_id)
        elif len(parts) == 4 and method == "POST":
            body = json.loads(event["body"])
            return create_item(store_id, body)
        elif path.startswith("/stores/") and "/items/" in path and method == "PUT":
            parts = path.split("/")
            store_id = parts[2]
            item_id = parts[4]
            body = json.loads(event["body"])
            return update_item(store_id, item_id, body)

    return {"statusCode": 400, "body": json.dumps({"error": "Invalid request"})}

def get_items(store_id):
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("store_id").eq(store_id)
    )
    return {"statusCode": 200, "body": json.dumps(response.get("Items", []))}

def get_item(store_id, item_id):
    response = table.get_item(Key={"id": item_id, "store_id": store_id})
    if "Item" not in response:
        return {"statusCode": 404, "body": json.dumps({"error": "Item not found"})}
    return {"statusCode": 200, "body": json.dumps(response["Item"])}

def create_item(store_id, item_data):
    item_data["store_id"] = store_id
    item_data["id"] = item_data.get("id", str(uuid.uuid4()))
    table.put_item(Item=item_data)
    return {"statusCode": 201, "body": json.dumps(item_data)}

def update_item(store_id, item_id, item_data):
    response = table.update_item(
        Key={"id": item_id, "store_id": store_id},
        UpdateExpression="SET #name = :name, #img = :img, #quantity = :quantity",
        ExpressionAttributeNames={"#name": "name", "#img": "img", "#quantity": "quantity"},
        ExpressionAttributeValues={":name": item_data["name"], ":img": item_data["img"], ":quantity": item_data["quantity"]},
        ReturnValues="ALL_NEW"
    )
    return {"statusCode": 200, "body": json.dumps(response.get("Attributes", {}))}

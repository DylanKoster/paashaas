import json
import boto3
import uuid
# import requests

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('stores')

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

# def lambda_handler(event, context):
#     """Sample pure Lambda function

#     Parameters
#     ----------
#     event: dict, required
#         API Gateway Lambda Proxy Input Format

#         Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

#     context: object, required
#         Lambda Context runtime methods and attributes

#         Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

#     Returns
#     ------
#     API Gateway Lambda Proxy Output Format: dict

#         Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
#     """

#     # try:
#     #     ip = requests.get("http://checkip.amazonaws.com/")
#     # except requests.RequestException as e:
#     #     # Send some context about this error to Lambda Logs
#     #     print(e)

#     #     raise e

#     if event['httpMethod'] == 'GET':
#         return {
#             'statusCode': 200,
#             'body': json.dumps('these are all the stores')
#         }
#     elif event['httpMethod'] == 'POST':
#         body = json.loads(event.get('body', '{}'))  # Parse the JSON body
#         return {
#             'statusCode': 200,
#             'body': json.dumps({
#                 'message': 'Hello, World! This is a POST request to stores.',
#                 'receivedData': body
#             })
#         }
#     else:
#         return {
#             'statusCode': 405,
#             'body': json.dumps('Method Not Allowed')
#         }

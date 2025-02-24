import json
import boto3
from models import Store

dynamodb = boto3.resource('dynamodb')
stores_table = dynamodb.Table('Stores')

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        store_id = event.get('pathParameters', {}).get('store_id')
        return get_store(store_id)
    elif event['httpMethod'] == 'POST':
        body = json.loads(event.get('body', '{}'))
        return add_store(body)
    elif event['httpMethod'] == 'PUT':
        store_id = event.get('pathParameters', {}).get('store_id')
        body = json.loads(event.get('body', '{}'))
        return alter_store(store_id, body)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps('Method Not Allowed')
        }


def get_store(store_id):
    response = stores_table.get_item(Key={'id': store_id})
    item = response.get('Item')

    if item:
        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('Not Found')
        }


def add_store(body):
    try:
        store = Store.model_validate(body)
        stores_table.put_item(Item=store.model_dump())
        return {
            'statusCode': 200,
            'body': json.dumps(store.model_dump())
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }


def alter_store(store_id, body):
    try:
        store = Store.model_validate(body)
        response = stores_table.update_item(
            Key={'id': store_id},
            UpdateExpression="SET #name = :name, #location = :location",
            ExpressionAttributeNames={
                '#name': 'name',
                '#location': 'location'
            },
            ExpressionAttributeValues={
                ':name': store.name,
                ':location': store.location
            },
            ReturnValues="ALL_NEW"
        )

        updated_store = response['Attributes']

        return {
            'statusCode': 200,
            'body': json.dumps(updated_store)
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
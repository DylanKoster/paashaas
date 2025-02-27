import json
import boto3
from models import InventoryItem
from decimal import Decimal
from util import close_expired_orders

dynamodb = boto3.resource('dynamodb')
items_table = dynamodb.Table('Items')
orders_table = dynamodb.Table('Orders')

class DecimalEncoder(json.JSONEncoder):
    # TODO: why does dynanomdb store quantity in decimal?
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)


def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        store_id = event.get('pathParameters', {}).get('store_id')
        if store_id:
            item_id = event.get('pathParameters', {}).get('item_id')
            if item_id:
                return get_item(store_id, item_id)
            else:
                return get_items(store_id)
    elif event['httpMethod'] == 'POST':
        store_id = event.get('pathParameters', {}).get('store_id')
        body = json.loads(event.get('body', '{}'))
        return add_item(store_id, body)
    elif event['httpMethod'] == 'PUT':
        store_id = event.get('pathParameters', {}).get('store_id')
        item_id = event.get('pathParameters', {}).get('item_id')
        body = json.loads(event.get('body', '{}'))
        return alter_item(store_id, item_id, body)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps('Method Not Allowed')
        }


def get_items(store_id):
    close_expired_orders(orders_table, items_table)
    response = items_table.scan(FilterExpression="store_id = :store_id", ExpressionAttributeValues={':store_id': store_id})
    items = response['Items']
    return {
        'statusCode': 200,
        'body': json.dumps(items, cls=DecimalEncoder)
    }


def get_item(store_id, item_id):
    close_expired_orders(orders_table, items_table)
    response = items_table.get_item(Key={'id': item_id, 'store_id': store_id})
    item = response.get('Item')
    return {
        'statusCode': 200,
        'body': json.dumps(item, cls=DecimalEncoder)
    }


def add_item(store_id, body):
    try:
        item = InventoryItem.model_validate(body)
        item.store_id = store_id
        items_table.put_item(Item=item.model_dump())
        return {
            'statusCode': 200,
            'body': json.dumps(item.model_dump())
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }


def alter_item(store_id, item_id, body):
    close_expired_orders(orders_table, items_table)
    try:
        item = InventoryItem.model_validate(body)
        response = items_table.update_item(
            Key={'id': item_id, 'store_id': store_id},
            UpdateExpression="SET #name = :name, #img = :img, #quantity = :quantity",
            ExpressionAttributeNames={
                '#name': 'name',
                '#img': 'img',
                '#quantity': 'quantity'
            },
            ExpressionAttributeValues={
                ':name': item.name,
                ':img': item.img,
                ':quantity': item.quantity
            },
            ReturnValues="ALL_NEW"
        )

        updated_item = response['Attributes']

        return {
            'statusCode': 200,
            'body': json.dumps(updated_item, cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }

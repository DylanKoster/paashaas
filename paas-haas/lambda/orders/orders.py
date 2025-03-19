import json
import boto3
from models import Order, InventoryItem
from boto3.dynamodb.conditions import Key
from decimal import Decimal
from util import close_expired_orders

dynamodb = boto3.resource('dynamodb')
orders_table = dynamodb.Table('Orders')
items_table = dynamodb.Table('Items')

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
            order_id = event.get('pathParameters', {}).get('order_id')
            if order_id:
                return get_order(store_id, order_id)
            else:
                return get_orders(store_id)
    elif event['httpMethod'] == 'POST':
        store_id = event.get('pathParameters', {}).get('store_id')
        body = json.loads(event.get('body', '{}'))
        return add_order(store_id, body)
    elif event['httpMethod'] == 'PUT':
        store_id = event.get('pathParameters', {}).get('store_id')
        order_id = event.get('pathParameters', {}).get('order_id')
        body = json.loads(event.get('body', '{}'))
        return alter_order(store_id, order_id, body)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps('Method Not Allowed')
        }


def get_orders(store_id):
    close_expired_orders(orders_table, items_table)
    # response = orders_table.scan(FilterExpression="store_id = :store_id", ExpressionAttributeValues={':store_id': store_id})
    response = orders_table.query(
        KeyconditionExpression=Key('store_id').eq(store_id)
    )
    orders = response['Items']
    return {
        'statusCode': 200,
        'body': json.dumps(orders, cls=DecimalEncoder)
    }


def get_order(store_id, order_id):
    close_expired_orders(orders_table, items_table)
    response = orders_table.get_item(Key={'id': order_id})
    order = response.get('Item')
    return {
        'statusCode': 200,
        'body': json.dumps(order, cls=DecimalEncoder)
    }


def add_order(store_id, body):
    close_expired_orders(orders_table, items_table)
    try:
        order = Order.model_validate(body)
        order.store_id = store_id

        for item in order.items:
            response = items_table.get_item(Key={'id': item.item_id, 'store_id': store_id})
            inv_item = InventoryItem(**response.get('Item'))
            if inv_item.quantity < item.quantity:
                raise Exception('Not enough stock for item: ' + inv_item.name)

        for item in order.items:
            items_table.update_item(
                Key={'id': item.item_id, 'store_id': store_id},
                UpdateExpression="SET #quantity = #quantity - :quantity",
                ExpressionAttributeNames={
                    '#quantity': 'quantity',
                },
                ExpressionAttributeValues={
                    ':quantity': item.quantity,
                },
                ReturnValues="ALL_NEW"
            )

        orders_table.put_item(Item=order.model_dump())
        return {
            'statusCode': 200,
            'body': json.dumps(order.model_dump())
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }


def alter_order(store_id, order_id, body):
    close_expired_orders(orders_table, items_table)
    try:
        order = Order.model_validate(body)
        response = orders_table.update_item(
            Key={'id': order_id},
            UpdateExpression="SET #status = :status",
            ExpressionAttributeNames={
                '#status': 'status',
            },
            ExpressionAttributeValues={
                ':status': order.status,
            },
            ReturnValues="ALL_NEW"
        )

        updated_order = response['Attributes']

        return {
            'statusCode': 200,
            'body': json.dumps(updated_order, cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }

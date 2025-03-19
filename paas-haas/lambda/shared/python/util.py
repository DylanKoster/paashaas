from boto3.dynamodb.conditions import Attr
from datetime import datetime
from decimal import Decimal
import json

class DecimalEncoder(json.JSONEncoder):
    # TODO: why does dynanomdb store quantity in decimal?
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)

def close_expired_orders(orders_table, items_table):
    # response = orders_table.query(
    #     IndexName='status-index',
    #     KeyConditionExpression=Key('status').eq('pending')
    # )
    current_time = datetime.now().timestamp()
    response = orders_table.scan(FilterExpression=Attr('status').eq('pending') & Attr('expiry_date').lt(current_time))
    for order in response['Items']:
        order = json.loads(json.dumps(order, cls=DecimalEncoder))
        orders_table.update_item(
            Key={'id': order['id']},
            UpdateExpression="set #status=:status",
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': 'cancelled'}
        )
        for order_item in order['items']:
            items_table.update_item(
                Key={'id': order_item['item_id'], 'store_id': order['store_id']},
                UpdateExpression="set quantity = quantity + :quantity",
                ExpressionAttributeValues={':quantity': order_item['quantity']}
            )

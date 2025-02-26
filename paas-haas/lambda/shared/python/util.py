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
    response = orders_table.scan()
    for order in response['Items']:
        order = json.loads(json.dumps(order, cls=DecimalEncoder))
        if order['status'] != 'pending':
            continue
        expiry_date = datetime.fromtimestamp(order['expiry_date'])
        if expiry_date < datetime.now():
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

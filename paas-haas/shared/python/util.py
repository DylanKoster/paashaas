from datetime import datetime

def close_expired_orders(orders_table, items_table):
    response = orders_table.scan()
    for order in response['Items']:
        if order['expiry_date'] < datetime.now().isoformat():
            orders_table.update_item(
                Key={'id': order['id'], 'store_id': order['store_id']},
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

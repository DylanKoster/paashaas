import json

def lambda_handler(event, context):
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hey there boys'
        })
    }

    return response

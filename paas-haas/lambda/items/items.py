import json

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    if event['httpMethod'] == 'GET':
        return {
            'statusCode': 200,
            'body': json.dumps('these are all the items')
        }
    elif event['httpMethod'] == 'POST':
        body = json.loads(event.get('body', '{}'))  # Parse the JSON body
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Hello, World! This is a POST request to items.',
                'receivedData': body
            })
        }
    else:
        return {
            'statusCode': 405,
            'body': json.dumps('Method Not Allowed')
        }

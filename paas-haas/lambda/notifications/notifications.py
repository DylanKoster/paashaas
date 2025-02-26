import json

def lambda_handler(event, context):
    if (len(event["Records"]) > 1):
        return {
            'statusCode': 500,
            'body': json.dumps('More than one record was returned.')
        }
    
    record = event['Records'][0]   
    item = record['dynamodb']['NewImage']
    
    # item contains store_id, id, img, name, and quantity.

    return 'Successfully processed {} records.'.format(len(event['Records']))
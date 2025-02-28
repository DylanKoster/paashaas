import json
import boto3
import os

ses_client = boto3.client("ses", region_name="eu-west-1")

def lambda_handler(event, context):
    print("Event Received:", json.dumps(event))

    if (len(event["Records"]) > 1):
        return {
            'statusCode': 500,
            'body': json.dumps('More than one record was returned.')
        }
    
    record = event['Records'][0]   
    item = record['dynamodb']['NewImage']
    
    recipient_email = "dylankoster40@gmail.com"  
    
    template_data= {
        "store_id": item['store_id']['S'],
        "item_id": item['id']['S'],
        "item_name": item['name']['S']
    }

    response = ses_client.send_templated_email(
        Source=os.environ['SES_EMAIL_SOURCE'],
        Destination={"ToAddresses": [os.environ['SES_EMAIL_DEST']]},
        Template="EmptyItemMailTemplate",
        TemplateData=json.dumps(template_data)
    )
    
    print("Email Sent! Message ID:", response["MessageId"])
import json
import boto3

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
    
    sender_email = "notifications.paashaas@gmail.com"
    recipient_email = "dylankoster40@gmail.com"  
    
    template_data= {
        "store_id": item['store_id']['S'],
        "item_id": item['id']['S'],
        "item_name": item['name']['S']
    }

    response = ses_client.send_templated_email(
        Source=sender_email,
        Destination={"ToAddresses": [recipient_email]},
        Template="EmptyItemMailTemplate",
        TemplateData=json.dumps(template_data)
    )
    
    print("Email Sent! Message ID:", response["MessageId"])
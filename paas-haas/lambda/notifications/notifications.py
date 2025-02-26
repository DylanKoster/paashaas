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
    
    # item contains store_id, id, img, name, and quantity.
    sender_email = "notifications.paashaas@gmail.com"  # Replace with your verified email
    recipient_email = "dylankoster40@gmail.com"  # Change this if needed
    subject = "PaaS-HaaS Empty Item Notification"
    
    message_body = f"An item in store {item['store_id']} has run out!\n\nDetails:\nItem ID: {item['id']}\nItem name: {item['name']}"
    
    response = ses_client.send_email(
        Source=sender_email,
        Destination={"ToAddresses": [recipient_email]},
            Message={
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": message_body}}
        }
    )
    
    print("Email Sent! Message ID:", response["MessageId"])
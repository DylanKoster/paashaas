import json
import boto3

ses_client = boto3.client("ses", region_name="us-east-1")

def lambda_handler(event, context):
    print("Event Received:", json.dumps(event))
    
    sender_email = "yourname@gmail.com"  # Replace with your verified email
    recipient_email = "recipient@example.com"  # Change this if needed
    subject = "DynamoDB Event Notification"
    
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            message_body = f"New item added to DynamoDB:\n\n{json.dumps(record['dynamodb']['NewImage'])}"
            
            response = ses_client.send_email(
                Source=sender_email,
                Destination={"ToAddresses": [recipient_email]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {"Text": {"Data": message_body}}
                }
            )
            print("Email Sent! Message ID:", response["MessageId"])
            
    return {"statusCode": 200, "body": json.dumps("Email sent successfully!")}
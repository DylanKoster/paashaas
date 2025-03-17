access_key = 'AKIA52V3ITOJBSLN57UM'
secret_key = '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'

import requests
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import json

region = 'eu-west-1'
method = 'POST'
service = 'execute-api'
url = 'https://bgwljg4yk7.execute-api.eu-west-1.amazonaws.com/Prod/stores'

data = {"name": "store", "location": "location"}

session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)


request = AWSRequest(
    method,
    url,
    data=json.dumps(data),
    headers={'Content-Type': 'application/json'}
)


SigV4Auth(session.get_credentials(), service, region).add_auth(request)

print(request.data)

try:
    response = requests.request(method, url, headers=dict(request.headers), data=request.data, timeout=5)
    response.raise_for_status()
    print(f'Response Status: {response.status_code}')
    print(f'Response Body: {response.content.decode("utf-8")}')
except Exception as e:
    print(f'Error: {e}')

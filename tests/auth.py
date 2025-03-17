

import requests
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import json

BASE_URL = 'https://bgwljg4yk7.execute-api.eu-west-1.amazonaws.com/Prod'
REGION = 'eu-west-1'

ACCESS_KEY = 'AKIA52V3ITOJBSLN57UM'
SECRET_KEY = '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'

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

def signed_request(method, url, data=None, service='execute-api', region=REGION):
    request = AWSRequest(
        method,
        url,
        data=json.dumps(data) if data else {},
        headers={'Content-Type': 'application/json'} if data else {}
    )

    SigV4Auth(session.get_credentials(), service, region).add_auth(request)
    return request


if __name__ == '__main__':
    try:
        req = signed_request('POST', BASE_URL + '/stores', {"name": "store", "location": "location"})
        response = requests.request('POST', BASE_URL + '/stores', headers=dict(req.headers), data=req.data, timeout=5)
        response.raise_for_status()
        store_id = response.json()['id']
        print(f'Response Status: {response.status_code}')
        print(f'Response Body: {response.content.decode("utf-8")}')
        req2 = signed_request('GET', BASE_URL + '/stores/' + store_id)
        response = requests.request('GET', BASE_URL + '/stores/' + store_id, headers=dict(req2.headers), timeout=5)
        print(f'Response Status: {response.status_code}')
        print(f'Response Body: {response.content.decode("utf-8")}')
    except Exception as e:
        print(f'Error: {e}')

import json
import os
import requests

def run(event, context):
    
    ALB_ENDPOINT = os.environ.get('alb_endpoint')
    print(ALB_ENDPOINT)
    
    custom_headers = {'X-CST-SClientA-DeviceIP': '2001:0db8:85a3:0000:0000:8a2e:0370:7334'}
    response = requests.get(f"http://{ALB_ENDPOINT}/", headers=custom_headers)
    print(response.text)

    return response.status_code
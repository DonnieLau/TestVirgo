import requests
import json

url = "http://172.16.98.40:8080/v1/openapi"
payload = json.dumps({"extendData": {"online": True}, "text": "参加线下POS支付活动时如何获知优惠名额剩余情况"})
headers = {'appId': 'b8f86d0e519f4b9995f3ba00c62c3488', 'userId': 'C000001',
           'sessionId': 'session_id_1', 'Content-Type': 'application/json'}

response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)
# print(payload)
# print(headers)


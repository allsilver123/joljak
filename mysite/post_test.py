import requests
import json

url = " https://alimtalk-api.bizmsg.kr/v2/sender/send"

headers = {
    "Content-type": "application/json",
    "userid": "IBEOBOM",
}


data = [{
    "message_type": "AT", 
    "phn": "01076466676",
    "profile": "dc468edce77a32d860ae5ddad48a535aef6be9b3",
    "msg": "dksudsklfj;asdlkfjaklfa;lkj",
    "tmplid" : "alimtalktest_004"
}]


json_data = json.dumps(data)

response = requests.post(url, headers=headers, data=json_data)

print(response.text)
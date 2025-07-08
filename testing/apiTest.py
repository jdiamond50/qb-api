import requests # used to make api request
import json # used to parse api request

print("HI")

response = requests.get("http://api.open-notify.org/astros")
print(response.status_code)
print(response.json())

def jprint(obj):
    text = json.dumps(obj, sort_keys=False, indent=4)
    print(text)

jprint(response.json())

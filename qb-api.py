import requests
import json

response = requests.get("https://www.qbreader.org/api/random-tossup")
print(response.status_code)

def jprint(obj):
    text = json.dumps(obj, sort_keys=False, indent=4)
    print(text)

tossup = response.json()["tossups"][0]

jprint(tossup)

print(tossup["question_sanitized"])
print(tossup["answer_sanitized"])

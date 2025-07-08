import requests
import json

def jprint(obj):
    text = json.dumps(obj, sort_keys=False, indent=4)
    print(text)

# random tossup
print("------------ RANDOM TOSSUP ------------")
response = requests.get("https://www.qbreader.org/api/random-tossup")
if (response.status_code == 200):
    tossup = response.json()["tossups"][0]

    # print("------- API RESPONSE JSON -------")
    # jprint(tossup) # uncomment to see available info about tossup

    print("------- TOSSUP -------")
    print(tossup["question_sanitized"])
    print(tossup["answer_sanitized"])

# random tossup difficulties 4-5
print("------------ TOSSUP DIFFS 4-5 ------------")
diffs = [4,5]
params = {"difficulties" : diffs}
response = requests.get("https://www.qbreader.org/api/random-tossup", params = params)
if (response.status_code == 200):
    tossup = response.json()["tossups"][0]

    # print("------- API RESPONSE JSON -------")
    # jprint(tossup)

    print("------- TOSSUP -------")
    print(tossup["question_sanitized"])
    print(tossup["answer_sanitized"])

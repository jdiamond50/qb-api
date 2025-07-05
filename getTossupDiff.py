import requests
import json

print("Enter Difficulties:")
print("(ex: \"3\" OR \"4-6, 8\")")
userResponse = input().split(", ")

def parseDiffs(userResponse):
    diffs = []
    for val in userResponse:
        try:
            index = val.index("-")
        except:
            diffs.append(int(val))
        else:
            diffRange = val.split("-")
            for i in range(int(diffRange[0]), int(diffRange[1])+1):
                diffs.append(i)
    return diffs

def jprint(obj):
    text = json.dumps(obj, sort_keys=False, indent=4)
    print(text)

def getTossup(diffs):
    params = {"difficulties" : diffs}
    response = requests.get("https://www.qbreader.org/api/random-tossup", params = params)
    if (response.status_code == 200):
        tossup = response.json()["tossups"][0]

        # print("------- API RESPONSE JSON -------")
        # jprint(tossup)

        print("Difficulty: ", tossup["difficulty"])
        print("------- QUESTION -------")
        print(tossup["question_sanitized"])
        print("------- ANSWER -------")
        print(tossup["answer_sanitized"])

diffs = parseDiffs(userResponse)
getTossup(diffs)

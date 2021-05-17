import json


MetaFilePath = ""

def getMeta():
    with open(MetaFilePath, "r") as f:
        data = json.load(f)
        print(data)

import json
def toHeaders(text):
    tmpList = text.strip().split("\n")
    ret = {}
    for i in tmpList:
        key = i.split(": ")[0]
        value = i[len(key)+len(": "):]
        ret[key] = value
    return json.dumps(ret)
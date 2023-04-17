import os
import json
import re

def readData(fileName):
    f = open(fileName, 'r', encoding='utf-8')
    data = []
    for i, line in enumerate(f):
        try:
            line = repr(line)
            line = line[1:len(line) - 3]
            data.append(line)
        except:
            print("err")
    return data

def writeJson(data,path):
    json_object = json.dumps(data, indent = 4,ensure_ascii=False)
    with open(path, 'w',encoding='utf-8') as json_file:
        json_file.write(json_object)

def readJson(path):
    with open(path, 'r',encoding="utf8") as f:
        return json.load(f)  

arrDir = os.listdir('./data_crawl')
for id in arrDir :
    data = readJson(f'./data_crawl/{id}/content.json')
    pattern = r'\(?\d{3}\)?-? *\d{3}-? *-?\d{4}'
    content = data["content"]
    phone_numbers = re.findall(pattern, content)
    print(phone_numbers)
    

import os
import json
import re

def writeFileTxt(fileName, content):
    with open(fileName, 'a', encoding="utf-8") as f1:
        f1.write(content + '\n')

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
regex1 = r'\(?\d{3}\)?-? *\d{3}-? *-?\d{4}'
regex2 = r'\(?\d{3}\)?.? *\d{3}.? *.?\d{4}'
regex3 = r'\(?\d{4}\)?.? *\d{3}.? *.?\d{3}'
regex4 = r'\(?\d{4}\)?-? *\d{3}-? *-?\d{3}'
regex5 = r'/(84[3|5|7|8|9])+([0-9]{8})\b/g'
regex6 = r'/^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$/'
regex7 = r'/^(0|\+84)(\s|\.)?((3[2-9])|(5[689])|(7[06-9])|(8[1-689])|(9[0-46-9]))(\d)(\s|\.)?(\d{3})(\s|\.)?(\d{3})$/'
regexList = [regex1,regex2,regex3,regex4,regex5,regex6,regex7]
fileName = 'Phone_Number.csv'
file_exists = os.path.exists(fileName)
if (not file_exists):
    writeFileTxt(fileName, '')

phoneNumber = []    
found_regex_list = []
for id in arrDir :
    data = readJson(f'./data_crawl/{id}/content.json')
    content = data["content"]
    print(content)
    for x in regexList:
        matchs = re.findall(x, content)     
        if matchs and matchs not in found_regex_list:
            found_regex_list.append(matchs)
            # print(matchs)
            for match in matchs:
                phoneNumber.append(match)
                print(f"====> {match} <====")

# print(found_regex_list)
    

import os
import tarfile
import time
import json
import re
from os import getcwd , listdir
from os.path import join , isfile , isdir

def read_file(file):
    i = 1
    out_str, buffer = '', None
    with open(file, "r", encoding='UTF-8', errors="ignore") as f:
        for line in f:
            matchObj = re.findall( r'mStatus.pLevel:\s+(.+?)%', line)
            if matchObj:
                if (int(matchObj[0]) < LowBatterLevel) or (int(matchObj[0]) > HighBatterLevel):
                    buffer = line
                    continue
            else:
                if KeyInLine(line):
                    buffer = line
            i += 1
            if buffer is not None:
                str = '%s...%s...%s...%s' % (file, ' line:', i, buffer)
                # write_result('report_pre.txt',str)
                out_str += str
                buffer = None
    return out_str

def write_result(file_name,buffer):
    with open(join(getcwd(),file_name),'a') as fo:
        fo.writelines(buffer)

# Get a list of all files that meet the 'condition' condition in this path
def get_all_log(condition):
    effective = []
    file_list = []
    file_list += open_dir(getcwd())
    for file in file_list:
        for str in condition:
            if str in file:
                effective.append(file)
    return effective

def open_dir(path):
    list_file = []
    if isfile(path):
        list_file.append(path)
    else:
        objlist = listdir(path)
        for f in objlist:
            path_now = join(path, f)
            if isfile(path_now):
                list_file.append(path_now)
            elif isdir(path_now):
                list_file += open_dir(path_now)
    return list_file

def do_check(filename):
    str = ''
    file_list = get_all_log(filename)
    #print ("file_list" + str(file_list))
    unzip_file(file_list)
    file_list = get_all_log(filename)
    for f in file_list:
        str += read_file(f)
    return str

def unzip_file(file_list):
    zip_file_list = []
    for file in file_list:
        if (".tar.gz" in file):
            #print("tgz file:" + file)
            tar = tarfile.open(file, "r:gz")
            dirs = file[:-7]
            print(dirs)
            tar.extractall(path = dirs)
            tar.close

def json_load():
    print (os.path.join(os.getcwd(),"Config.json"))
    f = open(os.path.join(os.getcwd(),"Config.json"), encoding='utf-8')
    json_file = json.load(f)
    jsonItemConditionAnalysis(json_file)
    f.close()

def jsonItemConditionAnalysis(Item_list):
    for Item in Item_list:
        if Item == 'tag':
            tag.update(Item_list[Item])
        elif Item == 'tagNot':
            tagNot.update(Item_list[Item])
        elif Item == 'filename':
            filename.extend(Item_list[Item])
        else :
            print("Item does not exist")
    HighBatterLevel = int(tag.pop('HighBatterLevel',100))
    LowBatterLevel = int(tag.pop('LowBatterLevel',0))

def KeywordFilter(line, key):
    for condition in tag[key]:
        if str(condition) in line:
            #print("Yes:" + str(condition))
            return True
    return False

def KeywordFilterNot(line, key):
    for condition in tagNot[key]:
        if not(str(condition) in line):
            #print("Not:" + str(condition))
            return True
    return False

def KeyInLine(line):
    result = False
    for key in tag.keys():
        if key in line:
            result = KeywordFilter(line, key)
    if not result:
        for key in tagNot.keys():
            if key in line:
                result = KeywordFilterNot(line, key)
    return result


tag = {}
tagNot = {}
filename = []
HighBatterLevel = 0
LowBatterLevel = 0
json_load()
write_result('report_pre.txt',do_check(filename))

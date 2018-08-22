import json
import os
import re

def json_load():
	print (os.path.join(os.getcwd(),"RebootConfig.json"))
	f = open(os.path.join(os.getcwd(),"RebootConfig.json"), encoding='utf-8')
	json_file = json.load(f)
	jsonItemConditionAnalysis(json_file)
	f.close()
	# print(" json read result:\n")
	# print(" tag: " + str(tag))
	# print("\n tagNot: " + str(tagNot))
	# print("\n filename: " + str(filename))
	# print("\n json load end")
	pass

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
	HighBatterLevel = tag.pop('HighBatterLevel',0)
	LowBatterLevel = tag.pop('LowBatterLevel',0)

def KeywordFilter(line, key):
	for condition in tag[key]:
		if str(condition) in line:
			print("Yes:" + str(condition))
			return True
	return False

def KeywordFilterNot(line, key):
	for condition in tagNot[key]:
		if not(str(condition) in line):
			print("Not:" + str(condition))
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

def main():
	#pattern = re.compile(r'\d+\%')
	#matchObj = re.search( r':\s+\d+', "01-10 00:13:12.628  2878  2878 D RunInTestII BatteryService: ***mStatus.pLevel: 17%", re.M|re.I)
	matchObj = re.findall( r'mStatus.pLevel:\s+(.+?)%', "01-10 00:13:12.628  2878  2878 D RunInTestII BatteryService: ***mStatus.pLevel: 17%")
	if matchObj:
   		print("search --> matchObj.group() : ", matchObj[0])
	else:
   		print("No match!!")
	#json_load()
	#print("test keyword filter:" + str(KeyInLine('05-18 20:00:52.152923   503   503 I factoryInterfaceJni_common: factoryInterface, tpOpenShort(): rt:result=0')))

	pass

tag = {}
tagNot = {}
filename = []
HighBatterLevel = 0
LowBatterLevel = 0
main()
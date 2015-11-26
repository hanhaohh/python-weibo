#coding:utf-8
import simplejson as json
import os 
import operator
import datetime
#set default encoding of terminal to UTF-8 to read chinese 
import sys
import re
import jieba
from nltk.corpus import stopwords

reload(sys)
sys.setdefaultencoding("utf-8")
from config import BASE_DIR,STATUS_FILE_DIR,COMMENTS_FILE_DIR,REPOSTS_FILE_DIR

def num_mention_by_brand_date():
	result = get_all_weibo()
	dic = {}
	for date, weibos in result.items():
		num_mention = 0
		for item in weibos:
			# here I only know the chinese name for MK is 迈克柯尔, so I used a OR in regular expression,  
			# also, case is ignored 
			if re.match( r'.*?(?:Kate Spade|凯特|丝蓓).*?', item[0], re.M|re.I):
				num_mention=num_mention+1
		dic[date] = num_mention
	return dic 

def find_peak_hour():
	result = get_all_weibo()
	hours=[]

	for date, weibos in result.items():
		for item in weibos:
			# here I only know the chinese name for MK is 迈克柯尔, so I used a OR in regular expression,  
			# also, case is ignored 
			if re.match( r'.*?(?:Kate Spade|凯特|丝蓓).*?', item[0], re.M|re.I):
				hours.append(item[3])
	return hours
def get_all_weibo():
	'''return dictionary with date as key and weibo_text ,user  ,location as value'''
	data = {}
	for date in os.listdir(STATUS_FILE_DIR)[1:]:
		# iterate different date file
		file_date = []
		for fi in os.listdir(STATUS_FILE_DIR+'/'+date):
			with open(STATUS_FILE_DIR+'/'+date+"/"+fi) as f:
				weibo = json.load(f)
				weibo_text =  weibo["text"]
				user = weibo["user"]["id"]
				location = weibo["user"]["province"]
				hour = datetime.datetime.strptime(weibo["created_at"], "%a %b %d %H:%M:%S +0800 %Y").hour
			f.close()
			file_date.append([weibo_text,user,location,hour])
		data[date] = file_date
		file_date=[]
	return data

def get_all_comments():
	'''return dictionary with date as key and weibo_text ,user  ,location as value'''
	data = {}
	for date in os.listdir(COMMENTS_FILE_DIR)[1:]:
		# iterate different date file
		file_date = []
		for fi in os.listdir(COMMENTS_FILE_DIR+'/'+date):
			with open(COMMENTS_FILE_DIR+'/'+date+"/"+fi) as f:
				weibo = json.load(f)
				weibo_text =  weibo["text"]
				user = weibo["user"]["id"]
				location = weibo["user"]["province"]
				hour = datetime.datetime.strptime(weibo["created_at"], "%a %b %d %H:%M:%S +0800 %Y").hour
			f.close()
			file_date.append([weibo_text,user,location,hour])
		data[date] = file_date
		file_date=[]
	return data


def find_post_has_brand():
	weibo_content = []
	province = []
	ids = []
	dic = {}
	# get_all_weibo imported from helper.py
	result = get_all_weibo()
	for date, weibos in result.items():
		for item in weibos:
			# here I only know the chinese name for MK is 迈克柯尔, so I used a OR in regular expression,  
			# also, case is ignored 
			if re.match( r'.*?(?:Kate Spade|凯特|丝蓓).*?', item[0], re.M|re.I):
				weibo_content.append(item[0])
				ids.append(item[1])
				province.append(item[2])
	dic["weibo_context"]= weibo_content
	dic["province"]= province
	dic["ids"]= ids
	return dic

def sort_dict(dic):
	sorted_d = sorted(dic.items(), key=operator.itemgetter(1))
	return sorted_d

def associate_10_words():
	weibo_content=[]
	dic = {}
	result = get_all_comments()
	for date, weibos in result.items():
		for item in weibos:
			# here I only know the chinese name for MK is 迈克柯尔, so I used a OR in regular expression,  
			# also, case is ignored 
			if re.match( r'.*?(?:Kate Spade|凯特|丝蓓).*?', item[0], re.M|re.I):
				#remove puncturation and stop words
				txt_remove_punc = remove_punc(item[0])
				txt_remove_stop= rm_stop_words(txt_remove_punc)
				weibo_content.extend(list(jieba.cut(txt_remove_stop, cut_all=False)))
	for i in set(weibo_content):
		dic[i]=weibo_content.count(i) 
	top_10_list = sort_dict(dic)
	top_10_list.reverse()
	return top_10_list

def remove_punc(text):
	import string
	for c in string.punctuation:
	    text= text.replace(c,"")
	text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),text)	
	return text

def rm_stop_words(token):
	if token not in stopwords.words("english"):
	    return token
	else :
	    return ""

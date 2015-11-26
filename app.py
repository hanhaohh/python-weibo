#coding:utf-8
import simplejson as json
import os 
#set default encoding of terminal to UTF-8 to read chinese 
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#import configuration file
from config import BASE_DIR,STATUS_FILE_DIR,COMMENTS_FILE_DIR,REPOSTS_FILE_DIR
from helper import get_all_weibo,sort_dict,find_post_has_brand,num_mention_by_brand_date,find_peak_hour
from helper import	get_all_comments,associate_10_words

import re

if __name__ == "__main__":
	print "Question 1"
	print "*************"
	result=find_post_has_brand()
	# get the user count and unqiue user count 
	ids =result["ids"]
	uniq_user = set(ids)
	count_ids={}
	for i in set(ids):
		count_ids[i]=ids.count(i)
	top10_user = (sort_dict(count_ids)[-10:])
	top10_user.reverse()

	# get the location count and unqiue user count 
	province = result["province"]
	count_province = {}
	for i in set(province):
		count_province[i]=province.count(i)
	top10_location = (sort_dict(count_province)[-10:])
	top10_location.reverse()

	print "total count: %s" % len(result["ids"])
	print "total user: %s" % len(result["ids"])
	print "unique user: %s" % len(uniq_user)
	print "top 10 user(user,id): %s" %  top10_user
	print "top 10 location: %s" %  top10_location

	print "*************"
	print "Question 2: "

	result_date_count = num_mention_by_brand_date()
	top10_date = (sort_dict(result_date_count)[-10:])
	top10_date.reverse()
	print "The day has the brand mentioned most is %s" % ((top10_date[0][0]))
	hours = find_peak_hour()
	print "hours count(time,count): "
	print [(i,hours.count(i)) for i in set(hours)]
	print "Peak hours are 10:00 am when people start their work, 13:00pm when they finish lunch, and 15:00 when they maybe take a break"
	print "*************"
	print "Question 3"
	comments_date = associate_10_words()
	for i,j in  comments_date[:10]:
		print i,j 




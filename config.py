#author Hao Han
'''
This is a configure file for running job app
'''
import os 

# define the directory 
BASE_DIR = os.path.dirname(__file__)
STATUS_FILE_DIR = os.path.join(BASE_DIR,"statuses")
COMMENTS_FILE_DIR = os.path.join(BASE_DIR,"reposts")
REPOSTS_FILE_DIR = os.path.join(BASE_DIR,"comments")

# print BASE_DIR,REPOST_FILE_DIR,COMMENTS_FILE_DIR,REPOSTS_FILE_DIR
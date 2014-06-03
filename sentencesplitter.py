'''Module to define functions required to tokenize any language in the world.

'''

import nltk
import csv
from collections import namedtuple
#TODO
# Convert the file data into static hardcode data in the end.



#The sentence splitter, will split the given text, in sentences using Punkt Tokenizer. 

Lang  = namedtuple('Lang',['codename','language', 'need_punkt','stopchar'])


def get_lang_info(lang):
	'''Reads langinfo.csv and returns information about the particular language as a namedtuple

	Returns in order : codename, language, need_punkt, stopcharlist(unicode)
	'''
	langinfolist = []
	with open("langinfo.csv",'rb') as f:
		c = csv.reader(f,delimiter = '\t')
		for row in c:
			if row[0] == lang:
				langinfolist = row
				break
	


	return 	Lang(lang, langinfolist[1].decode('utf-8'), langinfolist[2]=='True', langinfolist[3].decode('utf-8').split(u','))		

def splitter(text,lang):
	'''Tokenizes the text(unicode) in any specified language and returns as a list of unicode sentences

	Checks whether a language requires the usage of Punkt Tokenizer from hardcoded data about languages. If not, simply splits and returns.
	'''
	
	thislang = get_lang_info(lang)
	
	if thislang.need_punkt:
		sent_detector = nltk.data.load('tokenizers/punkt/%s.pickle'%(thislang.language))
		sentences = (sent_detector.tokenize(text.strip()))		
		return sentences
	else:
		return lang.split(thislang.stopchar[0])	


# print get_lang_info('eng')
# print splitter('hello. what the fuck in goig. Mr. what?','eng')
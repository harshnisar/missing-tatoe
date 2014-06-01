import nltk
import csv
#The sentence splitter, will split the given text, in sentences using Punkt Tokenizer. 

#Testone, train on english corpus which we already have.
#print 'Andar ka printing this is'
#eng = open('two bullocks','rb')
#print type(eng)


#count = 0



# sentences = []
# text_eng = eng.read()
# #We need to omit the \n
# sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
# sentences = (sent_detector.tokenize(text_eng.strip()))

#print sentences

# for sentence in sentences:
# 	print sentence
# 	co
# unt = count + 1

#print count

# eng.close()

class Lang:

	stopchar = []
	#need_punkt is True or False
	def __init__(self, codename, language, need_punkt, stopchar):
		self.need_punkt = need_punkt
		self.stopchar = stopchar
		self.language = language
		self.langcode = codename

def get_lang_info(lang):
	#Syntax of the csv, langname(fullname), need_punkt, stopchar list which is comma separated.
	langinfolist = []
	with open("langinfo.csv",'rb') as f:
		c = csv.reader(f,delimiter = '\t')
		for row in c:
			if row[0] == lang:
				langinfolist = row
				break
	


	return 	Lang(lang, langinfolist[1].decode('utf-8'), bool(langinfolist[2]), langinfolist[3].decode('utf-8').split(u','))		

def splitter(text,lang):
	#The function assumes that unicode text is being given. CHECK IF PUNKT USES UNICODE
	#returns a list of sentences with their fullstops
	
	thislang = get_lang_info('eng')
	print thislang.need_punkt
	if thislang.need_punkt:
		#for now it is enlgish pickle, but we will use the respective languages pickle from the downloaded pickles
				
		# sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
		
		sent_detector = nltk.data.load('tokenizers/punkt/%s.pickle'%(thislang.language))
		sentences = (sent_detector.tokenize(text.strip()))		
		return sentences
	else:

		return lang.split(thislang.stopchar[0])	


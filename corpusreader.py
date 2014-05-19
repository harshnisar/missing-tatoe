import subprocess
import traceback,sys



def corpusreader(lang,filename,n = 0):
	#cmd = ["""grep -i --word-regexp "%s" engsent.txt --count -m 1""" %(x)]
	cmd = ["""awk -F'\t' '($2 == "%s") { print $0 }' %s"""%(lang,filename)]
	try:
		sentenceblock = subprocess.check_output(cmd,shell=True,stderr=subprocess.STDOUT)
		print type(sentenceblock)
		sentences = []
		sentences = sentenceblock.split('\n')
		for i in range(0,len(sentences)-1):

			sentences[i]=sentences[i].split('\t')[2]
	except:
		traceback.print_exc(file=sys.stdout)
		
		return 0

	if n==0:
		return sentences
	else:
		return sentences[0:n]



lang = 'eng'
filename = 'sentences.csv'

x = corpusreader(lang,filename,12)
print x 
print len(x)

#-*- encoding: utf-8 -*-
import os
import re
from EnExtractor import EnExtractor
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getdoclist(path):
	return os.listdir(path)

def getfilelist(path,doc):
	return os.listdir(path+'/'+doc)

def getsentences(path,doc,filename):
	f = open(path+'/'+doc+'/'+filename)
	content = f.read()
	begin = content.find('<TEXT>')
	if begin:
		content = content[begin:]
	allsen = re.findall('<s docid=".*" num=".*" wdcount=".*">(.*?)</s>', content, re.M)
	#print len(allsen)
	result = []
	#ff = open('result.txt','w')
	for sen in allsen:
		result.append(sen.strip())
		#ff.write(sen.strip()+'\n')
	return result

def get_summary(sentences):
	extractor = EnExtractor()
	summary = extractor.summary_train(sentences)
	return summary

def main(path):
	abspath = '/home/chenbjin/SearchJob/DUC2002_Summarization_Documents/wn.system.summary/'
	doclist = sorted(getdoclist(path))
	for doc in doclist:
		print 'dealing with doc ',doc
		filelist = sorted(getfilelist(path, doc))

		for filename in filelist:
			print "------",filename
			f = open(abspath+doc+'.'+filename,'w+')
			sentences = getsentences(path, doc, filename)
			summary = get_summary(sentences)
			for line in summary:
				f.write(line+'\n')
			f.close()
	print '-------done----------' 

if __name__ == '__main__':
	path = '/home/chenbjin/SearchJob/DUC2002_Summarization_Documents/docs.with.sentence.breaks'
	main(path)
'''
 pyrouge_evaluate_plain_text_files -s /home/chenbjin/SearchJob/ASExtractor/wn.system.summary/ 
 -sfp 'd(\d+)(\w+).(\w+)(\d+)-(\d+).txt' -m /home/chenbjin/SearchJob/ASExtractor/model.summary/
 -mfp 'd(\d+)(\w+).(\w+)(\d+)-(\d+).txt'

 chenbjin@chenbjin-Acer:~$ pyrouge_evaluate_plain_text_files -s /home/chenbjin/SearchJob/ASExtractor/wn.system.summary/ -sfp 'd(\d+)[a-z].(\w+)(\d+)-(\d+).txt' -m /home/chenbjin/SearchJob/ASExtractor/model.summary/ -mfp 'd(\d+)[a-z].(\w+)(\d+)-(\d+).txt'
'''
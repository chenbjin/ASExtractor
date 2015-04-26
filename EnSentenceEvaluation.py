#-*- encoding: utf-8 -*-
'''
@chenbjin 2015-04-26
获取duc2002单文档语料的摘要
'''
import os
import re
from EnExtractor import EnExtractor
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getdoclist(path):
	return sorted(os.listdir(path))

def getfilelist(path,doc):
	return sorted(os.listdir(path+'/'+doc))

def getsentences(path,doc,filename):
	allsens = open(path+'/'+doc+'/'+filename).readlines()
	result = []
	for sen in allsens:
		tmp = sen.strip()
		if len(tmp) > 1:
			result.append(tmp)#remove blank line
	return result

def get_summary(sentences):
	extractor = EnExtractor()
	summary = extractor.summary_train(sentences)
	return summary

def main(path):
	abspath = '/home/chenbjin/SearchJob/DUC2002_Summarization_Documents/wordnet.system.summary/'
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
	path = '/home/chenbjin/SearchJob/DUC2002_Summarization_Documents/DUC2002_test_data'
	main(path)

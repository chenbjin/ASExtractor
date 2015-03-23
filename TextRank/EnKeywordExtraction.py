#-*- encoding:utf-8 -*-
import networkx as nx
import numpy as np
from EnSegmentation import EnSegmentation

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class EnKeywordExtraction(object):
	"""docstring for EnKeywordExtraction"""
	def __init__(self, stop_words_file=None):
		super(EnKeywordExtraction, self).__init__()
		self.text = ''
		self.keywords = []
		self.seg = EnSegmentation(stop_words_file=stop_words_file) 
		self.word_index = {}
		self.index_word = {}
		self.graph = None

	def combine(self, word_list,window = 2):
		if window < 2:  
			window = 2
		for x in xrange(1,window):
			if x >= len(word_list):
				break
			word_list2 = word_list[x:]
			result = zip(word_list,word_list2)
			for res in result:
				yield res

	def train(self, text, window = 2, lower = False, with_tag_filter = True, vertex_source = 'all_filters', edge_source = 'no_stop_words'):
		self.text = text
		(_, 
		self.words_no_filter, 
		self.words_no_stop_words, 
		self.words_all_filters) = self.seg.segment(text=text, lower=lower, with_tag_filter=with_tag_filter)

		if vertex_source == 'no_filter':
			vertex_source = self.words_no_filter
		elif vertex_source == 'no_stop_words':
			vertex_source = self.words_no_stop_words
		else:
			vertex_source = self.words_all_filters

		if edge_source == 'no_filter':
			edge_source = self.words_no_filter
		elif edge_source == 'no_stop_words':
			edge_source = self.words_no_stop_words
		else:
			edge_source = self.words_all_filters
		#构造节点
		index = 0
		for words in vertex_source:
			for word in words:
				if not self.word_index.has_key(word):
					self.word_index[word] = index
					self.index_word[index] = word
					index += 1

		#构造图
		words_number = index
		self.graph = np.zeros((words_number,words_number)) #matrix

		#构造边
		for word_list in edge_source:
			for w1,w2 in self.combine(word_list,window):
				if not self.word_index.has_key(w1):
					continue
				if not self.word_index.has_key(w2):
					continue
				index1 = self.word_index[w1]
				index2 = self.word_index[w2]
				self.graph[index1][index2] = 1.0
				self.graph[index2][index1] = 1.0
		#使用networkx库的pagerank算法		
		nx_graph = nx.from_numpy_matrix(self.graph)
		scores = nx.pagerank(nx_graph)

		#对各词得分进行排序
		sorted_scores = sorted(scores.items(),key = lambda item: item[1], reverse = True)
		for index,_ in sorted_scores:
			self.keywords.append(self.index_word[index])

	def get_keyphrases(self, article_type='Abstract'):
		if article_type == 'Abstract':
			aThird = len(self.keywords)
		elif article_type == 'Fulltext': 
			aThird = len(self.keywords)/3 
		keyphrases = self.keywords[0:aThird]
		#print keyphrases
		modifiedKeyphrases = []
		dealtWith = set([]) #keeps track of individual keywords that have been joined to form a keyphrase

		textlist = self.words_no_filter
		#print self.words_no_filter
		for textlist in self.words_no_filter:
			i = 0
			j = 1
			while j < len(textlist):
				firstWord = textlist[i]
				secondWord = textlist[j]
				#print firstWord,"&",secondWord
				k = j+1
				if k < len(textlist):
					thirdWord = textlist[k]
					if firstWord in keyphrases and secondWord in keyphrases and thirdWord in keyphrases:
						keyphrase = firstWord + ' ' + secondWord + ' '+ thirdWord
						#print '1:',keyphrase
						if keyphrase not in modifiedKeyphrases:
							modifiedKeyphrases.append(keyphrase)
						dealtWith.add(firstWord)
						dealtWith.add(secondWord)
						dealtWith.add(thirdWord)
						i = i+2
						j = j+2
					elif firstWord in keyphrases and secondWord in keyphrases:
						keyphrase = firstWord + ' ' + secondWord
						#print '2:',keyphrase
						if keyphrase not in modifiedKeyphrases:
							modifiedKeyphrases.append(keyphrase)
						dealtWith.add(firstWord)
						dealtWith.add(secondWord)
						i = i + 1
						j = j + 1
						continue
				elif firstWord in keyphrases and secondWord in keyphrases:
					keyphrase = firstWord + ' ' + secondWord
					#print '3:',keyphrase
					if keyphrase not in modifiedKeyphrases:
						modifiedKeyphrases.append(keyphrase)
					dealtWith.add(firstWord)
					dealtWith.add(secondWord)
				else:
					if firstWord in keyphrases and firstWord not in dealtWith: 
						modifiedKeyphrases.append(firstWord)
					if j == len(textlist)-1 and secondWord in keyphrases and secondWord not in dealtWith:
						modifiedKeyphrases.append(secondWord)
				i = i + 1
				j = j + 1
		return modifiedKeyphrases

	def get_tag(self,text):
		return self.seg.get_tag_text(text)


if __name__ == '__main__':

	text = open('../text/007.txt','r+').read()
	keyword = EnKeywordExtraction(stop_words_file='./trainer/stopword_en.data')
	keyword.train(text=text,with_tag_filter=True)

	#print keyword.keywords
	print keyword.get_keyphrases()
	word_tag =  keyword.get_tag(text)
	for w in word_tag:
		if w[1] == 'VBN':
			print w
#-*- encoding: utf-8 -*-
import networkx as nx
import numpy as np
import math
from EnSegmentation import EnSegmentation
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class EnSentenceExtraction(object):
	"""docstring for EnSentenceExtraction"""
	def __init__(self, stop_words_file):
		super(EnSentenceExtraction, self).__init__()
		self.seg = EnSegmentation(stop_words_file=stop_words_file)
		self.sentences = None
		self.graph = None
		self.key_sentences = None
		self.words_all_filters = None

	def train(self,text,lower=False, with_tag_filter=True,source='all_filters',sim_func='Standard'):
		self.key_sentences = []
		#(self.sentences,_,_,self.words_all_filters)=self.seg.segment(text=text, lower=lower, with_tag_filter=with_tag_filter)
		#'''test
		self.sentences = text
		self.words_all_filters = self.seg.word_segmentation.sentence2word(sentences=self.sentences, 
																			lower=lower, 
																			with_stop_words=True, 
																			with_tag_filter=True)
		#'''

		if source == 'all_filters':
			source = self.words_all_filters
		else:
			source = self.words_all_filters

		if sim_func == 'Standard':
			sim_function = self._get_similarity_standard
		elif sim_func == 'Levenshtein Distance':
			sim_function = self._get_similarity_ld
		else:
			sim_function = self._get_similarity_standard

		sentences_num = len(source)
		self.graph = np.zeros((sentences_num,sentences_num))

		for x in xrange(sentences_num):
			for y in xrange(x,sentences_num):
				similarity = sim_function(source[x],source[y])
				#print similarity
				self.graph[x,y] = similarity
				self.graph[y,x] = similarity

		nx_graph = nx.from_numpy_matrix(self.graph)
		#print nx_graph.degree()
		scores = nx.pagerank(nx_graph)
		sorted_scores = sorted(scores.items(),key = lambda item: item[1],reverse=True)
		#print sorted_scores
		#totol_score = 0

		for index, score in sorted_scores:
			self.key_sentences.append(self.sentences[index])
			#totol_score += score
		#print totol_score

	def _get_similarity_standard(self, sentence1, sentence2):
		'''
		计算句子相似度,sentence1,sentence2为待计算的两句子
		'''
		words = list(set(sentence1+sentence2))
		vector1 = [float(sentence1.count(word)) for word in words]
		vector2 = [float(sentence2.count(word)) for word in words]
		words_occur_in_common = [1 for x in xrange(len(vector1)) if vector1[x]*vector2[x] > 0.]
		num_of_common_words = sum(words_occur_in_common)

		if num_of_common_words == 0.:
			return 0.
		denominator = math.log(float(len(sentence1))) + math.log(float(len(sentence2)))
		if denominator == 0.:
			return 0.
		return num_of_common_words / denominator*1.0

	def _get_similarity_ld(self,sentence1,sentence2):
		if len(sentence1) > len(sentence2):
			sentence1,sentence2 = sentence2, sentence1
		distances = range(len(sentence1) + 1)
		for index2, char2 in enumerate(sentence2):
			newDistances = [index2 + 1]
			for index1, char1 in enumerate(sentence1):
				if char1 == char2:
					newDistances.append(distances[index1])
				else:
					newDistances.append(1 + min((distances[index1], distances[index1+1], newDistances[-1])))
			distances = newDistances
		return distances[-1]

	def get_key_sentences(self,sentences_percent='20%',num=None):
		result = []
		sentences_percent = filter(lambda x:x.isdigit(), sentences_percent)
		sentences_num = (len(self.sentences) * int(sentences_percent) )/ 100
		if sentences_num <= 0:
			sentences_num = 1

		result = self.key_sentences[:sentences_num]
		return result

	def get_key_sentences_100w(self,num=100):
		result = []
		lennum = 0
		for sen in self.key_sentences:
			#print len(sen.split())
			if lennum > num:
				break
			else :
				lennum += len(sen.split())
				result.append(sen)
		return result

if __name__ == '__main__':
	text = open('../../001.txt', 'r').readlines()
	senExtrac = EnSentenceExtraction(stop_words_file='./trainer/stopword_en.data')
	senExtrac.train(text=text, lower=True, with_tag_filter=True, source='all_filters')
	print senExtrac.get_key_sentences_100w()

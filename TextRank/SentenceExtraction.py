#-*- encoding:utf-8 -*-
'''
Created on March 17, 2015
@author: chenbjin
'''
import networkx as nx
import numpy as np
import math
from Segmentation import Segmentation

class SentenceExtraction(object):
	"""docstring for SentenceExtraction"""
	def __init__(self, stop_words_file = None, delimiters='?!;？！。；…\n'):
		'''
		stop_words_file: 默认为None,若设置为文件路径，将由该文件构造停止词过滤器
		delimiters: 分隔符集合
		'''
		super(SentenceExtraction, self).__init__()
		self.seg = Segmentation(stop_words_file=stop_words_file, delimiters=delimiters)
		self.sentences = None
		self.words_no_filter = None
		self.words_no_stop_words = None
		self.words_all_filters = None

		self.graph = None
		self.key_sentences = None

	def train(self, text, lower = False, speech_tag_filter = True,source = 'all_filters',sim_func='Standard'):
		'''
		text: 待处理文本
		lower: 是否将文本转化为小写
		speech_tag_filter：若为Ｔrue,则使用默认的self.default_speech_tag_filter过滤，
						若为list,则使用speech_tag_filter过滤
						否则不过滤
		source:（数据源）选择哪个分词结果来生成句子之间相似度
						默认值为`'all_filters'`，可选值为`'no_filter', 'no_stop_words', 'all_filters'
		'''
		self.key_sentences = []
		(self.sentences, 
		self.words_no_filter, 
		self.words_no_stop_words, 
		self.words_all_filters) = self.seg.segment_text(text=text, lower=lower, speech_tag_filter=speech_tag_filter)

		if source == 'no_filter':
			source = self.words_no_filter
		elif source == 'all_filters':
			source = self.words_all_filters
		else:
			source = self.words_no_stop_words

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
				self.graph[x,y] = similarity
				self.graph[y,x] = similarity

		nx_graph = nx.from_numpy_matrix(self.graph)
		scores = nx.pagerank(nx_graph)
		sorted_scores = sorted(scores.items(),key = lambda item: item[1],reverse=True)

		for index,_ in sorted_scores:
			self.key_sentences.append(self.sentences[index])

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
		return num_of_common_words / denominator

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


	def get_key_sentences(self, sentences_min_len = 6, sentences_percent = '10%'):
		'''
		获取关键句子，形成摘要。
		'''
		result = []
		total_len = 0
		sentences_percent = filter(lambda x:x.isdigit(), sentences_percent)
		sentences_num = (len(self.sentences) * int(sentences_percent) )/ 100
		if sentences_num <= 0:
			sentences_num = 1
		#test
		print len(self.sentences)
		print sentences_percent
		print sentences_num

		for sentence in self.key_sentences:
			if total_len >= sentences_num:
				break
			tmp = len(sentence)
			if tmp >= sentences_min_len :
				if total_len+1  <= sentences_num:
					result.append(sentence)
					total_len += 1
		return result

if __name__ == '__main__':
	import codecs
	text = codecs.open('../text/05.txt', 'r', 'utf-8').read()
	key_sentences = SentenceExtraction(stop_words_file='./trainer/stopword_zh.data')
	key_sentences.train(text=text, lower=True, speech_tag_filter=True, source='all_filters')
	f = codecs.open('./result_for_keysentence.txt','w+','utf-8','ignore')
	f.write('。'.decode('utf-8').join(key_sentences.get_key_sentences(sentences_percent = '10%'))+'。'.decode('utf-8'))
	#f.write('。'.decode('utf-8').join(key_sentences.sentences)+'。'.decode('utf-8'))
	f.close()
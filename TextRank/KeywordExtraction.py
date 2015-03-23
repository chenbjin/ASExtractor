#-*- encoding:utf-8 -*-
'''
Created on March 17, 2015
@author: chenbjin
'''
import networkx as nx
import numpy as np
from Segmentation import Segmentation

class KeywordExtraction(object):
	"""　关键词提取　"""
	def __init__(self, stop_words_file=None, delimiters='?!;？！。；…\n'):
		'''
		stop_words_file: 默认为None,若设置为文件路径，将由该文件构造停止词过滤器
		delimiters: 分隔符集合
		'''
		super(KeywordExtraction, self).__init__()
		'''变量说明
		self.keywords: 关键词列表
        self.words_no_filter：对text进行分词而得到的两级列表（每行为一个句子的分词结果列表）。
        self.words_no_stop_words：对text进行分词，同时去掉停止词而得到的两级列表。
        self.words_all_filters：对text进行分词，同时去停止词，保留指定词性的单词而得到的两级列表。
        self.word_index: 字典（单词－下标）
        self.index_word:　字典（下标－单词）
        self.graph: 由单词构成的图，用于pagerank算法
		'''
		self.text =''
		self.keywords = []
		self.seg = Segmentation(stop_words_file=stop_words_file, delimiters=delimiters)

		self.words_no_filter = None
		self.words_no_stop_words = None
		self.words_all_filters = None

		self.word_index = {}
		self.index_word = {}
		self.graph = None

	def combine(self, word_list, window = 2):
		'''函数功能：构造在window窗口长度下的单词组合，用来构造self.graph中单词之间的边。
        word_list: 由单词组成的列表。
        windows：窗口大小。
		'''
		window = int(window)
		if window < 2: window = 2
		for x in xrange(1,window):
			if x >= len(word_list):
				break
			word_list2 = word_list[x:]
			#zip()返回tuple词组
			result = zip(word_list,word_list2)
			#使用生成器yield
			for res in result:
				yield res

	def train(self, text, window = 2, lower = False, speech_tag_filter = True, vertex_source = 'all_filters', edge_source = 'no_stop_words'):
		'''
		函数功能：构建self.graph所需的节点和边，使用pagerank算法进行训练，返回按得分降序的词列表
        text：　待处理文本，字符串
        window：窗口大小，用来构造单词之间的边。默认值为2
        lower：是否将文本转换为小写。默认为False。
        speech_tag_filter：若为Ｔrue,则使用默认的self.default_speech_tag_filter过滤，
						若为list,则使用speech_tag_filter过滤
						否则不过滤
        vertex_source：（节点源）选择哪个分词结果来构造pagerank对应的图中的节点
                        默认值为'all_filters'，可选值为'no_filter', 'no_stop_words', 'all_filters'
                        关键词也来自vertex_source
        edge_source：（边源）选择使用哪个分词结果来构造pagerank对应的图中的节点之间的边
                        默认值为'no_stop_words'，可选值为'no_filter', 'no_stop_words', 'all_filters'边的构造要结合window参数
		'''
		self.text = text
		(_, 
		self.words_no_filter, 
		self.words_no_stop_words, 
		self.words_all_filters) = self.seg.segment_text(text=text, lower=lower, speech_tag_filter=speech_tag_filter)

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

	def get_keywords(self, num = 6, word_min_len = 1):
		'''函数功能：获取关键词列表
		num: 关键词个数
		word_min_len: 关键词最小长度
		'''
		result = []
		count = 0
		for word in self.keywords:
			if count >= num:
				break
			if len(word) >= word_min_len:
				result.append(word)
				count += 1
		return result

	def get_keyphrases(self, keywords_num = 12, min_occur_num = 2):
		'''函数功能：获取关键短语列表
		keywords_num: 关键词个数
		word_min_len: 关键词在原文中至少出现次数
		'''
		keywords_set = set(self.get_keywords(num=keywords_num,word_min_len=1))
		keyphrases = set()
		one_word = []
		for sentence_list in self.words_no_filter:
			for word in sentence_list:
				if word in keywords_set:
					one_word.append(word)
				else:
					if len(one_word) > 1:
						keyphrases.add(''.join(one_word))
						one_word = []
						continue
					one_word = []
		result = [phrase for phrase in keyphrases if self.text.count(phrase) >= min_occur_num]
		return result

if __name__ == '__main__':
	import codecs
	text = codecs.open('../text/02.txt','r+','utf-8','ignore').read()
	keyword = KeywordExtraction(stop_words_file='./trainer/stopword_zh.data')
	keyword.train(text=text, speech_tag_filter=True)

	f = codecs.open('./result_for_keyword.txt','w+','utf-8','ignore')
	for word in keyword.get_keywords(10, word_min_len=2):
		f.write(word+'/')

	for phrase in keyword.get_keyphrases(keywords_num=20, min_occur_num=2):
		f.write(phrase+'/')
	f.close()


						

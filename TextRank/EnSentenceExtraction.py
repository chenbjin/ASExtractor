#-*- encoding: utf-8 -*-
import networkx as nx
import numpy as np
import math
import time
from nltk.corpus import wordnet as wn
from EnSegmentation import EnSegmentation
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def time_me(fn):
    def _wrapper(*args, **kwargs):
        start = time.clock()
        fn(*args, **kwargs)
        print "%s cost %s second"%(fn.__name__, time.clock() - start)
    return _wrapper

class EnSentenceExtraction(object):
	"""docstring for EnSentenceExtraction"""
	def __init__(self, stop_words_file):
		super(EnSentenceExtraction, self).__init__()
		self.seg = EnSegmentation(stop_words_file=stop_words_file)
		self.sentences = None
		self.graph = None
		self.key_sentences = []
		self.words_all_filters = None
		self.sim_2word={}

	@time_me
	def train(self,text,lower=False, with_tag_filter=True,source='all_filters',sim_func='Standard'):
		self.key_sentences = []
		(self.sentences,_,_,self.words_all_filters)=self.seg.segment(text=text, lower=lower, with_tag_filter=with_tag_filter)
		'''test for evaluation
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
			sim_function = self._get_similarity_wordnet
		
		#print sim_function

		sentences_num = len(source)
		#print sentences_num
		self.graph = np.zeros((sentences_num,sentences_num))

		for x in xrange(sentences_num):
			for y in xrange(x+1,sentences_num):
				#print x,y
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
		基于信息量，计算句子相似度,sentence1,sentence2为待计算的两句子
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
		'''
		基于编辑距离，计算句子相似度,sentence1,sentence2为待计算的两句子
		'''
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

	def _get_similarity_wordnet(self,sentence1,sentence2):
		'''
		基于WordNet语义词典，计算句子相似度,sentence1,sentence2为待计算的两句子
		'''
		sen1_len = len(sentence1)
		sen2_len = len(sentence2)
		sen2 = sentence2[:]
		#L = sen1_len + abs((sen2_len-sen1_len))/2.0
		#L = (sen1_len + sen2_len )/ 2
		Sim_total = 0
		
		x = 0
		count = 0
		while x < sen1_len:		
			if len(sen2) == 0:
				break
			y = 0
			max_sim = 0
			index2 = -1
			while y < len(sen2):
				#print x,y
				tmp_sim = self._get_similarity_wordnet_2word(sentence1[x],sen2[y])
				if tmp_sim > max_sim:
					max_sim = tmp_sim
					index2 = y
				if max_sim == 1.0:
					break
				y += 1
			Sim_total += max_sim
			#print "max:",max_sim
			if index2 >= 0:
				del sen2[index2]
				count += 1
			x += 1
			'''
		
		for w1 in sentence1 :
			max_sim = 0
			for w2 in sentence2:
				tmp_sim = self._get_similarity_wordnet_2word(w1,w2)
				#print 'tmp_sim:',w1,w2,tmp_sim
				if tmp_sim > max_sim:
					max_sim = tmp_sim
				if max_sim == 1.0:
					break	
			if max_sim == 1.0:
				break
			#print 'max_sim:',max_sim
			Sim_total += max_sim
		'''
		if count == 0:
			result = 0
		else:
			result = Sim_total / count
		#print 'result:',result
		return result		

	def _get_similarity_wordnet_2word(self,word1,word2):
		'''
		print 'before stemmed:',word1
		print 'after stemmed:',wn.morphy(word1.lower())
		print 'before stemmed:',word2
		print 'after stemmed:',wn.morphy(word2.lower())
		'''
		#stemmed word
		if wn.morphy(word1.lower()) != None :
			word1 = wn.morphy(word1.lower())
		if wn.morphy(word2.lower()) != None :
			word2 = wn.morphy(word2.lower()) 

		key1 = '(%s,%s)'%(word1,word2)
		key2 = '(%s,%s)'%(word2,word1)

		if self.sim_2word.has_key(key1):
			return self.sim_2word[key1]
		if self.sim_2word.has_key(key2):
			return self.sim_2word[key2]

		word1_synsets = wn.synsets(word1)
		#print word1_synsets
		word2_synsets = wn.synsets(word2)
		#print word2_synsets
		sim = 0

		for syn1 in word1_synsets:
			w1 = wn.synset(syn1.name())
			for syn2 in word2_synsets:
				w2 = wn.synset(syn2.name())
				tmp = w1.path_similarity(w2)
				#print tmp,syn1.name(),syn2.name()
				if tmp > sim:
					sim = tmp
				if sim == 1.0:
					break
			if sim == 1.0:
				break		
		self.sim_2word[key1] = sim
		self.sim_2word[key2] = sim
		return sim

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
	senExtrac.train(text=text, lower=True, with_tag_filter=True, source='all_filters',sim_func='wordnet')
	print senExtrac.get_key_sentences_100w()

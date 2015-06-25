#-*- encoding:utf-8 -*-
import nltk
import networkx as nx
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class EnWordSegmentation(object):
	"""文本分割"""
	def __init__(self, stop_words_file=None, tag=['NN','JJ','NNP','NNS','NNPS']):
		super(EnWordSegmentation, self).__init__()
		self.speech_tag_filter = tag
		#self.stop_tokens = ",.?!:'\"/\\#%^&*()_+-={}[]"
		self.stop_tokens = ",.?!:'\"/\\#%^&*_+-=(){}[]"
		self.stop_words = set()

		if type(stop_words_file) is str:
			for word in open(stop_words_file):
				self.stop_words.add(word.strip())
		#print self.stop_words

	def _split_words(self, text, lower = True, with_stop_words = False,with_tag_filter = False):
		word_tokens = nltk.word_tokenize(text)
		#print word_tokens
		word_tagged = nltk.pos_tag(word_tokens)
		#print word_tagged
		if with_tag_filter:
			result = [word[0] for word in word_tagged if word[1] in self.speech_tag_filter]
		else:
			result= [word[0] for word in word_tagged]

		if lower:
			result = [word.lower() for word in result]

		if with_stop_words:
			result = [word.strip() for word in result 
							if word.strip() not in self.stop_words
							and word.strip() not in self.stop_tokens
							and len(word.strip()) > 0]
		else:
			#result = [word.strip() for word in result 
			#				if word.strip() not in self.stop_tokens
			#				and len(word.strip()) > 0]
			result = [word.strip() for word in result if len(word.strip()) > 0]
		return result
	
	def _split_sentences(self, text):
		#return nltk.sent_tokenize(text)
		tokenizer = nltk.data.load('file:'  + os.path.dirname(os.path.abspath(__file__))+ '/trainer/english.pickle')
		return tokenizer.tokenize(text.strip())

	def sentence2word(self, sentences, lower = True, with_stop_words = True, with_tag_filter = False):
		result = []
		for sentence in sentences:
			sen2word = self._split_words(text=sentence, 
									lower=lower, 
									with_stop_words=with_stop_words, 
									with_tag_filter=with_tag_filter)
			if len(sen2word) > 1:
				result.append(sen2word)
		return result

class EnSegmentation(object):
	"""docstring for EnSegmentation"""
	def __init__(self, stop_words_file = None):
		super(EnSegmentation, self).__init__()
		self.word_segmentation = EnWordSegmentation(stop_words_file)

	def segment(self,text,lower=False,with_tag_filter=True):
		sentences = self.word_segmentation._split_sentences(text)
		words_no_filter = self.word_segmentation.sentence2word(	sentences=sentences, 
																lower=lower, 
																with_stop_words=False, 
																with_tag_filter=False)
		words_no_stop_words = self.word_segmentation.sentence2word(sentences=sentences,
																	lower=lower,
																	with_stop_words=True,
																	with_tag_filter=False)
		words_all_filters = self.word_segmentation.sentence2word(sentences=sentences,
																	lower=lower,
																	with_stop_words=True,
																	with_tag_filter=True)
		return sentences,words_no_filter,words_no_stop_words,words_all_filters

	def get_tag_text(self,text):
		word_tokens = nltk.word_tokenize(text)
		word_tagged = nltk.pos_tag(word_tokens)
		return word_tagged

if __name__ == '__main__':
	extraction = EnSegmentation(stop_words_file='./trainer/stopword_en.data')

	text = open('../text/007.txt','r+').read()
	#text = "Good morning, my friends. I will finish my job this morning."
	sentence,words_no_filter,words_no_stop_words,words_all_filters = extraction.segment(text)
	print sentence
	#print words_no_filter
	print words_no_stop_words
	#print words_all_filters
	

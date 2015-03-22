#-*- encoding:utf-8 -*-
import codecs
from TextRank import KeywordExtraction, SentenceExtraction

class Extractor(object):
	"""docstring for Extractor"""
	def __init__(self, stop_words_file = None):
		super(Extractor, self).__init__()
		self.keyword_extraction = KeywordExtraction(stop_words_file=stop_words_file)
		self.sentence_extraction = SentenceExtraction(stop_words_file=stop_words_file)

	def keyword_train(self, text, num=10):
		self.keyword_extraction.train(text=text, window=2, lower=False, speech_tag_filter=True)
		keyword_res = self.keyword_extraction.get_keywords(num=num, word_min_len=2)
		keyphrase_res = self.keyword_extraction.get_keyphrases(keywords_num=20, min_occur_num=2)
		return keyword_res,keyphrase_res

	def sentence_train(self,text,sentences_percent='10%',sim_func='Standard'):
		self.sentence_extraction.train(text=text, lower=True, speech_tag_filter=True,source='all_filters',sim_func=sim_func)
		abstract = self.sentence_extraction.get_key_sentences(sentences_percent=sentences_percent)
		return abstract

if __name__ == '__main__':
	text = codecs.open('./text/05.txt','r+','utf-8', 'ignore').read()
	extractor = Extractor(stop_words_file='./trainer/stopword_zh.data')
	keyword,keyphrase = extractor.keyword_train(text=text)
	abstract = extractor.sentence_train(text, sentences_percent='10%')
	
	f = codecs.open('result_for_extractor.txt','w+','utf-8')
	
	f.write('keword:\n')
	f.write('/'.join(keyword))
	
	f.write('\nkeyphrase:\n')
	f.write('/'.join(keyphrase))

	f.write('\nabstract:\n')
	f.write(u'。'.join(abstract) + u'。')
	f.close()

#-*- encoding: utf-8 -*-
from TextRank import EnKeywordExtraction, EnSentenceExtraction

class EnExtractor(object):
	"""docstring for EnExtractor"""
	def __init__(self, stop_words_file = './TextRank/trainer/stopword_en.data'):
		super(EnExtractor, self).__init__()
		self.keyphrase_extraction = EnKeywordExtraction(stop_words_file=stop_words_file)
		self.summary_extraction = EnSentenceExtraction(stop_words_file=stop_words_file)

	def keyphrase_train(self,text,article_type='Abstract'):
		self.keyphrase_extraction.train(text=text,lower=True)
		keyphrase = self.keyphrase_extraction.get_keyphrases_maximal(article_type=article_type)
		#print self.get_tag(text)
		return keyphrase

	def summary_train(self,text,sentences_percent='10%', sim_func='Levenshtein Distance',num=100):
		self.summary_extraction.train(text=text, sim_func=sim_func)
		summary = self.summary_extraction.get_key_sentences_100w()
		return summary

	def get_tag(self,text):
		return self.keyphrase_extraction.get_tag(text)

if __name__ == '__main__':
	text = open('../001.txt','r+').read()
	#text = """"""
	extractor = EnExtractor(stop_words_file='./TextRank/trainer/stopword_en.data')
	keyphrase = extractor.keyphrase_train(text=text)
	summary = extractor.summary_train(text)
	print keyphrase
	print"--------------------"
	print summary
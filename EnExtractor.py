#-*- encoding: utf-8 -*-
from TextRank import EnKeywordExtraction, EnSentenceExtraction

class EnExtractor(object):
	"""docstring for EnExtractor"""
	def __init__(self, stop_words_file = None):
		super(EnExtractor, self).__init__()
		self.keyphrase_extraction = EnKeywordExtraction(stop_words_file=stop_words_file)
		self.summary_extraction = EnSentenceExtraction(stop_words_file=stop_words_file)

	def keyphrase_train(self,text,article_type='Fulltext'):
		self.keyphrase_extraction.train(text=text)
		keyphrase = self.keyphrase_extraction.get_keyphrases(article_type=article_type)
		return keyphrase

	def summary_train(self,text,sentences_percent='10%', sim_func='Standard'):
		self.summary_extraction.train(text=text, sim_func=sim_func)
		summary = self.summary_extraction.get_key_sentences(sentences_percent=sentences_percent)
		return summary

if __name__ == '__main__':
	text = open('../001.txt','r+').read()
	#text = """"""
	extractor = EnExtractor(stop_words_file='./TextRank/trainer/stopword_en.data')
	keyphrase = extractor.keyphrase_train(text=text)
	summary = extractor.summary_train(text, sentences_percent='10%')
	print keyphrase
	print"--------------------"
	print summary
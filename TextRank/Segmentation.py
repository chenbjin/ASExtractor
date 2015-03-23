#-*- encoding:utf-8 -*-
'''
Created on March 17,2015
@author:chenbjin
'''

import jieba.posseg as pseg
import codecs

class WordSegmentation(object):
	''' 分词 '''
	def __init__(self, stop_words_file = None):
		'''函数功能：默认构造函数
		stop_words_file: 保存停止词的文件路径
		'''
		super(WordSegmentation, self).__init__()
		'''变量说明
		self.default_speech_tag_filter:  默认词性标注过滤器(只保留相应词性)
		self.stop_tokens: 分词停止符号
		self.stop_words;  停止词
		'''
		self.default_speech_tag_filter = ['an', 'i', 'j', 'l', 'n', 'nr', 'nrfg', 'ns', 
											'nt', 'nz', 't', 'v', 'vd', 'vn', 'eng']
		self.stop_tokens = "，。！？：；“”\"/\\`!#%^&*()_+-={}[]|;:'‘’<>?,.～·—「；：《》（）、― ―".decode('utf-8')
		self.stop_words = set()
		if type(stop_words_file) is str:
			for word in codecs.open(stop_words_file,'r+','utf-8','ignore'):
				self.stop_words.add(word.strip())

	def segment_text(self, text, lower = True, with_stop_words = True, speech_tag_filter = False):
		'''函数功能：对text进行分词处理
		text: 待处理文本
		lower = True: 是否将英语单词转化为小写
		with_stop_words: 若为True,则用停止词集合来过滤（去掉停止词），否则不过滤
		speech_tag_filter: 　若为Ｔrue,则使用默认的self.default_speech_tag_filter过滤，
							若为list,则使用speech_tag_filter过滤
							否则不过滤
		'''
		'''变量说明
		jieba_cut_result: 使用结巴分词对text进行分词得到结果
		result: 经分词，过滤处理后的最终结果
		'''
		jieba_cut_result = pseg.cut(text)

		'''词性过滤'''
		if type(speech_tag_filter) == bool and speech_tag_filter == True:
			jieba_cut_result = [w.word for w in jieba_cut_result if w.flag in self.default_speech_tag_filter]
		elif type(speech_tag_filter) == list:
			jieba_cut_result = [w.word for w in jieba_cut_result if w.flag in speech_tag_filter]
		else:
			jieba_cut_result = [w.word for w in jieba_cut_result]

		if lower:
			jieba_cut_result = [word.lower() for word in jieba_cut_result]

		'''停止词过滤'''
		if with_stop_words:
			result = [word.strip() for word in jieba_cut_result 
						if word.strip() not in self.stop_tokens 
						and word.strip() not in self.stop_words
						and len(word.strip()) > 0]
		else:
			result = [word.strip() for word in jieba_cut_result
						if word.strip() not in self.stop_tokens
						and len(word.strip()) > 0]

		return result

	def segment_sentences(self, sentences, lower = True, with_stop_words = True, speech_tag_filter = False):
		'''函数功能：对sentences进行分词处理
		sentences: 待处理句子列表
		lower = True: 是否将英语单词转化为小写
		with_stop_words: 若为True,则用停止词集合来过滤（去掉停止词），否则不过滤
		speech_tag_filter: 　若为Ｔrue,则使用默认的self.default_speech_tag_filter过滤，
							若为list,则使用speech_tag_filter过滤
							否则不过滤,默认不过滤
		'''
		result = []
		for sentence in sentences:
			result.append(self.segment_text(text=sentence, 
											lower=lower, 
											with_stop_words=with_stop_words, 
											speech_tag_filter=speech_tag_filter))
		return result

class SentenceSegmentation(object):
	"""　分句　"""
	def __init__(self, delimiters='?!;？！。；…\n'):
		'''函数功能：默认构造函数
		delimiters: 分隔符集合
		'''
		super(SentenceSegmentation, self).__init__()
		self.delimiters = delimiters.decode('utf-8')

	def __split(self, text, delimiters):
		'''函数功能：　根据分隔符集合，将text分割成一个一个的句子
		text: 待处理文本
		delimiters: 分隔符集合
		'''
		result = [unicode(text)]
		for tag in delimiters:
			text, result = result, []
			for seq in text:
				result += seq.split(tag)
		result = [sen.strip() for sen in result if len(sen.strip()) > 0]
		return result

	def segment_text(self, text):
		return self.__split(text, self.delimiters)

class Segmentation(object):
	"""　分割器　"""
	def __init__(self, stop_words_file = None, delimiters='?!;？！。；…\n'):
		'''函数功能：　默认构造函数
		stop_words_file: 停止词文件
		delimiters: 分隔符集合
		'''
		super(Segmentation, self).__init__()
		self.word_segmentation = WordSegmentation(stop_words_file)
		self.sentence_segmentation = SentenceSegmentation(delimiters)

	def segment_text(self, text, lower = False, speech_tag_filter = True):
		'''函数功能：　对text进行分割处理（分词／分句）
		text: 待处理文本
		lower: 是否将英语单词转化为小写
		speech_tag_filter: 词性过滤器
		'''		
		sentences = self.sentence_segmentation.segment_text(text)
		words_no_filter = self.word_segmentation.segment_sentences( sentences=sentences, 
																	lower=lower, 
																	with_stop_words=False, 
																	speech_tag_filter=False)
		words_no_stop_words = self.word_segmentation.segment_sentences(sentences=sentences, 
																	lower=lower, 
																	with_stop_words=True, 
																	speech_tag_filter=False)
		words_all_filters = self.word_segmentation.segment_sentences(sentences=sentences, 
																	lower=lower, 
																	with_stop_words=True, 
																	speech_tag_filter=speech_tag_filter)

		return sentences, words_no_filter, words_no_stop_words, words_all_filters

if __name__ == '__main__':
	ss = SentenceSegmentation()
	seg = Segmentation(stop_words_file='./trainer/stopword_zh.data')
	text = codecs.open('../text/01.txt','r+','utf-8','ignore').read()
	sentences, words_no_filter, words_no_stop_words, words_all_filters = seg.segment_text(text=text,lower=True,speech_tag_filter=True)
	f = codecs.open('./result.txt','w+','utf-8','ignore')
	for s in sentences:
		f.write(s+'\n')
	for ss in words_no_filter:
		f.write(' '.join(ss)+'\n')
	for ss in words_no_stop_words:
		f.write('/'.join(ss)+'\n')
	for ss in words_all_filters:
		f.write('%'.join(ss)+'\n')
	f.close()
		




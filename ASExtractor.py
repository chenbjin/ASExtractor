#-*- coding: utf-8 -*-
import wx
import os
import codecs
from TextRank import KeywordExtraction, SentenceExtraction
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ASExtractor(wx.Frame):
	"""docstring for ASExtractors"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(800,-1))
		self.sourcePage = wx.TextCtrl(self,style=wx.TE_MULTILINE | wx.HSCROLL)
		self.abstractPage = wx.TextCtrl(self,style=wx.TE_MULTILINE | wx.HSCROLL)
		self.CreateStatusBar()
		#Setting up the file menu
		filemenu = wx.Menu()

		# wx.ID_ABOUT and wx.ID_EXIT are stanbdard ids provided by wxWidgets.
		menuOpen = filemenu.Append(wx.ID_OPEN,"&Open"," Open new file")
		filemenu.AppendSeparator()
		menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the progqram")
		
		# Setting up the more menu
		moremenu = wx.Menu()
		menuAbout = moremenu.Append(wx.ID_ABOUT,"&About"," Information about this program")
 		
 		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,"&File")
		menuBar.Append(moremenu,"&More")
		self.SetMenuBar(menuBar)

		# Creating the button
		extractButton = wx.Button(self,label="Extract")
		clearButton = wx.Button(self,label="Clear") 
		text = wx.StaticText(self,label="The source article is bellow :")
		# Set events
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)	
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_BUTTON,self.OnExtract,extractButton)
		self.Bind(wx.EVT_BUTTON,self.OnClear,clearButton)

		# Set the Layout
		hbox = wx.BoxSizer()
		hbox.Add(extractButton,proportion=0,flag=wx.RIGHT,border=5)
		hbox.Add(clearButton,proportion=0,flag=wx.RIGHT,border=5)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(text,proportion=0,flag=wx.EXPAND|wx.LEFT,border=8)
		vbox.Add(self.sourcePage,proportion=1,flag=wx.EXPAND | wx.ALL,border=5)
		vbox.Add(hbox,proportion=0,flag=wx.EXPAND|wx.LEFT,border=5)
		vbox.Add(self.abstractPage,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT,border=5)

		self.SetSizer(vbox)
		self.Show(True)
	
	def OnOpen(self,events):
		self.dirname = ''
		dlg = wx.FileDialog( self, "Choose a file",self.dirname, "", "*.*",wx.OPEN)
		if 	dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			#f = open(os.path.join(self.dirname, self.filename), 'r')
			f = codecs.open(os.path.join(self.dirname, self.filename), 'r', 'utf-8')
			self.sourcePage.SetValue(f.read())
			f.close()

		dlg.Destroy()

	def OnExit(self,events):
		self.Close(True)

	def OnAbout(self,events):
		dlg = wx.MessageDialog( self, "An Automatic Summarization program\n\nAuthor: chenbjin\nTime: 2015-03-03","About",wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def OnExtract(self,events):
		text = self.sourcePage.GetValue().strip()
		if text != '':
			#print "Click on extractButton"
			keyword_extraction = KeywordExtraction(stop_words_file='./stopword.data')  # 导入停止词
			#使用词性过滤，文本小写，窗口为2
			keyword_extraction.train(text=text, speech_tag_filter=True, lower=True, window=2)  

			result = '关键词：\n'
			# 20个关键词且每个的长度最小为1
			result +='/'.join(keyword_extraction.get_keywords(20, word_min_len=1))  

			result += '\n关键短语：\n'
			# 20个关键词去构造短语，短语在原文本中出现次数最少为2
			result += '/'.join(keyword_extraction.get_keyphrases(keywords_num=20, min_occur_num= 2))  
			    
			sentence_extractiorn = SentenceExtraction(stop_words_file='./stopword.data')

			# 使用词性过滤，文本小写，使用words_all_filters生成句子之间的相似性
			sentence_extractiorn.train(text=text, speech_tag_filter=True, lower=True, source = 'all_filters')

			result += '\n\n摘要：\n'
			result += '\n'.join(sentence_extractiorn.get_key_sentences(num=2)) # 重要性最高的三个句子
			self.abstractPage.SetValue(result)
		else:
			print "No article"

	def OnClear(self,events):
		self.sourcePage.SetValue('')
		self.abstractPage.SetValue('')
		print "Clear all"

app = wx.App(False)
win = ASExtractor(None,'ASExtractor')
app.MainLoop()

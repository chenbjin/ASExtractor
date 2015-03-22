#-*- coding: utf-8 -*-
import wx
import os
import codecs
from Extractor import Extractor
from TextRank import KeywordExtraction, SentenceExtraction
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ASExtractor(wx.Frame):
	"""docstring for ASExtractors"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(800,600))
		self.sourcePage = wx.TextCtrl(self,style=wx.TE_MULTILINE )
		self.abstractPage = wx.TextCtrl(self,style=wx.TE_MULTILINE )
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
		#Set events of menu
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)	
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

		# Creating the button
		extractButton = wx.Button(self,label="Extract")
		clearButton = wx.Button(self,label="Clear") 
		self.Bind(wx.EVT_BUTTON,self.OnExtract,extractButton)
		self.Bind(wx.EVT_BUTTON,self.OnClear,clearButton)

		article_hint = wx.StaticText(self,label="The source article is bellow :")

		article_type_label = wx.StaticText(self,-1,label="文章类型:")
		article_type_list = ['English','Chinese']
		self.articleType = wx.ComboBox(self, size=(100, -1), choices=article_type_list, style=wx.CB_DROPDOWN | wx.CB_READONLY)
		self.articleType.SetSelection(0)

		sentences_percent_label = wx.StaticText(self,-1,label="比例:")
		sentences_percent_list = ['5%','10%','12%','15%','20%']
		self.sentencesPercent = wx.ComboBox(self, size=(80, -1), choices=sentences_percent_list, style=wx.CB_DROPDOWN)
		self.sentencesPercent.SetSelection(3) 

		similarity_function_label = wx.StaticText(self,-1,label="相似度函数:")
		similarity_function_list = ['Standard','Levenshtein Distance','Vector Space Model']
		self.similarityFunction = wx.ComboBox(self, size=(140, -1), choices=similarity_function_list, style=wx.CB_DROPDOWN | wx.CB_READONLY)
		self.similarityFunction.SetSelection(0) 

		# Set the Layout
		hbox = wx.BoxSizer()
		hbox.Add(article_type_label,proportion=0,flag=wx.ALIGN_CENTER)
		hbox.Add(self.articleType,proportion=0,flag=wx.ALIGN_CENTER,border=8)
		hbox.Add(sentences_percent_label,proportion=0,flag=wx.ALIGN_CENTER)
		hbox.Add(self.sentencesPercent,proportion=0,flag=wx.ALIGN_CENTER)
		hbox.Add(similarity_function_label,proportion=0,flag=wx.ALIGN_CENTER)
		hbox.Add(self.similarityFunction,proportion=0,flag=wx.ALIGN_CENTER)
		hbox.Add(extractButton,proportion=0,flag=wx.ALIGN_CENTER)
		hbox.Add(clearButton,proportion=0,flag=wx.ALIGN_CENTER)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(article_hint,proportion=0,flag=wx.EXPAND|wx.LEFT,border=8)
		vbox.Add(self.sourcePage,proportion=1,flag=wx.EXPAND | wx.ALL,border=5)
		vbox.Add(hbox,proportion=0,flag=wx.EXPAND|wx.LEFT,border=5)
		vbox.Add(self.abstractPage,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT,border=5)

		self.SetSizer(vbox)
		self.Center()
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
		dlg = wx.MessageDialog( self, "An Automatic Summarization program based on TextRank\n\nAuthor: chenbjin\nTime: 2015-03-03","About",wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def OnExtract(self,events):
		text = self.sourcePage.GetValue().strip()
		if text != '':
			sentences_percent = self.sentencesPercent.GetValue()
			similarity_function = self.similarityFunction.GetValue()
			print similarity_function
			extractor = Extractor(stop_words_file='./trainer/stopword_zh.data')
			keyword,keyphrase = extractor.keyword_train(text=text)
			abstract = extractor.sentence_train(text, sentences_percent=sentences_percent,sim_func=similarity_function)
			 
			result = '关键词：\n' + '/'.join(keyword)
			result += '\n关键短语：\n' + '/'.join(keyphrase)
			result += '\n摘要：\n' + '。'.join(abstract)+r'。'

			self.abstractPage.SetValue(result)
		else:
			#test 
			sentences_percent = self.sentencesPercent.GetValue()
			print filter(lambda x:x.isdigit(), sentences_percent)
			print "No article"

	def OnClear(self,events):
		self.sourcePage.SetValue('')
		self.abstractPage.SetValue('')
		print "Clear all"

if __name__ == '__main__':
	app = wx.App(False)
	win = ASExtractor(None,'ASExtractor')
	app.MainLoop()

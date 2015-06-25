#-*- coding: utf-8 -*-
import wx
import wx.py.images
import os
import codecs
from Extractor import Extractor
from EnExtractor import EnExtractor
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ASExtractor(wx.Frame):
	"""文摘系统ASExtractors"""
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(800,600))
		self.InitUI()
		self.Center()
		self.Show()

	def InitUI(self):
		#状态栏
		self.CreateStatusBar()		
		#工具栏
		toolbar = self.CreateToolBar()
		for each in self.toolbarData():
			self.addtool(toolbar, *each)
			toolbar.AddSeparator()
			toolbar.Realize()
		#源文件/摘要/关键词 展示区
		self.sourcePage = wx.TextCtrl(self,style=wx.TE_MULTILINE,size=(750,220))
		self.abstractPage = wx.TextCtrl(self,style=wx.TE_MULTILINE|wx.TE_RICH,size=(750,150))
		self.keywordPage = wx.TextCtrl(self,style=wx.TE_MULTILINE,size=(750,90))
	
		#提示条
		article_hint = wx.StaticText(self,label="源文档内容:")
		abstract_hint = wx.StaticText(self,label="摘要:")
		keyword_hint = wx.StaticText(self,label="关键词:")

		# 按钮
		extractButton = wx.Button(self,label="Extract")
		clearButton = wx.Button(self,label="Clear") 
		self.Bind(wx.EVT_BUTTON,self.OnExtract,extractButton)
		self.Bind(wx.EVT_BUTTON,self.OnClear,clearButton)

		language_type_label = wx.StaticText(self,-1,label="语言:")
		language_type_list = ['English','Chinese']
		self.languageType = wx.ComboBox(self, size=(90, -1), choices=language_type_list, style=wx.CB_DROPDOWN | wx.CB_READONLY)
		self.languageType.SetSelection(0)
		self.Bind(wx.EVT_COMBOBOX, self.OnLanguageSelected, self.languageType)

		sentences_percent_label = wx.StaticText(self,-1,label="比例:")
		sentences_percent_list = ['default','10%','12%','15%','20%']
		self.sentencesPercent = wx.ComboBox(self, size=(80, -1), choices=sentences_percent_list, style=wx.CB_DROPDOWN)
		self.sentencesPercent.SetSelection(0) 

		similarity_function_label = wx.StaticText(self,-1,label="相似度函数:")
		similarity_function_list = ['Standard','Levenshtein Distance','WordNet']
		self.similarityFunction = wx.ComboBox(self, size=(140, -1), choices=similarity_function_list, style=wx.CB_DROPDOWN | wx.CB_READONLY)
		self.similarityFunction.SetSelection(0) 

		article_type_label = wx.StaticText(self,-1,label="文本类型:")
		article_type_list = ['Fulltext','Abstract']
		self.articleType = wx.ComboBox(self, size=(90, -1), choices=article_type_list, style=wx.CB_DROPDOWN | wx.CB_READONLY)
		self.articleType.SetSelection(0) 
		self.Bind(wx.EVT_COMBOBOX, self.OnArticleSelected, self.articleType)
		# Set the Layout
		self.hbox = wx.BoxSizer()
		self.hbox.Add(language_type_label,proportion=0,flag=wx.ALIGN_CENTER)
		self.hbox.Add(self.languageType,proportion=0,flag=wx.ALIGN_CENTER,border=8)
		self.hbox.Add(article_type_label,proportion=0,flag=wx.ALIGN_CENTER)
		self.hbox.Add(self.articleType,proportion=0,flag=wx.ALIGN_CENTER)
		self.hbox.Add(sentences_percent_label,proportion=0,flag=wx.ALIGN_CENTER)
		self.hbox.Add(self.sentencesPercent,proportion=0,flag=wx.ALIGN_CENTER)
		self.hbox.Add(similarity_function_label,proportion=0,flag=wx.ALIGN_CENTER)
		self.hbox.Add(self.similarityFunction,proportion=0,flag=wx.ALIGN_CENTER)
		self.hbox.Add(extractButton,proportion=0,flag=wx.ALIGN_CENTER)
		self.hbox.Add(clearButton,proportion=0,flag=wx.ALIGN_CENTER)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.hbox,proportion=0,flag=wx.EXPAND|wx.LEFT,border=8)
		vbox.Add(article_hint,proportion=0,flag=wx.EXPAND|wx.LEFT,border=8)
		vbox.Add(self.sourcePage,proportion=0,flag=wx.EXPAND | wx.ALL,border=5)
		vbox.Add(abstract_hint,proportion=0,flag=wx.EXPAND|wx.LEFT,border=8)
		vbox.Add(self.abstractPage,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
		vbox.Add(keyword_hint,proportion=0,flag=wx.EXPAND|wx.LEFT,border=8)
		vbox.Add(self.keywordPage,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
		self.SetSizer(vbox)

	def addmenu():
		openmenu = wx.Menu()
		menuOpen = openmenu.Append(wx.ID_OPEN,"&Open"," Open new file")
		#filemenu.AppendSeparator()
		savemenu = wx.Menu()
		menuSave = savemenu.Append(wx.ID_Exit,"E&xit"," Terminate the progqram")	
		# Setting up the more menu
		moremenu = wx.Menu()
		menuAbout = moremenu.Append(wx.ID_ABOUT,"&About"," Information about this program")	
 		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(openmenu,"&Open")
		menuBar.Append(savemenu,"&Save")
		menuBar.Append(moremenu,"&More")
		self.SetMenuBar(menuBar)
		#Set events of menu
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)	
		self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

	def addtool(self,toolbar,label,imgname,helpword,handler):
		if not label:
			toolbar.AddSeparator()
			return
		bmp = wx.Image(imgname,wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		tool = toolbar.AddSimpleTool(wx.NewId(),bmp,label,helpword)
		self.Bind(wx.EVT_MENU,handler,tool)

  	def toolbarData(self):
  		return (("Open", "./images/open.png", "Open existing file",self.OnOpen),
  			("Save", "./images/save.png", "Save abstract to file",self.OnSave),
  			("About", "./images/about.png", "Create new sketch",self.OnAbout))
    
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

	def OnSave(self,events):
		self.Close(True)

	def OnAbout(self,events):
		dlg = wx.MessageDialog( self, "An Automatic Summarization program based on TextRank\n\nAuthor: chenbjin\nTime: 2015-03-03","About",wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def OnLanguageSelected(self,events):
		#print self.languageType.GetSelection()
		lang = self.languageType.GetSelection()
		if lang == 1:
			self.articleType.Enable(False)
			self.sentencesPercent.Enable(True)
		else:
			self.articleType.Enable(True)

	def OnArticleSelected(self,events):
		lang = self.languageType.GetSelection()
		art = self.articleType.GetSelection()
		if lang == 0 and art == 1:
			self.sentencesPercent.Enable(False)
		else:
			self.sentencesPercent.Enable(True)
	
	def OnExtract(self,events):
		text = self.sourcePage.GetValue().strip()
		keyword_result=''
		result = ''
		if text != '':
			if self.languageType.GetSelection() == 1:
				sentences_percent = self.sentencesPercent.GetValue()
				similarity_function = self.similarityFunction.GetValue()
				print similarity_function
				extractor = Extractor(stop_words_file='./TextRank/trainer/stopword_zh.data')
				keyword,keyphrase = extractor.keyword_train(text=text)
				abstract = extractor.sentence_train(text, sentences_percent=sentences_percent,sim_func=similarity_function)
				 
				keyword_result = '/'.join(keyword)
				keyword_result += '\n关键短语：\n' + '/'.join(keyphrase)
				result += '。'.join(abstract)+r'。'
				self.abstractPage.SetValue(result)
				#设置文本样式 
				#f = wx.Font(10, wx.ROMAN, wx.NORMAL, wx.NORMAL, True)  #创建一个字体
				#self.abstractPage.SetStyle(0, len(result), wx.TextAttr('black',wx.NullColor,f))
				self.keywordPage.SetValue(keyword_result)	
			else :
				art_type = self.articleType.GetSelection()
				extractor = EnExtractor(stop_words_file='./TextRank/trainer/stopword_en.data')
				if art_type == 1:
					keyphrase = extractor.keyphrase_train(text,article_type='Abstract')
					keyword_result = 'Keyphrases:\n'+'/'.join(keyphrase)
				else:
					sentences_percent = self.sentencesPercent.GetValue()
					similarity_function = self.similarityFunction.GetValue()
					keyphrase = extractor.keyphrase_train(text,article_type='Fulltext')
					summary = extractor.summary_train(text,sentences_percent = sentences_percent,sim_func=similarity_function)
					keyword_result = '/'.join(keyphrase)
					result += '   '+' '.join(summary)
				self.abstractPage.SetValue(result)
				#设置文本样式 
				f = wx.Font(10, wx.ROMAN, wx.NORMAL, wx.NORMAL, True)  #创建一个字体
				self.abstractPage.SetStyle(0, len(result), wx.TextAttr('black',wx.NullColor,f))
		
				self.keywordPage.SetValue(keyword_result)	
		else:
			#test 
			#sentences_percent = self.sentencesPercent.GetValue()
			#print filter(lambda x:x.isdigit(), sentences_percent)
			print "No article"

	def OnClear(self,events):
		self.sourcePage.SetValue('')
		self.abstractPage.SetValue('')
		print "Clear all"
            

if __name__ == '__main__':
	app = wx.App(False)
	win = ASExtractor(None,'自动文档摘要系统')
	app.MainLoop()

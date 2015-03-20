#coding:UTF-8
'''
Created on 2010-5-14

wxPython的文本输入控件(wx.TextCtrl)操作范例

@author: zyl508@gmail.com
'''

import wx

class TextFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,"Example For TextCtrl",
                         size=(300,100))
        panel=wx.Panel(self,-1)
        
        #添加用户名 文本输入框
        userLabel=wx.StaticText(panel,-1,"User Name:")
        userText=wx.TextCtrl(panel,-1,"Entry your name",
                             size=(175,-1))
        #设置默认的插入点，整数索引，开始位置为0
        userText.SetInsertionPoint(0)
        
        #添加密码 输入框
        passwdLabel=wx.StaticText(panel,-1,"Password:")
        passwdText=wx.TextCtrl(panel,-1,'',size=(175,-1),
                               style=wx.TE_PASSWORD)
        #用sizer控制界面布局
        sizer=wx.FlexGridSizer(cols=2,hgap=6,vgap=6)
        sizer.AddMany([userLabel,userText,passwdLabel,passwdText])
        panel.SetSizer(sizer)

class MyApp(wx.App):
    def OnInit(self):
        frame=TextFrame()
        frame.Show(True)
        return True #如果没有返回值，结果一闪而过，不能驻留窗口

def main():
    app=MyApp()
    app.MainLoop()

if __name__=="__main__":
    main()
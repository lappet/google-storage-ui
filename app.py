#!/usr/bin/python
#Raviprakash R <ravi87@gmail.com>
import wx
import os
import gs

class BotoSettings(wx.Dialog):
        	def __init__(self,parent,title):
		        #Initial stuff
		        wx.Dialog.__init__(self,parent,title=title,size=(500,250))
			
			self.label = wx.StaticText(self, -1, "BotoSettings",pos=wx.Point(10,0),size=(100,15))
		        
			self.botoPath = wx.TextCtrl(self, pos=wx.Point(10,20),size=(200,20)) 
			config = open("config","r")
			path = config.readline().split(":")[1].strip()
			self.botoPath.SetValue(path)

			self.textControl = wx.TextCtrl(self, style = wx.TE_MULTILINE,size=(450,100),pos=wx.Point(0,40))
			botoFileSettings = open(self.botoPath.GetValue(),"r")
			self.textControl.SetValue(botoFileSettings.read())

			self.updateButton = wx.Button(self,id=-1,label="Update",size=(100,50),pos=wx.Point(10,160))
			self.updateButton.SetToolTip(wx.ToolTip("Click to update Boto config"))
			self.updateButton.Bind(wx.EVT_BUTTON,self.OnUpdate)

		        self.Show(False)
		def OnUpdate(self,event):
			print "Heha"


class MyFrame(wx.Frame):
	def __init__(self,parent,title):
                self.botoFrame = BotoSettings(None,"BotoSettings")
		#Initial stuff
		wx.Frame.__init__(self,parent,title=title,size=(700,600))
               
		self.bktList = wx.ListBox(choices=gs.getbuckets(),parent=self,style=wx.LC_REPORT|wx.SUNKEN_BORDER,size=(200,100),pos=wx.Point(5,5))
                self.bktList.Bind(wx.EVT_LISTBOX,self.OnListBox)
                self.fileList = wx.ListBox(choices=[],parent=self,style=wx.LC_REPORT|wx.SUNKEN_BORDER,size=(400,100),pos=wx.Point(210,5))
		self.fileList.Bind(wx.EVT_LISTBOX,self.Download)
		self.dirCtrl = wx.GenericDirCtrl(self,size=(200,200),pos=wx.Point(5,120))
		self.dir_tree = self.dirCtrl.GetTreeCtrl()
		self.dir_tree.SetWindowStyle(self.dir_tree.GetWindowStyle() | wx.TR_MULTIPLE)
		self.uploadButton = wx.Button(self,label="Upload",size=(100,50),pos=wx.Point(250,200))
		self.uploadButton.Bind(wx.EVT_BUTTON,self.OnUpload)
		self.refreshButton = wx.Button(self,label="Refresh",size=(100,50),pos = wx.Point(250,270))
		self.refreshButton.Bind(wx.EVT_BUTTON,self.OnRefresh)
		self.CreateStatusBar() #Create a status bar

		#Setting up the menu
		filemenu = wx.Menu()
		menuItem = filemenu.Append(wx.ID_ANY,"Boto&Settings","View/Modify BotoSettings")
		self.Bind(wx.EVT_MENU,self.OnBoto,menuItem)
		filemenu.AppendSeparator()
		menuItem = filemenu.Append(wx.ID_EXIT,"E&xit","Get outta here!")
		self.Bind(wx.EVT_MENU,self.OnExit,menuItem)

		#Setting up the menu bar
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,"&File")
		self.SetMenuBar(menuBar)
		
		self.Show(True)

        def OnBoto(self,event):
                self.botoFrame.Show(True)

        def OnListBox(self,event):
                selName = self.bktList.GetStringSelection()
                self.fileList.Set(gs.getobjects(selName))
	
	def Download(self,event):
		bucketName = self.bktList.GetStringSelection()
		fileName = self.fileList.GetStringSelection()
		dlg = wx.DirDialog(self, message="Pick a directory")
		dlg.ShowModal()
		dirName = dlg.GetPath()
		self.StatusBar.SetStatusText("Downloading...")
		gs.downloadObject(bucketName,fileName,dirName)
		self.StatusBar.SetStatusText("Done!")
		dlg.Destroy()

	def OnUpload(self,event):
		print self.dirCtrl.GetFilePath()
		bucketName = self.bktList.GetStringSelection()
		fileName = self.dirCtrl.GetFilePath()
		self.StatusBar.SetStatusText("Uploading...")
		gs.uploadObjects(bucketName,[fileName])
		self.StatusBar.SetStatusText("Done!")
		#refresh
		self.fileList.Set(gs.getobjects(bucketName))
		
	def OnRefresh(self,event):
		self.bktList.Set(gs.getbuckets())
		self.StatusBar.SetStatusText("Refreshing...")	
	
	def OnExit(self,event):
		app.Exit()



app = wx.App(False)
frame = MyFrame(None,'GSBrowser')
app.MainLoop()


#!/usr/bin/python
#Raviprakash R <ravi87@gmail.com>
import wx
import os
import gs

class BotoSettings(wx.Dialog):
        	def __init__(self,parent,title):
			"""This class is for the BotoSettings Dialog box. You can set the path of the boto.config file"""
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
               
		self.bktList = wx.ListBox(choices=gs.getBuckets(),parent=self,style=wx.LC_REPORT|wx.SUNKEN_BORDER,size=(200,100),pos=wx.Point(5,5))
                self.bktList.Bind(wx.EVT_LISTBOX,self.OnListBox)
                self.fileList = wx.ListCtrl(parent=self,size=(400,100),pos=wx.Point(210,5))
		self.fileList.InsertColumn(0,"Objects")
		#self.fileList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.Download)
		self.fileList.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightClick)
		self.dirCtrl = wx.GenericDirCtrl(self,size=(200,200),pos=wx.Point(5,120))
		self.dir_tree = self.dirCtrl.GetTreeCtrl()
		self.dir_tree.SetWindowStyle(self.dir_tree.GetWindowStyle() | wx.TR_MULTIPLE)
		self.uploadButton = wx.Button(self,label="Upload",size=(100,50),pos=wx.Point(250,200))
		self.uploadButton.Bind(wx.EVT_BUTTON,self.OnUpload)
		self.refreshButton = wx.Button(self,label="Refresh",size=(100,50),pos = wx.Point(250,270))
		self.refreshButton.Bind(wx.EVT_BUTTON,self.OnRefresh)
		self.CreateStatusBar() #Create a status bar
        

		#Setting up the menu
		fileMenu = wx.Menu()
		menuItem = fileMenu.Append(wx.ID_ANY,"Boto&Settings","View/Modify BotoSettings")
		self.Bind(wx.EVT_MENU,self.OnBoto,menuItem)
		fileMenu.AppendSeparator()
		menuItem = fileMenu.Append(wx.ID_ANY,"&About","About this app")
		self.Bind(wx.EVT_MENU,self.OnAbout, menuItem)
		menuItem = fileMenu.Append(wx.ID_EXIT,"E&xit","Get outta here!")
		self.Bind(wx.EVT_MENU,self.OnExit,menuItem)

		#Setting up the menu bar
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu,"&File")
		self.SetMenuBar(menuBar)
		
		self.Show(True)

	def GetSelectedItems(self,listCtrl):
		"""    Gets the selected items for the list control.
		Selection is returned as a list of selected indices,
		low to high. This function is taken from http://ginstrom.com/scribbles/2008/09/14/getting-selected-items-from-a-listctrl-in-wxpython/		"""
		selection = []
		index = listCtrl.GetFirstSelected()
		selection.append(index)
		while len(selection) != listCtrl.GetSelectedItemCount():
		  index = listCtrl.GetNextSelected(index)
		  selection.append(index)
		names = []
		for index in selection:
			item = listCtrl.GetItem(index,0)
			names.append(item.GetText())
		return names


	def OnAbout(self,event):
		wx.MessageBox("GSBrowser\n---------\nCode in wxPython\n---------\nR Raviprakash","About")

        def OnBoto(self,event):
                self.botoFrame.Show(True)

        def OnListBox(self,event):
                selName = self.bktList.GetStringSelection()
                self.fileList.ClearAll()
                for x in gs.getObjects(selName): self.fileList.InsertStringItem(0,x)
		#self.fileList.Set(gs.getObjects(selName))

	def OnRightClick(self,event):
		#selectedObjText = event.GetText()
		selectedItems =  self.GetSelectedItems(self.fileList)
		popupMenu = wx.Menu()        
		menuItem = popupMenu.Append(wx.ID_ANY,"Download","Download this object")	    
	        self.Bind(wx.EVT_MENU,lambda evt, temp=selectedItems: self.Download(evt, temp),menuItem)
	        menuItem = popupMenu.Append(wx.ID_ANY,"Delete","Delete this object")
	        self.Bind(wx.EVT_MENU,lambda evt, temp=selectedItems: self.OnDelete(evt, temp),menuItem)
		menuItem = popupMenu.Append(wx.ID_ANY,"Get Info","Get meta data")
		self.Bind(wx.EVT_MENU,self.OnInfo,menuItem)
		currentPosition = wx.Point(event.GetPoint().x+200,event.GetPoint().y)
		self.PopupMenu(popupMenu, currentPosition)
		popupMenu.Destroy()
		print "You right clicked!"

	def OnInfo(self,event):
		print "on info"
	
	def OnDelete(self,event,fileNameList):
		 msgBox = wx.MessageDialog(self,"Are you sure you want to delete these object(s)?\n"+helper.list2str(fileNameList),"GS",wx.YES_NO)
		 if msgBox.ShowModal() == wx.ID_NO:
			return
		 bucketName = self.bktList.GetStringSelection()
		 self.StatusBar.SetStatusText("Deleting object "+str(fileNameList)+" in bucket "+bucketName)
		 gs.deleteObjects(bucketName,fileNameList)
		 self.StatusBar.SetStatusText("Updating...")
		 self.OnListBox(event) #refresh
		 self.StatusBar.SetStatusText("Done!")	
		
	def Download(self,event,fileNameList):
		bucketName = self.bktList.GetStringSelection()
		dlg = wx.DirDialog(self, message="Pick a directory")
		if dlg.ShowModal() != wx.ID_CANCEL:		
			dirName = dlg.GetPath()
			self.StatusBar.SetStatusText("Downloading...")
			gs.downloadObjects(bucketName,fileNameList,dirName)
			self.StatusBar.SetStatusText("Done!")
		dlg.Destroy()

	def OnUpload(self,event):
		path = self.dirCtrl.GetFilePath()
		print path, type(path)
		bucketName = self.bktList.GetStringSelection()
		fileName = self.dirCtrl.GetFilePath()
		self.StatusBar.SetStatusText("Uploading...")
		gs.uploadObject(bucketName,[fileName])
		self.StatusBar.SetStatusText("Done!")
		#refresh
                self.fileList.InsertStringItem(0,os.path.basename(path))
		
	def OnRefresh(self,event):
		self.bktList.Set(gs.getBuckets())		
		self.StatusBar.SetStatusText("Refreshing...")	
		self.fileList.ClearAll()
	
	def OnExit(self,event):
		app.Exit()



app = wx.App(False)
frame = MyFrame(None,'GSBrowser')
app.MainLoop()


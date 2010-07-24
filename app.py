#!/usr/bin/python
#Raviprakash R <ravi87@gmail.com>
import wx
import os
import gs
import helper

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
               
		#The Bucket List
		self.bktList = wx.ListCtrl(parent=self,style=wx.LC_REPORT|wx.SUNKEN_BORDER,size=(200,100),pos=wx.Point(5,5))
                self.bktList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnListBox)
		self.bktList.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightClickForBucketList)
		self.bktList.InsertColumn(0,"Buckets")
		for x in gs.getBuckets(): self.bktList.InsertStringItem(0,x)

		#The Object/File list 
                self.fileList = wx.ListCtrl(parent=self,size=(400,100),pos=wx.Point(210,5))
		self.fileList.InsertColumn(0,"Objects")
		#self.fileList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.Download)
		self.fileList.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightClickForObjectList)

		#The Local Directory structure
		self.dirCtrl = wx.GenericDirCtrl(self,size=(200,200),pos=wx.Point(5,120))
		self.dir_tree = self.dirCtrl.GetTreeCtrl()
		self.dir_tree.SetWindowStyle(self.dir_tree.GetWindowStyle() | wx.TR_MULTIPLE) #TR_MULTIPLE for multiple selections

		#Upload & Refresh Buttons
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
		"""Shows the About dialog which for now is just a stupid MessageBox"""
		wx.MessageBox("GSBrowser\n---------\nCode in wxPython\n---------\nR Raviprakash","About")

        def OnBoto(self,event):
		"""Shows the BotoSettings dialog"""
                self.botoFrame.Show(True)

        def OnListBox(self,event):
		"""Handles the selection of a bucket in the bucket list"""
                selName = self.GetSelectedItems(self.bktList)[0]
                self.fileList.ClearAll()
                for x in gs.getObjects(selName): self.fileList.InsertStringItem(0,x)
		#self.fileList.Set(gs.getObjects(selName))

	def OnRightClickForBucketList(self,event):
		print event.GetText()


	def OnRightClickForObjectList(self,event):
		"""Handles RightClick for the object list"""
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
		 bucketName = self.GetSelectedItems(self.bktList)[0]
		 self.StatusBar.SetStatusText("Deleting object "+str(fileNameList)+" in bucket "+bucketName)
		 gs.deleteObjects(bucketName,fileNameList)
		 self.StatusBar.SetStatusText("Updating...")
		 self.OnListBox(event) #refresh
		 self.StatusBar.SetStatusText("Done!")	
		
	def Download(self,event,fileNameList):
		bucketName = self.GetSelectedItems(self.bktList)[0]
		dlg = wx.DirDialog(self, message="Pick a directory")
		if dlg.ShowModal() != wx.ID_CANCEL:		
			dirName = dlg.GetPath()
			self.StatusBar.SetStatusText("Downloading...")
			gs.downloadObjects(bucketName,fileNameList,dirName)
			self.StatusBar.SetStatusText("Done!")
		dlg.Destroy()

	def OnUpload(self,event):
		selections = self.dir_tree.GetSelections()
		filesToUpload = []
		for item in selections:
			k = self.dir_tree.GetItemData(item)
			print "Text:", self.dir_tree.GetItemText(item)
		        path= self.dirCtrl.GetDirItemData(item).m_path
			print path
			filesToUpload.append(path)
		bucketName = self.GetSelectedItems(self.bktList)[0]
		self.StatusBar.SetStatusText("Uploading...")
		gs.uploadObject(bucketName,filesToUpload)
		self.StatusBar.SetStatusText("Done!")
		#refresh
                self.OnListBox(event)
		
	def OnRefresh(self,event):
		self.bktList.ClearAll()
		for x in gs.getBuckets(): self.bktList.InsertStringItem(0,x)
		self.StatusBar.SetStatusText("Refreshing...")	
		self.fileList.ClearAll()
	
	def OnExit(self,event):
		app.Exit()



app = wx.App(False)
frame = MyFrame(None,'GSBrowser')
app.MainLoop()


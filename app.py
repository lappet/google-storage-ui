#!/usr/bin/python
#Raviprakash R <ravi87@gmail.com>
#The Main Application
import os
os.environ['BOTO_CONFIG'] = 'config'
import sys

import wx

import gs
import helper


class BotoSettings(wx.Dialog):
	"""The Class for the boto config"""

	def __init__(self,parent,title):
		#Initial stuff
		wx.Dialog.__init__(self,parent,title=title,size=(600,250))
		self.Bind(wx.EVT_SHOW,self.OnShow)
		self.botoPath = wx.TextCtrl(self, pos=wx.Point(10,20),size=(550,100),style=wx.TE_MULTILINE) 
		self.LoadConfig()
		
		self.updateButton = wx.Button(self,id=-1,label="Update",size=(100,50),pos=wx.Point(10,160))
		self.updateButton.SetToolTip(wx.ToolTip("Click to update Boto config"))
		self.updateButton.Bind(wx.EVT_BUTTON,self.OnUpdate)

		self.Show(False)

	def OnShow(self,event):
		self.LoadConfig()
	
	def LoadConfig(self):
		path = os.path.join(sys.path[0],"config")
		config = open(path,"r")
		data = config.read()
		self.botoPath.SetValue(data)

	def OnUpdate(self,event):
		k = wx.MessageDialog(self,"If you select Yes, your config file will be modified, but you can see the impact only when you restart the application. Are you sure you want to proceed?","GS",wx.YES_NO)
		if k.ShowModal() == wx.ID_YES:
			data = self.botoPath.GetValue()
			path = os.path.join(sys.path[0],"config")
			f = open(path,"w")
			f.write(data)
			self.Show(False)
			self.LoadConfig()



class MyFrame(wx.Frame):
	"""The Class for the Main Application"""
	def __init__(self,parent,title):
		#Initial stuff
                self.botoFrame = BotoSettings(None,"BotoSettings")
		wx.Frame.__init__(self,parent,title=title,size=(700,600))
               
		#The Bucket List
		self.bktList = wx.ListCtrl(parent=self,style=wx.LC_REPORT|wx.SUNKEN_BORDER,size=(200,100),pos=wx.Point(5,5))
                self.bktList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnListBox)
		self.bktList.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightClickForBucketList)
		self.bktList.InsertColumn(0,"Buckets")
		self.bkts = gs.getBuckets()
		if self.bkts:
			for x in self.bkts: self.bktList.InsertStringItem(0,x)

		#The Object/File list 
                self.fileList = wx.ListCtrl(parent=self,size=(400,100),pos=wx.Point(210,5))
		self.fileList.InsertColumn(0,"Objects")
		self.fileList.SetToolTip(wx.ToolTip("Right click for options"))
		#self.fileList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnDownload)
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
		"""Handles RightClick for the bucket list"""
		popupMenu = wx.Menu()
		menuItem = popupMenu.Append(wx.ID_ANY,"Create new bucket","Create a new bucket")
		self.Bind(wx.EVT_MENU,self.OnCreateBucket)
		menuItem = popupMenu.Append(wx.ID_ANY,"Delete this bucket","Delete this bucket")
		self.Bind(wx.EVT_MENU,lambda evt, temp=event.GetText(): self.OnDeleteBucket(evt,temp),menuItem)
		currentPosition = wx.Point(event.GetPoint().x,event.GetPoint().y)
		self.PopupMenu(popupMenu, currentPosition)
		popupMenu.Destroy()

	def OnCreateBucket(self,event):
		"""Creates new bucket"""
		inputBox = wx.TextEntryDialog(self,"Enter the name of the bucket","GS")
		if inputBox.ShowModal() == wx.ID_OK:
			bucketName = inputBox.GetValue()
			m = gs.createBucket(bucketName)
			wx.MessageBox(str(m[0])+"\n"+str(m[1]),"Response")
			self.bkts = gs.getBuckets()
			if self.bkts:		
				for x in self.bkts: self.bktList.InsertStringItem(0,x)
			

	def OnDeleteBucket(self,event,bucketName):
		"""Deletes an exising bucket"""
		k = wx.MessageDialog(self,"If the bucket is not empty, this will empty the contents of the bucket too. Are you sure you want to proceed?","GS",wx.YES_NO)
		if k.ShowModal() == wx.ID_YES:
			gs.deleteBucket(bucketName)
			self.OnListBox(event)



	def OnRightClickForObjectList(self,event):
		"""Handles RightClick for the object list"""
		selectedItems =  self.GetSelectedItems(self.fileList)
		popupMenu = wx.Menu()        
		menuItem = popupMenu.Append(wx.ID_ANY,"Download","Download this object")	    
	        self.Bind(wx.EVT_MENU,lambda evt, temp=selectedItems: self.OnDownload(evt, temp),menuItem)
	        menuItem = popupMenu.Append(wx.ID_ANY,"Delete","Delete this object")
	        self.Bind(wx.EVT_MENU,lambda evt, temp=selectedItems: self.OnDelete(evt, temp),menuItem)
		menuItem = popupMenu.Append(wx.ID_ANY,"Get Info","Get meta data")
		self.Bind(wx.EVT_MENU,lambda evt, temp=selectedItems: self.OnInfo(evt, temp),menuItem)
		currentPosition = wx.Point(event.GetPoint().x+200,event.GetPoint().y)
		self.PopupMenu(popupMenu, currentPosition)
		popupMenu.Destroy()

	def OnInfo(self,event,fileNameList):
		"""Displays information about an object"""
		for fname in fileNameList:
			bucketName = self.GetSelectedItems(self.bktList)[0]
			info = gs.getObjectInfo(bucketName,fname)
			data = ""+"Name:"+info[0]+"\nSize in bytes:"+str(info[1])+"\nLast Modified:"+info[2]
			wx.MessageBox(data,"Info")
	
	def OnDelete(self,event,fileNameList):
		"""Delete(s) object(s)"""
		 msgBox = wx.MessageDialog(self,"Are you sure you want to delete these object(s)?\n"+helper.list2str(fileNameList),"GS",wx.YES_NO)
		 if msgBox.ShowModal() == wx.ID_NO:
			return
		 bucketName = self.GetSelectedItems(self.bktList)[0]
		 self.StatusBar.SetStatusText("Deleting object "+str(fileNameList)+" in bucket "+bucketName)
		 gs.deleteObjects(bucketName,fileNameList)
		 self.StatusBar.SetStatusText("Updating...")
		 self.OnListBox(event) #refresh
		 self.StatusBar.SetStatusText("Done!")	
		
	def OnDownload(self,event,fileNameList):
		"""Downloads object(s)"""
		bucketName = self.GetSelectedItems(self.bktList)[0]
		dlg = wx.DirDialog(self, message="Pick a directory")
		if dlg.ShowModal() != wx.ID_CANCEL:		
			dirName = dlg.GetPath()
			self.StatusBar.SetStatusText("Downloading...")
			normalCursor = self.GetCursor()
			busyCursor = wx.StockCursor(wx.CURSOR_WAIT)
			self.SetCursor(busyCursor)
			wx.Yield()
			for fileName in fileNameList:
				pdlg = wx.ProgressDialog(fileName,"FileDownload",maximum=gs.getObjectSize(bucketName,fileName))
				pdlg.SetSize((400,100))
				def update(m,n):
					pdlg.Update(m,str(100*m/n)+ "% done")
				gs.downloadObject(bucketName,fileName,dirName,update)
			self.StatusBar.SetStatusText("Done!")
			self.SetCursor(normalCursor)
		dlg.Destroy()

	def OnUpload(self,event):
		"""Uploads object(s)/directory(ies)"""
		bucketName = self.GetSelectedItems(self.bktList)[0]
		selections = self.dir_tree.GetSelections()
		filesToUpload = []
		self.StatusBar.SetStatusText("Uploading...")
		normalCursor = self.GetCursor()
		busyCursor = wx.StockCursor(wx.CURSOR_WAIT)
		self.SetCursor(busyCursor)
		for item in selections:
			k = self.dir_tree.GetItemData(item)
		        path= self.dirCtrl.GetDirItemData(item).m_path
			if os.path.isdir(path)==False: #if its not a directory, simply append the path
				filesToUpload.append(path)
			else: #if its a directory, upload all the files in the directory
				msgBox = wx.MessageDialog(self,"You have also selected a directory, do you want to upload its entire contents?","GS",wx.YES_NO)
				if msgBox.ShowModal() == wx.ID_NO:
					pass
				else: #user said Yes!
					dirlist = []
					for i in os.listdir(path):
						dirlist.append(os.path.join(path,i))
					for fname in dirlist:
						pdlg = wx.ProgressDialog(fname,"FileUpload",maximum=os.path.getsize(fname))
						pdlg.SetSize((400,100))
						def update(m,n):
							pdlg.Update(m,str(100*m/n)+ "% done")
						gs.uploadObject(bucketName,fname,update)
		for fname in filesToUpload:
			pdlg = wx.ProgressDialog(fname,"FileUpload",maximum=os.path.getsize(fname))
			pdlg.SetSize((400,100))
			def update(m,n):
				pdlg.Update(m,str(100*m/n)+ "% done")
			gs.uploadObject(bucketName,fname,update)
		self.StatusBar.SetStatusText("Done!")
		self.SetCursor(normalCursor)
		#refresh
                self.OnListBox(event)
		
	def OnRefresh(self,event):
		"""Refreshes current bucket's contents"""
		self.fileList.DeleteAllItems()
	        self.OnListBox(event)

	def OnExit(self,event):
		"""Kill the app & exit"""
		app.Exit()

status = helper.ping()
app = wx.App(False)
if status == 0:
	wx.MessageBox("Sorry, net down, check your internet connection")
	app.Exit()
else:
	frame = MyFrame(None,'GSBrowser')
	app.MainLoop()


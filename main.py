# -*- coding: utf-8 -*-

import wx
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import xlwt
import gc
import traceback

class FileLoader():
    def __init__(self, parent, axis=""):
        self.loadButton = wx.Button(parent, label = "Open " + axis)
        self.fileText = wx.TextCtrl(parent)
        self.fileText.SetEditable(False)
        self.nameList = wx.ListBox(parent)
#        self.filterText = wx.TextCtrl(parent)
#        self.filterButton = wx.Button(parent, label = "Filter")
        self.search = wx.SearchCtrl(parent, size=(100,-1),
                                    style=wx.TE_PROCESS_ENTER)
        self.search.ShowCancelButton(True)
#        filterBox = wx.BoxSizer()
#        filterBox.Add(self.filterText)
#        filterBox.Add(self.filterButton)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.loadButton, proportion = 0,flag = wx.WEST |  wx.EAST |wx.NORTH, border =5)
        self.vbox.Add(self.fileText, proportion = 0, flag = wx.WEST | wx.NORTH | wx.EAST | wx.EXPAND, border = 5)
        self.vbox.Add(self.search, proportion = 0, flag = wx.WEST | wx.NORTH |  wx.EAST | wx.EXPAND, border = 5)
#        self.vbox.Add(filterBox, proportion = 0,flag = wx.WEST | wx.NORTH, border =5)
        self.vbox.Add(self.nameList, proportion = 1, flag = wx.WEST |  wx.EAST |wx.NORTH | wx.EXPAND, border =5)
        self.nameList.Clear()

        self.loadButton.Bind(wx.EVT_BUTTON, self.OnLoadButton)
        self.search.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
        self.search.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnSearch)
        
        self.parent = parent

        self.names_orig = None
    def OnSearch(self, evt):
        if evt.GetEventType() == wx.EVT_SEARCHCTRL_CANCEL_BTN.typeId:
            self.search.Clear()
        self.RefreshList(self.search.GetValue())
        
    def OnLoadButton(self, evt):
        dlg = wx.FileDialog(
            self.parent, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            style=wx.OPEN | wx.CHANGE_DIR
            )

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            path = dlg.GetPath()
            #print paths
            self.fileText.SetValue(os.path.basename(path))
            self.LoadFileContent(path)
            self.RefreshList(self.search.GetValue())

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()
    
    def LoadFileContent(self, filename):
        wx.BeginBusyCursor()
        contentArr = None
        try :
            f = open(filename, "r")
            contents = f.readlines()[1:]
            #print contents
            contentArr = np.array([l.split() for l in contents])
            f.close()

            name_orig_temp = contentArr[:, 0];
            sort_arg = np.argsort(name_orig_temp)
            
            self.names_orig = name_orig_temp[sort_arg]
            self.values_orig = contentArr[:,1:][sort_arg].astype(np.float)

        except BaseException:
            showError(traceback.format_exc())
        finally :
            if f != None:
                f.close()
        del contentArr
        gc.collect()
        wx.EndBusyCursor()

        
        #print values
        #self.nameList.Clear()
        #for item in items:
        #    self.nameList.Append(item)
        #pass
    def RefreshList(self, searchString, sort=0):
        wx.BeginBusyCursor()
        try :
            self._RefreshList(searchString, sort)
        except BaseException:
            showError(traceback.format_exc())
        gc.collect()
        wx.EndBusyCursor()

    def _RefreshList(self, searchString, sort=0):
        searchString = searchString.upper().strip()
        self.nameList.Clear()
        if searchString == "" :
            self.names_disp = self.names_orig
            self.values_disp = self.values_orig
        else :
        #sort_arg = np.argsort(self.names_orig)
        #names_sort = self.names_orig[sort_arg]
            search_array = np.array([ l.upper().find(searchString) >= 0 for l in self.names_orig])
        #print search_array
            self.names_disp = self.names_orig[search_array]
            self.values_disp = self.values_orig[search_array]
        
        #for name in self.names_disp :
        #    self.nameList.Append(name)
        self.nameList.SetItems(self.names_disp)

def showError(msg):
    dlg = wx.MessageDialog(None, msg,
                           'Message',
                           wx.OK | wx.ICON_INFORMATION
                           )
    dlg.ShowModal()
    dlg.Destroy()

def doAnalyze(evt):
    index1 = load1.nameList.GetSelection()
    index2 = load2.nameList.GetSelection()
    if index1 < 0 or index2 < 0 :
        showError('No selection!')
        return

    try:
        data_x = load1.values_disp[index1, :]
        data_y = load2.values_disp[index2, :]
    except BaseException:
        showError("Data format error! (0x11)")
        return
    else:
        pass

    if data_x.shape[0] != data_y.shape[0] :
        showError("Data length doesn't match!")
        return
    #WA: for error "QCoreApplication::exec: The event loop is already running" 
    plt.ion()

    plt.clf()
    plt.plot(data_x, data_y, 'ro')
    #print data_x
    z1 = np.polyfit(data_x, data_y, 1)
    #print z1
    x1 = np.array([data_x.min(), data_x.max()])
    y1 = x1*z1[0] + z1[1]
    plt.plot(x1, y1, 'b')

    (r, p) = stats.pearsonr(data_x, data_y)
    title = "r={}, p={}".format(r,p)
    plt.title(title)

    plt.show()
    pass

def onDumpResult(evt):
    wx.BeginBusyCursor()
    try:
        _onDumpResult(evt)
    except BaseException:
        showError(traceback.format_exc())
    gc.collect()
    wx.EndBusyCursor()

def _onDumpResult(evt):
    if evt.GetId() == ID_DUMP1 :
        _load1 = load1
        _load2 = load2
    else:
        _load1 = load2
        _load2 = load1

    index = _load1.nameList.GetSelection()
    if index < 0 or load2.names_orig is None or load2.names_orig.size <= 0 :
        showError('No selection!')
        return
 
    if _load1.values_orig.shape[0] != _load1.values_orig.shape[0] :
        showError("Data length doesn't match!")
        return

    dlg = wx.FileDialog(
            frame, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard="Excel file (*.xls) |*.xls",
            style=wx.SAVE | wx.CHANGE_DIR
            )
    
    if dlg.ShowModal() == wx.ID_OK:
        # This returns a Python list of files that were selected.
        path = dlg.GetPath()
    else :
        path = ""
    dlg.Destroy()
    if path == "" :
        return;

    wb = xlwt.Workbook()
    ws = wb.add_sheet("sheet1")

    data1 = _load1.values_disp[index, :]

    ws.write(0, 0, _load1.names_disp[index])
    ws.write(0, 1, "R")
    ws.write(0, 2, "P")

    for index2 in range(0, _load2.values_orig.shape[0]) :
        index2_xls = index2 + 1
        if evt.GetId() == ID_DUMP1 :
            (r, p) = stats.pearsonr(data1, _load2.values_orig[index2])
        else:
            (r, p) = stats.pearsonr(_load2.values_orig[index2], data1)
        ws.write(index2_xls, 0, _load2.names_orig[index2])
        ws.write(index2_xls, 1, r)
        ws.write(index2_xls, 2, p)
    
    wb.save(path)
    showError("DONE!")
    pass

app = wx.App(False)
frame = wx.Frame(None, title = "Linear Regression (v1.0)", size = (400,400))

bkg = wx.Panel(frame)

load1 = FileLoader(bkg, "[X]")
load2 = FileLoader(bkg, "[Y]")

hbox = wx.BoxSizer()
hbox.Add(load1.vbox, flag = wx.EXPAND, proportion = 1)
hbox.Add(load2.vbox, flag = wx.EXPAND, proportion = 1)

runButton = wx.Button(bkg, label = "RUN")
bkgBox = wx.BoxSizer(wx.VERTICAL)
bkgBox.Add(hbox, proportion = 1, flag = wx.EXPAND)
bkgBox.Add(runButton, proportion = 0, flag = wx.ALL, border = 10)

runButton.Bind(wx.EVT_BUTTON, doAnalyze)

bkg.SetSizer(bkgBox)

#Menu
filemenu = wx.Menu()

ID_DUMP1 = 1
ID_DUMP2 = 2
# wx.ID_ABOUT和wx.ID_EXIT是wxWidgets提供的标准ID
menuDump1 = filemenu.Append(ID_DUMP1, "Left(1) vs Right(All)", \
            " Information about this program")    # (ID, 项目名称, 状态栏信息)
#filemenu.AppendSeparator()
menuDump2 = filemenu.Append(ID_DUMP2, "Left(All) vs Right(1)", \
            " Terminate the program")    # (ID, 项目名称, 状态栏信息)

# 创建菜单栏
menuBar = wx.MenuBar()
menuBar.Append(filemenu, "&File")    # 在菜单栏中添加filemenu菜单
frame.SetMenuBar(menuBar)    # 在frame中添加菜单栏

# 设置events
frame.Bind(wx.EVT_MENU, onDumpResult, menuDump1)
frame.Bind(wx.EVT_MENU, onDumpResult, menuDump2)

frame.Show()

app.MainLoop()

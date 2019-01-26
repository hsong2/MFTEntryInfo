# -*- coding: utf-8 -*-
from getMFTEntry import *
from mftAnalysis import *
from PyQt5 import QtCore, QtGui, QtWidgets
from openpyxl import load_workbook
import tkFileDialog
import os
import time
import sys
from datetime import datetime, timedelta, date
import win32com.client


TotalList = []
SortList = []
FilterList = []
FilterListSave = []
ListCheck = 0
Item = ''
sortText = ''
sortNum = 0


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1145, 784)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 121, 21))
        self.label.setObjectName("label")
        self.Search_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Search_Button.setGeometry(QtCore.QRect(750, 10, 101, 41))
        self.Search_Button.setObjectName("Search_Button")
        self.Excel_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Excel_Button.setGeometry(QtCore.QRect(1020, 710, 101, 41))
        self.Excel_Button.setObjectName("Excel_Button")
        self.Target_Address_Edit = QtWidgets.QLineEdit(self.centralwidget)
        self.Target_Address_Edit.setGeometry(QtCore.QRect(130, 10, 611, 41))
        self.Target_Address_Edit.setReadOnly(True)
        self.Target_Address_Edit.setObjectName("Target_Address_Edit")
        self.MFT_Print_Edit = QtWidgets.QTextEdit(self.centralwidget)
        self.MFT_Print_Edit.setGeometry(QtCore.QRect(20, 480, 1101, 221))
        self.MFT_Print_Edit.setReadOnly(True)
        self.MFT_Print_Edit.setObjectName("MFT_Print_Edit")
        self.Result_Table = QtWidgets.QTableWidget(self.centralwidget)
        self.Result_Table.setGeometry(QtCore.QRect(20, 60, 1101, 371))
        self.Result_Table.setObjectName("Result_Table")
        self.Result_Table.setColumnCount(7)
        column_header = ['D/F', '이름', '확장자', '생성시간', '수정시간', '접근시간', '크기']
        self.Result_Table.setHorizontalHeaderLabels(column_header)
        self.Result_Table.setColumnWidth(0, 70)
        self.Result_Table.setColumnWidth(1, 200)
        self.Result_Table.setColumnWidth(2, 100)
        self.Result_Table.setColumnWidth(3, 190)
        self.Result_Table.setColumnWidth(4, 190)
        self.Result_Table.setColumnWidth(5, 190)
        self.Result_Table.setColumnWidth(6, 100)
        self.Result_Table.horizontalHeader().setStretchLastSection(True)
        self.Result_Table.setRowCount(1)
        self.Analysis_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Analysis_Button.setGeometry(QtCore.QRect(860, 10, 101, 41))
        self.Analysis_Button.setObjectName("Analysis_Button")
        self.Filtering_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Filtering_Button.setGeometry(QtCore.QRect(970, 10, 81, 41))
        self.Filtering_Button.setObjectName("Filtering_Button")
        self.Restoration_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Restoration_Button.setGeometry(QtCore.QRect(1060, 10, 71, 41))
        self.Restoration_Button.setObjectName("Restoration_Button")
        self.Sort_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Sort_Button.setGeometry(QtCore.QRect(1000, 430, 121, 41))
        self.Sort_Button.setObjectName("Sort_pushButton")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setGeometry(QtCore.QRect(20, 430, 1101, 41))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.DF_Sort_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.DF_Sort_radioButton.setGeometry(QtCore.QRect(30, 440, 101, 22))
        self.DF_Sort_radioButton.setObjectName("DF_Sort_radioButton")
        self.Name_Sort_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.Name_Sort_radioButton.setGeometry(QtCore.QRect(170, 440, 81, 22))
        self.Name_Sort_radioButton.setObjectName("Name_Sort_radioButton")
        self.Ext_Sort_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.Ext_Sort_radioButton.setGeometry(QtCore.QRect(300, 440, 101, 22))
        self.Ext_Sort_radioButton.setObjectName("Ext_Sort_radioButton")
        self.Ctime_Sort_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.Ctime_Sort_radioButton.setGeometry(QtCore.QRect(440, 440, 121, 22))
        self.Ctime_Sort_radioButton.setObjectName("Ctime_Sort_radioButton")
        self.Mtime_Sort_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.Mtime_Sort_radioButton.setGeometry(QtCore.QRect(590, 440, 111, 22))
        self.Mtime_Sort_radioButton.setObjectName("Mtime_Sort_radioButton")
        self.Atime_Sort_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.Atime_Sort_radioButton.setGeometry(QtCore.QRect(730, 440, 111, 22))
        self.Atime_Sort_radioButton.setObjectName("Atime_Sort_radioButton")
        self.Size_Sort_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.Size_Sort_radioButton.setGeometry(QtCore.QRect(880, 440, 69, 22))
        self.Size_Sort_radioButton.setObjectName("Size_Sort_radioButton")
        self.tableWidget_2.raise_()
        self.label.raise_()
        self.Search_Button.raise_()
        self.Excel_Button.raise_()
        self.Target_Address_Edit.raise_()
        self.MFT_Print_Edit.raise_()
        self.Result_Table.raise_()
        self.Analysis_Button.raise_()
        self.Filtering_Button.raise_()
        self.Restoration_Button.raise_()
        self.Sort_Button.raise_()
        self.DF_Sort_radioButton.raise_()
        self.Name_Sort_radioButton.raise_()
        self.Ext_Sort_radioButton.raise_()
        self.Ctime_Sort_radioButton.raise_()
        self.Mtime_Sort_radioButton.raise_()
        self.Atime_Sort_radioButton.raise_()
        self.Size_Sort_radioButton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.Search_Button.clicked.connect(self.Target_Search)
        self.Excel_Button.clicked.connect(self.To_Excel)
        self.Analysis_Button.clicked.connect(self.Target_Analysis)
        self.Sort_Button.clicked.connect(self.Sort)
        self.Filtering_Button.clicked.connect(self.Filter)
        self.Restoration_Button.clicked.connect(self.Restore)
        self.DF_Sort_radioButton.clicked.connect(self.radioButtonClicked)
        self.Name_Sort_radioButton.clicked.connect(self.radioButtonClicked)
        self.Ext_Sort_radioButton.clicked.connect(self.radioButtonClicked)
        self.Ctime_Sort_radioButton.clicked.connect(self.radioButtonClicked)
        self.Mtime_Sort_radioButton.clicked.connect(self.radioButtonClicked)
        self.Atime_Sort_radioButton.clicked.connect(self.radioButtonClicked)
        self.Size_Sort_radioButton.clicked.connect(self.radioButtonClicked)
        self.Result_Table.itemSelectionChanged.connect(self.MFT_Print)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NTFS Parser"))
        self.label.setText(_translate("MainWindow", "선택된 폴더 :"))
        self.Search_Button.setText(_translate("MainWindow", "폴더 선택"))
        self.Excel_Button.setText(_translate("MainWindow", "문서 저장"))
        self.Analysis_Button.setText(_translate("MainWindow", "파일 분석"))
        self.Filtering_Button.setText(_translate("MainWindow", "필터링"))
        self.Restoration_Button.setText(_translate("MainWindow", "복원"))
        self.Sort_Button.setText(_translate("MainWindow", "정렬"))
        self.DF_Sort_radioButton.setText(_translate("MainWindow", "Dir/File"))
        self.Name_Sort_radioButton.setText(_translate("MainWindow", "이름"))
        self.Ext_Sort_radioButton.setText(_translate("MainWindow", "확장자"))
        self.Ctime_Sort_radioButton.setText(_translate("MainWindow", "생성시간"))
        self.Mtime_Sort_radioButton.setText(_translate("MainWindow", "수정시간"))
        self.Atime_Sort_radioButton.setText(_translate("MainWindow", "접근시간"))
        self.Size_Sort_radioButton.setText(_translate("MainWindow", "크기"))

    def MFT_Print(self):
        path = TotalList[self.Result_Table.currentRow()]['fullPath']
        select_file = TotalList[self.Result_Table.currentRow()]['D/F']
        mft_entry = getFileMFTEntry(path, select_file)
        mft_entry_str = analysisMFTEntry(mft_entry)
        self.MFT_Print_Edit.setText(mft_entry_str)

    def Target_Search(self):
        folder = tkFileDialog.askdirectory()
        self.Target_Address_Edit.setText(folder)

    def Target_Analysis(self):
        global TotalList
        global SortList
        global FilterListSave
        global ListCheck
        TotalList = []
        SortList = []
        FilterListSave = []

        target_dir = self.Target_Address_Edit.text()

        fDic = {}
        dDic = {}
        i = 0
        j = 0

        
        target_dir = target_dir.replace("/", "\\")
        #target_dir = os.path.normpath(target_dir)  # 입력받은 경로를 정규화 시킴
        
        for (path, dir, files)in os.walk(target_dir):  # 해당경로의 파일들을 모두 불러옴
            if (path == target_dir):
                for filename in files:
                    # 파일 부분
                    full_path = os.path.join(path, filename)
                    if "." in filename:
                        ext = filename.split(".")[-1]
                        filename = filename.split(".")[:-1]
                        filename = ".".join(filename)
                    else:
                        ext = ''
                    
                    fDic[j] = {'D/F': "File", 'name': filename, 'ext': ext, 'cTime': os.path.getctime(full_path),
                               'mTime': os.path.getmtime(full_path),
                               'aTime': os.path.getatime(full_path), 'size': os.path.getsize(full_path),
                               'fullPath': full_path}
                    TotalList.append(fDic[j])
                    j = j + 1
                for dirname in dir:
                    # 디렉터리 부분
                    full_path = os.path.join(path, dirname)
                    dDic[i] = {'D/F': 'Dir', 'name': dirname, 'ext': '', 'cTime': os.path.getctime(full_path),
                               'mTime': os.path.getmtime(full_path),
                               'aTime': os.path.getatime(full_path), 'size': os.path.getsize(full_path),
                               'fullPath': full_path}
                    TotalList.append(dDic[i])
                    i = i + 1
            else:
                break
            
        self.Result_Table.clear()
        column_header = ['D/F', '이름', '확장자', '생성시간', '수정시간', '접근시간', '크기']
        self.Result_Table.setHorizontalHeaderLabels(column_header)
        self.Result_Table.setRowCount(len(TotalList))
        
        for k in range(0, len(TotalList)):
            self.Result_Table.setItem(k, 0, QtWidgets.QTableWidgetItem(TotalList[k]['D/F']))
            self.Result_Table.setItem(k, 1, QtWidgets.QTableWidgetItem(TotalList[k]['name']))
            self.Result_Table.setItem(k, 2, QtWidgets.QTableWidgetItem(TotalList[k]['ext']))
            self.Result_Table.setItem(k, 3, QtWidgets.QTableWidgetItem(str(datetime.fromtimestamp(TotalList[k]['cTime']))))
            self.Result_Table.setItem(k, 4, QtWidgets.QTableWidgetItem(str(datetime.fromtimestamp(TotalList[k]['mTime']))))
            self.Result_Table.setItem(k, 5, QtWidgets.QTableWidgetItem(str(datetime.fromtimestamp(TotalList[k]['aTime']))))
            if TotalList[k]['size'] < 1024:
                self.Result_Table.setItem(k, 6, QtWidgets.QTableWidgetItem(str(TotalList[k]['size']) + 'Byte'))
            else:
                self.Result_Table.setItem(k, 6, QtWidgets.QTableWidgetItem(str(TotalList[k]['size'] / 1024) + 'KB'))
        SortList = TotalList
        FilterListSave = TotalList
        ListCheck = 1
        
    def To_Excel(self):
        if ListCheck == 1:
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = True
            wb = excel.Workbooks.Add()
            ws = wb.Worksheets("Sheet1")

            ws.Cells(1, 2).Value = "D/F"
            ws.Cells(1, 3).Value = "Name"
            ws.Cells(1, 4).Value = "Ext"
            ws.Cells(1, 5).Value = "C_Time"
            ws.Cells(1, 6).Value = "M_Time"
            ws.Cells(1, 7).Value = "A_Time"
            ws.Cells(1, 8).Value = "Size"
            for i in range(0, len(TotalList)):
                ws.Cells(i + 2, 1).Value = i + 1
                ws.Cells(i + 2, 2).Value = TotalList[i]['D/F']
                ws.Cells(i + 2, 3).Value = TotalList[i]['name']
                if TotalList[i]['ext'] != '':
                    ws.Cells(i + 2, 4).Value = str(TotalList[i]['ext']).split('.')[1]
                ws.Cells(i + 2, 5).Value = str(datetime.fromtimestamp(TotalList[i]['cTime']))
                ws.Cells(i + 2, 6).Value = str(datetime.fromtimestamp(TotalList[i]['mTime']))
                ws.Cells(i + 2, 7).Value = str(datetime.fromtimestamp(TotalList[i]['aTime']))
                ws.Cells(i + 2, 8).Value = TotalList[i]['size']
        elif ListCheck == 2:
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = True
            wb = excel.Workbooks.Add()
            ws = wb.Worksheets("Sheet1")

            ws.Cells(1, 2).Value = "D/F"
            ws.Cells(1, 3).Value = "Name"
            ws.Cells(1, 4).Value = "Ext"
            ws.Cells(1, 5).Value = "C_Time"
            ws.Cells(1, 6).Value = "M_Time"
            ws.Cells(1, 7).Value = "A_Time"
            ws.Cells(1, 8).Value = "Size"
            for i in range(0, len(SortList)):
                ws.Cells(i + 2, 1).Value = i + 1
                ws.Cells(i + 2, 2).Value = SortList[i]['D/F']
                ws.Cells(i + 2, 3).Value = SortList[i]['name']
                if SortList[i]['ext'] != '':
                    ws.Cells(i + 2, 4).Value = str(SortList[i]['ext']).split('.')[1]
                ws.Cells(i + 2, 5).Value = str(datetime.fromtimestamp(SortList[i]['cTime']))
                ws.Cells(i + 2, 6).Value = str(datetime.fromtimestamp(SortList[i]['mTime']))
                ws.Cells(i + 2, 7).Value = str(datetime.fromtimestamp(SortList[i]['aTime']))
                ws.Cells(i + 2, 8).Value = SortList[i]['size']
        elif ListCheck == 3:
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = True
            wb = excel.Workbooks.Add()
            ws = wb.Worksheets("Sheet1")

            ws.Cells(1, 2).Value = "D/F"
            ws.Cells(1, 3).Value = "Name"
            ws.Cells(1, 4).Value = "Ext"
            ws.Cells(1, 5).Value = "C_Time"
            ws.Cells(1, 6).Value = "M_Time"
            ws.Cells(1, 7).Value = "A_Time"
            ws.Cells(1, 8).Value = "Size"
            for i in range(0, len(FilterList)):
                ws.Cells(i + 2, 1).Value = i + 1
                ws.Cells(i + 2, 2).Value = FilterList[i]['D/F']
                ws.Cells(i + 2, 3).Value = FilterList[i]['name']
                if FilterList[i]['ext'] != '':
                    ws.Cells(i + 2, 4).Value = str(FilterList[i]['ext']).split('.')[1]
                ws.Cells(i + 2, 5).Value = str(datetime.fromtimestamp(FilterList[i]['cTime']))
                ws.Cells(i + 2, 6).Value = str(datetime.fromtimestamp(FilterList[i]['mTime']))
                ws.Cells(i + 2, 7).Value = str(datetime.fromtimestamp(FilterList[i]['aTime']))
                ws.Cells(i + 2, 8).Value = FilterList[i]['size']
        else:
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = True
            wb = excel.Workbooks.Add()
            ws = wb.Worksheets("Sheet1")

    def radioButtonClicked(self):
        global Item

        if self.DF_Sort_radioButton.isChecked():
            Item = 'D/F'
        elif self.Name_Sort_radioButton.isChecked():
            Item = 'name'
        elif self.Ext_Sort_radioButton.isChecked():
            Item = 'ext'
        elif self.Ctime_Sort_radioButton.isChecked():
            Item = 'cTime'
        elif self.Mtime_Sort_radioButton.isChecked():
            Item = 'mTime'
        elif self.Atime_Sort_radioButton.isChecked():
            Item = 'aTime'
        else:
            Item = 'size'

    def Sort(self):
        global sortText
        global sortNum
        global ListCheck

        if sortText != Item:
            sortNum = 0
        length = len(SortList)

        for i in range(length - 1):
            indexMin = i
            for j in range(i + 1, length):
                if SortList[indexMin][Item] > SortList[j][Item]:
                    indexMin = j
            SortList[i], SortList[indexMin] = SortList[indexMin], SortList[i]

        self.Result_Table.clear()
        column_header = ['D/F', '이름', '확장자', '생성시간', '수정시간', '접근시간', '크기']
        self.Result_Table.setHorizontalHeaderLabels(column_header)
        self.Result_Table.setRowCount(len(SortList))

        if sortNum == 0:
            for k in range(0, len(SortList)):
                self.Result_Table.setItem(k, 0, QtWidgets.QTableWidgetItem(SortList[k]['D/F']))
                self.Result_Table.setItem(k, 1, QtWidgets.QTableWidgetItem(SortList[k]['name']))
                if SortList[k]['ext'] != '':
                    self.Result_Table.setItem(k, 2, QtWidgets.QTableWidgetItem(str(SortList[k]['ext']).split('.')[1]))
                self.Result_Table.setItem(k, 3,
                                          QtWidgets.QTableWidgetItem(str(datetime.fromtimestamp(SortList[k]['cTime']))))
                self.Result_Table.setItem(k, 4,
                                          QtWidgets.QTableWidgetItem(str(datetime.fromtimestamp(SortList[k]['mTime']))))
                self.Result_Table.setItem(k, 5,
                                          QtWidgets.QTableWidgetItem(str(datetime.fromtimestamp(SortList[k]['aTime']))))
                if SortList[k]['size'] < 1024:
                    self.Result_Table.setItem(k, 6, QtWidgets.QTableWidgetItem(str(SortList[k]['size']) + 'Byte'))
                else:
                    self.Result_Table.setItem(k, 6, QtWidgets.QTableWidgetItem(str(SortList[k]['size'] / 1024) + 'KB'))
        else:
            for k in range(0, len(SortList)):
                self.Result_Table.setItem(len(SortList) - k - 1, 0, QtWidgets.QTableWidgetItem(SortList[k]['D/F']))
                self.Result_Table.setItem(len(SortList) - k - 1, 1, QtWidgets.QTableWidgetItem(SortList[k]['name']))
                if SortList[k]['ext'] != '':
                    self.Result_Table.setItem(len(SortList) - k - 1, 2,
                                              QtWidgets.QTableWidgetItem(str(SortList[k]['ext']).split('.')[1]))
                self.Result_Table.setItem(len(SortList) - k - 1, 3,
                                          QtWidgets.QTableWidgetItem(str(datetime.fromtimestamp(SortList[k]['cTime']))))
                self.Result_Table.setItem(len(SortList) - k - 1, 4,
                                          QtWidgets.QTableWidgetItem(str(datetime.fromtimestamp(SortList[k]['mTime']))))
                self.Result_Table.setItem(len(SortList) - k - 1, 5,
                                          QtWidgets.QTableWidgetItem(str(datetime.fromtimestamp(SortList[k]['aTime']))))
                if SortList[k]['size'] < 1024:
                    self.Result_Table.setItem(len(SortList) - k - 1, 6,
                                              QtWidgets.QTableWidgetItem(str(SortList[k]['size']) + 'Byte'))
                else:
                    self.Result_Table.setItem(len(SortList) - k - 1, 6,
                                              QtWidgets.QTableWidgetItem(str(SortList[k]['size'] / 1024) + 'KB'))

        sortNum += 1
        sortNum %= 2
        sortText = Item
        ListCheck = 2

    def Filter(self):
        global dlg
        global FilterList
        global ListCheck
        global FilterListSave
        global SortList
        global cTime_Start_Filter
        global cTime_End_Filter
        global mTime_Start_Filter
        global mTime_End_Filter
        global aTime_Start_Filter
        global aTime_End_Filter
        FilterList = []
        SortList = []
        cTime_Start_Filter = 0
        cTime_End_Filter = 0
        mTime_Start_Filter = 0
        mTime_End_Filter = 0
        aTime_Start_Filter = 0
        aTime_End_Filter = 0

        dlg = FilteringDialog()
        dlg.exec_()

        if dlg.closeBool == False:
            cTime_Start_Filter = time.mktime(
                date(int(dlg.cTimeY_Start), int(dlg.cTimeM_Start), int(dlg.cTimeD_Start)).timetuple())
            cTime_End_Filter = time.mktime(
                date(int(dlg.cTimeY_End), int(dlg.cTimeM_End), int(dlg.cTimeD_End)).timetuple())
            mTime_Start_Filter = time.mktime(
                date(int(dlg.mTimeY_Start), int(dlg.mTimeM_Start), int(dlg.mTimeD_Start)).timetuple())
            mTime_End_Filter = time.mktime(
                date(int(dlg.mTimeY_End), int(dlg.mTimeM_End), int(dlg.mTimeD_End)).timetuple())
            aTime_Start_Filter = time.mktime(
                date(int(dlg.aTimeY_Start), int(dlg.aTimeM_Start), int(dlg.aTimeD_Start)).timetuple())
            aTime_End_Filter = time.mktime(
                date(int(dlg.aTimeY_End), int(dlg.aTimeM_End), int(dlg.aTimeD_End)).timetuple())

            for i in range(0, len(FilterListSave)):
                if dlg.sizeOrder == '':
                    self.Filter_Func(i)
                elif dlg.sizeOrder == u'이상':
                    if int(dlg.size) <= FilterListSave[i]['size']:
                        self.Filter_Func(i)
                else:
                    if int(dlg.size) >= FilterListSave[i]['size']:
                        self.Filter_Func(i)

            self.Result_Table.clear()
            column_header = ['D/F', '이름', '확장자', '생성시간', '수정시간', '접근시간', '크기']
            self.Result_Table.setHorizontalHeaderLabels(column_header)
            self.Result_Table.setRowCount(len(FilterList))

            for k in range(0, len(FilterList)):
                self.Result_Table.setItem(k, 0, QtWidgets.QTableWidgetItem(FilterList[k]['D/F']))
                self.Result_Table.setItem(k, 1, QtWidgets.QTableWidgetItem(FilterList[k]['name']))
                if FilterList[k]['ext'] != '':
                    self.Result_Table.setItem(k, 2, QtWidgets.QTableWidgetItem(str(FilterList[k]['ext']).split('.')[1]))
                self.Result_Table.setItem(k, 3, QtWidgets.QTableWidgetItem(
                    str(datetime.fromtimestamp(FilterList[k]['cTime']))))
                self.Result_Table.setItem(k, 4, QtWidgets.QTableWidgetItem(
                    str(datetime.fromtimestamp(FilterList[k]['mTime']))))
                self.Result_Table.setItem(k, 5, QtWidgets.QTableWidgetItem(
                    str(datetime.fromtimestamp(FilterList[k]['aTime']))))
                if FilterList[k]['size'] < 1024:
                    self.Result_Table.setItem(k, 6, QtWidgets.QTableWidgetItem(str(FilterList[k]['size']) + 'byte'))
                else:
                    self.Result_Table.setItem(k, 6,
                                              QtWidgets.QTableWidgetItem(str(FilterList[k]['size'] / 1024) + 'KB'))

            SortList = FilterList
            FilterListSave = FilterList
            ListCheck = 3

    def Filter_Func(self, i):
        global dlg
        if dlg.df in FilterListSave[i]['D/F']:
            if dlg.name in FilterListSave[i]['name']:
                if dlg.ext in FilterListSave[i]['ext']:
                    if cTime_Start_Filter <= FilterListSave[i]['cTime']:
                        if cTime_End_Filter >= FilterListSave[i]['cTime']:
                            if mTime_Start_Filter <= FilterListSave[i]['mTime']:
                                if mTime_End_Filter >= FilterListSave[i]['mTime']:
                                    if aTime_Start_Filter <= FilterListSave[i]['aTime']:
                                        if aTime_End_Filter >= FilterListSave[i]['aTime']:
                                            FilterList.append(FilterListSave[i])

    def Restore(self):
        global SortList
        global FilterListSave
        global ListCheck
        SortList = []

        self.Result_Table.clear()
        column_header = ['D/F', '이름', '확장자', '생성시간', '수정시간', '접근시간', '크기']
        self.Result_Table.setHorizontalHeaderLabels(column_header)
        self.Result_Table.setRowCount(len(TotalList))

        for k in range(0, len(TotalList)):
            self.Result_Table.setItem(k, 0, QtWidgets.QTableWidgetItem(TotalList[k]['D/F']))
            self.Result_Table.setItem(k, 1, QtWidgets.QTableWidgetItem(TotalList[k]['name']))
            if TotalList[k]['ext'] != '':
                self.Result_Table.setItem(k, 2, QtWidgets.QTableWidgetItem(str(TotalList[k]['ext']).split('.')[1]))
            self.Result_Table.setItem(k, 3,
                                      QtWidgets.QTableWidgetItem(str(datetime.fromtimestamp(TotalList[k]['cTime']))))
            self.Result_Table.setItem(k, 4,
                                      QtWidgets.QTableWidgetItem(str(datetime.fromtimestamp(TotalList[k]['mTime']))))
            self.Result_Table.setItem(k, 5,
                                      QtWidgets.QTableWidgetItem(str(datetime.fromtimestamp(TotalList[k]['aTime']))))
            if TotalList[k]['size'] < 1024:
                self.Result_Table.setItem(k, 6, QtWidgets.QTableWidgetItem(str(TotalList[k]['size']) + 'Byte'))
            else:
                self.Result_Table.setItem(k, 6, QtWidgets.QTableWidgetItem(str(TotalList[k]['size'] / 1024) + 'KB'))

        SortList = TotalList
        FilterListSave = TotalList
        ListCheck = 1


class FilteringDialog(QtWidgets.QDialog):
    def __init__(self):
        super(FilteringDialog, self).__init__()
        self.setupUI()

        self.df = ''
        self.name = ''
        self.ext = ''
        self.cTimeY_Start = '1971'
        self.cTimeY_End = '2020'
        self.cTimeM_Start = '1'
        self.cTimeM_End = '1'
        self.cTimeD_Start = '1'
        self.cTimeD_End = '1'
        self.mTimeY_Start = '1971'
        self.mTimeY_End = '2020'
        self.mTimeM_Start = '1'
        self.mTimeM_End = '1'
        self.mTimeD_Start = '1'
        self.mTimeD_End = '1'
        self.aTimeY_Start = '1971'
        self.aTimeY_End = '2020'
        self.aTimeM_Start = '1'
        self.aTimeM_End = '1'
        self.aTimeD_Start = '1'
        self.aTimeD_End = '1'
        self.size = '0'
        self.sizeOrder = ''

        self.closeBool = False

    def setupUI(self):
        self.setGeometry(1250, 200, 500, 600)
        self.setWindowTitle("필터 설정창")

        df_Label = QtWidgets.QLabel("1. Dir or File : ", self)
        df_Label.setGeometry(20, 20, 120, 30)
        name_Label = QtWidgets.QLabel("2. 이     름 : ", self)
        name_Label.setGeometry(20, 70, 120, 30)
        ext_Label = QtWidgets.QLabel("3. 확 장 자 : ", self)
        ext_Label.setGeometry(20, 120, 120, 30)
        cTime_Label = QtWidgets.QLabel("4. 생성시간 : ", self)
        cTime_Label.setGeometry(20, 170, 120, 30)
        mTime_Label = QtWidgets.QLabel("5. 수정시간 : ", self)
        mTime_Label.setGeometry(20, 270, 120, 30)
        aTime_Label = QtWidgets.QLabel("6. 접근시간 : ", self)
        aTime_Label.setGeometry(20, 370, 120, 30)
        size_Label = QtWidgets.QLabel("7. 크     기 : ", self)
        size_Label.setGeometry(20, 470, 120, 30)

        dfList = ['', 'Dir', 'File']
        yearListStart = []
        yearListEnd = ['2020']
        monthList = []
        dayList = []
        orderList = ['', '이전', '이후']
        sizeOrderList = ['', '이상', '이하']
        for i in range(1971, 2021):
            yearListStart.append(str(i))
        for i in range(1971, 2021):
            yearListEnd.append(str(i))
        for i in range(1, 13):
            monthList.append(str(i))
        for i in range(1, 32):
            dayList.append(str(i))

        self.df_ComboBox = QtWidgets.QComboBox(self)
        self.df_ComboBox.setGeometry(140, 20, 60, 30)
        self.df_ComboBox.addItems(dfList)
        self.name_LineEdit = QtWidgets.QLineEdit(self)
        self.name_LineEdit.setGeometry(140, 70, 250, 30)
        self.ext_LineEdit = QtWidgets.QLineEdit(self)
        self.ext_LineEdit.setGeometry(140, 120, 250, 30)
        self.cTimeY_Start_ComboBox = QtWidgets.QComboBox(self)
        self.cTimeY_Start_ComboBox.setGeometry(140, 170, 80, 30)
        self.cTimeY_Start_ComboBox.addItems(yearListStart)
        cTimeY_Start_Label = QtWidgets.QLabel("년", self)
        cTimeY_Start_Label.setGeometry(225, 170, 25, 30)
        self.cTimeM_Start_ComboBox = QtWidgets.QComboBox(self)
        self.cTimeM_Start_ComboBox.setGeometry(250, 170, 60, 30)
        self.cTimeM_Start_ComboBox.addItems(monthList)
        cTimeM_Start_Label = QtWidgets.QLabel("월", self)
        cTimeM_Start_Label.setGeometry(315, 170, 25, 30)
        self.cTimeD_Start_ComboBox = QtWidgets.QComboBox(self)
        self.cTimeD_Start_ComboBox.setGeometry(340, 170, 60, 30)
        self.cTimeD_Start_ComboBox.addItems(dayList)
        cTimeD_Start_Label = QtWidgets.QLabel("일", self)
        cTimeD_Start_Label.setGeometry(405, 170, 25, 30)
        cTimeLink_Label = QtWidgets.QLabel("~", self)
        cTimeLink_Label.setGeometry(155, 220, 30, 30)
        self.cTimeY_End_ComboBox = QtWidgets.QComboBox(self)
        self.cTimeY_End_ComboBox.setGeometry(185, 220, 80, 30)
        self.cTimeY_End_ComboBox.addItems(yearListEnd)
        cTimeY_End_Label = QtWidgets.QLabel("년", self)
        cTimeY_End_Label.setGeometry(270, 220, 25, 30)
        self.cTimeM_End_ComboBox = QtWidgets.QComboBox(self)
        self.cTimeM_End_ComboBox.setGeometry(295, 220, 60, 30)
        self.cTimeM_End_ComboBox.addItems(monthList)
        cTimeM_End_Label = QtWidgets.QLabel("월", self)
        cTimeM_End_Label.setGeometry(360, 220, 25, 30)
        self.cTimeD_End_ComboBox = QtWidgets.QComboBox(self)
        self.cTimeD_End_ComboBox.setGeometry(385, 220, 60, 30)
        self.cTimeD_End_ComboBox.addItems(dayList)
        cTimeD_End_Label = QtWidgets.QLabel("일", self)
        cTimeD_End_Label.setGeometry(450, 220, 25, 30)
        self.mTimeY_Start_ComboBox = QtWidgets.QComboBox(self)
        self.mTimeY_Start_ComboBox.setGeometry(140, 270, 80, 30)
        self.mTimeY_Start_ComboBox.addItems(yearListStart)
        mTimeY_Start_Label = QtWidgets.QLabel("년", self)
        mTimeY_Start_Label.setGeometry(225, 270, 25, 30)
        self.mTimeM_Start_ComboBox = QtWidgets.QComboBox(self)
        self.mTimeM_Start_ComboBox.setGeometry(250, 270, 60, 30)
        self.mTimeM_Start_ComboBox.addItems(monthList)
        mTimeM_Start_Label = QtWidgets.QLabel("월", self)
        mTimeM_Start_Label.setGeometry(315, 270, 25, 30)
        self.mTimeD_Start_ComboBox = QtWidgets.QComboBox(self)
        self.mTimeD_Start_ComboBox.setGeometry(340, 270, 60, 30)
        self.mTimeD_Start_ComboBox.addItems(dayList)
        mTimeD_Start_Label = QtWidgets.QLabel("일", self)
        mTimeD_Start_Label.setGeometry(405, 270, 25, 30)
        mTimeLink_Label = QtWidgets.QLabel("~", self)
        mTimeLink_Label.setGeometry(155, 320, 30, 30)
        self.mTimeY_End_ComboBox = QtWidgets.QComboBox(self)
        self.mTimeY_End_ComboBox.setGeometry(185, 320, 80, 30)
        self.mTimeY_End_ComboBox.addItems(yearListEnd)
        mTimeY_End_Label = QtWidgets.QLabel("년", self)
        mTimeY_End_Label.setGeometry(270, 320, 25, 30)
        self.mTimeM_End_ComboBox = QtWidgets.QComboBox(self)
        self.mTimeM_End_ComboBox.setGeometry(295, 320, 60, 30)
        self.mTimeM_End_ComboBox.addItems(monthList)
        mTimeM_End_Label = QtWidgets.QLabel("월", self)
        mTimeM_End_Label.setGeometry(360, 320, 25, 30)
        self.mTimeD_End_ComboBox = QtWidgets.QComboBox(self)
        self.mTimeD_End_ComboBox.setGeometry(385, 320, 60, 30)
        self.mTimeD_End_ComboBox.addItems(dayList)
        mTimeD_End_Label = QtWidgets.QLabel("일", self)
        mTimeD_End_Label.setGeometry(450, 320, 25, 30)
        self.aTimeY_Start_ComboBox = QtWidgets.QComboBox(self)
        self.aTimeY_Start_ComboBox.setGeometry(140, 370, 80, 30)
        self.aTimeY_Start_ComboBox.addItems(yearListStart)
        aTimeY_Start_Label = QtWidgets.QLabel("년", self)
        aTimeY_Start_Label.setGeometry(225, 370, 25, 30)
        self.aTimeM_Start_ComboBox = QtWidgets.QComboBox(self)
        self.aTimeM_Start_ComboBox.setGeometry(250, 370, 60, 30)
        self.aTimeM_Start_ComboBox.addItems(dayList)
        aTimeM_Start_Label = QtWidgets.QLabel("월", self)
        aTimeM_Start_Label.setGeometry(315, 370, 25, 30)
        self.aTimeD_Start_ComboBox = QtWidgets.QComboBox(self)
        self.aTimeD_Start_ComboBox.setGeometry(340, 370, 60, 30)
        self.aTimeD_Start_ComboBox.addItems(dayList)
        aTimeD_Start_Label = QtWidgets.QLabel("일", self)
        aTimeD_Start_Label.setGeometry(405, 370, 25, 30)
        aTimeLink_Label = QtWidgets.QLabel("~", self)
        aTimeLink_Label.setGeometry(155, 420, 30, 30)
        self.aTimeY_End_ComboBox = QtWidgets.QComboBox(self)
        self.aTimeY_End_ComboBox.setGeometry(185, 420, 80, 30)
        self.aTimeY_End_ComboBox.addItems(yearListEnd)
        aTimeY_End_Label = QtWidgets.QLabel("년", self)
        aTimeY_End_Label.setGeometry(270, 420, 25, 30)
        self.aTimeM_End_ComboBox = QtWidgets.QComboBox(self)
        self.aTimeM_End_ComboBox.setGeometry(295, 420, 60, 30)
        self.aTimeM_End_ComboBox.addItems(monthList)
        aTimeM_End_Label = QtWidgets.QLabel("월", self)
        aTimeM_End_Label.setGeometry(360, 420, 25, 30)
        self.aTimeD_End_ComboBox = QtWidgets.QComboBox(self)
        self.aTimeD_End_ComboBox.setGeometry(385, 420, 60, 30)
        self.aTimeD_End_ComboBox.addItems(dayList)
        aTimeD_End_Label = QtWidgets.QLabel("일", self)
        aTimeD_End_Label.setGeometry(450, 420, 25, 30)
        self.size_LineEdit = QtWidgets.QLineEdit(self)
        self.size_LineEdit.setGeometry(140, 470, 250, 30)
        self.sizeOrder_ComboBox = QtWidgets.QComboBox(self)
        self.sizeOrder_ComboBox.setGeometry(400, 470, 60, 30)
        self.sizeOrder_ComboBox.addItems(sizeOrderList)

        self.apply_PushButton = QtWidgets.QPushButton("적  용", self)
        self.apply_PushButton.setGeometry(170, 530, 120, 40)
        self.close_PushButton = QtWidgets.QPushButton("종  료", self)
        self.close_PushButton.setGeometry(320, 530, 120, 40)

        self.apply_PushButton.clicked.connect(self.Application)
        self.close_PushButton.clicked.connect(self.Close)

    def Application(self):
        self.df = self.df_ComboBox.currentText()
        self.name = self.name_LineEdit.text()
        self.ext = self.ext_LineEdit.text()
        self.cTimeY_Start = self.cTimeY_Start_ComboBox.currentText()
        self.cTimeY_End = self.cTimeY_End_ComboBox.currentText()
        self.cTimeM_Start = self.cTimeM_Start_ComboBox.currentText()
        self.cTimeM_End = self.cTimeM_End_ComboBox.currentText()
        self.cTimeD_Start = self.cTimeD_Start_ComboBox.currentText()
        self.cTimeD_End = self.cTimeD_End_ComboBox.currentText()
        self.mTimeY_Start = self.mTimeY_Start_ComboBox.currentText()
        self.mTimeY_End = self.mTimeY_End_ComboBox.currentText()
        self.mTimeM_Start = self.mTimeM_Start_ComboBox.currentText()
        self.mTimeM_End = self.mTimeM_End_ComboBox.currentText()
        self.mTimeD_Start = self.mTimeD_Start_ComboBox.currentText()
        self.mTimeD_End = self.mTimeD_End_ComboBox.currentText()
        self.aTimeY_Start = self.aTimeY_Start_ComboBox.currentText()
        self.aTimeY_End = self.aTimeY_End_ComboBox.currentText()
        self.aTimeM_Start = self.aTimeM_Start_ComboBox.currentText()
        self.aTimeM_End = self.aTimeM_End_ComboBox.currentText()
        self.aTimeD_Start = self.aTimeD_Start_ComboBox.currentText()
        self.aTimeD_End = self.aTimeD_End_ComboBox.currentText()
        self.size = self.size_LineEdit.text()
        self.sizeOrder = self.sizeOrder_ComboBox.currentText()

        self.closeBool = False
        self.close()

    def Close(self):
        self.closeBool = True
        self.close()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


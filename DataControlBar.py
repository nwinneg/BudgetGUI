import os
import DataFunctions
import numpy as np

from PyQt6.QtCore import Qt

from PyQt6.QtGui import (
    QFont,
)

from PyQt6.QtWidgets import (
    QWidget, 
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QComboBox,
    QPushButton
)

class DataControlBar(QWidget):
    def __init__(self,dataSpreadsheet):
        super().__init__()

        # Member variables for month selection
        self.availableMonths = ["Select Month"]
        self.selectedMonth = "Select Month"
        self.spreadsheet = dataSpreadsheet

        # Make a layout to house the widget
        layout = QHBoxLayout()

        # Widget related member vars
        self.dropdownWidget = QComboBox()
        self.dropdownWidget.addItems(self.availableMonths)
        layout.addWidget(self.dropdownWidget)
        
        # Make update dropdown button
        self.refreshMonthsButton = QPushButton("Refresh Months")
        self.refreshMonthsButton.clicked.connect(self.on_refresh_button_click)
        layout.addWidget(self.refreshMonthsButton)

        # # Make calculate button
        # self.calculateButton = QPushButton("Calculate Costs")
        # self.calculateButton.clicked.connect(self.on_calculate_button_click)
        # layout.addWidget(self.calculateButton)

        # On switch 
        self.dropdownWidget.currentTextChanged.connect(self.on_selection_change)
        
        # Set the layout to this widget
        self.setLayout(layout)


    def on_selection_change(self,text):
        self.selectedMonth = text

    def updateAvailableMonths(self,monthList):
        # Used from data
        self.dropdownWidget.clear()
        self.availableMonths = ["Select Month"]
        for mm in range(len(monthList)):
            self.availableMonths.append(monthList[mm])
        self.dropdownWidget.addItems(self.availableMonths)
    
    # def on_calculate_button_click(self):
    #     print("TODO Calc")
    
    def on_refresh_button_click(self):
        # print("TODO Refresh Months")
        if len(self.spreadsheet.filePaths) > 0:
            DataFunctions.getAccountType(self.spreadsheet.filePaths[0])

        monthArrays = []
        venmoMonths = []
        # Loop through files and get available months
        for row in range(self.spreadsheet.table_widget.rowCount()):

            fpath = self.spreadsheet.filePaths[row]
            cardType = self.spreadsheet.table_widget.item(row,1).text()
            tmpAvail = DataFunctions.getAvailableMonths(fpath,cardType)
            
            if cardType == "Venmo":
                venmoMonths.append(tmpAvail)
            else:
                monthArrays.append(tmpAvail)
            
        if venmoMonths != []:
            monthArrays.append(venmoMonths)

        availableMonths = set(monthArrays[0])

        for sublist in monthArrays[1:]:
            availableMonths &= set(sublist)

        # Convert back to list if needed
        availableMonths = list(availableMonths)

        # Update member variable
        self.updateAvailableMonths(list(availableMonths))

class AppControlBar(QWidget):
    def __init__(self,costSheet,fileSheet,transactionSheet,controlBar):
        super().__init__()

        self.costSheet = costSheet
        self.fileSheet = fileSheet
        self.transactionSheet = transactionSheet
        self.controlBar = controlBar
        
        self.resetButton = QPushButton("Reset")
        self.resetButton.setStyleSheet(
            "QPushButton {"
            "color: red;"  # Change font color
            "font-weight: bold;"  # Make the font bold
            "}"
        )
        self.resetButton.clicked.connect(self.resetApp)

        self.calculateButton = QPushButton("Calculate Costs")
        self.calculateButton.setStyleSheet(
            "QPushButton {"
            "color: black;"  # Change font color
            "font-weight: bold;"  # Make the font bold
            "}"
        )
        self.calculateButton.clicked.connect(self.calculate)

        self.copySelectedButton = QPushButton("Copy Selected")
        self.copySelectedButton.setStyleSheet(
            "QPushButton {"
            "color: blue;"  # Change font color
            "font-weight: bold;"  # Make the font bold
            "}"
        )
        self.copySelectedButton.clicked.connect(self.copySelected)

        layout = QHBoxLayout()
        layout.addWidget(self.resetButton)
        layout.addWidget(self.calculateButton)
        layout.addWidget(self.copySelectedButton)
        self.setLayout(layout)

    def resetApp(self):
        print("TODO: RESET")

    def copySelected(self):
        print("TODO: COPY")

    def calculate(self):
        fileList = self.fileSheet.filePaths
        
        cardTypes = []
        for ff in range(len(fileList)):
            cardTypes.append(self.fileSheet.table_widget.item(ff,1).text())
        
        month = self.controlBar.selectedMonth
        if month == "Select Month":
            return 1

        # Returns the table to put into transaction table
        DataFunctions.calculateCosts(fileList,cardTypes,month,self.costSheet,self.transactionSheet)
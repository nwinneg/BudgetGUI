import os
import DataFunctions

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

        # Make calculate button
        self.calculateButton = QPushButton("Calculate Costs")
        self.calculateButton.clicked.connect(self.on_calculate_button_click)
        layout.addWidget(self.calculateButton)

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
        self.avaliableMonths.append(monthList)
        self.dropdownWidget.addItems(self.availableMonths)
    
    def on_calculate_button_click(self):
        print("TODO Calc")
    
    def on_refresh_button_click(self):
        # print("TODO Refresh Months")
        if len(self.spreadsheet.filePaths) > 0:
            DataFunctions.getAccountType(self.spreadsheet.filePaths[0])

        # print(self.spreadsheet.filePaths)

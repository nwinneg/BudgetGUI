import sys
from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
    QMimeData,
    QTimer
)
from PyQt6.QtGui import (
    QDragEnterEvent, 
    QDropEvent,
    QFont,
    QClipboard,
    QAction
)
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QLabel,
    QLayout,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QTableWidget, 
    QTableWidgetItem, 
    QSizePolicy,
    QPushButton,
    QFileDialog,
    QMessageBox
)
import venmoTools_v2
import bofaTools
import capitalOneTools

import csv
import subprocess
import datetime
import numpy as np

#set PATH=%PATH%;C:\Users\nwinn\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\LocalCache\local-packages\Python38\Scripts
# set PATH=%PATH%;C:\Users\nwinn\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\LocalCache\local-packages\Python38\site-packages
# cmd prompt: >> auto-py-to-exe to make executable

class BudgetApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainWindow = QMainWindow

        self.setWindowTitle("Budget Calculator")

        self.Version = 1.0
        self.Author = "NIW"

        self.winWidth = 800
        self.winHeight = 600

        self.setGeometry(100, 100, self.winWidth, self.winHeight)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        # Initialize nested layout
        resetSaveLayout = QHBoxLayout()
        leftLayout = QVBoxLayout()
        appLayout = QHBoxLayout()
        topLayout = QVBoxLayout() # top most layout
        rightLayout = QVBoxLayout()

        # Add title to top layout
        self.createTitleField(topLayout)

        # Drag Drop Buttons
        self.createDropField("Savor",0,leftLayout)
        self.createDropField("Journey",0,leftLayout)
        self.createDropField("Venmo",0,leftLayout)
        self.createDropField("Bofa",0,leftLayout)

        # Make save button
        self.saveButton = self.createSaveButton(resetSaveLayout)

        # Make copy button
        self.copyButton = self.createCopyButton(resetSaveLayout)

        # Make a reset button
        self.resetButton = self.createResetButton(resetSaveLayout)
        self.resetButton.clicked.connect(self.resetApp)

        resetSaveWidget = QWidget()
        resetSaveWidget.setLayout(resetSaveLayout)
        resetSaveWidget.setMaximumHeight(resetSaveWidget.minimumSizeHint().height())
        leftLayout.addWidget(resetSaveWidget)

        leftWidget = QWidget()
        leftWidget.setLayout(leftLayout)
        # leftWidget.setMinimumWidth(int(self.winWidth/2))
        leftWidget.setAutoFillBackground(True)

        appLayout.addWidget(leftWidget)
        self.spreadsheet = self.createSpreadsheet(rightLayout)

        # Actions on copy and save button clicks
        self.copyButton.clicked.connect(self.copySelected)
        self.saveButton.clicked.connect(self.saveSpreadsheet)

        nameLabel = QLabel(f"Version: {self.Version} \t Author: {self.Author}")
        nameLabel.setMaximumHeight(nameLabel.minimumSizeHint().height())
        rightLayout.addWidget(nameLabel,alignment=Qt.Alignment.AlignHCenter)
        appLayout.addLayout(rightLayout)

        appLayout.setStretchFactor(leftWidget,2)
        
        appWidget = QWidget()
        appWidget.setLayout(appLayout)
        appWidget.setMinimumHeight(self.spreadsheet.minHeight)

        topLayout.addWidget(appWidget)

        centralWidget.setLayout(topLayout)

    def createTitleField(self,layout):
        # Add title to top layout
        titleLabel = QLabel("<h1><i>Budget Manager</i></h1>")
        layout.addWidget(titleLabel,alignment=Qt.Alignment.AlignHCenter)

    def createDropField(self,fieldName,colorFlag,layout):
        # Create the drop area to the right of the label
        dropArea = DropArea(self,fieldName)
        layout.addWidget(dropArea)

    def createSpreadsheet(self,layout):
        spreadsheet = Spreadsheet(self.winWidth)
        layout.addWidget(spreadsheet)
        return spreadsheet
    
    def getSpreadsheet(self):
        return self.spreadsheet
    
    def handleFileDroppedVenmo(self,fpath):
        vsum = venmoTools_v2.venmoCompute(fpath)
        wifiCost = venmoTools_v2.getWifi(fpath)
        Spreadsheet.modifyField(self.spreadsheet,'Venmo Bofa Net',-vsum)
        Spreadsheet.modifyField(self.spreadsheet,'Wifi',wifiCost)

    def handleFileDroppedBofa(self,fpath):
        eversourceTotal = bofaTools.getEversource(fpath)
        travelersTotal = bofaTools.getTravelers(fpath)
        Spreadsheet.modifyField(self.spreadsheet,'Utilities (Gas/Elect)',-eversourceTotal)
        Spreadsheet.modifyField(self.spreadsheet,'Car Insurance',-travelersTotal)

    def handleFileDroppedCapitalOne(self,fpath):
        cardNum = capitalOneTools.getCardNumber(fpath)
        costs = capitalOneTools.computeCosts(fpath)
        if cardNum == 8949:
            spotifyCost = capitalOneTools.getSpotify(fpath)
            costs['Other'] = costs['Other'] - spotifyCost
        Spreadsheet.modifyField(self.spreadsheet,'Groceries',costs['Groceries'])
        Spreadsheet.modifyField(self.spreadsheet,'Merchandise',costs['Merchandise'])
        Spreadsheet.modifyField(self.spreadsheet,'Dining Out',costs['Dining Out'])
        Spreadsheet.modifyField(self.spreadsheet,'Gas/Auto',costs['Gas/Auto'])
        Spreadsheet.modifyField(self.spreadsheet,'Other',costs['Other'])
        if cardNum == 8949:
            Spreadsheet.modifyField(self.spreadsheet,'Spotify',spotifyCost)

    def createSaveButton(self,layout):
        button = QPushButton("SAVE")
        button.setStyleSheet("color: black")
        layout.addWidget(button)
        return button

    def createResetButton(self,layout):
        button = QPushButton("RESET")
        button.setStyleSheet("color: red")
        layout.addWidget(button)
        return button

    def createCopyButton(self,layout):
        button = QPushButton("COPY SELECTED")
        button.setStyleSheet("color: blue")
        layout.addWidget(button)
        return button

    def saveSpreadsheet(self):
        Spreadsheet.save_to_csv(self.spreadsheet)

    def copySelected(self):
        Spreadsheet.copy_selected_data(self.spreadsheet)

    def resetApp(self):
        # self.close()
        # subprocess.call("python"+" nw_v2.py",shell=True)
        self.mainWindow = QMainWindow

        self.setWindowTitle("Budget Calculator")

        self.Version = 1.0
        self.Author = "NIW"

        self.winWidth = 800
        self.winHeight = 600

        self.setGeometry(100, 100, self.winWidth, self.winHeight)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        # Initialize nested layout
        resetSaveLayout = QHBoxLayout()
        leftLayout = QVBoxLayout()
        appLayout = QHBoxLayout()
        topLayout = QVBoxLayout() # top most layout
        rightLayout = QVBoxLayout()

        # Add title to top layout
        self.createTitleField(topLayout)

        # Drag Drop Buttons
        self.createDropField("Savor",0,leftLayout)
        self.createDropField("Journey",0,leftLayout)
        self.createDropField("Venmo",0,leftLayout)
        self.createDropField("Bofa",0,leftLayout)

        # Make save button
        self.saveButton = self.createSaveButton(resetSaveLayout)

        # Make copy button
        self.copyButton = self.createCopyButton(resetSaveLayout)

        # Make a reset button
        self.resetButton = self.createResetButton(resetSaveLayout)
        self.resetButton.clicked.connect(self.resetApp)

        resetSaveWidget = QWidget()
        resetSaveWidget.setLayout(resetSaveLayout)
        resetSaveWidget.setMaximumHeight(resetSaveWidget.minimumSizeHint().height())
        leftLayout.addWidget(resetSaveWidget)

        leftWidget = QWidget()
        leftWidget.setLayout(leftLayout)
        # leftWidget.setMinimumWidth(int(self.winWidth/2))
        leftWidget.setAutoFillBackground(True)

        appLayout.addWidget(leftWidget)
        self.spreadsheet = self.createSpreadsheet(rightLayout)

        # Actions on copy and save button clicks
        self.copyButton.clicked.connect(self.copySelected)
        self.saveButton.clicked.connect(self.saveSpreadsheet)

        nameLabel = QLabel(f"Version: {self.Version} \t Author: {self.Author}")
        nameLabel.setMaximumHeight(nameLabel.minimumSizeHint().height())
        rightLayout.addWidget(nameLabel,alignment=Qt.Alignment.AlignHCenter)
        appLayout.addLayout(rightLayout)

        appLayout.setStretchFactor(leftWidget,2)
        
        appWidget = QWidget()
        appWidget.setLayout(appLayout)
        appWidget.setMinimumHeight(self.spreadsheet.minHeight)

        topLayout.addWidget(appWidget)

        centralWidget.setLayout(topLayout)


class DropArea(QWidget):

    def __init__(self,appInstance,source_data):
        super().__init__()
        self.appInstance = appInstance
        self.source_data = source_data
        self.setAcceptDrops(True)
        self.labelFormat = ["<h4>","</h4>"]
        layout = QVBoxLayout(self)
        self.label = QLabel(f"{self.labelFormat[0]}{self.source_data}{self.labelFormat[1]}", self)
        self.label.setAlignment(Qt.Alignment.AlignCenter)
        self.label.setStyleSheet("color: blue; background-color: #d3d3d3")
        layout.addWidget(self.label)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.label.setText(f"{self.labelFormat[0]}{self.source_data}{self.labelFormat[1]}\n{file_path}")
            self.label.setStyleSheet("color: green; background-color: #d3d3d3")
            self.label.setWordWrap(True)
            # If it's a venmo file, do this
            if self.source_data == 'Venmo':
                BudgetApp.handleFileDroppedVenmo(self.appInstance,file_path)
            elif self.source_data == 'Bofa':
                BudgetApp.handleFileDroppedBofa(self.appInstance,file_path)
            elif self.source_data == 'Journey' or self.source_data == 'Savor':
                BudgetApp.handleFileDroppedCapitalOne(self.appInstance,file_path)

class Spreadsheet(QWidget):
    def __init__(self,winWidth):
        super().__init__()

        self.winWidth = winWidth

        layout = QVBoxLayout(self)
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(2)
        self.table_widget.setMaximumWidth(int(self.winWidth/3))
        layout.addWidget(self.table_widget)
        
        self.data = {
            "Rent": "1550",
            "Utilities (Gas/Elect)": "0",
            "Wifi": "0",
            "Groceries": "0",
            "Merchandise": "0",
            "Dining Out": "0",
            "Rental Insurance": "0",
            "Rent Deposits": "0",
            "Gas/Auto": "0",
            "Car Insurance": "0",
            "Spotify": "0",
            "Venmo Bofa Net": "0",
            "Healthcare": "0",
            "Other": "0",
            "Total": "1550"
        }

        self.set_data()
        self.minHeight = self.table_widget.minimumSizeHint().height()

    def set_data(self):
        row_count = len(self.data)
        self.table_widget.setRowCount(row_count)
        
        row = 0
        for field, value in self.data.items():
            field_item = QTableWidgetItem(field)
            field_item.setTextAlignment(Qt.Alignment.AlignCenter)
            value_item = QTableWidgetItem(value)
            value_item.setTextAlignment(Qt.Alignment.AlignCenter)
            self.table_widget.setItem(row, 0, field_item)
            self.table_widget.setItem(row, 1, value_item)
            row += 1

        self.table_widget.setHorizontalHeaderLabels(["Catagory", "Summed Expenses"])
        headerFont = QFont()
        headerFont.setBold(True)
        self.table_widget.horizontalHeader().setFont(headerFont)

        self.table_widget.resizeColumnsToContents()
    
    def modifyField(self,field,value):
        self.data[field] = str(float(self.data[field]) + np.round(value,2))
        self.data['Total'] = str(np.round(np.sum(np.array(list(self.data.values()))[0:-1].astype(float))))
        self.set_data()

    def save_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "C:/Users/nwinn/Desktop/"+'BudgetCosts_'+str(datetime.date.today()).replace(' ',''), "CSV Files (*.csv)")
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for row in range(self.table_widget.rowCount()):
                row_data = []
                for column in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, column)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                writer.writerow(row_data)

    def copy_selected_data(self):
        clipboard = QApplication.clipboard()
        selected_items = self.table_widget.selectedItems()
        
        if selected_items:
            mime_data = QMimeData()
            table_data = ""

            # Build a tab-separated string from the selected items
            for item in selected_items:
                table_data += item.text() + "\n"
            
            mime_data.setText(table_data.strip())  # Set the text data in the MIME data
            clipboard.setMimeData(mime_data)
            # Maybe put up a message -- TODO
        else:
            # Maybe put up a message -- TODO
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BudgetApp()
    window.show()
    sys.exit(app.exec())
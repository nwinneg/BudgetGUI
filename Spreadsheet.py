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
    QVBoxLayout,
    QTableWidget, 
    QTableWidgetItem, 
    QHeaderView,
    QLabel
)

# USAGE
#   Create a spreadsheet object by calling Spreadsheet(winWidth,winHeight)
#   Use the member function to set the size and 

class FileSpreadsheet(QWidget):
    def __init__(self, winWidth, winHeight):
        super().__init__()

        # Generalized Spreadsheet Class
        self.table_widget = QTableWidget(self)

        # Store the window size
        self.winWidth = winWidth
        self.winHeight = winHeight

        # Store a list of file paths that correspond to the table
        self.filePaths = []

        # Set it up to accept files if desired (defaults to false)
        self.setAcceptDrops(True)
        self.acceptClicks = True

        # Set it up to handle delete click event
        self.table_widget.cellClicked.connect(self.on_cell_clicked)

        layout = QVBoxLayout()

        layout.addWidget(self.table_widget)
        self.setLayout(layout)        

    def setSheetParams(self, **kwargs):
        # Set the number of rows and columns for the table
        sz = kwargs["size"]
        self.table_widget.setRowCount(sz[0])
        self.table_widget.setColumnCount(sz[1])

        # Set the column titles (headers)
        self.table_widget.setHorizontalHeaderLabels(kwargs['titles'])
        headerFont = QFont()
        headerFont.setBold(True)
        # if len(kwargs['titles']) < 2:
        #     self.table_widget.setSpan(0, 0, 1, sz[1]) 
        self.table_widget.horizontalHeader().setFont(headerFont)

        # Make a matrix of data to fill in
        #   If 1D, defaults to first column, otherwise follow matrix structure
        if 'dataLabels' in kwargs:
            dataLabels = kwargs['dataLabels']
            addLabels = True
            onlyOneRow = False
            if any(dim == 1 for dim in dataLabels.shape) | (dataLabels.ndim == 1):
                onlyOneRow = True
        else:
            addLabels = False
            onlyOneRow = True

        # Calcualte row height
        sizePct = kwargs["sizePct"]
        rowHeight = (self.winHeight * sizePct[0]) / (sz[0])
        colWidth = (self.winWidth * sizePct[1]) / (sz[1])

        header = self.table_widget.horizontalHeader()
 
        # Populate the table with empty strings
        for row in range(sz[0]):

            self.table_widget.resizeRowToContents(row)

            for col in range(sz[1]):
                if addLabels & (onlyOneRow) & (col == 0):
                    item = QTableWidgetItem(dataLabels[row])
                elif addLabels & (not onlyOneRow):
                    item = QTableWidgetItem(dataLabels[row,col])
                else:
                    item = QTableWidgetItem("")

                self.table_widget.setItem(row, col, item)
                self.table_widget.setColumnWidth(col,colWidth)

        # Resize the called out ones and then maximize the rest
        if 'sizeColsOnContent' in kwargs:
            
            listToShrink = kwargs['sizeColsOnContent']
            listToGrow = [item for item in range(sz[1]) if item not in listToShrink]
            
            for col in kwargs['sizeColsOnContent']:
                self.table_widget.resizeColumnToContents(col)

            if len(listToGrow) > 0:
                # maxWidth = self.table_widget.width()
                header = self.table_widget.horizontalHeader()
                # remainingWidth = maxWidth- sum([header.sectionSize(i) for i in listToShrink])
                # nRemainingCols = len(listToGrow)

                for col in listToGrow:
                    header.setSectionResizeMode(col,QHeaderView.ResizeMode.Stretch)

        self.table_widget.setMaximumWidth(self.winWidth * sizePct[1])
        self.table_widget.setMaximumHeight(self.winHeight * sizePct[0])

        # Delete the first row on init
        if self.table_widget.columnCount() > 2:
            self.deleteRow(0,True)

    def addRow(self):
        row_position = self.table_widget.rowCount()  # Get the current row count
        self.table_widget.insertRow(row_position)  # Insert a row at the end

        for col in range(self.table_widget.columnCount()):
            hdr = self.get_column_header(col)
            if hdr == "Delete":
                item = QTableWidgetItem("X")
                item.setTextAlignment(Qt.Alignment.AlignCenter)
                self.table_widget.setItem(row_position, col, item)
            else:
                self.table_widget.setItem(row_position, col, QTableWidgetItem(""))
            
    def addRowData(self,data):
        #TODO: This will be easier
        pass

    def deleteRow(self,rowIndex,isInit=False):
        if rowIndex >= self.table_widget.rowCount():
            return
        self.table_widget.removeRow(rowIndex)
        
        if (not isInit):
            del self.filePaths[rowIndex]

    def get_column_header(self, col: int) -> str:
        """Returns the header label for the given column index."""
        return self.table_widget.horizontalHeaderItem(col).text()
    
    def dragEnterEvent(self, event):
        """Handle the drag enter event."""
        # Check if the dragged data is of type files (Mime data for files)
        if event.mimeData().hasUrls():
            event.acceptProposedAction()  # Accept the drag
        else:
            event.ignore()  # Ignore the drag if not a file

    def dropEvent(self, event):
        """Handle the drop event."""
        # Get the URLs (file paths) dropped onto the widget
        file_urls = event.mimeData().urls()

        for url in file_urls:
            file_path = url.toLocalFile()  # Convert URL to file path
            if os.path.isfile(file_path) & url.toLocalFile().lower().endswith(".csv"):  # Check if it's a valid file (CSV Only for now)
                if self.table_widget.item(1,0) != "":
                    self.addRow()
                rowPos = self.table_widget.rowCount()-1
                filename = file_path.split("/")
                filename = filename[-1]
                self.filePaths.append(file_path)
                cardType = DataFunctions.getAccountType(file_path)
                self.table_widget.setItem(rowPos, 0, QTableWidgetItem("File: {}".format(filename)))
                self.table_widget.setItem(rowPos,1,QTableWidgetItem(cardType))
                

    def on_cell_clicked(self,row,col):
        # Check whether to act at all
        if not self.acceptClicks:
            return
        
        # Get the header
        hdr = self.get_column_header(col)

        if hdr == "Delete":
            self.deleteRow(row)

class CostSpreadsheet(QWidget):
    def __init__(self,winWidth,winHeight):
        super().__init__()

        self.table_widget = QTableWidget()

        # Store the window size
        self.winWidth = winWidth
        self.winHeight = winHeight

        self.data = {"Rent":"0",
                     "Utilities (Gas/Elect)":"0",
                     "Wifi":"0",
                      "Groceries":"0",
                      "Merchandise":"0",
                      "Dining Out":"0",
                      "Rental Insurance":"0",
                      "Rent Deposits":"0",
                      "Gas/Auto":"0",
                      "Car Insurance":"0",
                      "Spotify":"0",
                      "Venmo Bofa Net":"0",
                      "Healthcare":"0",
                      "Other":"0",
                      "Total":"0"}
                
        self.colHeaders = ["Catagory","Total Cost"]

        self.table_widget.setRowCount(len(self.data))
        self.table_widget.setColumnCount(len(self.colHeaders))
        
        self.initializeTable()

        self.table_widget.setMinimumHeight(self.winHeight*0.75)
        # self.table_widget.setMinimumWidth(self.winWidth*.1)
        # self.table_widget.resizeColumnsToContents()

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget,alignment=Qt.Alignment.AlignTop)
        self.setLayout(layout)

        # Initialize the table

    def initializeTable(self):

        # Set the headers
        self.table_widget.setHorizontalHeaderLabels(self.colHeaders)
        header = self.table_widget.horizontalHeader()
        bold_font = header.font()
        bold_font.setBold(True)
        header.setFont(bold_font)

        # Disable row numbers
        self.table_widget.verticalHeader().setVisible(False)

        # Init table size
        self.table_widget.setRowCount(len(self.data))
        self.table_widget.setColumnCount(len(self.colHeaders))

        # Populate with initial data
        self.setData()

    def setData(self):
        rowCount = len(self.data)

        # Update the table
        header = self.table_widget.horizontalHeader()
        row = 0
        for field,value in self.data.items():
            
            field_item = QTableWidgetItem(field)
            field_item.setTextAlignment(Qt.Alignment.AlignCenter)

            value_item = QTableWidgetItem(value)
            value_item.setTextAlignment(Qt.Alignment.AlignCenter)

            self.table_widget.setItem(row, 0, field_item)
            self.table_widget.setItem(row, 1, value_item)

            self.table_widget.resizeRowToContents(row)

            self.table_widget.resizeColumnToContents(0)
            self.table_widget.resizeColumnToContents(1)

            self.table_widget.setColumnWidth(0, max(self.table_widget.columnWidth(0),header.sectionSize(0)))
            self.table_widget.setColumnWidth(1, max(self.table_widget.columnWidth(1),header.sectionSize(1)))

            row += 1

        # Resize the table to be the width of the columns
        tabWidth = self.table_widget.columnWidth(0) + self.table_widget.columnWidth(1) + 2
        if self.table_widget.verticalScrollBar().isVisible():
            tabWidth += self.table_widget.verticalScrollBar().width()
        self.table_widget.setFixedWidth(tabWidth)
        
    def updateTotal(self):
        # Update the total
        keys = list(self.data.keys())
        tsum = 0
        for key in keys:
            if key == "Total":
                continue
            tsum += float(self.data[key])
        self.data["Total"] = str(tsum)
        
    def resetTable(self):
        self.data = {"Rent":"0",
                     "Utilities (Gas/Elect)":"0",
                     "Wifi":"0",
                      "Groceries":"0",
                      "Merchandise":"0",
                      "Dining Out":"0",
                      "Rental Insurance":"0",
                      "Rent Deposits":"0",
                      "Gas/Auto":"0",
                      "Car Insurance":"0",
                      "Spotify":"0",
                      "Venmo Bofa Net":"0",
                      "Healthcare":"0",
                      "Other":"0",
                      "Total":"0"}
        
        self.initializeTable()

class TransactionSheet(QWidget):
    def __init__(self,winWidth,winHeight):
        super().__init__()

        self.table_widget = QTableWidget()

        self.winWidth = winWidth
        self.winHeight = winHeight

        self.colHeaders = ["Account","Description","Date","Cost"]
        self.colsToShrink = [0,2,3] # Resize these columns to content

        self.table_widget.setColumnCount(len(self.colHeaders))

        self.table_widget.setHorizontalHeaderLabels(self.colHeaders)
        header = self.table_widget.horizontalHeader()
        bold_font = header.font()
        bold_font.setBold(True)
        header.setFont(bold_font)

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)
    
    def updateSheet(self,newSheet):
        self.table_widget.setColumnCount(4)
        self.table_widget.setRowCount(newSheet.shape[0])

        for row in range(newSheet.shape[0]):
            for col in range(newSheet.shape[1]):
                item = QTableWidgetItem(str(newSheet.iat[row, col]))  # Convert cell to string
                self.table_widget.setItem(row, col, item)
                self.table_widget.resizeColumnToContents(col)
                # if col == 1:
                #     self.table_widget.resizeColumnToContents(col)
                    




        

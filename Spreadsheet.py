import os
import DataFunctions

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

class Spreadsheet(QWidget):
    def __init__(self, winWidth, winHeight,acceptDrops=False,acceptClicks=False):
        super().__init__()

        # Generalized Spreadsheet Class
        self.table_widget = QTableWidget(self)

        # Store the window size
        self.winWidth = winWidth
        self.winHeight = winHeight

        # Store a list of file paths that correspond to the table
        self.filePaths = []

        # Set it up to accept files if desired (defaults to false)
        self.setAcceptDrops(acceptDrops)
        self.acceptClicks = acceptClicks

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
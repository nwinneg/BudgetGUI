from PyQt6.QtGui import (
    QFont,
)

from PyQt6.QtWidgets import (
    QWidget, 
    QHBoxLayout,
    QVBoxLayout,
    QTableWidget, 
    QTableWidgetItem, 
)

class Spreadsheet(QWidget):
    def __init__(self, winWidth, winHeight):
        super().__init__()

        # Generalized Spreadsheet Class
        self.table_widget = QTableWidget(self)

        # Store the window size
        self.winWidth = winWidth
        self.winHeight = winHeight

        # Create the layout and set the layout to the widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

        # Initialize the spreadsheet with test data


    def setSheetSize(self, widthRatio, heightRatio, xpos, ypos):
        self.xrat = widthRatio
        self.yrat = heightRatio
        self.xpos = xpos  # From the top left
        self.ypos = ypos  # From the top left

        # Resize the table widget based on the ratios (if needed)
        self.table_widget.setMaximumWidth(int(self.winWidth * self.xrat))
        self.table_widget.setMaximumHeight(int(self.winHeight * self.yrat))

        # Optionally, use `move` if you want to move the table widget
        # self.table_widget.move(xpos, ypos)

    def setSheetParams(self, **kwargs):
        # Set the number of rows and columns for the table
        sz = kwargs["size"]
        self.table_widget.setRowCount(sz[0])
        self.table_widget.setColumnCount(sz[1])

        # Set the column titles (headers)
        self.table_widget.setHorizontalHeaderLabels(kwargs['titles'])
        headerFont = QFont()
        headerFont.setBold(True)
        self.table_widget.horizontalHeader().setFont(headerFont)

        # Populate the table with empty strings
        for row in range(sz[0]):
            for col in range(sz[1]):
                item = QTableWidgetItem("")
                self.table_widget.setItem(row, col, item)
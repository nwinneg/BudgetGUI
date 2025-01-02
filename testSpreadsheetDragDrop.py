import sys
import Spreadsheet
import DataControlBar
import PieChartWidget
import numpy as np

from PyQt6.QtCore import Qt
# from PyQt6.QtCore import (
#     Qt,
#     pyqtSignal,
#     QMimeData,
#     QTimer
# )
# from PyQt6.QtGui import (
    # QFont,
    # QDragEnterEvent, 
    # QDropEvent,
    # QClipboard,
    # QAction
# )
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget,
    QLayout,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QLabel
)

class SpreadsheetTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainWindow = QMainWindow

        self.setWindowTitle("Test Spreadsheet Class")

        self.winWidth = 800
        self.winHeight = 600

        self.setGeometry(100, 100, self.winWidth, self.winHeight)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        # rlLayout = QHBoxLayout(centralWidget)
        topLvlLayout = QVBoxLayout(centralWidget)

        # Create the title label
        titleLabel = QLabel("<h1><strong>ClariFi</strong></h1>")
        topLvlLayout.addWidget(titleLabel,alignment=Qt.Alignment.AlignTop | Qt.Alignment.AlignHCenter)

        # Create the middle layout
        midLayout = QHBoxLayout()
        midLeftLayout = QVBoxLayout()
   
        # Set up the spreadsheets 
        costSheet = Spreadsheet.CostSpreadsheet(self.winWidth,self.winHeight)
        fileSheet = Spreadsheet.FileSpreadsheet(self.winWidth,self.winHeight)
        fileSheet.setSheetParams(size=[1, 3], titles=["FilePath","Account","Delete"], sizePct=[.25,.65], sizeColsOnContent=[1,2])
        transactionSheet = Spreadsheet.TransactionSheet(self.winWidth,self.winHeight)

        # Set up data control bar
        dataControlBar = DataControlBar.DataControlBar(fileSheet)

        # Set up Pie Chart
        # pieChart = PieChartWidget.PieChartWidget(costSheet)

        # Add the sheets to the middle layout
        midLeftLayout.addWidget(fileSheet,alignment=Qt.Alignment.AlignTop)
        midLeftLayout.addWidget(dataControlBar)
        midLeftLayout.addWidget(transactionSheet)
        appControlBar = DataControlBar.AppControlBar(costSheet,fileSheet,transactionSheet,dataControlBar)
        midLeftLayout.addWidget(appControlBar)
        
        # midLeftLayout.addWidget(pieChart)

        # Add some other stuff
        midLeftWidget = QWidget()
        midLeftWidget.setLayout(midLeftLayout)

        midRightLayout = QVBoxLayout()
        midRightLayout.addWidget(costSheet,alignment= Qt.Alignment.AlignRight | Qt.Alignment.AlignTop)

        label = QLabel("Author: NIW\tVersion: 3.0")
        label.setStyleSheet(
            "QPushButton {"
            "color: blue;"  # Change font color
            "font-weight: bold;"  # Make the font bold
            "}"
        )
        midRightLayout.addWidget(label,alignment = Qt.Alignment.AlignCenter)
        midRightWidget = QWidget()
        midRightWidget.setLayout(midRightLayout)

        midLayout.addWidget(midLeftWidget,alignment=Qt.Alignment.AlignTop)
        # midLayout.addWidget(costSheet,alignment= Qt.Alignment.AlignRight | Qt.Alignment.AlignTop)
        midLayout.addWidget(midRightWidget,alignment= Qt.Alignment.AlignRight | Qt.Alignment.AlignTop)

        # midLayout.addWidget(costSheet)

        # Create a middle widget to store all of that 
        midWidget = QWidget()
        midWidget.setLayout(midLayout)

        # Add the midwidget to the top level layout
        topLvlLayout.addWidget(midWidget)

        # topLvlLayout.addWidget(mySpreadsheet,alignment=Qt.Alignment.AlignTop)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpreadsheetTestWindow()
    window.show()
    sys.exit(app.exec())

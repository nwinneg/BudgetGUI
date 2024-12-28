import sys
import Spreadsheet
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
   
        # Set up the spreadsheets 
        costSheet = Spreadsheet.Spreadsheet(self.winWidth,self.winHeight)
        fileSheet = Spreadsheet.Spreadsheet(self.winWidth,self.winHeight,True,True)

        colLabels = np.array(["Rent","Utilities (Gas/Elect)", "Wifi", "Groceries","Merchandise",
            "Dining Out","Rental Insurance","Rent Deposits","Gas/Auto","Car Insurance",
            "Spotify","Venmo Bofa Net","Healthcare","Other","Total"])
        costSheet.setSheetParams(size=[14, 2], titles=["Catagory","Expense"], sizePct=[.85,.3], dataLabels=colLabels,sizeColsOnContent=[0])
        fileSheet.setSheetParams(size=[1, 3], titles=["FilePath","Account","Delete"], sizePct=[.25,.65], sizeColsOnContent=[1,2])

        # Add the sheets to the middle layout
        midLayout.addWidget(fileSheet,alignment=Qt.Alignment.AlignTop)
        midLayout.addWidget(costSheet,alignment=Qt.Alignment.AlignRight)

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

import sys
import Spreadsheet
import numpy as np
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
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QSpacerItem
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
        topLvlLayout = QVBoxLayout(centralWidget)
        
        # Set up the spreadsheet
        mySpreadsheet = Spreadsheet.Spreadsheet(self.winWidth,self.winHeight)
        sheetTitles = ["Catagory", "Expense"]
        colLabels = np.array(["Rent","Utilities (Gas/Elect)", "Wifi", "Groceries","Merchandise",
            "Dining Out","Rental Insurance","Rent Deposits","Gas/Auto","Car Insurance",
            "Spotify","Venmo Bofa Net","Healthcare","Other","Total"])
        mySpreadsheet.setSheetParams(size=[14, 2], titles=sheetTitles, sizePct=[.75,.3], dataLabels=colLabels)
        topLvlLayout.addWidget(mySpreadsheet)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpreadsheetTestWindow()
    window.show()
    sys.exit(app.exec())

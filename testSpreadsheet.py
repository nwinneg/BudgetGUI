import sys
import Spreadsheet
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
# import pandas as pd

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
        topLvlLayout = QHBoxLayout(centralWidget)
        
        # Set up the spreadsheet
        mySpreadsheet = Spreadsheet.Spreadsheet(self.winWidth,self.winHeight)
        mySpreadsheet.setSheetSize(1, 1, 50, 50)
        sheetSizeInit = [4, 3]
        sheetTitles = ["title1", "title2", "title3"]
        mySpreadsheet.setSheetParams(size=sheetSizeInit, titles=sheetTitles)
        topLvlLayout.addWidget(mySpreadsheet)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpreadsheetTestWindow()
    window.show()
    sys.exit(app.exec())

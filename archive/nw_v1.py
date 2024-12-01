import sys
import csv
from PyQt6.QtCore import (
    Qt,                 # Main Qt class contains misc identifiers
    QMimeData           # Facilitates drag and drop by reading info stored in clipboard
)
from PyQt6.QtGui import (
    QDragEnterEvent,    # Provides event sent to widget when drag and drop enters it
    QDropEvent          # Provides event sent to widget when drop event completes
)
from PyQt6.QtWidgets import (
    QApplication,       # Primary GUI Object, controls flow and main settings
    QLayout,            # Base class of geometry managers to organize window
    QMainWindow,        # Provides the main application window
    QVBoxLayout,        # Aligns widgets vertically
    QLabel,             # Provides text or image display
    QWidget,            # Base class for all UI Objects
    QVBoxLayout,        # Lays out widgets vertically
    QGridLayout,        # Lays out widgets in a grid
    QTableWidget,       # Provides item based table view with default model
    QTableWidgetItem,   # Provides an item for use in QTableWidget
    QPushButton,        # Provides a command button
    QFileDialog         # Provides dialog that allows user to select file or directories
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Version of the tool
        self.version = 0.1

        # Initialize window title and size
        self.setWindowTitle("Budget Parser")
        self.resize(600, 600)
        self.setGeometry(100, 100, 500, 500)

        # Create a central widget and layout
        central_widget = QWidget(self)
        layout = QGridLayout(central_widget)    # When adding widgets, addWidget(self,QWidget,row,col,rowspan,colspan)
        # layout = QVBoxLayout(central_widget) 

        # Create Widget Title
        self.create_title_label(layout)     

        self.setCentralWidget(central_widget)   

    def create_title_label(self, layout):
        """
        Method that creates a centered title for the application GUI

        Args: 
            layout: Geometry object for the GUI layout

        Returns: 
            None
        """
        title = 'Budget Parser v{}'.format(self.version)
        label = QLabel("<h2>{}</h2>".format(title))
        # label = QLabel("{}".format(title))
        layout.addWidget(label,0,0,1,3,alignment=Qt.Alignment.AlignCenter)
        print(title)

    def create_drop_field(self, layout, annotation, glocation):
        """
        Method Description
        """

    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        Method Description
        """

    def dropEvent(self, event: QDropEvent):
        """
        Method Description
        """

class DropArea:
    def __init__(self, file_types, parent=None):
        super().__init__(parent)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        Method Desctiption
        """

    def dropEvent(self, event: QDropEvent):
        """
        Method Desctiption
        """

class SpreadsheetWindow:
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
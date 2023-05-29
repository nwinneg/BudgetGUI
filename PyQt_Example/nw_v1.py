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
    QGridLayout,        # Lays out widgets in a grid
    QTableWidget,       # Provides item based table view with default model
    QTableWidgetItem,   # Provides an item for use in QTableWidget
    QPushButton,        # Provides a command button
    QFileDialog         # Provides dialog that allows user to select file or directories
)

class MainWindow:
    def __init__(self):
        super().__init__()

    def create_title_label(self):
        """
        Method Description
        """

    def create_drop_field(self, layout, annotation, file_types):
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


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())
import sys
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QGridLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set version of tool
        self.version = 0.1

        self.setWindowTitle("Budget Parser")
        self.resize(600, 600)
        
        self.setGeometry()

        # Create a central widget and layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        # layout = QGridLayout(central_widget)

        # Create Widget Title
        self.create_title_label(layout)

        # Create the drop fields with annotations

        self.create_drop_field(layout, "Drop CSV files here", ".csv")
        self.create_drop_field(layout, "Drop Image files here", ".jpg .png .bmp")
        self.create_drop_field(layout, "Drop Text files here", ".txt")

        self.setCentralWidget(central_widget)

    def create_title_label(self,layout):
        """
        Create a widget at at the top left to display application title

        Args:
            layout (QLayout): The window layout we will add the title to
        
        Returns: 
            None
        """
        title = 'Budget Parser v{}'.format(self.version)
        # label = QLabel("<h1><U>{}</U></h1>".format(title))
        label = QLabel("<h1>{}</h1>".format(title))
        # layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # layout.setAlignment(Qt.AlignLeft)
        layout.addWidget(label,alignment=Qt.Alignment.AlignCenter) # Do alignment in add widget

    def create_drop_field(self, layout, annotation, file_types):
        """
        Create a drop field with an annotation label.

        Args:
            layout (QLayout): The layout to which the drop field will be added.
            annotation (str): The annotation text for the drop field.
            file_types (str): The supported file types as a space-separated string.

        Returns:
            None
        """
        label = QLabel(annotation, self)
        # label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # label.setAlignment(Qt.AlignLeft)
        layout.addWidget(label)
        
        # Create a custom drop area widget for each field
        drop_area = DropArea(file_types, self)
        layout.addWidget(drop_area)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        Handle the drag enter event.

        This method is called when a drag operation enters the widget area.
        It checks if the dragged data has URLs and accepts the proposed action if true.

        Args:
            event (QDragEnterEvent): The drag enter event object.

        Returns:
            None
        """
        if event.mimeData().hasUrls():  # Check if the dragged data has URLs
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """
        Handle the drop event.

        This method is called when a drop event occurs in the widget area.
        It retrieves the dropped file path from the URLs and prints the file type and path.

        Args:
            event (QDropEvent): The drop event object.

        Returns:
            None
        """
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()  # Get the local file path of the dropped URL
            print("Dropped file:", file_path)

class DropArea(QWidget):
    def __init__(self, file_types, parent=None):
        super().__init__(parent)

        self.file_types = file_types
        self.setAcceptDrops(True)

        

    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        Handle the drag enter event.

        This method is called when a drag operation enters the drop area.
        It checks if the dragged data has URLs and if the dropped file matches the supported file types.
        If the file type matches, it accepts the proposed action; otherwise, it ignores the event.

        Args:
            event (QDragEnterEvent): The drag enter event object.

        Returns:
            None
        """
        if event.mimeData().hasUrls():  # Check if the dragged data has URLs
            # Check if the dropped file matches the supported file types
            urls = event.mimeData().urls()
            for url in urls:
                file_path = url.toLocalFile()
                if file_path.lower().endswith(self.file_types):  # Check file type compatibility
                    event.acceptProposedAction()  # Accept the proposed action
                    return

    def dropEvent(self, event: QDropEvent):
        """
        Handle the drop event.

        This method is called when a drop event occurs in the drop area.
        It retrieves the dropped file path from the URLs and prints the file type and path.

        Args:
            event (QDropEvent): The drop event object.

        Returns:
            None
        """
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()  # Get the local file path of the dropped URL
            print(f"Dropped {self.file_types} file:", file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

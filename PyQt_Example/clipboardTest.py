import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QMenuBar, QMenu, QApplication, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QClipboard, QAction

def copy_selected_data():
    clipboard = QApplication.clipboard()
    selected_items = table_widget.selectedItems()
    
    if selected_items:
        mime_data = QMimeData()
        table_data = ""

        # Build a tab-separated string from the selected items
        for item in selected_items:
            table_data += item.text() + "\t"
        
        mime_data.setText(table_data.strip())  # Set the text data in the MIME data
        clipboard.setMimeData(mime_data)
        QMessageBox.information(window, "Copy to Clipboard", "Data copied to clipboard.")
    else:
        QMessageBox.warning(window, "Copy to Clipboard", "No data selected.")

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Copy Table to Clipboard")
central_widget = QWidget()
window.setCentralWidget(central_widget)
layout = QVBoxLayout(central_widget)

table_widget = QTableWidget()
table_widget.setRowCount(5)  # Set the number of rows
table_widget.setColumnCount(3)  # Set the number of columns

# Fill the table with sample data
for row in range(5):
    for col in range(3):
        item = QTableWidgetItem(f"Row {row}, Col {col}")
        table_widget.setItem(row, col, item)

layout.addWidget(table_widget)

copy_button = QPushButton("Copy Selected Data to Clipboard")
copy_button.clicked.connect(copy_selected_data)
layout.addWidget(copy_button)

menu_bar = window.menuBar()
file_menu = menu_bar.addMenu("File")
copy_action = QAction("Copy Selected Data", window)
copy_action.triggered.connect(copy_selected_data)
file_menu.addAction(copy_action)

window.show()
sys.exit(app.exec())

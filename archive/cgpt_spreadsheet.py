import sys
from PyQt6.QtCore import Qt
# from PyQt6.QtWidgets import (
#     QApplication, 
#     QMainWindow, 
#     QWidget, 
#     QLabel, 
#     QGridLayout, 
#     QTableWidget, 
#     QTableWidgetItem, 
#     QPushButton
# )

import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QTableWidget, QTableWidgetItem, \
    QPushButton, QFileDialog


class SpreadsheetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spreadsheet Example")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        central_widget.setLayout(layout)

        # Centered title label
        title_label = QLabel("Spreadsheet")
        title_label.setObjectName("titleLabel")
        # layout.addWidget(title_label, 0, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(title_label, 0, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Buttons on the left
        field_buttons = ["Button 1", "Button 2", "Button 3", "Button 4"]
        self.table = None  # To hold the QTableWidget instance

        def show_table():
            if self.table is None:
                self.table = QTableWidget()
                self.table.setColumnCount(2)
                self.table.setRowCount(12)

                # Populate the table with some sample data
                for row in range(12):
                    for column in range(2):
                        item = QTableWidgetItem(f"Row {row}, Column {column}")
                        self.table.setItem(row, column, item)

            layout.addWidget(self.table, 1, 1, 12, 2)

        def save_to_csv():
            if self.table is not None:
                file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "/Users/natewinneg/Desktop", "CSV Files (*.csv)")
                if file_path:
                    with open(file_path, 'w', newline='') as file:
                        writer = csv.writer(file)
                        for row in range(self.table.rowCount()):
                            row_data = []
                            for column in range(self.table.columnCount()):
                                item = self.table.item(row, column)
                                if item is not None:
                                    row_data.append(item.text())
                                else:
                                    row_data.append("")
                            writer.writerow(row_data)

        for row, button_label in enumerate(field_buttons):
            button = QPushButton(button_label)
            button.clicked.connect(show_table)
            layout.addWidget(button, row + 1, 0)

        save_button = QPushButton("Save to CSV")
        save_button.clicked.connect(save_to_csv)
        layout.addWidget(save_button, len(field_buttons) + 1, 0, 1, 2)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpreadsheetWindow()
    mainWindow.show()
    sys.exit(app.exec())
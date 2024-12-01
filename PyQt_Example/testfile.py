import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.button = QPushButton("Click me!")
        self.button.clicked.connect(self.reinitialize)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                self.clearLayout(item.layout())

    def reinitialize(self):
        self.clearLayout(self.layout)
        self.layout.addWidget(QPushButton("New Button"))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWidget()
    window.setWindowTitle("Reinitialization Demo")
    window.show()

    sys.exit(app.exec())

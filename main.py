import sys
from PyQt6.QtWidgets import QApplication
import appCreation

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = appCreation.BudgetApp()
    window.show()
    sys.exit(app.exec())
# BudgetGUI
GUI tool developed with PyQt6 to convert bank and credit card csv downloads to spending summary table.

A useful resource: https://het.as.utexas.edu/HET/Software/PyQt/classes.html

## Some notes on creating an executable
PyInstaller is a good tool for this
- pip install pyinstaller
- pyinstaller --onefile main.py (Creates the executable)
- It may be necessary to go find the pyinstaller exe in Python3.X/Scripts and add it's directory to PATH
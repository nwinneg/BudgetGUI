import sys
import random
import colorsys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

class PieChartWidget(QWidget):
    def __init__(self,spreadSheet,parent=None):
        super().__init__(parent)

        # self.setGeometry(400, 400, 600, 400)
        self.setMinimumSize(200,200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.spreadsheet = spreadSheet.table_widget

        self.data, self.labels = self.getSpreadsheetData()
        
        self.colors = self.generate_distinct_colors(len(self.labels))

        self.setLayout(QVBoxLayout())
        self.update()

    def getSpreadsheetData(self):
        rowCount = self.spreadsheet.rowCount()
        data = []
        labels = []
        for row in range(rowCount):
            dataItem = self.spreadsheet.item(row,1)
            labelItem = self.spreadsheet.item(row,0)
            if dataItem.text() == "":
                data.append(0)
            else:
                data.append(int(dataItem.text()))
            labels.append(labelItem.text())
        
        if sum(data) == 0:
            for k in range(len(data)):
                data[k] = 1

        data = [round(x / max(sum(data), 1) * 100,3) for x in data]
        print(self.height())

        return data, labels

    def paintEvent(self, event):
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # Enable anti-aliasing
        bkgd = 230
        painter.setBrush(QColor(bkgd, bkgd, bkgd))  # Set the brush color (white)
        painter.drawRect(self.rect())  # Draw the background rectangle

        # Draw the pie chart
        self.draw_pie_chart(painter)

        # Draw the legend
        self.draw_legend(painter)

    def draw_pie_chart(self, painter):
        # Start angle and initial position for the pie slices
        start_angle = 0

        # Draw the pie slices
        for i, size in enumerate(self.data):
            # Calculate the sweep angle based on data
            span_angle = (size / sum(self.data)) * 360 * 16  # Convert to 1/16 degree units

            # Set brush for each slice's color
            painter.setBrush(self.colors[i])

            # Draw the pie slice (use arc with specified start and sweep angles)
            painter.drawPie(20, 20, 150, 150, start_angle, span_angle)

            # Update the start angle for the next slice
            start_angle += span_angle

    def draw_legend(self, painter):
        # Set the font for the legend
        painter.setFont(QFont("Arial", 8))

        legend_x = 200  # X position for the legend
        legend_y = 10  # Starting Y position for the legend

        halfIdx = round(len(self.labels)/2)
        moveOver = True

        for i, label in enumerate(self.labels):

            if (i > halfIdx) & moveOver:
                moveOver = False
                legend_x += 150
                legend_y = 10

            # Draw the color box for each label
            painter.setBrush(self.colors[i])
            painter.drawRect(legend_x, legend_y, 15, 15)  # Draw a small square for color box

            # Draw the label text next to the color box
            painter.setPen(Qt.GlobalColor.black)
            painter.drawText(legend_x + 20, legend_y + 11, label)  # Draw the text next to the color box

            # Move the Y position down for the next legend entry
            legend_y += 20

    def generate_distinct_colors(self,num_colors):
        colors = []
        hue_step = 1.0 / num_colors
        
        for i in range(num_colors):
            hue = i * hue_step
            saturation = 1.0
            value = .75
            
            # Convert HSV to RGB
            r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
            
            # Scale RGB values to 0-255 range and create QColor object
            color = QColor(int(r * 255), int(g * 255), int(b * 255))
            colors.append(color)
        
        return colors
        
    def update_pie_chart(self):
        pass
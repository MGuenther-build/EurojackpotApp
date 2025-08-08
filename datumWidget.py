
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QColor

class Datum(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.datum = QLabel()
        self.datum.setStyleSheet("color: black; font-size: 32px; font-family: Garamond")
        self.datum.setAlignment(Qt.AlignRight | Qt.AlignTop)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor("#F7F7F7"))
        shadow.setOffset(0, 2)  # Nur nach unten, leichter Schatten
        shadow.setBlurRadius(4)
        self.datum.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout()
        layout.addWidget(self.datum)
        self.setLayout(layout)
        
        self.update_datetime()
        timer = QTimer(self)
        timer.timeout.connect(self.update_datetime)
        timer.start(1000)
    
    def update_datetime(self):
        now = QDateTime.currentDateTime()
        self.datum.setText(now.toString("dddd, d. MMMM yyyy"))

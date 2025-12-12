from controllers.generatePick import generate_a_pick
from utils.dateWidget import DateWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QSizePolicy, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QColor



class generateYourPicks(QWidget):
    def __init__(self, back_callback):
        super().__init__()
        self.back_callback = back_callback
        self.init_ui()
    
    def init_ui(self):
        grid = QGridLayout(self)
        grid.setRowStretch(0, 2)
        grid.setRowStretch(1, 6)
        grid.setRowStretch(2, 3)
        
        self.datumWidget = DateWidget()
        grid.addWidget(self.datumWidget, 0, 0, alignment=Qt.AlignTop | Qt.AlignRight)
        self.datumWidget.setContentsMargins(0, 0, 10, 0)
        
        layout = QVBoxLayout()
        self.ueberschrift = QLabel("Deine Glückszahlen lauten:")
        self.ueberschrift.setFont(QFont("Showcard Gothic", 30))
        self.ueberschrift.setAlignment(Qt.AlignCenter)
        self.glueckszahlen = QLabel("")
        self.glueckszahlen.setFont(QFont("Showcard Gothic", 66))
        self.glueckszahlen.setAlignment(Qt.AlignCenter)
        shadow_glueck = QGraphicsDropShadowEffect()
        shadow_glueck.setBlurRadius(15)
        shadow_glueck.setOffset(2, 18)
        shadow_glueck.setColor(QColor("#FEDFA052"))
        self.glueckszahlen.setGraphicsEffect(shadow_glueck)
        
        layout.addWidget(self.ueberschrift)
        layout.addSpacing(10)
        layout.addWidget(self.glueckszahlen)
        grid.addLayout(layout, 1, 0, alignment=Qt.AlignCenter)
        
        button_style_subsite1 = """
                                QPushButton {
                                    font-size: 10pt;
                                    font-family: Tahoma;
                                    background-color: #000000;
                                    color: #FEDFA0;
                                    border-radius: 10px;
                                    padding-left: 20px;
                                    padding-right: 20px;
                                    border: 2px solid #DCF3FC;
                                }
                                QPushButton:hover {
                                    background-color: #262626;
                                    border: 2px solid #FFFFFF;
                                }
                                QPushButton:pressed {
                                    background-color: #0d0d0d;
                                    border: 2px solid #FFFFFF;
                                    padding-top: 2px;
                                    padding-left: 22px;
                                    padding-right: 18px;
                                }"""
        
        button_gluck1 = QPushButton("Glückszahlen generieren")
        button_gluck1.setStyleSheet(button_style_subsite1)
        button_gluck1.clicked.connect(self.zahlen_generieren)
        
        button_gluck1_back = QPushButton("zurück zur Hauptseite")
        button_gluck1_back.setStyleSheet(button_style_subsite1)
        button_gluck1_back.clicked.connect(self.back_callback)
        button_gluck1_back.clicked.connect(self.auto_leeren_bei_leave)

        def set_shadow(button):
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setOffset(3, 3)
            shadow.setColor(QColor("#E73755"))
            button.setGraphicsEffect(shadow)

        def remove_shadow(button):
            button.setGraphicsEffect(None)

        self.buttons = [button_gluck1, button_gluck1_back]

        for btn in self.buttons:
            set_shadow(btn)
            btn.pressed.connect(lambda b=btn: remove_shadow(b))
            btn.released.connect(lambda b=btn: set_shadow(b))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        buttonglueck_layout = QHBoxLayout()
        buttonglueck_layout.addWidget(button_gluck1)
        buttonglueck_layout.addWidget(button_gluck1_back)
        buttonglueck_layout.setSpacing(int(self.width() * 0.03))
        
        footer = QWidget()
        footer_layout = QVBoxLayout(footer)
        footer_layout.addStretch(1)
        footer_layout.addLayout(buttonglueck_layout)
        footer_layout.setContentsMargins(0, 0, 0, 50)
        footer.setMinimumHeight(int(self.height() * 0.08))
        grid.addWidget(footer, 2, 0, alignment=Qt.AlignBottom)
    
    def resizeEvent(self, event):
        h = self.height()
        for btn in self.buttons:
            btn.setFixedHeight(int(h * 0.045))
        super().resizeEvent(event)

    def auto_leeren_bei_leave(self):
        self.glueckszahlen.setText("")
        self.back_callback()
    
    def zahlen_generieren(self):
        text = generate_a_pick()
        self.glueckszahlen.setText(text)
    
    def mousePressEvent(self, event):
        if QApplication.focusWidget():
            QApplication.focusWidget().clearFocus()
        event.accept()
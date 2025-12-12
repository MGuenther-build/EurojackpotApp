from controllers.checkPick import check_picks
from utils.dateWidget import DateWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QSizePolicy, QDialog, QPushButton, QLabel, QDialog, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, QLineEdit
from PyQt5.QtGui import QIntValidator, QFont, QColor



class checkYourPicks(QWidget):
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
        self.ueberschrift = QLabel("Gebe deinen Tipp ein:")
        self.ueberschrift.setFont(QFont("Showcard Gothic", 30))
        self.ueberschrift.setAlignment(Qt.AlignCenter)
        self.tippeingabefeld = []
        self.tippfelder_layout = QHBoxLayout()
        
        for i in range(7):
            if i == 5:
                self.spacer = QWidget()
                self.tippfelder_layout.addWidget(self.spacer)
            tippfelder = QLineEdit("")
            tippfelder.setValidator(QIntValidator(1, 99))
            tippfelder.setFont(QFont("Showcard Gothic", 36))
            tippfelder.setAlignment(Qt.AlignCenter)
            tippfelder.setStyleSheet("""
                                    QLineEdit {
                                        background-color: black;
                                        color: white;
                                        border: 2px solid gray;
                                        padding: 2px;
                                        border-radius: 6px;
                                        }
                                    QLineEdit:hover {
                                        background-color: #262626;
                                        }
                                        """)
            self.tippfelder_layout.addWidget(tippfelder)
            self.tippeingabefeld.append(tippfelder)
            
        layout.addWidget(self.ueberschrift)
        layout.addSpacing(40)
        layout.addLayout(self.tippfelder_layout)
        grid.addLayout(layout, 1, 0, alignment=Qt.AlignCenter)

        button_style_subsite2 = """
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
        
        button_pruef = QPushButton("Tipp prüfen")
        button_pruef.setStyleSheet(button_style_subsite2)
        button_pruef.clicked.connect(self.get_pruef)
        
        button_pruef_leeren = QPushButton("Felder leeren")
        button_pruef_leeren.setStyleSheet(button_style_subsite2)
        button_pruef_leeren.clicked.connect(self.felder_leer)

        button_pruef_back = QPushButton("zurück zur Hauptseite")
        button_pruef_back.setStyleSheet(button_style_subsite2)
        button_pruef_back.clicked.connect(self.auto_leeren_bei_leave)

        def set_shadow(button):
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setOffset(3, 3)
            shadow.setColor(QColor("#E73755"))
            button.setGraphicsEffect(shadow)

        def remove_shadow(button):
            button.setGraphicsEffect(None)

        self.buttons = [button_pruef, button_pruef_back, button_pruef_leeren]

        for btn in self.buttons:
            set_shadow(btn)
            btn.pressed.connect(lambda b=btn: remove_shadow(b))
            btn.released.connect(lambda b=btn: set_shadow(b))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
        buttonpruef_layout = QHBoxLayout()
        buttonpruef_layout.addWidget(button_pruef)
        buttonpruef_layout.addWidget(button_pruef_leeren)
        buttonpruef_layout.addWidget(button_pruef_back)
        buttonpruef_layout.setSpacing(int(self.width() * 0.03))
        
        footer = QWidget()
        footer_layout = QVBoxLayout(footer)
        footer_layout.addStretch(1)
        footer_layout.addLayout(buttonpruef_layout)
        footer_layout.setContentsMargins(0, 0, 0, 50)
        footer.setMinimumHeight(int(self.height() * 0.08))
        grid.addWidget(footer, 2, 0, alignment=Qt.AlignBottom)
        
    def resizeEvent(self, event):
        h = self.height()
        w = self.width()
        for feld in self.tippeingabefeld:
            feld.setFixedWidth(int(w * 0.07))
            feld.setFixedHeight(int(h * 0.08))
        for btn in self.buttons:
            btn.setFixedHeight(int(h * 0.045))
        self.tippfelder_layout.setSpacing(int(w * 0.04))
        self.spacer.setFixedWidth(int(self.width() * 0.02))
        super().resizeEvent(event)

    def felder_leer(self):
        for feld in self.tippeingabefeld:
            feld.clear()
    
    def auto_leeren_bei_leave(self):
        for feld in self.tippeingabefeld:
            feld.clear()
        self.back_callback()
    
    def mousePressEvent(self, event):
        if QApplication.focusWidget():
            QApplication.focusWidget().clearFocus()
        event.accept()

    def get_pruef(self):
        eingabe = " ".join(feld.text() for feld in self.tippeingabefeld)
        ergebnis = check_picks(eingabe)
        dialog = QDialog(self)
        dialog.setMinimumSize(700, 260)
        dialog.setMaximumSize(1000, 375)
        dialog.setWindowTitle("Prüfergebnis")
        dialog.setStyleSheet("background-color: black;")
        layout = QVBoxLayout(dialog)
        label = QLabel(ergebnis)
        label.setWordWrap(True)
        label.setFont(QFont("Showcard Gothic", 24))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #DCF3FC;")
        layout.addWidget(label)
        dialog.exec_()

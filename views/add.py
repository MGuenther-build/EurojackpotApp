from controllers.saveDraw import add_draw
from backend.dbPath import db_path
from utils.dateWidget import DateWidget
from utils.timestampWidget import get_Timestamp, add_Timestamp
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QSizePolicy, QDialog, QPushButton, QLabel, QDialog, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, QLineEdit
from PyQt5.QtGui import QIntValidator, QFont, QColor
from datetime import datetime



class addDraw(QWidget):
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
        self.ueberschrift = QLabel("Jackpotzahlen zur Datenbank hinzufügen:")
        self.ueberschrift.setFont(QFont("Showcard Gothic", 30))
        self.ueberschrift.setAlignment(Qt.AlignCenter)
        self.updated = QLabel(f"Zuletzt aktualisiert am: ---")
        self.updated.setFont(QFont("Tahoma", 10))
        self.updated.setAlignment(Qt.AlignLeft)
        self.updated.setStyleSheet("color: #000000")
      
        zeitstempel = get_Timestamp(db_path())
        if zeitstempel:
            self.updated.setText(f"🕒 Zuletzt aktualisiert: {zeitstempel} Uhr")
        else:
            self.updated.setText(f"🕒 Zuletzt aktualisiert: ---")

        self.addfeld = []
        self.addfeld_layout = QHBoxLayout()
        
        for i in range(7):
            if i == 5:
                self.spacer = QWidget()
                self.addfeld_layout.addWidget(self.spacer)
                
            addfelder = QLineEdit("")
            addfelder.setValidator(QIntValidator(1, 99))
            addfelder.setFont(QFont("Showcard Gothic", 36))
            addfelder.setAlignment(Qt.AlignCenter)
            addfelder.setStyleSheet("""
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
            self.addfeld_layout.addWidget(addfelder)
            self.addfeld.append(addfelder)
        
        layout.addWidget(self.ueberschrift)
        layout.addSpacing(40)
        layout.addLayout(self.addfeld_layout)
        layout.addSpacing(8)
        layout.addWidget(self.updated)
        grid.addLayout(layout, 1, 0, alignment=Qt.AlignCenter)

        button_style_subsite3 = """
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
        
        button_add = QPushButton("Zahlen hinzufügen")
        button_add.setStyleSheet(button_style_subsite3)
        button_add.clicked.connect(self.set_add)
        
        button_add_leeren = QPushButton("Felder leeren")
        button_add_leeren.setStyleSheet(button_style_subsite3)
        button_add_leeren.clicked.connect(self.felder_leer)

        button_add_back = QPushButton("zurück zur Hauptseite")
        button_add_back.setStyleSheet(button_style_subsite3)
        button_add_back.clicked.connect(self.auto_leeren_bei_leave)

        def set_shadow(button):
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setOffset(3, 3)
            shadow.setColor(QColor("#E73755"))
            button.setGraphicsEffect(shadow)

        def remove_shadow(button):
            button.setGraphicsEffect(None)

        self.buttons = [button_add, button_add_back, button_add_leeren]

        for btn in self.buttons:
            set_shadow(btn)
            btn.pressed.connect(lambda b=btn: remove_shadow(b))
            btn.released.connect(lambda b=btn: set_shadow(b))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
        buttonadd_layout = QHBoxLayout()
        buttonadd_layout.addWidget(button_add)
        buttonadd_layout.addWidget(button_add_leeren)
        buttonadd_layout.addWidget(button_add_back)
        buttonadd_layout.setSpacing(int(self.width() * 0.03))
        
        footer = QWidget()
        footer_layout = QVBoxLayout(footer)
        footer_layout.addStretch(1)
        footer_layout.addLayout(buttonadd_layout)
        footer_layout.setContentsMargins(0, 0, 0, 50)
        footer.setMinimumHeight(int(self.height() * 0.08))
        grid.addWidget(footer, 2, 0, alignment=Qt.AlignBottom)
    
    def resizeEvent(self, event):
        h = self.height()
        w = self.width()
        for btn in self.buttons:
            btn.setFixedHeight(int(h * 0.045))
        self.addfeld_layout.setSpacing(int(w * 0.035))
        if hasattr(self, "spacer"):
            self.spacer.setFixedWidth(int(w * 0.05))
        for feld in self.addfeld:
            feld.setFixedWidth(int(w * 0.07))
            feld.setFixedHeight(int(h * 0.08))
        super().resizeEvent(event)

    def felder_leer(self):
        for feld in self.addfeld:
            feld.clear()
    
    def auto_leeren_bei_leave(self):
        for feld in self.addfeld:
            feld.clear()
        self.back_callback()
    
    def mousePressEvent(self, event):
        if QApplication.focusWidget():
            QApplication.focusWidget().clearFocus()
        event.accept()
    
    def set_add(self):
        eingabe = [feld.text().strip() for feld in self.addfeld]
        add_zahlen = " ".join(eingabe)
        ergebnis = add_draw(add_zahlen)
        dialog = QDialog(self)
        dialog.setFixedSize(800, 300)
        dialog.setWindowTitle("Status")
        dialog.setStyleSheet("background-color: black;")
        layout = QVBoxLayout(dialog)
        label = QLabel(ergebnis)
        label.setWordWrap(True)
        label.setFont(QFont("Showcard Gothic", 24))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #DCF3FC;")
        layout.addWidget(label)
        dialog.exec_()
        if ergebnis.startswith("✅"):
            zeit = datetime.now().strftime("%d.%m.%Y um %H:%M")
            self.updated.setText(f"🕒 Zuletzt aktualisiert: {zeit} Uhr")
            add_Timestamp(db_path(), zeit)
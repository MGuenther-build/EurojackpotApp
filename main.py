
from functions.saveDraw import zahlen_eintragen
from functions.generatePick import lottozahlen
from functions.checkPick import check_zahlen
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QSizePolicy, QDialog, QMessageBox, QSplashScreen, QPushButton, QLabel, QDialog, QVBoxLayout, QHBoxLayout, QSpacerItem, QLabel, QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QStackedLayout, QLineEdit
from PyQt5.QtGui import QIntValidator, QFont, QFontDatabase, QPainter, QLinearGradient, QColor, QPixmap, QGuiApplication, QIcon
from utils.dateWidget import Datum
from utils.timestampWidget import get_Timestamp, add_Timestamp
from datetime import datetime
import sys
import os
import logging



class Zahlen_add(QWidget):
    def __init__(self, back_callback):
        super().__init__()
        self.back_callback = back_callback
        self.init_ui()
    
    def init_ui(self):
        grid = QGridLayout(self)
        grid.setRowStretch(0, 2)
        grid.setRowStretch(1, 6)
        grid.setRowStretch(2, 3)
        
        self.datumWidget = Datum()
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

        if getattr(sys, 'frozen', False):
            pfad = sys._MEIPASS
        else:
            pfad = os.path.dirname(os.path.abspath(__file__))
        db_pfad = os.path.join(pfad, "backend", "Jackpot_DB.db")        
        zeitstempel = get_Timestamp(db_pfad)
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
        ergebnis = zahlen_eintragen(add_zahlen)
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
        if getattr(sys, 'frozen', False):
            pfad = sys._MEIPASS
        else:
            pfad = os.path.dirname(os.path.abspath(__file__))
        
        db_pfad = os.path.join(pfad, "backend", "Jackpot_DB.db")
        if ergebnis.startswith("✅"):
            zeit = datetime.now().strftime("%d.%m.%Y um %H:%M")
            self.updated.setText(f"🕒 Zuletzt aktualisiert: {zeit} Uhr")
            add_Timestamp(db_pfad, zeit)



class Tipps_checken(QWidget):
    def __init__(self, back_callback):
        super().__init__()
        self.back_callback = back_callback
        self.init_ui()
    
    def init_ui(self):
        grid = QGridLayout(self)
        grid.setRowStretch(0, 2)
        grid.setRowStretch(1, 6)
        grid.setRowStretch(2, 3)
        
        self.datumWidget = Datum()
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
        ergebnis = check_zahlen(eingabe)
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



class Glueckszahlen(QWidget):
    def __init__(self, back_callback):
        super().__init__()
        self.back_callback = back_callback
        self.init_ui()
    
    def init_ui(self):
        grid = QGridLayout(self)
        grid.setRowStretch(0, 2)
        grid.setRowStretch(1, 6)
        grid.setRowStretch(2, 3)
        
        self.datumWidget = Datum()
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
        text = lottozahlen()
        self.glueckszahlen.setText(text)
    
    def mousePressEvent(self, event):
        if QApplication.focusWidget():
            QApplication.focusWidget().clearFocus()
        event.accept()



class EurojackpotApp(QWidget):
    def __init__(self):
        super().__init__()
        aufloesung = QGuiApplication.primaryScreen()
        screen_size = aufloesung.availableGeometry()
        width = int(screen_size.width() * 0.85)
        height = int(screen_size.height() * 0.85)
        self.setWindowTitle("EurojackpotApp")
        favicon_pfad = os.path.dirname(os.path.abspath(__file__))
        favicon = os.path.join(favicon_pfad, "backend", "images", "Eurojackpot.ico")
        self.setWindowIcon(QIcon(favicon))
        self.resize(width, height)
        self.setMinimumSize(1200, 800)
        self.setMaximumSize(3840, 2400)
        self.move(screen_size.center().x() - self.width() // 2, screen_size.center().y() - self.height() // 2)
        self.stack = QStackedLayout()
        self.setLayout(self.stack)
        
        self.main = QWidget()
        grid = QGridLayout(self.main)
        grid.setRowStretch(0, 2)
        grid.setRowStretch(1, 6)
        grid.setRowStretch(2, 3)
        
        self.datumWidget = Datum()
        grid.addWidget(self.datumWidget, 0, 0, alignment=Qt.AlignTop | Qt.AlignRight)
        self.datumWidget.setContentsMargins(0, 0, 10, 0)

        title = QLabel("Eurojackpot")
        title.setFont(QFont("Showcard Gothic", 72))
        title.setAlignment(Qt.AlignCenter)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(2, 18)
        shadow.setColor(QColor("#FEDFA052"))
        title.setGraphicsEffect(shadow)
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.addStretch(1)
        title_layout.addWidget(title, alignment=Qt.AlignCenter)
        title_layout.addStretch(1)
        grid.addWidget(title_container, 1, 0)

        button_style_hauptseite = """
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

        button1 = QPushButton("Glückszahlen generieren")
        button1.setStyleSheet(button_style_hauptseite)
        button1.clicked.connect(self.show_glueckszahlen)

        button2 = QPushButton("Tippcheck")
        button2.setStyleSheet(button_style_hauptseite)
        button2.clicked.connect(self.show_tippeingabefeld)

        button3 = QPushButton("Jackpotzahlen hinzufügen")
        button3.setStyleSheet(button_style_hauptseite)
        button3.clicked.connect(self.show_addfeld)
        
        def set_shadow(button):
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setOffset(3, 3)
            shadow.setColor(QColor("#E73755"))
            button.setGraphicsEffect(shadow)

        def remove_shadow(button):
            button.setGraphicsEffect(None)

        self.buttons = [button1, button2, button3]

        for btn in self.buttons:
            set_shadow(btn)
            btn.pressed.connect(lambda b=btn: remove_shadow(b))
            btn.released.connect(lambda b=btn: set_shadow(b))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        button_layout = QHBoxLayout()
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.addWidget(button3)
        button_layout.setSpacing(int(self.width() * 0.03))
        
        footer = QWidget()
        footer_layout = QVBoxLayout(footer)
        footer_layout.addStretch(1)
        footer_layout.addLayout(button_layout)
        footer_layout.setContentsMargins(0, 0, 0, 50)
        footer.setMinimumHeight(int(self.height() * 0.08))
        grid.addWidget(footer, 2, 0, alignment=Qt.AlignBottom)
        
        self.addfeld = Zahlen_add(back_callback=self.show_main)
        self.tippeingabefeld = Tipps_checken(back_callback=self.show_main)
        self.glueckszahlen = Glueckszahlen(back_callback=self.show_main)
        
        self.stack.addWidget(self.main)
        self.stack.addWidget(self.addfeld)
        self.stack.addWidget(self.tippeingabefeld)
        self.stack.addWidget(self.glueckszahlen)
    
    def resizeEvent(self, event):
        h = self.height()
        for btn in self.buttons:
            btn.setFixedHeight(int(h * 0.045))
        super().resizeEvent(event)
    
    def mousePressEvent(self, event):
        if QApplication.focusWidget():
            QApplication.focusWidget().clearFocus()
        event.accept()

    def show_addfeld(self):
        self.stack.setCurrentWidget(self.addfeld)
    
    def show_tippeingabefeld(self):
        self.stack.setCurrentWidget(self.tippeingabefeld)

    def show_glueckszahlen(self):
        self.stack.setCurrentWidget(self.glueckszahlen)

    def show_main(self):
        self.stack.setCurrentWidget(self.main)
         
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#D0ECF7"))
        gradient.setColorAt(1, QColor("#F7C562"))
        painter.fillRect(self.rect(), gradient)
    
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "EurojackpotApp",
            "Programm wirklich schließen?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def fade_out_Loading_Screen(widget, duration=900, wenn_fertig=None):
    if getattr(widget, "_fade_animation", None) is not None:
        return
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)
    animation = QPropertyAnimation(effect, b"opacity")
    animation.setDuration(duration)
    animation.setStartValue(1.0)
    animation.setEndValue(0.0)
    animation.start()
    widget._fade_animation = animation
    animation.finished.connect(lambda: (widget.close(), wenn_fertig and wenn_fertig()))

def font_specs():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(base_path, "backend", "images", "Showcard Gothic.ttf")
    fontID = QFontDatabase.addApplicationFont(font_path)
    font_group = QFontDatabase.applicationFontFamilies(fontID)
    if font_group:
        return QFont(font_group[0], 14)
    else:
        return QFont()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenster = EurojackpotApp()
    showcard_font = font_specs()
    fenster.setFont(showcard_font)
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    intro_path = os.path.join(base_path, "backend", "images", "Loading_Screen.webp")
    try:
        pixmap = QPixmap(intro_path)
        if pixmap.isNull():
            raise FileNotFoundError(f"Intro konnte nicht geladen werden: {intro_path}")
        screen_size = app.primaryScreen().size()
        width = int(screen_size.width() * 0.5)
        pixmap_size = pixmap.scaledToWidth(width, Qt.SmoothTransformation)
        intro = QSplashScreen(pixmap_size)
        intro.show()
        app.processEvents()
        show_intro = True
    except Exception as x:
        logging.error(f"[Intro wurde übersprungen] - Grund: {x}")
        show_intro = False
    if show_intro:
        QTimer.singleShot(1000, lambda: fade_out_Loading_Screen(intro, wenn_fertig=fenster.show))
    else:
        fenster.show()
    
    sys.exit(app.exec_())

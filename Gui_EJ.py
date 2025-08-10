
from Zahlen_hinzu import zahlen_eintragen
from Zahlengenerieren import lottozahlen
from Tippcheck import check_zahlen
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMessageBox, QSplashScreen, QPushButton, QLabel, QDialog, QVBoxLayout, QHBoxLayout, QSpacerItem, QLabel, QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QStackedLayout, QLineEdit
from PyQt5.QtGui import QIntValidator, QFont, QFontDatabase, QPainter, QLinearGradient, QColor, QPixmap, QGuiApplication, QIcon
from datumWidget import Datum
from datetime import datetime
import sys
import os
import logging



# Lottozahlen hinzufügen
class Zahlen_add(QWidget):
    def __init__(self, back_callback):
        super().__init__()
        self.back_callback = back_callback
        self.init_ui()
    
    def init_ui(self):
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
        txt_pfad = os.path.join(pfad, "backend", "add_Datumstempel.txt")
        try:
            with open(txt_pfad, "r", encoding="utf-8") as y:
                zeitstempel = y.read().strip()
                self.updated.setText(f"🕒 Zuletzt aktualisiert: {zeitstempel} Uhr")
        except FileNotFoundError:
            pass

        self.addfeld = []
        addfeld_layout = QHBoxLayout()
        addfeld_layout.setSpacing(20)
        
        for i in range(7):
            if i == 5:
                spacer = QWidget()
                spacer.setFixedWidth(10)
                addfeld_layout.addWidget(spacer)
            addfelder = QLineEdit("")
            addfelder.setValidator(QIntValidator(1, 99))
            addfelder.setMinimumSize(90, 90)
            addfelder.setMaximumSize(120, 120)
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
            addfeld_layout.addWidget(addfelder)
            self.addfeld.append(addfelder)
        
        # Button Designs
        button_style_subsite3 = """
                                QPushButton {
                                    font-size: 19px;
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
        button_add.setMinimumSize(500,60)
        button_add.setMaximumSize(700,80)
        
        button_add.setStyleSheet(button_style_subsite3)
        button_add.clicked.connect(self.set_add)
        
        button_add_leeren = QPushButton("Felder leeren")
        button_add_leeren.setMinimumSize(300,60)
        button_add_leeren.setMaximumSize(500,80)
        button_add_leeren.setStyleSheet(button_style_subsite3)
        button_add_leeren.clicked.connect(self.felder_leer)

        button_add_back = QPushButton("zurück zur Hauptseite")
        button_add_back.setMinimumSize(500,60)
        button_add_back.setMaximumSize(700,80)
        button_add_back.setStyleSheet(button_style_subsite3)
        button_add_back.clicked.connect(self.auto_leeren_bei_leave)

        # Button Eindrückeffekt
        def set_shadow(button):
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setOffset(3, 3)
            shadow.setColor(QColor("#E73755"))
            button.setGraphicsEffect(shadow)

        def remove_shadow(button):
            button.setGraphicsEffect(None)

        buttons = [button_add, button_add_back, button_add_leeren]

        for btn in buttons:
            set_shadow(btn)
            btn.pressed.connect(lambda b=btn: remove_shadow(b))
            btn.released.connect(lambda b=btn: set_shadow(b))
    
        # horizontale Anordnung der Buttons
        buttonadd_layout = QHBoxLayout()
        buttonadd_layout.addWidget(button_add)
        buttonadd_layout.addWidget(button_add_leeren)
        buttonadd_layout.addWidget(button_add_back)

        # Datum
        self.datumWidget = Datum()
        self.datumWidget.setFixedHeight(200)
        
        # Layout der Seite
        datum_layout = QVBoxLayout()
        datum_layout.addWidget(self.datumWidget)
        datum_layout.setContentsMargins(10, 26, 17, 150)
        layout.addLayout(datum_layout)
        layout.addWidget(self.ueberschrift)
        layout.addSpacing(150)
        layout.addLayout(addfeld_layout)
        updated_layout = QHBoxLayout()
        updated_layout.addWidget(self.updated)
        updated_layout.setContentsMargins(130,30,0,0)
        layout.addLayout(updated_layout)
        layout.addSpacing(600)
        layout.addLayout(buttonadd_layout)
        layout.addSpacerItem(QSpacerItem(0,100))

        # Layout auf Fenster anwenden
        self.setLayout(layout)


    def felder_leer(self):
        for feld in self.addfeld:
            feld.clear()
    
    def auto_leeren_bei_leave(self):
        for feld in self.addfeld:
            feld.clear()
        self.back_callback()
    
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
        txt_pfad = os.path.join(pfad, "backend", "add_Datumstempel.txt")
        if ergebnis.startswith("✅"):
            zeit = datetime.now().strftime("%d.%m.%Y um %H:%M")
            self.updated.setText(f"🕒 Zuletzt aktualisiert: {zeit} Uhr")
            with open(txt_pfad, "w", encoding="utf-8") as x:
                x.write(zeit)





# Tippcheck
class Tipps_checken(QWidget):
    def __init__(self, back_callback):
        super().__init__()
        self.back_callback = back_callback
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()

        self.ueberschrift = QLabel("Gebe deinen Tipp ein:")
        self.ueberschrift.setFont(QFont("Showcard Gothic", 30))
        self.ueberschrift.setAlignment(Qt.AlignCenter)
        
        self.tippeingabefeld = []
        tippfelder_layout = QHBoxLayout()
        tippfelder_layout.setSpacing(20)
        
        for i in range(7):
            if i == 5:
                spacer = QWidget()
                spacer.setFixedWidth(10)
                tippfelder_layout.addWidget(spacer)
            tippfelder = QLineEdit("")
            tippfelder.setValidator(QIntValidator(1, 99))
            tippfelder.setMinimumSize(90, 90)
            tippfelder.setMaximumSize(120, 120)
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
            tippfelder_layout.addWidget(tippfelder)
            self.tippeingabefeld.append(tippfelder)

    
        # Button Designs
        button_style_subsite2 = """
                                QPushButton {
                                    font-size: 19px;
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
        button_pruef.setMinimumSize(500, 60)
        button_pruef.setMaximumSize(700, 80)
        button_pruef.setStyleSheet(button_style_subsite2)
        button_pruef.clicked.connect(self.get_pruef)
        
        button_pruef_leeren = QPushButton("Felder leeren")
        button_pruef_leeren.setMinimumSize(300, 60)
        button_pruef_leeren.setMaximumSize(500, 80)
        button_pruef_leeren.setStyleSheet(button_style_subsite2)
        button_pruef_leeren.clicked.connect(self.felder_leer)

        button_pruef_back = QPushButton("zurück zur Hauptseite")
        button_pruef_back.setMinimumSize(500, 60)
        button_pruef_back.setMaximumSize(700, 80)
        button_pruef_back.setStyleSheet(button_style_subsite2)
        button_pruef_back.clicked.connect(self.auto_leeren_bei_leave)

        # Button Eindrückeffekt
        def set_shadow(button):
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setOffset(3, 3)
            shadow.setColor(QColor("#E73755"))
            button.setGraphicsEffect(shadow)

        def remove_shadow(button):
            button.setGraphicsEffect(None)

        buttons = [button_pruef, button_pruef_back, button_pruef_leeren]

        for btn in buttons:
            set_shadow(btn)
            btn.pressed.connect(lambda b=btn: remove_shadow(b))
            btn.released.connect(lambda b=btn: set_shadow(b))
    
        # horizontale Anordnung der Buttons
        buttonpruef_layout = QHBoxLayout()
        buttonpruef_layout.addWidget(button_pruef)
        buttonpruef_layout.addWidget(button_pruef_leeren)
        buttonpruef_layout.addWidget(button_pruef_back)

        # Datum
        self.datumWidget = Datum()
        self.datumWidget.setFixedHeight(200)
        
        # Layout der Seite
        datum_layout = QVBoxLayout()
        datum_layout.addWidget(self.datumWidget)
        datum_layout.setContentsMargins(17, 26, 17, 150)
        layout.addLayout(datum_layout)
        layout.addWidget(self.ueberschrift)
        layout.addSpacing(150)
        layout.addLayout(tippfelder_layout)
        layout.addSpacing(600)
        layout.addLayout(buttonpruef_layout)
        layout.addSpacerItem(QSpacerItem(0,100))
    
        self.setLayout(layout)


    def felder_leer(self):
        for feld in self.tippeingabefeld:
            feld.clear()
    
    def auto_leeren_bei_leave(self):
        for feld in self.tippeingabefeld:
            feld.clear()
        self.back_callback()

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





# Glückzahlen generieren
class Glueckszahlen(QWidget):
    def __init__(self, back_callback):
        super().__init__()
        self.back_callback = back_callback
        self.init_ui()
    
    def init_ui(self):
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
        
        # Button Designs
        button_style_subsite1 = """
                                QPushButton {
                                    font-size: 19px;
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
        button_gluck1.setMinimumSize(500, 60)
        button_gluck1.setMaximumSize(700, 80)
        button_gluck1.setStyleSheet(button_style_subsite1)
        button_gluck1.clicked.connect(self.zahlen_generieren)
        
        button_gluck1_back = QPushButton("zurück zur Hauptseite")
        button_gluck1_back.setMinimumSize(500, 60)
        button_gluck1_back.setMaximumSize(700, 80)
        button_gluck1_back.setStyleSheet(button_style_subsite1)
        button_gluck1_back.clicked.connect(self.back_callback)
        button_gluck1_back.clicked.connect(self.auto_leeren_bei_leave)

        # Button Eindrückeffekt
        def set_shadow(button):
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setOffset(3, 3)
            shadow.setColor(QColor("#E73755"))
            button.setGraphicsEffect(shadow)

        def remove_shadow(button):
            button.setGraphicsEffect(None)

        buttons = [button_gluck1, button_gluck1_back]

        for btn in buttons:
            set_shadow(btn)
            btn.pressed.connect(lambda b=btn: remove_shadow(b))
            btn.released.connect(lambda b=btn: set_shadow(b))
        
        # horizontale Anordnung der Buttons
        buttonglueck_layout = QHBoxLayout()
        buttonglueck_layout.addWidget(button_gluck1)
        buttonglueck_layout.addWidget(button_gluck1_back)

        # Datum
        self.datumWidget = Datum()
        self.datumWidget.setFixedHeight(200)
        
        # Layout
        datum_layout = QVBoxLayout()
        datum_layout.addSpacing(200)
        datum_layout.addWidget(self.datumWidget)
        datum_layout.setContentsMargins(17, 27, 17, 500)
        layout.addSpacing(60)
        layout.addLayout(datum_layout)
        layout.addWidget(self.ueberschrift)
        layout.addSpacing(100)
        layout.addWidget(self.glueckszahlen)
        layout.addSpacing(400)
        layout.addLayout(buttonglueck_layout)
        layout.addSpacerItem(QSpacerItem(0,100))
        
        # Layout auf Fenster anwenden
        self.setLayout(layout)


    # leert die Seite nach Verlassen
    def auto_leeren_bei_leave(self):
        self.glueckszahlen.setText("")
        self.back_callback()
    
    def zahlen_generieren(self):
        text = lottozahlen()
        self.glueckszahlen.setText(text)





# Hauptklasse
class EurojackpotApp(QWidget):
    def __init__(self):
        super().__init__()
        aufloesung = QGuiApplication.primaryScreen()
        screen_size = aufloesung.availableGeometry()
        width = int(screen_size.width() * 0.85)
        height = int(screen_size.height() * 0.85)
        self.setWindowTitle("EurojackpotApp")
        favicon_pfad = os.path.dirname(os.path.abspath(__file__))
        favicon = os.path.join(favicon_pfad, "Backend", "Eurojackpot.ico")
        self.setWindowIcon(QIcon(favicon))
        self.resize(width, height)
        self.setMinimumSize(1536, 864)
        self.setMaximumSize(3072, 1920)
        self.move(screen_size.center().x() - self.width() // 2, screen_size.center().y() - self.height() // 2)
        self.stack = QStackedLayout()
        self.main = QWidget()
        
        # Datum
        self.datumWidget = Datum()
        self.datumWidget.setFixedHeight(200)

        # Seite (Hauptschrift)
        title = QLabel("Eurojackpot")
        title.setFont(QFont("Showcard Gothic", 72))
        title.setAlignment(Qt.AlignCenter)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(2, 18)
        shadow.setColor(QColor("#FEDFA052"))
        title.setGraphicsEffect(shadow)

        # Button Designs
        button_style_hauptseite = """
                                   QPushButton {
                                       font-size: 19px;
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
        button1.setMinimumSize(400, 60)
        button1.setMaximumSize(600, 80)
        button1.setStyleSheet(button_style_hauptseite)
        button1.clicked.connect(self.show_glueckszahlen)

        button2 = QPushButton("Tippcheck")
        button2.setMinimumSize(400, 60)
        button2.setMaximumSize(600, 80)
        button2.setStyleSheet(button_style_hauptseite)
        button2.clicked.connect(self.show_tippeingabefeld)

        button3 = QPushButton("Jackpotzahlen hinzufügen")
        button3.setMinimumSize(400, 60)
        button3.setMaximumSize(600, 80)
        button3.setStyleSheet(button_style_hauptseite)
        button3.clicked.connect(self.show_addfeld)
        
        # Button Eindrückeffekt
        def set_shadow(button):
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setOffset(3, 3)
            shadow.setColor(QColor("#E73755"))
            button.setGraphicsEffect(shadow)

        def remove_shadow(button):
            button.setGraphicsEffect(None)

        buttons = [button1, button2, button3]

        for btn in buttons:
            set_shadow(btn)
            btn.pressed.connect(lambda b=btn: remove_shadow(b))
            btn.released.connect(lambda b=btn: set_shadow(b))

        # Einbindung Buttons nebeneinander
        button_layout = QHBoxLayout()
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.addWidget(button3)

        # Layout
        datum_layout = QVBoxLayout()
        datum_layout.addStretch()
        datum_layout.addWidget(self.datumWidget)
        datum_layout.setContentsMargins(17, 30, 17, 500)
        main_layout = QVBoxLayout()
        main_layout.addSpacing(24)
        main_layout.addLayout(datum_layout)
        main_layout.addWidget(title)
        main_layout.addSpacing(500)
        main_layout.addLayout(button_layout)
        main_layout.addSpacerItem(QSpacerItem(0,100))

        # Layout in Fenster anzeigen
        self.main.setLayout(main_layout)
        self.addfeld = Zahlen_add(back_callback=self.show_main)
        self.tippeingabefeld = Tipps_checken(back_callback=self.show_main)
        self.glueckszahlen = Glueckszahlen(back_callback=self.show_main)
        
        self.stack.addWidget(self.main)
        self.stack.addWidget(self.addfeld)
        self.stack.addWidget(self.tippeingabefeld)
        self.stack.addWidget(self.glueckszahlen)
        self.setLayout(self.stack)


    def show_addfeld(self):
        self.stack.setCurrentWidget(self.addfeld)
    
    def show_tippeingabefeld(self):
        self.stack.setCurrentWidget(self.tippeingabefeld)

    def show_glueckszahlen(self):
        self.stack.setCurrentWidget(self.glueckszahlen)

    def show_main(self):
        self.stack.setCurrentWidget(self.main)

         
    # Hauptseite (Hintergrundbild)
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
    font_path = os.path.join(base_path, "Backend", "Showcard Gothic.ttf")
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
    intro_path = os.path.join(base_path, "Backend", "Loading_Screen.png")
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

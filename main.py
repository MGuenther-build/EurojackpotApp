from views.add import addDraw
from views.check import checkYourPicks
from views.generate import generateYourPicks
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QSizePolicy, QMessageBox, QSplashScreen, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QStackedLayout
from PyQt5.QtGui import QFont, QFontDatabase, QPainter, QLinearGradient, QColor, QPixmap, QGuiApplication, QIcon
from utils.dateWidget import DateWidget
import sys
import os
import logging



class App(QWidget):
    def __init__(self):
        super().__init__()
        aufloesung = QGuiApplication.primaryScreen()
        screen_size = aufloesung.availableGeometry()
        width = int(screen_size.width() * 0.85)
        height = int(screen_size.height() * 0.85)
        self.setWindowTitle("EurojackpotApp")
        favicon_path = os.path.dirname(os.path.abspath(__file__))
        favicon = os.path.join(favicon_path, "backend", "images", "Eurojackpot.ico")
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
        
        self.datumWidget = DateWidget()
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
        
        self.addfeld = addDraw(back_callback=self.show_main)
        self.tippeingabefeld = checkYourPicks(back_callback=self.show_main)
        self.glueckszahlen = generateYourPicks(back_callback=self.show_main)
        
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
    fenster = App()
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

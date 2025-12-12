from views.mainpage import App
from utils.splashScreenWidget import fade_out_Loading_Screen
from utils.fonts import font
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
import sys
import os
import logging



if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenster = App()
    showcard_font = font()
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

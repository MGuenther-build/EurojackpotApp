from views.mainpage import App
from utils.splashScreenWidget import show_splash, fade_out_Loading_Screen
from utils.fonts import font
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
import sys
import logging



if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenster = App()
    showcard_font = font()
    fenster.setFont(showcard_font)

    try:
        intro = show_splash()
        intro.show()
        app.processEvents()
        QTimer.singleShot(1000, lambda: fade_out_Loading_Screen(intro, wenn_fertig=fenster.show))
    except Exception as x:
        logging.error(f"[Intro wurde übersprungen] - Grund: {x}")
        fenster.show()
    
    sys.exit(app.exec_())

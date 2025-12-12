from PyQt5.QtGui import QFont, QFontDatabase
import sys
import os



def font():
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
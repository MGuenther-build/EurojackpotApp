from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QSplashScreen
from PyQt5.QtGui import QPixmap
import sys
import os



def splashScreen_path(*parts):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
        internal_path = os.path.join(base_path, "_internal")
        identified_path = os.path.join(internal_path, *parts)
        if os.path.exists(identified_path):
            return identified_path
        
        # Fallback
        return os.path.join(base_path, *parts)

    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(base_path, ".."))
        return os.path.join(project_root, *parts)



def show_splash(scale_factor: float = 0.5) -> QSplashScreen:
    intro_path = splashScreen_path("backend/images/Loading_Screen.webp")
    pixmap = QPixmap(intro_path)
    if pixmap.isNull():
        raise FileNotFoundError(f"Splash konnte nicht geladen werden: {intro_path}")
    screen_size = QSplashScreen().screen().size()
    pixmap_size = pixmap.scaledToWidth(int(screen_size.width() * scale_factor), Qt.SmoothTransformation)
    return QSplashScreen(pixmap_size)


    
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

from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QGraphicsOpacityEffect



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
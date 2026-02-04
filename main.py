import sys
import os

from PyQt6.QtWidgets import QApplication

from gui.audio_device import AudioSwitcher

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    icon_p = resource_path('source/icon.ico')
    nircmd_p = resource_path('source/nircmd.exe')

    ex = AudioSwitcher(icon=icon_p, nircmd_path=nircmd_p)
    ex.show()
    sys.exit(app.exec())
import sys
import threading
import keyboard
from PyQt5.QtWidgets import QApplication
from gui import App

def exit_on_esc(app, window):
    keyboard.wait("esc")
    window.gesture.stop()
    app.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()

    threading.Thread(target=exit_on_esc, args=(app, window), daemon=True).start()

    sys.exit(app.exec_())
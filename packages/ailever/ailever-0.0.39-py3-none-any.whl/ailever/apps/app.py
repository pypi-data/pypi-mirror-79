from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import UIAilever

class AileverApp(QMainWindow, UIAilever.Ui_MainWindow):
    def __init__(self, parent=None):
        super(AileverApp, self).__init__(parent)
        self.setupUi(self)

def run():
    app = QApplication(sys.argv)
    form = AileverApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    run()

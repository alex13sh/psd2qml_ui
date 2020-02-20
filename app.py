from PyQt5.QtWidgets import QApplication
from MainWindw import MyWindow

def startApp(postWinFunc=None):
    import sys
    app = QApplication(sys.argv)
    win = MyWindow(); win.show()
    if postWinFunc: postWinFunc(win)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    startApp()

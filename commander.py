import sys, PyQt5, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi # Import all PyQt5 Widgets

def tryexcept(func):
    def x(*args, **kwargs):
        try: return(func(*args, **kwargs))
        except Exception as e: print(func.__name__,":", "'{}'".format(e))
    return x

class Commander(QMainWindow): # Create a 'mainWindow' class that inherits from the PyQt equivalent
    def __init__(self, *args): 
        super().__init__(*args) # Pass the window arguments to the Qt Class - we don't need it
        self.setWindowFlags(
        QtCore.Qt.Window |
        QtCore.Qt.CustomizeWindowHint |
        QtCore.Qt.WindowTitleHint |
        QtCore.Qt.WindowCloseButtonHint |
        QtCore.Qt.WindowStaysOnTopHint
        )
        self.StartPage()
        self.setTopRight()
        self.show()
        self.activateWindow()
        self.turnOff()
        self.set = False

    def turnOff(self):
        self.taskLabel.setText("Current Task:\n"+"None")
        self.nextButton.setEnabled(False)
        self.backButton.setEnabled(False)

    def turnOn(self):
        self.nextButton.setEnabled(True)
        self.backButton.setEnabled(True)
    
    def setTopRight(self):
        try:
            self.move(1568,0)
        except Exception as e: print("error: ",e)

        
    @tryexcept
    def StartPage(self):
        loadUi("commander.ui", self)
##        self.exitButton.clicked.connect(lambda: sys.exit(app.exec_()))
        
    def updateTask(self,text): self.taskLabel.setText("Current Task:\n"+text)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mWindow = Commander()
    sys.exit(app.exec_()) # Wait for the app to close, then close the program


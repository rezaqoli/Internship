#!/usr/bin/python
import sys
from PyQt5.QtWidgets import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(50,50,300,450)
        self.setWindowTitle("This Our window's Title")
        self.UI()
        

    def UI(self):
        text=QLabel("Hello Python",self)
        text1=QLabel("Hello World",self)
        text1.move(100,50)
        text.move(200,150)
        enterButton=QPushButton('Enter',self)
        exitButton=QPushButton('Exit',self)
        enterButton.move(100,80)
        exitButton.move(200,80)
        self.show()
        


def main():
    App =QApplication(sys.argv)
    window=Window()
    sys.exit(App.exec_())

if __name__ == "__main__":
    main()

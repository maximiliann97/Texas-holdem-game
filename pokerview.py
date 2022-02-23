from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


qt_app = QApplication(sys.argv)


window = QWidget()


betButton = QPushButton("Bet")
callButton = QPushButton("Call")
foldButton = QPushButton("Fold")

hbox = QHBoxLayout()
hbox.addStretch(1)

hbox.addWidget(betButton)
hbox.addWidget(callButton)
hbox.addWidget(foldButton)

vbox = QVBoxLayout()
vbox.addLayout(hbox)
vbox.addStretch(1)

window.setLayout(vbox)


window.show()

ret = qt_app.exec_()


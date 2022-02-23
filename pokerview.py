from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


qt_app = QApplication(sys.argv)


class VerticalMenuBar(QWidget):
    def __init__(self, labels):
        super().__init__()
        self.labels = labels
        vbox = QVBoxLayout()
        vbox.addStretch(1)

        for label in labels:
            button = QPushButton(label)
            button.clicked.connect(lambda checked, label=label: print(label))
            vbox.addWidget(button)
        self.setLayout(vbox)


class PlayerMoney(QLabel):
    def __init__(self, starting_money):
        super().__init__()
        self.starting_money = starting_money
        self.setText(starting_money)


class MyBox(QGroupBox):
    def __init__(self):
        super().__init__("Poker Table")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(VerticalMenuBar(['Bet', 'Call', 'Fold']))

        hbox.addWidget(PlayerMoney("Money\n 200"))
        self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 150)

win = MyBox()
win.show()
qt_app.exec_()



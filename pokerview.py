from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


qt_app = QApplication(sys.argv)


class VerticalActionBar(QWidget):
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


class PlayerMoneyView(QLabel):
    def __init__(self):
        super().__init__()
        #self.money_model = money_model
        #self.starting_money = starting_money
        self.setText('placeholder')

    #def update_label(self, new_value):
     #   self.setText(f"€{new_value}")


class ActionBar(QGroupBox):
    def __init__(self):
        super().__init__()
        label1 = QLabel("Turn")
        label2 = QLabel("Blind")
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(VerticalActionBar(['Bet', 'Call', 'Fold']))

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)


class PlayerView(QGroupBox):
    def __init__(self):
        super().__init__("Player's name")

        label = QLabel()
        label.setText("Money")

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(label)

        self.setLayout(vbox)


class GameView(QWidget):
    def __init__(self):
        super().__init__()
        hbox = QHBoxLayout()
        label = QLabel("Table Cards")
        hbox.addWidget(label)

        self.setLayout(hbox)


class GraphicView(QGroupBox):
    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout()
        vbox.addWidget(PlayerView())
        vbox.addWidget(GameView())
        vbox.addWidget(PlayerView())
        vbox.addStretch(1)

        self.setLayout(vbox)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()

        layout = QHBoxLayout()
        layout.addWidget(GraphicView())
        layout.addWidget(ActionBar())
        widget.setLayout(layout)
        self.setCentralWidget(widget)


win = MyWindow()
win.show()
qt_app.exec_()



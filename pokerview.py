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


class PlayerMoneyView(QLabel):
    def __init__(self):
        super().__init__()
        #self.money_model = money_model
        #self.starting_money = starting_money
        self.setText('placeholder')

    #def update_label(self, new_value):
     #   self.setText(f"€{new_value}")


class ToolBar(QGroupBox):
    def __init__(self):
        super().__init__()

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(VerticalMenuBar(['Bet', 'Call', 'Fold']))

        self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 150)


class PlayerView(QGroupBox):
    def __init__(self):
        super().__init__("Player's name")

        label = QLabel()
        label.setText("Money")
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(label)
        #vbox.addWidget(card_view)






class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        tool_bar = ToolBar()
        player_view = PlayerView()
        dockWidget = QDockWidget(player_view)
        self.setCentralWidget(tool_bar)
        self.addDockWidget(Qt.TopDockWidgetArea, dockWidget)


win = MyWindow()
win.show()
qt_app.exec_()



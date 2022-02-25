from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


qt_app = QApplication(sys.argv)







class MyCounterView(QWidget):
    def __init__(self, model):
        super().__init__()
        # Let us store this in self to have a convenient reference to it later:
        self.model = model
        self.counter_label = QLabel()

        # but we won't need to access this again in this simple application:
        button = QPushButton("Increment")
        button.clicked.connect(self.button_click)

        # Present the information to the user:
        vbox = QVBoxLayout()
        vbox.addWidget(self.counter_label)
        vbox.addWidget(button)
        self.setLayout(vbox)

        # This is a View, we need to listen to our model to know when we should update the representation:
        self.model.my_signal.connect(self.update_count)

        # Lets also trigger it once from the start so we're up-to-date.
        self.update_count()

    def button_click(self):
        self.model.increment()

    def update_count(self):
        self.counter_label.setText(f'{self.model.count}')


win = MyCounterView(c)
win.show()
qt_app.exec_()
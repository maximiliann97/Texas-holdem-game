from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


qt_app = QApplication(sys.argv)


# def some_func():
#     print("some function has been called!")
#
# def some_other_func():
#     print("some other function has been called!")
#
# qt_app = QApplication.instance()
# button = QPushButton("Call some function")
#
# button.clicked.connect(some_func)
#
#
# button.clicked.connect(some_other_func)
#
#
# button.show()
# qt_app.exec_()

# class MyCounter(QObject):
#     my_signal = pyqtSignal(int)
#
#     def __init__(self, initial_value):
#         super().__init__()
#         self.count = initial_value
#
#     def increment(self):
#         self.count += 1
#         self.my_signal.emit(self.count)
#
#
# c = MyCounter(42)
# c.my_signal.connect(lambda x: print(f'Counter is now at {x}'))
#
# print(c.increment())


class AddOneGame(QObject):
    new_total = pyqtSignal()
    winner = pyqtSignal((str,))

    def __init__(self):
        super().__init__()  # Don't forget super init when inheriting!
        self.players = ['Micke', 'Thomas']
        self.total = [0, 0]

    def player_click(self, index):
        self.total[index] += 1
        self.new_total.emit()  # order matters!
        self.check_winner()

    def reset(self):
        self.total = [0, 0]
        self.new_total.emit()

    def check_winner(self):
        for total, player in zip(self.total, self.players):
            if total >= 10:
                self.winner.emit(player + " won!")
                self.reset()


class GameView(QWidget):
    def __init__(self, game_model):
        super().__init__()

        # The init method for views should always be quite familiar; it has a section for creating widgets
        buttons = [QPushButton(game_model.players[0]), QPushButton(game_model.players[1])]
        self.labels = [QLabel(), QLabel()]
        # then arranging them in the desired layout
        vbox = QVBoxLayout()
        vbox.addWidget(buttons[0])
        vbox.addWidget(self.labels[0])
        vbox.addWidget(buttons[1])
        vbox.addWidget(self.labels[1])

        reset_button = QPushButton('Reset')
        vbox.addWidget(reset_button)

        self.setLayout(vbox)

        # Controller part happens to be inside this widget as well application
        def player0_click(): game_model.player_click(0)

        buttons[0].clicked.connect(player0_click)

        def player1_click(): game_model.player_click(1)

        buttons[1].clicked.connect(player1_click)
        reset_button.clicked.connect(game_model.reset)

        # almost always storing a reference to the related model
        self.game = game_model
        # and connecting some method for updating the state to the corresponding signals
        game_model.new_total.connect(self.update_labels)
        game_model.winner.connect(self.alert_winner)
        # and giving it an initial update so that we show the initial state
        self.update_labels()

        # This also happens to be the main window, so we can opt to show it immediately
        # (we could also very well leave this up to the caller)
        self.show()

    def update_labels(self):
        for i in range(2): self.labels[i].setText('Points: {}'.format(self.game.total[i]))

    def alert_winner(self, text: str):
        msg = QMessageBox()
        msg.setText(text)
        msg.exec()

qt_app = QApplication.instance()
game = AddOneGame()
view = GameView(game)
qt_app.exec_()


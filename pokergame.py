from pokerview import *
import sys


def main():
    player_1 = input("Player 1 enter your name: ", )
    player_2 = input("Player 2 enter your name: ", )
    qt_app = QApplication(sys.argv)
    game = TexasHoldEm([Player(player_1), Player(player_2)])
    win = MyWindow(game)
    win.show()

    qt_app.exec_()


if __name__ == '__main__':
    main()

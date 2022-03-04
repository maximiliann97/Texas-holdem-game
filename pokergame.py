from pokerview import *
import sys


def main():
    qt_app = QApplication(sys.argv)
    game = TexasHoldEm([Player('Maximilian'), Player('Axel')])
    win = MyWindow(game)
    win.show()

    qt_app.exec_()


if __name__ == '__main__':
    main()

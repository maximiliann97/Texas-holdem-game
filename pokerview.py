from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
import cardlib
import sys

import pokermodel
from pokermodel import *


class TableScene(QGraphicsScene):
    """ A scene with a table cloth background """
    def __init__(self):
        super().__init__()
        self.tile = QPixmap('cards/table.png')
        self.setBackgroundBrush(QBrush(self.tile))


class CardItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """
    def __init__(self, renderer, position):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = position


def read_cards():
    """
    Reads all the 52 cards from files.
    :return: Dictionary of SVG renderers
    """
    all_cards = dict()  # Dictionaries let us have convenient mappings between cards and their images
    for suit in 'HDSC':  # You'll need to map your suits to the filenames here. You are expected to change this!
        for value_file, value in zip(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], range(2, 15)):
            file = value_file + suit
            key = (value, suit)  # I'm choosing this tuple to be the key for this dictionary
            all_cards[key] = QSvgRenderer('cards/' + file + '.svg')
    return all_cards


class CardView(QGraphicsView):
    """ A View widget that represents the table area displaying a players cards. """

    # We read all the card graphics as static class variables
    back_card = QSvgRenderer('cards/Red_Back_2.svg')
    all_cards = read_cards()

    def __init__(self, card_model: CardModel, card_spacing: int = 250, padding: int = 10):
        """
        Initializes the view to display the content of the given model
        :param cards_model: A model that represents a set of cards. Needs to support the CardModel interface.
        :param card_spacing: Spacing between the visualized cards.
        :param padding: Padding of table area around the visualized cards.
        """
        self.scene = TableScene()
        super().__init__(self.scene)

        self.card_spacing = card_spacing
        self.padding = padding

        self.model = card_model
        # Whenever the this window should update, it should call the "__change_cards" method.
        # This view can do so by listening to the matching signal:
        card_model.new_cards.connect(self.__change_cards)

        # Add the cards the first time around to represent the initial state.
        self.__change_cards()

    def __change_cards(self):  # double underscore indicates that this is a private method
        # Add the cards from scratch
        self.scene.clear()
        for i, card in enumerate(self.model):
            # The ID of the card in the dictionary of images is a tuple with (value, suit), both integers
            graphics_key = (card.get_value(), card.suit)
            renderer = self.back_card if self.model.flipped() else self.all_cards[graphics_key]
            c = CardItem(renderer, i)

            # Shadow effects are cool!
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))  # Semi-transparent black!
            c.setGraphicsEffect(shadow)

            # Place the cards on the default positions
            c.setPos(c.position * self.card_spacing, 0)
            # We could also do cool things like marking card by making them transparent if we wanted to!
            # c.setOpacity(0.5 if self.model.marked(i) else 1.0)
            self.scene.addItem(c)

        self.update_view()

    def update_view(self):
        scale = (self.viewport().height()-2*self.padding)/313
        self.resetTransform()
        self.scale(scale, scale)
        # Put the scene bounding box
        self.setSceneRect(-self.padding//scale, -self.padding//scale,
                          self.viewport().width()//scale, self.viewport().height()//scale)

    def resizeEvent(self, painter):
        # This method is called when the window is resized.
        # If the widget is resize, we gotta adjust the card sizes.
        # QGraphicsView automatically re-paints everything when we modify the scene.
        self.update_view()
        super().resizeEvent(painter)


class VerticalActionBar(QWidget):
    def __init__(self, labels, game: TexasHoldEm):
        super().__init__()
        self.game = game
        game.new_value.connect(self.update_value)

        self.bet = QPushButton("Bet")
        self.call = QPushButton("Call")
        self.fold = QPushButton("Fold")
        vbox = QVBoxLayout()
        vbox.addStretch(1)

        self.setLayout(vbox)

        # Controller part
        def actions():
            action_list = [game.bet(), game.call(), game.fold()]

        for action in action_list:
            self.action.clicked.connect(actions)



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
        label1 = QLabel()
        label2 = QLabel()
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(VerticalActionBar())

    self.setLayout(vbox)

    self.setGeometry(300, 300, 300, 150)

    def update_pot(self):
        self.label1.setText("Pot\n" + str(self.game.pot()))

####


class PlayerView(QGroupBox):
    def __init__(self, player: Player):
        super().__init__("Player's name")
        self.label = QLabel()
        card_view = CardView(player.hand, card_spacing=50)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.label)
        vbox.addWidget(card_view)

        self.setLayout(vbox)

    def update_money(self):
        self.label.setText("Money\n" + str(self.player.money()))







class GameView(QWidget):
    def __init__(self):
        super().__init__()
        hbox = QHBoxLayout()
        hand = HandModel()
        label = CardView(hand)
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
    def __init__(self, game: TexasHoldEm):
        super().__init__()
        widget = QWidget()

        layout = QHBoxLayout()
       # layout.addWidget(GraphicView(TexasHoldEm))
        layout.addWidget(ActionBar(game))
        widget.setLayout(layout)
        self.setCentralWidget(widget)

# pokergame.py:
qt_app = QApplication(sys.argv)
win = MyWindow()
win.show()
qt_app.exec_()



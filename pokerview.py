from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from cardlib import *
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
    for suit_file, suit in zip('HSCD', Suit):
        for value_file, value in zip(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], range(2, 15)):
            file = value_file + suit_file
            key = (value, suit)  # I'm choosing this tuple to be the key for this dictionary
            all_cards[key] = QSvgRenderer('cards/' + file + '.svg')
        #print(all_cards)
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


####

class ActionBar(QGroupBox):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.pot = QLabel()
        self.active_label = QLabel()
        self.blind_label = QLabel()
        self.bet = QPushButton("Bet")
        self.call = QPushButton("Call")
        self.check = QPushButton("Check")
        self.fold = QPushButton("Fold")
        self.betting_amount = QSpinBox()
        self.betting_amount.setMinimum(50)

        vbox = QVBoxLayout()

        # Adding widgets to action bar
        vbox.addWidget(self.active_label)
        vbox.addWidget(self.blind_label)
        vbox.addWidget(self.pot)
        vbox.addWidget(self.bet)
        vbox.addWidget(self.call)
        vbox.addWidget(self.bet)
        vbox.addWidget(self.check)
        vbox.addWidget(self.fold)
        vbox.addWidget(self.betting_amount)

        self.setLayout(vbox)

        # Connect logic
        game.pot.new_value.connect(self.update_pot)
        game.active_player_changed.connect(self.update_active_player)
        game.active_player_changed.connect(self.update_maximum_bet)
        game.active_player_changed.connect(self.update_blind)

        # Updates
        self.update_pot()
        self.update_active_player()
        self.update_maximum_bet()
        self.update_blind()

        def bet():
            game.bet(self.betting_amount.value())
        self.bet.clicked.connect(bet)

        def call():
            game.call()
        self.call.clicked.connect(call)

        def check():
            game.check()
        self.check.clicked.connect(check)

        def fold():
            game.fold()
        self.fold.clicked.connect(fold)

    def update_pot(self):
        self.pot.setText("Pot\n$ " + str(self.game.pot.value))

    def update_active_player(self):
        self.active_label.setText(str(self.game.the_active_player_name))

    def update_maximum_bet(self):
        self.betting_amount.setMaximum(self.game.the_active_player_money)

    def update_blind(self):
        self.blind_label.setText('Blind: ' + str(self.game.blind_player_name))


class PlayerView(QGroupBox):
    def __init__(self, player, game):
        super().__init__(player.name)
        self.player = player
        self.money_label = QLabel()

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        vbox.addWidget(self.money_label)
        vbox.addStretch(1)

        hand_card_view = CardView(player.hand)
        vbox.addWidget(hand_card_view)

        # Connect logic:
        self.game = game
        player.money.new_value.connect(self.update_money)

        self.update_money()

    def update_money(self):
        self.money_label.setText('Money\n$ {}' .format(self.player.money.value))


class GameView(QWidget):
    def __init__(self, game):
        super().__init__()
        hbox = QHBoxLayout()
        hand = HandModel()
        table_card_view = CardView(game.table)
        hbox.addWidget(table_card_view)

        self.setLayout(hbox)

        self.game = game
        game.game_message.connect(self.game_alerts)

    @staticmethod
    def game_alerts(text):
        msg = QMessageBox()
        msg.setText(text)
        msg.exec_()


class GraphicView(QGroupBox):
    def __init__(self, game):
        super().__init__()
        self.game = game

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        vbox.addWidget(PlayerView(game.players[0], game))
        vbox.addWidget(GameView(game))
        vbox.addWidget(PlayerView(game.players[1], game))


class MyWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        widget = QWidget()
        self.game = game

        layout = QHBoxLayout()
        layout.addWidget(GraphicView(game))
        layout.addWidget(ActionBar(game))
        widget.setLayout(layout)
        self.setCentralWidget(widget)




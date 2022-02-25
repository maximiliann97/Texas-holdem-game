from PyQt5.QtCore import *
import abc
import cardlib


class CardModel(QObject):
    """ Base class that described what is expected from the CardView widget """

    new_cards = pyqtSignal()  #: Signal should be emited when cards change.

    @abc.abstractmethod
    def __iter__(self):
        """Returns an iterator of card objects"""

    @abc.abstractmethod
    def flipped(self):
        """Returns true of cards should be drawn face down"""


# A trivial card class (you should use the stuff you made in your library instead!
class MySimpleCard:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def get_value(self):
        return self.value


# You have made a class similar to this (hopefully):
class Hand:
    def __init__(self):
        # Lets use some hardcoded values for most of this to start with
        self.cards = [MySimpleCard(13, 'H'), MySimpleCard(7, 'D'), MySimpleCard(13, 'S')]

    def add_card(self, card):
        self.cards.append(card)


class HandModel(Hand, CardModel):
    def __init__(self):
        Hand.__init__(self)
        CardModel.__init__(self)
        # Additional state needed by the UI
        self.flipped_cards = False

    def __iter__(self):
        return iter(self.cards)

    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.new_cards.emit()  # something changed, better emit the signal!

    def flipped(self):
        # This model only flips all or no cards, so we don't care about the index.
        # Might be different for other games though!
        return self.flipped_cards

    def add_card(self, card):
        super().add_card(card)
        self.new_cards.emit()  # something changed, better emit the signal!


class Player(QObject):
    def __init__(self, name):
        super.__init__()
        self.name = name
        self.money = 200        #amount player starts with

    def money(self):
        return self.money

    def change_money(self):
        







class TableModel(CardModel):
    def flipped(self):
        return False


class TexasHoldEm(QObject):
    def __init__(self, names):
        super.__init__()
        self.players = [Player(name, 1000) for name in names]
        self.deck = ...
        self.pot = ...
        self.active_player = 0

    new_value = pyqtSignal()

    def new_round(self):
        self.pot = 0

    def fold(self):
        player = self.players[self.active_player]

    def bet(self, amount: int):
        player = self.players[self.active_player]
        player.money -= amount
        self.pot += amount
        self.new_value.emit()

    def call(self):
        player = self.players[self.active_player]
        pass


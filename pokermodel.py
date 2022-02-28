from PyQt5.QtCore import *
import abc
from cardlib import *


class CardModel(QObject):
    """ Base class that described what is expected from the CardView widget """

    new_cards = pyqtSignal()  #: Signal should be emited when cards change.

    @abc.abstractmethod
    def __iter__(self):
        """Returns an iterator of card objects"""

    @abc.abstractmethod
    def flipped(self):
        """Returns true of cards should be drawn face down"""


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


class MoneyModel(QObject):
    new_value = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.value = 1000       # The amount players start with

    def __isub__(self, other):
        self.value -= other
        self.new_value.emit()
        return self

    def __iadd__(self, other):
        self.value += other
        self.new_value.emit()
        return self


class Player(QObject):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.hand = HandModel()
        self.money = MoneyModel()

    def set_active(self, active):
        self.active = active


class TexasHoldEm(QObject):

    pot_changed = pyqtSignal()
    card_data_changed = pyqtSignal()
    game_message = pyqtSignal((str,))

    def __init__(self, players):
        super().__init__()
        self.players = players
        self.new_round()

    def new_round(self):
        self.active_player = 0
        self.pot = 0
        self.table = []
        self.check_stepper = 0
        self.deck = StandardDeck()
        self.deck.shuffle()
        self.players[self.active_player].set_active(True)
        self.card_data_changed.emit()

        for player in self.players:
            player.hand.cards.clear()
            player.hand.add_card(self.deck.draw())
            player.hand.add_card(self.deck.draw())
            print(player.hand)

    def deal(self, number_of_cards: int):
        for card in range(number_of_cards):
            self.table.append(self.deck.draw())
        self.card_data_changed.emit()
        self.check_stepper += 1

    def check(self):
        if self.check_stepper == 0:
            self.deal(3)
        elif self.check_stepper == 1 or self.check_stepper == 2:
            self.deal(1)

    def player_money(self):
        return self.players.money

    def pot(self):
        return self.pot

    def bet(self, amount: int):
        self.pot += amount
        self.players[self.active_player].money -= amount
        self.players[self.active_player].set_active(False)
        self.active_player = (self.active_player + 1) % len(self.players)
        self.players[self.active_player].set_active(True)
        self.pot_changed.emit()

    def call(self, amount: int):
        self.pot += amount
        self.players[self.active_player].money -= amount
        self.players[self.active_player].set_active(False)
        self.active_player = (self.active_player + 1) % len(self.players)
        self.players[self.active_player].set_active(True)
        self.pot_changed.emit()

    def fold(self):
        self.players[self.active_player].set_active(False)
        self.active_player = (self.active_player + 1) % len(self.players)
        self.players[self.active_player].set_active(True)
        self.players[self.active_player].money += self.pot
        self.new_round()
        self.pot_changed.emit()









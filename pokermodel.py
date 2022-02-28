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


class TableModel(CardModel):
    def __init__(self):
        CardModel.__init__(self)
        self.cards = []

    def __iter__(self):
        return iter(self.cards)

    def flipped(self):
        # This model only flips all or no cards, so we don't care about the index.
        # Might be different for other games though!
        return False

    def add_cards(self, cards):
        self.cards.append(cards)
        self.new_cards.emit()  # something changed, better emit the signal!

    def clear(self):
        self.cards = []
        self.new_cards.emit()


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

    def clear(self):
        self.cards = []
        self.new_cards.emit()


class MoneyModel(QObject):
    new_value = pyqtSignal()

    def __init__(self, init_val=0):
        super().__init__()
        self.value = init_val       # The amount players start with

    def __isub__(self, other):
        self.value -= other
        self.new_value.emit()
        return self

    def __iadd__(self, other):
        self.value += other
        self.new_value.emit()
        return self

    def clear(self):
        self.value = 0
        self.new_value.emit()


class Player(QObject):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.hand = HandModel()
        self.money = MoneyModel(1000)
        self.betted = MoneyModel()

    def place_bet(self, amount):
        self.money -= amount
        self.betted += amount

    def receive_pot(self, amount):
        self.money += amount

    def clear(self):
        self.hand.clear()
        self.betted.clear()

    def set_active(self, active):
        self.active = active


class TexasHoldEm(QObject):

    game_message = pyqtSignal((str,))

    def __init__(self, players):
        super().__init__()
        self.players = players
        self.pot = MoneyModel()
        self.table = TableModel()
        self.__new_round()

    def __new_round(self):
        self.loser()
        self.active_player = 0
        self.pot.clear()
        self.table.clear()
        self.check_stepper = 0
        self.deck = StandardDeck()
        self.deck.shuffle()
        self.players[self.active_player].set_active(True)

        for player in self.players:
            player.clear()
            player.hand.add_card(self.deck.draw())
            player.hand.add_card(self.deck.draw())

        self.check()

    def deal(self, number_of_cards: int):
        for card in range(number_of_cards):
            self.table.add_cards(self.deck.draw())
        self.table.new_cards.emit()
        self.check_stepper += 1

    def check(self):
        if self.check_stepper == 0:
            self.deal(3)
        elif self.check_stepper == 1 or self.check_stepper == 2:
            self.deal(1)
        else:
            pass

        self.players[self.active_player].set_active(False)
        self.active_player = (self.active_player + 1) % len(self.players)
        self.players[self.active_player].set_active(True)

    def bet(self, amount: int):
        self.pot += amount
        self.players[self.active_player].place_bet(amount)
        self.players[self.active_player].set_active(False)
        self.active_player = (self.active_player + 1) % len(self.players)
        self.players[self.active_player].set_active(True)

    def call(self):
        max_bet = max([player.betted.value for player in self.players])
        amount = max_bet - self.players[self.active_player].betted.value
        if amount != 0:
            self.pot += amount
            self.players[self.active_player].place_bet(amount)
            self.players[self.active_player].set_active(False)
            self.active_player = (self.active_player + 1) % len(self.players)
            self.players[self.active_player].set_active(True)
        else:
            self.game_message.emit("You cannot call!")

    def fold(self):
        self.players[self.active_player].set_active(False)
        self.active_player = (self.active_player + 1) % len(self.players)
        self.players[self.active_player].set_active(True)
        self.players[self.active_player].receive_pot(self.pot.value)
        self.__new_round()

    def loser(self):
        for player in self.players:
            if player.money.value <= 0:
                self.game_message.emit(player.name + "is out of money!")
                quit()









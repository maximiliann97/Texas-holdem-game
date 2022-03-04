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
        self.value = init_val

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
        self.money = MoneyModel(1000)   # Define the amount of money the players start with
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

    def clear_money(self):
        self.money.clear()


class TexasHoldEm(QObject):

    active_player_changed = pyqtSignal()    # Signal only handling when the active player is changed.
    game_message = pyqtSignal((str,))       # Signal handling game messages

    def __init__(self, players):
        super().__init__()
        self.players = players
        self.active_player = 0
        self.pot = MoneyModel()
        self.table = TableModel()
        self.__new_round()  # Initializes a new round when program is launched

    def __new_round(self):
        self.loser()    # Checks if someone is out of money and therefore the game is ended.
        self.check_counter = 0
        self.pot.clear()
        self.table.clear()
        self.deck = StandardDeck()
        self.deck.shuffle()
        self.players[self.active_player].set_active(True)

        for player in self.players:
            player.clear()
            player.hand.add_card(self.deck.draw())
            player.hand.add_card(self.deck.draw())

        self.blind(self.players[self.active_player])
        self.change_active_player()
        self.players[self.active_player].hand.flip()
        self.change_active_player()
        self.check()

    def deal(self, number_of_cards: int):
        for card in range(number_of_cards):
            self.table.add_cards(self.deck.draw())
        self.table.new_cards.emit()

    def check(self):
        min_bet = min([player.betted.value for player in self.players])
        if min_bet <= 0:
            self.game_message.emit("You cannot check")
        else:
            if self.check_counter == 2:     # After both players checks the first time the flop is dealt
                self.deal(3)
            elif self.check_counter == 4 or self.check_counter == 6:    # After both check again another card is dealt
                self.deal(1)
            elif self.check_counter == 8:      # When all 5 cards is on the table and both players check, winner is checked.
                self.check_round_winner()
                self.players[self.active_player].hand.flip()

            self.check_counter += 1
            self.change_active_player()

    def bet(self, amount: int):
        if self.players[self.active_player].money.value <= 0:
            self.game_message.emit("You are out of money")
        else:
            self.pot += amount
            self.players[self.active_player].place_bet(amount)
            self.change_active_player()

    def call(self):
        max_bet = max([player.betted.value for player in self.players])
        amount = max_bet - self.players[self.active_player].betted.value
        if amount != 0:     # Proceeds if a call is possible otherwise a message is provided.
            self.pot += amount
            self.players[self.active_player].place_bet(amount)
            self.change_active_player()
        else:
            self.game_message.emit("You cannot call!")

    def fold(self):
        self.change_active_player()
        self.players[self.active_player].receive_pot(self.pot.value)
        self.game_message.emit(self.players[self.active_player].name + ' won $ ' + str(self.pot.value))
        self.__new_round()
        self.players[self.active_player].hand.flip()

    def check_round_winner(self):
        best_poker_hands = [player.hand.best_poker_hand(self.table.cards) for player in self.players]   # Saves both
        # player's best poker hands in a list

        if best_poker_hands[0] > best_poker_hands[1]:
            self.players[0].receive_pot(self.pot.value)
            self.game_message.emit(self.players[0].name + ' won $ ' + str(self.pot.value))

        elif best_poker_hands[1] > best_poker_hands[0]:
            self.players[1].receive_pot(self.pot.value)
            self.game_message.emit(self.players[1].name + ' won $ ' + str(self.pot.value))

        else:
            for player in self.players:
                player.receive_pot(self.pot.value/2)
            self.game_message.emit('Draw! Pot splits between both players')

        self.__new_round()
        self.check_counter -= 1     # Drops the check counter after the winner is determined to prevent only one
        # check being required to show the flop thereafter.

    def loser(self):
        for player in self.players:
            if player.money.value <= 0:
                self.game_message.emit(player.name + " is out of money, game ends!")
                quit()

    def change_active_player(self):
        """
        Method to change the player and show who's the active player, also saving the amount of money the active player
        has, which is useful for setting a maximum bet in the view.
        """

        self.players[self.active_player].set_active(False)
        self.active_player = (self.active_player + 1) % len(self.players)
        self.players[self.active_player].set_active(True)

        if self.active_player == 0:
            self.the_active_player_name = str(self.players[0].name) + '\'s turn'
            self.the_active_player_money = self.players[0].money.value
            self.active_player_changed.emit()
            self.players[1].hand.flip()
            self.players[0].hand.flip()
        else:
            self.the_active_player_name = str(self.players[1].name) + '\'s turn'
            self.the_active_player_money = self.players[1].money.value
            self.active_player_changed.emit()
            self.players[0].hand.flip()
            self.players[1].hand.flip()

    def blind(self, blind_player):
        self.pot += 50
        blind_player.place_bet(50)
        self.blind_player_name = blind_player.name



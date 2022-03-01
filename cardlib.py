from enum import Enum
from abc import ABC, abstractmethod
from random import shuffle
from collections import Counter


class Suit(Enum):
    """
    Class of Enum type implemented in order to sort using the __lt__ operator
    """
    Hearts = 3
    Spades = 2
    Clubs = 1
    Diamonds = 0

    def __str__(self):
        return self.name

class PlayingCard(ABC):
    """
    Is an abstract base class, which will work as a blueprint for creating the cards.
    """

    def __init__(self, suit: Suit):
        """
        Constructs suit

        :param suit:

        """
        self.suit = suit

    @abstractmethod
    def get_value(self):
        """
        Abstract method for retrieving values of cards, serves as a contract: in order to be considered a card
        this method must be implemented in the card.
        """
        pass

    def __eq__(self, other):
        """
        Equal operator that enables comparing if values are equal

        :param other:

        :return: True or False
        """
        return self.get_value() == other.get_value()

    def __lt__(self, other):
        """
        Less than operator enables comparing magnitude of values.

        :param other:

        :return: True or False
        """
        return self.get_value() < other.get_value()


class NumberedCard(PlayingCard):
    """
    Subclass of PlayingCard which it inherits from. Subclass is the numbered cards in a deck.
    """
    def __init__(self, value, suit):
        """
        Constructs the card with value and inherit suit from PlayingCard

        :param value:

        :param suit:
        """
        self.value = value
        super().__init__(suit)

    def get_value(self):
        """
        Method of retrieving card values

        :return: value
        """
        return self.value

    def __repr__(self):
        """
        Overloads the __repr__ to print the card in a neat manner

        """
        return f"{str(self.value)} of {str(self.suit.name)}"

class JackCard(PlayingCard):
    """
    Subclass of PlayingCard which it inherits from. Subclass is the Jack card in a deck corresponding to value 11.
    """
    def get_value(self):
        """
        Method of retrieving card values

        :return: value = 11
        """
        return 11

    def __repr__(self):
        """
        Overloads the __repr__ to print the card in a neat manner

        """
        return f"Jack of {self.suit.name}"


class QueenCard(PlayingCard):
    """
    Subclass of PlayingCard which it inherits from. Subclass is the Queen card in a deck corresponding to value 12.
    """

    def get_value(self):
        """
        Method of retrieving card values

        :return: value = 12
        """
        return 12

    def __repr__(self):
        """
        Overloads the __repr__ to print the card in a neat manner

        """
        return f"Queen of {self.suit.name}"


class KingCard(PlayingCard):
    """
    Subclass of PlayingCard which it inherits from. Subclass is the King card in a deck corresponding to value 13.
    """
    def get_value(self):
        """
        Method of retrieving card values
        :return: value = 13

        """
        return 13

    def __repr__(self):
        """
        Overloads the __repr__ to print the card in a neat manner

        """
        return f"King of {self.suit.name}"


class AceCard(PlayingCard):
    """
    Subclass of PlayingCard which it inherits from. Subclass is the Ace card in a deck corresponding to value 14.
    """
    def get_value(self):
        """
        Method of retrieving card values

        :return: value = 14
        """
        return 14

    def __repr__(self):
        """
        Overloads the __repr__ to print the card in a neat manner

        """
        return f"Ace of {self.suit.name}"


class StandardDeck:
    """
    Class that creates the deck of cards containing 52 unique cards, incorporates methods for shuffling the deck and
    drawing cards.
    """
    def __init__(self):
        """
        Constructs an empty list which is to be filled with cards in no particular order.
        """
        self.cards = []

        for suit in Suit:
            self.cards.append(AceCard(suit))
            self.cards.append(KingCard(suit))
            self.cards.append(QueenCard(suit))
            self.cards.append(JackCard(suit))
            for value in range(2, 11):
                self.cards.append(NumberedCard(value, suit))

    def shuffle(self):
        """
        Shuffles the deck with the shuffle function
        """
        shuffle(self.cards)

    def draw(self):
        """
        Draws the first card of the deck.

        """
        return self.cards.pop(0)

    def __repr__(self):
        """
        Overloads the __repr__ to print the cards of the deck

        """
        return str(self.cards)


class Hand:
    """
    Class that represents a player's hand with methods that add, drop and sorting cards. It also includes a method that
    returns the best poker hand based on the cards on the table and the cards on the hand.
    """
    def __init__(self):
        """
        Construct a hand with cards

        :param cards:
        """
        self.cards = []


    def add_card(self, card):
        """
        Method that add cards to the hand

        :param card:
        """
        self.cards.append(card)

    def drop_cards(self, indices):
        """
        dropping cards from the hand based on index

        :param indices:
        """
        for index in sorted(indices, reverse=True):
            del self.cards[index]

    def sort(self):
        """
        Sort the cards on the hand

        """
        self.cards.sort()

    def best_poker_hand(self, cards=[]):
        """
        Gives the best poker hand based on cards on the table and cards on the hand

        :param cards: list of cards

        :return: The hand type with it's Enum value and a list with all the cards (cards on hand and cards on table, i.e. 7 cards)
        """
        return PokerHand(self.cards + cards)

    def __repr__(self):
        """
        Overloads the __repr__ to print the cards of the hand

        """
        return str(self.cards)


class HandType(Enum):
    """
    Enum class that assign a value to each hand type
    """

    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIRS = 3
    PAIR = 2
    HIGH_CARD = 1

    def __lt__(self, other):
        """
        Less than operator enables comparing magnitude of values.

        :param other:

        :return: True or False
        """
        return self.value < other.value

    def __eq__(self, other):
        """
        Equal operator that enables comparing if values are equal

        :param other:

        :return: True or False
        """
        return self.value == other.value


class PokerHand:
    """
    Class that checks the hand type of the poker hand
    """
    def __init__(self, cards: list):
        """
        Construct self.type that represent the highest hand type of the poker hand

        :param cards: List of cards
        """
        self.cards = cards.sort(reverse=True)
        checkers = [self.check_straight_flush, self.check_four_of_a_kind, self.check_full_house,
                    self.check_flush, self.check_straight, self.check_diff_pairs]

        for checker in checkers:
            v = checker(cards)
            if v is not None:
                self.type, self.values = v
                break

    def __lt__(self, other):
        """
        Less than operator enables comparing magnitude of values.

        :param other:

        :return: True or False
        """
        return (self.type, self.values) < (other.type, other.values)

    def __eq__(self, other):
        """
        Equal operator that enables comparing if values are equal

        :param other:

        :return: True or False
        """
        return (self.type, self.values) == (other.type, other.values)

    @staticmethod
    def check_straight_flush(cards):
        """
        Static method to check if there is a straight flush

        :param cards: List of cards

        :return: HandType and list of the considered cards in descending order
        """
        vals = [(c.get_value(), c.suit) for c in cards] \
               + [(1, c.suit) for c in cards if c.get_value() == 14]  # Add the aces!
        for c in reversed(cards):  # Starting point (high card)
            # Check if we have the value - k in the set of cards:
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k, c.suit) not in vals:
                    found_straight = False
                    break
            if found_straight:
                return HandType.STRAIGHT_FLUSH, cards[0:7]

    @staticmethod
    def check_four_of_a_kind(cards):
        """
        Static method to check if there is a four of a kind

        :param cards: List of cards

        :return: HandType and list of the considered cards in descending order
        """
        value_count = Counter()
        for c in cards:
            value_count[c.get_value()] += 1
        # Find the card ranks that have at least four of a kind
        fours = [v[0] for v in value_count.items() if v[1] >= 4]
        fours.sort()
        if fours:
            return HandType.FOUR_OF_A_KIND, cards[0:7]

    @staticmethod
    def check_full_house(cards):
        """
        Static method to check if there is a full house

        :param cards: List of cards

        :return: HandType and list of the considered cards in descending order
        """
        value_count = Counter()
        for c in cards:
            value_count[c.get_value()] += 1
        # Find the card ranks that have at least three of a kind
        threes = [v[0] for v in value_count.items() if v[1] >= 3]
        threes.sort()
        # Find the card ranks that have at least a pair
        twos = [v[0] for v in value_count.items() if v[1] >= 2]
        twos.sort()
        # Threes are dominant in full house, lets check that value first:
        for three in reversed(threes):
            for two in reversed(twos):
                if two != three:
                    return HandType.FULL_HOUSE, (three, two)

    @staticmethod
    def check_flush(cards):
        """
        Static method to check if there is a flush

        :param cards: List of cards

        :return: HandType and list of the considered cards in descending order
        """
        suits = [c.suit for c in cards]
        # Find suit if suit is found at least 5 times
        flush_check = ([item for item, count in Counter(suits).items() if count >= 5])
        if flush_check:
            return HandType.FLUSH, cards[0:7]

    @staticmethod
    def check_straight(cards):
        """
        Static method to check if there is a straight

        :param cards: List of cards

        :return: HandType and list of the considered cards in descending order
        """
        vals = [c.get_value() for c in cards] \
               + [1 for c in cards if c.get_value() == 14]  # Add the aces!
        for c in reversed(cards):  # Starting point (high card)
            # Check if we have the value - k in the set of cards:
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k) not in vals:
                    found_straight = False
                    break
            if found_straight:
                return HandType.STRAIGHT, cards[0:7]

    @staticmethod
    def check_diff_pairs(cards):
        """
        Static method to check if there is a threes/two pair/pair or just a high card.

        :param cards: List of cards

        :return: HandType and list of either threes, two pair, pair and then with the considered cards in descending order
                 if HandType is High card the list that is returned contains only cards in descending order
        """
        value_count = Counter()
        for c in cards:
            value_count[c.get_value()] += 1
        # Find the card ranks that have at least three of a kind
        threes = [v[0] for v in value_count.items() if v[1] >= 3]
        threes.sort()
        # Find the card ranks that have at least a pair
        twos = [v[0] for v in value_count.items() if v[1] >= 2]
        twos.sort(reverse=True)     # Sort the pairs in descending order

        list_of_cards_twos = [twos, cards[0:7]]  # Creates list with the pair/pairs in the first index/indices and then the cards
        list_of_cards_threes = [threes, cards[0:7]] # Creates list with the threes in the first index and then the cards

        if threes:
            return HandType.THREE_OF_A_KIND, list_of_cards_threes
        if twos:
            if len(twos) == 2:
                return HandType.TWO_PAIRS, list_of_cards_twos
            elif len(twos) == 1:
                return HandType.PAIR, list_of_cards_twos
        return HandType.HIGH_CARD, cards[0:7]

    def __repr__(self):
        """
        Overloads the __repr__ to print the type of the hand and the cards

        """
        return f"{self.type, self.values}"

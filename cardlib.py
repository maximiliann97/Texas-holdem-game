from enum import Enum
from abc import ABC, abstractmethod
from random import shuffle
from collections import Counter


class Suit(Enum):
    Hearts = 3
    Spades = 2
    Clubs = 1
    Diamonds = 0

    def __str__(self):
        return self.name


class PlayingCard(ABC):
    def __init__(self, suit: Suit):
        self.suit = suit

    @abstractmethod
    def get_value(self):
        pass

    def __eq__(self, other):
        return self.get_value() == other.get_value()

    def __lt__(self, other):
        return self.get_value() < other.get_value()

    def __repr__(self):
        return f"{self.suit} of {self.get_value()}"


class NumberedCard(PlayingCard):
    def __init__(self, value, suit):
        self.value = value
        super().__init__(suit)

    def get_value(self):
        return self.value


class JackCard(PlayingCard):

    def get_value(self):
        return 11


class QueenCard(PlayingCard):

    def get_value(self):
        return 12


class KingCard(PlayingCard):

    def get_value(self):
        return 13


class AceCard(PlayingCard):

    def get_value(self):
        return 14


class StandardDeck:
    def __init__(self):
        self.cards = []

        for suit in Suit:
            self.cards.append(AceCard(suit))
            self.cards.append(KingCard(suit))
            self.cards.append(QueenCard(suit))
            self.cards.append(JackCard(suit))
            for value in range(2, 11):
                self.cards.append(NumberedCard(value, suit))

    def __iter__(self):
        return iter(self.cards)

    def shuffle(self):
        shuffle(self.cards)

    def draw(self):
        return self.cards.pop(0)


class Hand:
    def __init__(self, cards=None):
        if cards is None:
            self.cards = []  # We almost always want to initialise variables.
        else:
            self.cards = cards

    def add_card(self, card):
        self.cards.append(card)  # ska man inte ha en if sats, tänker man kan väl inte ha två av samma kort

    def drop_cards(self, indices):
        for index in sorted(indices, reverse=True):
            del self.cards[index]

    def sort(self):
        return self.cards.sort()

    def best_poker_hand(self, cards):
        return PokerHand(self.cards + cards)


class HandType(Enum):

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
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value


class PokerHand:
    def __init__(self, cards: list):
        self.cards = cards.sort(reverse=True)
        checkers = [self.check_straight_flush(cards), self.check_four_of_a_kind(cards), self.check_full_house(cards),
                    self.check_flush(cards), self.check_straight(cards), self.check_diff_pairs(cards)]

        for checker in checkers:
            v = checker
            if v is not None:
                self.type = v
                break

    def __lt__(self, other):
        return self.type < other.type

    def __eq__(self, other):
        return self.type == other.type

    @staticmethod
    def check_straight_flush(cards):
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
        suits = [c.suit for c in cards]
        values = [(c.get_value(), c.suit) for c in cards]
        # Find suit if suit is found at least 5 times
        flush_check = ([item for item, count in Counter(suits).items() if count >= 5])
        if flush_check:
            return HandType.FLUSH, cards[0:7]




        # for c in reversed(cards):
        #     if c.suit != cards[0].suit:
        #         break
        #     else:
        #         return HandType.FLUSH, cards[0:7]

    @staticmethod
    def check_straight(cards):
        vals = [c.get_value() for c in cards] \
               + [1 for c in cards if c.get_value() == 14]  # Add the aces!
        for c in reversed(cards):  # Starting point (high card)
            # Check if we have the value - k in the set of cards:
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k, c.suit) not in vals:
                    found_straight = False
                    break
            if found_straight:
                return HandType.STRAIGHT, cards[0:7]

    @staticmethod
    def check_diff_pairs(cards):
        value_count = Counter()
        for c in cards:
            value_count[c.get_value()] += 1
        # Find the card ranks that have at least three of a kind
        threes = [v[0] for v in value_count.items() if v[1] >= 3]
        threes.sort()
        # Find the card ranks that have at least a pair
        twos = [v[0] for v in value_count.items() if v[1] >= 2]
        twos.sort(reverse=True)

        list_of_cards_twos = [twos, cards[0:7]]
        list_of_cards_threes = [threes, cards[0:7]]

        if threes:
            return HandType.THREE_OF_A_KIND, list_of_cards_threes
        if twos:
            if len(twos) == 2:
                return HandType.TWO_PAIRS, list_of_cards_twos
            elif len(twos) == 1:
                return HandType.PAIR, list_of_cards_twos
        return HandType.HIGH_CARD, cards[0:7]

    def __repr__(self):
        return f'{self.type}'



h1 = Hand()
h1.add_card(JackCard(Suit.Clubs))
h1.add_card(QueenCard(Suit.Clubs))

cards_on_table = [NumberedCard(4, Suit.Clubs), NumberedCard(5, Suit.Clubs), NumberedCard(6, Suit.Clubs),
                  AceCard(Suit.Hearts), KingCard(Suit.Diamonds)]

poker_hand1 = h1.best_poker_hand(cards_on_table)
print(poker_hand1)
print(PokerHand.check_flush(cards_on_table))




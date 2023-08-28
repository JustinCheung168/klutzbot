import random
from enum import Enum


class Suit(str, Enum):
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"
    HEARTS = "Hearts"
    SPADES = "Spades"


class Rank(str, Enum):
    ACE = "Ace"
    TWO = "Two"
    THREE = "Three"
    FOUR = "Four"
    FIVE = "Five"
    SIX = "Six"
    SEVEN = "Seven"
    EIGHT = "Eight"
    NINE = "Nine"
    TEN = "Ten"
    JACK = "Jack"
    QUEEN = "Queen"
    KING = "King"


class ValueRule(Enum):
    STANDARD = "Standard"
    ACEHIGH = "Ace High"


class Pack(Enum):
    STANDARD_52 = "Standard 52-card pack"


class ValueLookup:
    DEFAULT_RANK_VALUES = {
        Rank.ACE: 1,
        Rank.TWO: 2,
        Rank.THREE: 3,
        Rank.FOUR: 4,
        Rank.FIVE: 5,
        Rank.SIX: 6,
        Rank.SEVEN: 7,
        Rank.EIGHT: 8,
        Rank.NINE: 9,
        Rank.TEN: 10,
        Rank.JACK: 11,
        Rank.QUEEN: 12,
        Rank.KING: 13,
    }

    def __init__(self, value_rule: ValueRule = ValueRule.STANDARD):
        self.value_rule = value_rule
        self.rank_values = self.DEFAULT_RANK_VALUES
        match value_rule:
            case ValueRule.STANDARD:
                pass
            case ValueRule.ACEHIGH:
                self.rank_values[Rank.ACE] = 14

    def rank_to_value(self, rank: Rank):
        return self.rank_values[rank]


class Card:
    def __init__(self, suit, rank, value: int | None = None, face_up: bool = True):
        """
        The value (numeric value of the card within the context of some game)
        would normally be set by a deck or game.
        """
        self.suit: Suit = suit
        self.rank: Rank = rank
        self.value: int = value
        self.face_up: bool = face_up

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.suit}, {self.rank}, value={self.value}, face_up={self.face_up})"

    def flip_up(self):
        if not self.face_up:
            self.face_up = True

    def flip_down(self):
        if self.face_up:
            self.face_up = False


class Deck:
    def __init__(
        self,
        initial: list[Card] | None = None,
        pack: Pack | None = None,
        shuffle: bool = True,
        seed: int | None = None,
        value_rule: ValueRule | None = ValueRule.STANDARD,
    ):
        """
        A deck of cards (ordered set of cards).

        Initializes with no cards by default.
        Initialize to a certain list of cards using initial.
        Initialize to a standard deck of 52 cards using pack
        """
        if initial is None:
            self._deck: list[Card] = []  # Internal deck; avoid accessing directly
        else:
            self._deck = initial

        if pack == Pack.STANDARD_52:
            self._insert_standard_52()

        if shuffle:
            self.shuffle(seed)

        self.value_rule = value_rule
        if self.value_rule is not None:
            self.value_lookup = ValueLookup(value_rule)
            self._assign_values()

    def __len__(self):
        return len(self._deck)

    def __str__(self):
        if len(self) == 0:
            deck_str = "Empty Deck"
        else:
            deck_str = f"Deck of {len(self)} cards:\n"
            for card in self._deck:
                deck_str += str(card) + "\n"
        return deck_str

    def _insert_standard_52(self) -> None:
        # Put one of every card into the deck face-down.
        for suit in list(Suit):
            for rank in list(Rank):
                self._deck.append(Card(suit, rank, face_up=False))

    def _assign_values(self) -> None:
        """Assign values to every card in this deck."""
        for card in self._deck:
            card.value = self.value_lookup.rank_to_value(card.rank)

    def shuffle(self, seed: int | None = None) -> None:
        """Perfectly shuffle this deck."""
        if seed is not None:
            random.seed(seed)
        random.shuffle(self._deck)

    def view(self, position: int = 0) -> Card:
        """View card at a certain position without taking it from the deck."""
        return self._deck[position]

    def draw_card(self, position: int = 0) -> Card:
        """
        Draw card at given position without putting it back.
        """
        drawn_card = self._deck[position]
        self._deck.pop(position)
        return drawn_card

    def draw_cards(self, n: int, position: int = 0) -> list[Card]:
        """
        Draw n cards starting from given position and going towards the back
            without returning them to the deck.

        Defaults to drawing from the top of the deck (position 0) going towards the back.
        Negative indexing is valid as an input for position;
            the -1 case represents drawing from the back of the deck towards the front.
        """
        drawn_cards = []
        for _ in range(n):
            drawn_card = self.draw_card(position)
            drawn_cards.append(drawn_card)
        return drawn_cards

    def draw_cards_from_back(self, n: int) -> list[int]:
        return self.draw_cards(n, -1)

    def find(self, suit: Suit, rank: Rank) -> int | None:
        """
        Find the position of the first card in the deck with the given suit and rank.
        If the card cannot be found, return None.
        """
        for i in range(len(self._deck)):
            card = self.view(i)
            if (card.suit == suit) and (card.rank == rank):
                return i
        return None

    def sort(self):
        """
        Sort by suit then value.

        Suit is sorted by alphabetical order as is traditionally done.
        """
        self._deck = sorted(self._deck, key=lambda x: (x.suit, x.value))

    def add_card(self, card: Card, position: int = 0):
        """
        Add a card to the deck.

        By default, the card is added to the top of the deck.
        The card can be added to the bottom of the deck with position = -1.
        """
        if position == -1:
            self._deck.append(card)
        else:
            self._deck.insert(position, card)

    def add_cards(self, cards: list[Card], position: int = 0):
        """
        Add cards to the deck so that they are in the same order as in the original list.

        By default, the card is added to the top of the deck.
        The card can be added to the bottom of the deck with position = -1.
        """

        for card in cards.copy().reverse():
            if position == -1:
                self._deck.append(card)
            else:
                self._deck.insert(position, card)


class Player:
    """A person who can own cards and/or participate in a game."""

    def __init__(self, name: str, hand: Deck, points: int = 0):
        self.name = name
        self.hand = hand
        self.points = points

    def prompt(self, history):
        """Request a prompt from this player and return their sanitized response."""
        pass


class AIState:
    """
    An AIPlayer's internal memory of its own strategy that should be updated each turn.
    This is not the history of what actions have been taken.
    """

    def __init__(self):
        # Locations of
        self.card_location_estimates: dict[Card, dict[Player, float]] = {}


class AIPlayer(Player):
    """A player who takes actions via automated response instead of by human input."""

    def __init__(self, name: str, hand: Deck, points: int = 0):
        super().__init__(name, hand, points)
        self.state: AIState = AIState()

    def prompt(self, history):
        """Run an automatic response."""
        raise NotImplementedError("Must override")


class Crazy8sAIPlayer(Player):
    """An AI player using a strategy for Crazy Eights."""

    def prompt(self, game_state):
        pass


class TurnActivity:
    """New information that has occurred in the most recent turn of a game."""


class Game:
    def play(self):
        pass


if __name__ == "__main__":
    a = Deck(pack=Pack.STANDARD_52)
    print(str(a))

    print(a)
    a.sort()
    print(a)

# Ungrateful - a 52 (or 54 if you want Jokers) card deck emulator by Trevor DeCamp. Heavily modified (probably for the better) for NET 202
# To ensure true randomness, every action taken on class Deck will seed the randomizer.

import random
from os.path import join

class Card:
    def __init__(self, givenSuit = "Spades", givenValue = "Ace"):
        '''Create a Card, default card with no args is the Ace of Spades'''
        self.suit = givenSuit
        self.value = givenValue
        if givenSuit != "Joker":
            if isinstance(givenValue, int):
                self.sprite = join("assets", "card" + givenSuit + str(givenValue) + ".png")
            else: 
                self.sprite = join("assets", "card" + givenSuit + givenValue[:1] + ".png")
        else: 
            self.sprite = join("assets", "cardJoker.png")

    def toString(self):
        '''Will return a string in the format of Value/Face of Suit'''
        if self.suit != 'Joker':
            return str(self.value) + " of " + self.suit
        else: return self.suit

    def getSuit(self):
        '''Returns Suit'''
        return self.suit

    def getSuitInt(self):
        '''Integer only return; 1 for Diamonds, 2 for Hearts 3 for Clubs, 4 for Spades'''
        if(self.suit == "Diamonds"):
            return 1
        elif(self.suit == "Hearts"):
            return 2
        elif(self.suit == "Clubs"):
            return 3
        elif(self.suit == "Spades"):
            return 4

    def setSuit(self, givenSuit):
        '''Overwrite Suit, and returns False if not a valid arg'''
        if(givenSuit in ["Diamonds", "Hearts", "Clubs", "Spades"]):
            self.suit = givenSuit
        else : return False
    
    def setSuitInt(self, givenSuitInt):
        '''Overwrite Suit with an int; 1 for Diamonds, 2 for Hearts 3 for Clubs, 4 for Spades, and returns False if not a valid arg'''
        if(givenSuitInt == 1):
            self.suit = "Diamonds"
        elif(givenSuitInt == 2):
            self.suit = "Hearts"
        elif(givenSuitInt == 3):
            self.suit = "Clubs"
        elif(givenSuitInt == 4):
            self.suit = "Spades"
        else: return False

    def getValue(self):
        '''Returns Value; Volaltile, can return int or str (if a face card)'''
        return self.value

    def getValueInt(self):
        '''Integer only return; for the Face cards Aces = 1, Jacks = 11, Queens = 12, Kings = 13, Jokers = 0'''
        if(self.value == "Joker"):
            return 1
        elif(self.value == "Jack"):
            return 11
        elif(self.value == "Queen"):
            return 12
        elif(self.value == "King"):
            return 13
        elif(self.value == "Ace"):
            return 14
        else: return self.value

    def setValue(self, givenValue):
        '''Overwrite Value, and returns False if not a valid arg'''
        if(givenValue in ["Joker", "Ace", "Jack", "Queen", "King"] or (givenValue >= 2 and givenValue <= 10)):
            self.value = givenValue
        else : return False

    def setValueInt(self, givenValueInt):
        '''Overwrite Value with an int only; For the Face cards 1 for Ace, 11 for Jack, 12 for Queen, 13 for King, Jokers = 0, and returns False if not a valid arg'''
        if(givenValueInt == 0):
            self.value = "Joker"
        elif(givenValueInt == 11):
            self.value = "Jack"
        elif(givenValueInt == 12):
            self.value = "Queen"
        elif(givenValueInt == 13):
            self.value = "King"
        elif(givenValueInt == 14):
            self.value = "Ace"
        elif(givenValueInt >= 2 and givenValueInt <= 10):
            self.value = givenValueInt
        else : return False

    def isEqualTo(self, givenCard):
        '''Comparator Function'''
        try:
            if(self.suit == givenCard.suit and self.value == givenCard.value):
                return True
            else: return False
        except: return False

    def image(self):
        return self.sprite


class Deck:
    def __init__(self, jokerBool=False):
        '''Deck is generated and shuffled. Cards cannot be taken out of play or added to play once the deck is made. Add True as an arg for Jokers.'''
        random.seed()
        # This is absolutely disgusting but we'll live...
        self.cards = [Card('Hearts', 'Ace'),
                      Card('Hearts', 2),
                      Card('Hearts', 3),
                      Card('Hearts', 4),
                      Card('Hearts', 5),
                      Card('Hearts', 6),
                      Card('Hearts', 7),
                      Card('Hearts', 8),
                      Card('Hearts', 9),
                      Card('Hearts', 10),
                      Card('Hearts', 'Jack'),
                      Card('Hearts', 'Queen'),
                      Card('Hearts', 'King'),
                      Card('Clubs', 'Ace'),
                      Card('Clubs', 2),
                      Card('Clubs', 3),
                      Card('Clubs', 4),
                      Card('Clubs', 5),
                      Card('Clubs', 6),
                      Card('Clubs', 7),
                      Card('Clubs', 8),
                      Card('Clubs', 9),
                      Card('Clubs', 10),
                      Card('Clubs', 'Jack'),
                      Card('Clubs', 'Queen'),
                      Card('Clubs', 'King'),
                      Card('Diamonds', 'Ace'),
                      Card('Diamonds', 2),
                      Card('Diamonds', 3),
                      Card('Diamonds', 4),
                      Card('Diamonds', 5),
                      Card('Diamonds', 6),
                      Card('Diamonds', 7),
                      Card('Diamonds', 8),
                      Card('Diamonds', 9),
                      Card('Diamonds', 10),
                      Card('Diamonds', 'Jack'),
                      Card('Diamonds', 'Queen'),
                      Card('Diamonds', 'King'),
                      Card('Spades', 'Ace'),
                      Card('Spades', 2),
                      Card('Spades', 3),
                      Card('Spades', 4),
                      Card('Spades', 5),
                      Card('Spades', 6),
                      Card('Spades', 7),
                      Card('Spades', 8),
                      Card('Spades', 9),
                      Card('Spades', 10),
                      Card('Spades', 'Jack'),
                      Card('Spades', 'Queen'),
                      Card('Spades', 'King')
                      ]
        if(jokerBool):
            self.cards.append(Card('Joker', 'Joker'))
            self.cards.append(Card('Joker', 'Joker'))
        self.discard = []
        self.shuffle()

    def draw(self):
        '''Returns a card, adds it to the discard pile, and returns False if the deck is empty'''
        random.seed()
        if len(self.cards) != 0:
            chosen = self.cards.pop(0)
            self.discard.append(chosen)
            return chosen
        else:
            return None

    def shuffle(self):
        '''Shuffles the deck and discard pile back together.'''
        random.seed()
        self.cards = self.cards + self.discard
        self.discard = []
        random.shuffle(self.cards)

    def length(self):
        return len(self.cards)
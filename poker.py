from cards import Deck

class pokerState():
    def __init__(self):
        # 0 - Pre Game (Betting State)
        # 1 - After the First Deal
        # 2 - After the Second Deal (Results)
        self.STATE = 0
        self.CREDITS = 100
        self.BET = 0
        self.BET_MAX = 5
        self.DECK = Deck()
        self.HAND = [None, None, None, None, None]
        self.HOLDS = [False, False, False, False, False]

state = pokerState()
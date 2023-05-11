from tkinter import *
from tkinter.messagebox import askyesnocancel, showinfo
from PIL import ImageTk, Image
from playsound import playsound
from os.path import join
from collections import Counter
from io import BytesIO
import pickle

import poker, cards

window = Tk()

# REUSED ASSET FILEPATHS
DEFAULT_IMAGE = ImageTk.PhotoImage(Image.open(join("assets","cardBack_blue2.png")))
BET_SFX = join('assets','smw_coin.wav')
BET_MAX_SFX = join("assets","smw_dragon_coin.wav")
DRAW_SFX = join("assets","smw_stomp.wav")
WIN_SFX = join("assets","smw_1-up.wav")
LOSE_SFX = join("assets","smw_stomp_koopa_kid.wav")

# TK FORM
window.iconbitmap(join("assets","favicon.ico"))
window.title("Python Video Poker") 
window.resizable(False, False)

menubar = Menu(window)
window.config(menu=menubar)
file_menu = Menu(menubar, tearoff=False)
help_menu = Menu(menubar, tearoff=False)    
menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Help", menu=help_menu)

panel1 = Label(window, image = DEFAULT_IMAGE, borderwidth=3, relief="raised")
panel1.grid(row=0,column=0)
panel2 = Label(window, image = DEFAULT_IMAGE, borderwidth=3, relief="raised")
panel2.grid(row=0,column=1)
panel3 = Label(window, image = DEFAULT_IMAGE, borderwidth=3, relief="raised")
panel3.grid(row=0,column=2)
panel4 = Label(window, image = DEFAULT_IMAGE, borderwidth=3, relief="raised")
panel4.grid(row=0,column=3)
panel5 = Label(window, image = DEFAULT_IMAGE, borderwidth=3, relief="raised")
panel5.grid(row=0,column=4)

lblBet = Label(window, text="BET: 0")
lblBet.grid(row=1,column=0,sticky=W)
lblCredits = Label(window, text="CREDITS: 0")
lblCredits.grid(row=1,column=4,sticky=E)

btnBetOne = Button(window, text="Bet\nOne")
btnBetOne.grid(row=2, column=0, sticky=W)
btnBetMax = Button(window, text="Bet\nMax")
btnBetMax.grid(row=2, column=0, padx=35, sticky=W)
lblResults = Label(window, text = "")
lblResults.grid(row=2, column=1, columnspan=3)
btnDeal = Button(window, text="Deal\n")
btnDeal.grid(row=2, column=4, sticky=E)

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Only allow poker and card modules, nothing else
        if module == "poker":
            return getattr(poker, name)
        elif module == "cards":
            return getattr(cards, name)
        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                     (module, name))
                                
def pickle_restrictedLoads(s):
    return RestrictedUnpickler(BytesIO(s.read())).load()

def deal():
    if poker.state.STATE == 0 or poker.state.STATE == 2:
        if poker.state.BET > 0:
            # First Deal
            lblResults.config(text="")
            poker.state.HOLDS = [False, False, False, False, False]
            poker.state.HAND = [None, None, None, None, None]
            if poker.state.DECK.length() < 10:
                poker.state.DECK.shuffle()
            for x in range(len(poker.state.HAND)):
                poker.state.HAND[x] = poker.state.DECK.draw()
            drawImages()
            playsound(DRAW_SFX, False)
            poker.state.STATE = 1
        else:
            lblResults.config(text="You must place a bet before dealing...")
    elif poker.state.STATE == 1:
        # Second Deal
        for x in range(len(poker.state.HAND)):
            if not poker.state.HOLDS[x]:
                poker.state.HAND[x] = poker.state.DECK.draw()
        drawImages()
        determineWin()
        poker.state.BET = 0
        poker.state.STATE = 2
        updateHUD()
        
def betOne():
    if poker.state.STATE == 2:
        resetImages()
        lblResults.config(text="")
        poker.state.STATE = 0
    if poker.state.STATE == 0:
        if poker.state.CREDITS >= 1:
            poker.state.BET += 1
            if poker.state.BET > poker.state.BET_MAX:
                poker.state.BET = poker.state.BET_MAX
            else:
                poker.state.CREDITS -= 1
            playsound(BET_SFX, False)
            updateHUD()
        else:
            lblResults.config(text="Out of credits. Game Over.")

def betMax():
    if poker.state.STATE == 2:
        resetImages()
        lblResults.config(text="")
        poker.state.STATE = 0
    if poker.state.STATE == 0:
        temp = poker.state.BET_MAX - poker.state.BET
        if poker.state.CREDITS >= temp:
            poker.state.BET += temp
            poker.state.CREDITS -= temp
            playsound(BET_MAX_SFX, False)
            updateHUD()
        else:
            lblResults.config(text="You cannot take the Max Bet.")

def hold(x):
    if poker.state.STATE == 1:
        if x == 1:
            if not poker.state.HOLDS[0]:
                panel1.config(relief="sunken")
                poker.state.HOLDS[0] = True
            else:
                panel1.config(relief="raised")
                poker.state.HOLDS[0] = False
        elif x == 2:
            if not poker.state.HOLDS[1]:
                panel2.config(relief="sunken")
                poker.state.HOLDS[1] = True
            else:
                panel2.config(relief="raised")
                poker.state.HOLDS[1] = False
        elif x == 3:
            if not poker.state.HOLDS[2]:
                panel3.config(relief="sunken")
                poker.state.HOLDS[2] = True
            else:
                panel3.config(relief="raised")
                poker.state.HOLDS[2] = False
        elif x == 4:
            if not poker.state.HOLDS[3]:
                panel4.config(relief="sunken")
                poker.state.HOLDS[3] = True
            else:
                panel4.config(relief="raised")
                poker.state.HOLDS[3] = False
        elif x == 5:
            if not poker.state.HOLDS[4]:
                panel5.config(relief="sunken")
                poker.state.HOLDS[4] = True
            else:
                panel5.config(relief="raised")
                poker.state.HOLDS[4] = False

def determineWin():
    # Gather intel about our hand
    vals = [x.getValueInt() for x in poker.state.HAND]
    Cv = Counter(vals)
    Cs = Counter([x.getSuit() for x in poker.state.HAND])
    unique = list(Cv)
    straight = max(vals) - min(vals) + 1
    four = [x for x in Cv if Cv[x]==4]
    three = [x for x in Cv if Cv[x]==3]
    twos = [x for x in Cv if Cv[x]==2]
    flush = [x for x in Cs if Cs[x]==5]
    # Determine Win Condition and Pay Out
    # Royal Flush x800
    if straight == len(vals) and len(unique) == len(vals) and flush and max(vals) == 14:
        playsound(WIN_SFX, False)
        lblResults.config(text="Royal Flush.")
        poker.state.CREDITS += poker.state.BET * 250
        return 0
    # Straight Flush x50
    if straight == len(vals) and len(unique) == len(vals) and flush:
        playsound(WIN_SFX, False)
        lblResults.config(text="Straight Flush.")
        poker.state.CREDITS += poker.state.BET * 50
        return 0
    # Four of a Kind x25
    if four:
        playsound(WIN_SFX, False)
        lblResults.config(text="Four of a Kind.")
        poker.state.CREDITS += poker.state.BET * 25
        return 0
    # Full House x9
    if twos and three:
        playsound(WIN_SFX, False)
        lblResults.config(text="Full House.")
        poker.state.CREDITS += poker.state.BET * 9
        return 0
    # Flush x6
    if flush:
        playsound(WIN_SFX, False)
        lblResults.config(text="Flush.")
        poker.state.CREDITS += poker.state.BET * 6
        return 0
    # Straight x4
    if straight == len(vals) and len(unique) == len(vals):
        playsound(WIN_SFX, False)
        lblResults.config(text="Straight.")
        poker.state.CREDITS += poker.state.BET * 4
        return 0
    # Three of a Kind x3
    if three:
        playsound(WIN_SFX, False)
        lblResults.config(text="Three of a Kind.")
        poker.state.CREDITS += poker.state.BET * 3
        return 0
    # Two Pair x2
    if len(twos) == 2:
        playsound(WIN_SFX, False)
        lblResults.config(text="Two Pair.")
        poker.state.CREDITS += poker.state.BET * 2
        return 0
    # Pair of Jacks or Better x1
    if len(twos) == 1 and twos[0] > 10:
        playsound(WIN_SFX, False)
        lblResults.config(text="Pair of Jacks or Better.")
        poker.state.CREDITS += poker.state.BET * 1
        return 0
    # Else
    playsound(LOSE_SFX, False)
    lblResults.config(text="Miss.")
    return 0  

def resetImages():
    panel1.config(image = DEFAULT_IMAGE, relief="raised")
    panel1.image = DEFAULT_IMAGE
    panel2.config(image = DEFAULT_IMAGE, relief="raised")
    panel2.image = DEFAULT_IMAGE
    panel3.config(image = DEFAULT_IMAGE, relief="raised")
    panel3.image = DEFAULT_IMAGE
    panel4.config(image = DEFAULT_IMAGE, relief="raised")
    panel4.image = DEFAULT_IMAGE
    panel5.config(image = DEFAULT_IMAGE, relief="raised")
    panel5.image = DEFAULT_IMAGE

def drawImages():
    with Image.open(poker.state.HAND[0].image()) as img:
        card1 = ImageTk.PhotoImage(img)
        panel1.config(image = card1, relief="raised")
        panel1.image = card1
    with Image.open(poker.state.HAND[1].image()) as img:
        card2 = ImageTk.PhotoImage(img)
        panel2.config(image = card2, relief="raised")
        panel2.image = card2
    with Image.open(poker.state.HAND[2].image()) as img:
        card3 = ImageTk.PhotoImage(img)
        panel3.config(image = card3, relief="raised")
        panel3.image = card3
    with Image.open(poker.state.HAND[3].image()) as img:
        card4 = ImageTk.PhotoImage(img)
        panel4.config(image = card4, relief="raised")
        panel4.image = card4
    with Image.open(poker.state.HAND[4].image()) as img:
        card5 = ImageTk.PhotoImage(img)
        panel5.config(image = card5, relief="raised")
        panel5.image = card5

def updateHUD():
    lblBet.config(text="BET: %s" % poker.state.BET)
    lblCredits.config(text="CREDITS: %s" % poker.state.CREDITS)

def resetGame():
    poker.state = poker.pokerState()
    updateHUD()
    resetImages()

def saveGame():
    with open('save.bin', 'wb') as fw:
        pickle.dump(poker.state, fw, pickle.HIGHEST_PROTOCOL)
        lblResults.config(text="Game Saved")

def loadGame(): 
    try:
        temp = poker.state
        del poker.state
        with open('save.bin', 'rb') as fr:
            #poker.state = pickle.loads(fr)
            poker.state = pickle_restrictedLoads(fr)
        if poker.state.STATE != 0:
            poker.state.STATE = 0
        if poker.state.BET > 0:
            poker.state.CREDITS += poker.state.BET
            poker.state.BET = 0
        resetImages()
        updateHUD()
        lblResults.config(text="Game Loaded")
    except Exception as e: 
        poker.state = temp
        lblResults.config(text="Load Failed: %s" % e)
    finally:
        del temp

def about():
    showinfo("About Python Video Poker", "\
Python Video Poker\n\
---------------------------\n\
Video Poker written in Python using Tkinter.\n\
Simulates Video Poker with a single deck of cards that is automatically shuffled as you go.\n\
cards.py is a bit more verbose than it needs to be as it was originally written in 2016.\n\
Cross Platform, should run just fine on any OS that can run Python.\n\n\
Credits\n\
---------------\n\
Programmed by Me (TheDerpySage), 2023.\n\
Card Sprites by [Kenney](https://www.kenney.nl/), 2015.\n\
SFX from Super Mario World. Super Nintendo version, Nintendo, 1990.\
    ")

def howToPlay():
    showinfo("How To Play Python Video Poker", "\
Python Video Poker\n\
---------------------------\n\
A game of 5 Card Drop with Betting.\n\
Try to make the best poker hand by drawing 5, selecting any cards you wish to keep, and redrawing the rest.\n\
Payouts are as follows...\n\
Royal Flush\tx250\n\
Straight Flush\tx50\n\
Four of a Kind\tx25\n\
Full House\tx9\n\
Flush\t\tx6\n\
Straight\t\tx4\n\
Three of a Kind\tx3\n\
Two Pair\t\tx2\n\
Pair Jacks or +\tx1\
    ")

def end():
    res = askyesnocancel('Quitting', 'Would you like to save first?')
    if res == True: 
        saveGame()
        window.destroy()
    elif res == False:
        window.destroy()

def main(): 
    # BIND FUNCTIONS
    panel1.bind("<Button-1>",lambda e,x=1:hold(x))
    panel2.bind("<Button-1>",lambda e,x=2:hold(x))
    panel3.bind("<Button-1>",lambda e,x=3:hold(x))
    panel4.bind("<Button-1>",lambda e,x=4:hold(x))
    panel5.bind("<Button-1>",lambda e,x=5:hold(x))
    btnDeal.config(command=deal)
    btnBetOne.config(command=betOne)
    btnBetMax.config(command=betMax)
    file_menu.add_command(label='Save', command=saveGame)
    file_menu.add_command(label='Load', command=loadGame)
    file_menu.add_command(label="Reset", command=resetGame)
    file_menu.add_command(label='Quit', command=end)
    help_menu.add_command(label='How To Play', command=howToPlay)
    help_menu.add_command(label='About', command=about)
    window.protocol('WM_DELETE_WINDOW', end)
    # START
    updateHUD()
    window.mainloop()

if __name__ == "__main__":
    main()
from datetime import datetime
from tkinter import ttk
import tkinter as tk
from db import DBController
import locale as lc
from object import Deck, Hand, Session
from decimal import Decimal


class Gui(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent
        lc.setlocale(lc.LC_ALL, "")
        self.dbController = DBController()
        self.playing = False
        self.playerAction = False
        self.session = Session()

        # Define string variables for text entry fields
        self.money = tk.StringVar(value=self.dbController.get_last_session())
        self.bet = tk.StringVar()
        self.dealerCards = tk.StringVar()
        self.dealerPoints = tk.StringVar()
        self.playerCards = tk.StringVar()
        self.playerPoints = tk.StringVar()
        self.result = tk.StringVar()

        self.init_components()

    def init_components(self):
        self.pack()
        ttk.Label(self, text="Money:").grid(
            column=0, row=0, sticky=tk.E)
        ttk.Entry(self, width=60, textvariable=self.money, state="readonly").grid(
            column=1, row=0)
        ttk.Label(self, text="Bet:").grid(
            column=0, row=1, sticky=tk.E)
        ttk.Entry(self, width=60, textvariable=self.bet).grid(
            column=1, row=1)
        ttk.Label(self, text="DEALER").grid(
            column=0, row=2, sticky=tk.E)
        ttk.Label(self, text="Cards:").grid(
            column=0, row=3, sticky=tk.E)
        ttk.Entry(self, width=60, textvariable=self.dealerCards, state="readonly",).grid(
            column=1, row=3)
        ttk.Label(self, text="Points:").grid(
            column=0, row=4, sticky=tk.E)
        ttk.Entry(self, width=60, textvariable=self.dealerPoints, state="readonly").grid(
            column=1, row=4)
        ttk.Label(self, text="YOU").grid(
            column=0, row=5, sticky=tk.E)
        ttk.Label(self, text="Cards:").grid(
            column=0, row=6, sticky=tk.E)
        ttk.Entry(self, width=60, textvariable=self.playerCards, state="readonly").grid(
            column=1, row=6)
        ttk.Label(self, text="Points:").grid(
            column=0, row=7, sticky=tk.E)
        ttk.Entry(self, width=60, textvariable=self.playerPoints, state="readonly").grid(
            column=1, row=7)
        playActionFrame = ttk.Frame(self)
        playActionFrame.grid(column=0, row=8, columnspan=2, sticky=tk.E)
        ttk.Button(playActionFrame, text="Hit",
                   command=self.hit_action).grid(column=0, row=0, padx=5)
        ttk.Button(playActionFrame, text="Stand",
                   command=self.stand_action).grid(column=1, row=0)
        ttk.Label(self, text="Result:").grid(
            column=0, row=9, sticky=tk.E)
        ttk.Entry(self, width=60, textvariable=self.result, state="readonly").grid(
            column=1, row=9)
        mainActionsFrame = ttk.Frame(self)
        mainActionsFrame.grid(column=0, row=10, columnspan=2, sticky=tk.E)
        ttk.Button(mainActionsFrame, text="Play",
                   command=self.play_action).grid(column=0, row=0, padx=5)
        ttk.Button(mainActionsFrame, text="Exit",
                   command=self.parent.destroy).grid(column=1, row=0)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

    def play_action(self):
        if not self.playing:
            if self.bet.get() == '':
                self.result.set("You must place a valid bet to play.")
            else:
                try:
                    bet = Decimal(self.bet.get())
                    if(bet < 5):
                        self.result.set("Bet amount can't be less than 5.")
                    elif bet > Decimal(self.money.get()):
                        self.result.set(
                            f"You have only {lc.currency(Decimal(self.money.get()), grouping=True)} can't bet more.")
                    else:
                        self.result.set("")
                        self.playerHand = Hand()
                        self.dealerHand = Hand()
                        self.stepsCount = 1
                        self.playerCards.set("")
                        self.playerPoints.set("")
                        self.dealerCards.set("")
                        self.dealerPoints.set("")
                        self.playing = True
                        self.playerAction = True
                        self.session.set_start_time(datetime.now())
                        self.deck = Deck()
                        self.deck.shuffle()
                        self.playerHand.add_card(self.deck.deal())
                        self.playerHand.add_card(self.deck.deal())
                        self.playerHand.adjust_for_ace()
                        self.dealerHand.add_card(self.deck.deal())
                        self.dealerHand.add_card(self.deck.deal())
                        self.dealerHand.adjust_for_ace()

                        self.show_some_cards()
                except:
                    self.result.set("Please enter valid bet.")

    def show_some_cards(self):
        self.dealerCards.set(f"<card hidden>, {self.dealerHand.cards[1]}")
        self.dealerPoints.set(self.dealerHand.cards[1].value)
        self.playerCards.set(', '.join(map(str, self.playerHand.cards)))
        self.playerPoints.set(self.playerHand.value)

    def show_all_cards(self):
        self.dealerCards.set(', '.join(map(str, self.dealerHand.cards)))
        self.playerCards.set(', '.join(map(str, self.playerHand.cards)))
        self.playerPoints.set(self.playerHand.value)
        self.dealerPoints.set(self.dealerHand.value)

    def hit_action(self):
        if self.playerAction:
            self.stepsCount += 1
            self.playerHand.add_card(self.deck.deal())
            self.playerHand.adjust_for_ace()
            self.show_some_cards()
            self.check_value()

    def stand_action(self):
        if self.playerAction:
            self.playerAction = False
            while self.dealerHand.value < 17:
                self.dealerHand.add_card(self.deck.deal())
                self.dealerHand.adjust_for_ace()
            self.check_value()

    def check_value(self):
        if self.stepsCount == 1 and self.playerHand.value == 21:
            self.end_game("blackjack", "Player is blackjack")
        elif self.stepsCount != 1 and self.playerHand.value == 21:
            self.end_game("win", "Player win")
        elif self.playerHand.value > 21:
            self.end_game("lose", "Player bust")
        elif self.dealerHand.value > 21:
            self.end_game("win", "Dealer bust")
        elif self.playerHand.value == self.dealerHand.value and self.playerAction == False:
            self.end_game("draw", "Its a push! Player and Dealer tie!")
        elif self.playerAction == False and self.dealerHand.value < self.playerHand.value:
            self.end_game("win", "Player win")
        elif self.playerAction == False and self.dealerHand.value > self.playerHand.value:
            self.end_game("lose", "Dealer win")

    def end_game(self, type, message):
        self.playing = False
        self.playerAction = False
        self.result.set(message)
        self.show_all_cards()
        if(type == "blackjack"):
            money = Decimal(self.money.get())
            bet = Decimal(self.bet.get())
            self.money.set(bet + money + (bet/2))
        elif(type == "win"):
            self.money.set(Decimal(self.bet.get()) + Decimal(self.money.get()))
        elif(type == "lose"):
            self.money.set(Decimal(self.money.get())-Decimal(self.bet.get()))
        self.session.set_stop_money(self.money.get())
        self.dbController.add_session(self.session)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Assignment 4")
    Gui(root)
    root.mainloop()

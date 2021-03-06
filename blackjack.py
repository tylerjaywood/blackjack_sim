
# TODO
# hand.compute_score shouldn't fail on 0 cards in array

# get Game.win_lose to handle splits/multiple hands

# doesn't support PUSH well. need more robust handling of decisions
# see ln 15

# implement a payout method in Game

# figure out what happens when it's time to shuffle

# Move strategy-sets into separate class?
# Have a decision class for handling strategy sets? -- all the 
# game decision logic in Player is shitty

# move 'win counter' into player class and out of the test-game loop

# blackjacky.py
import random
import time

H = 'hit'
S = 'stand'
D = 'double'
Sp = 'split'

player_logic_soft_totals = {
    '21': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':S,'8':S,'9':S,'10':S,'1':S},
    '20': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':S,'8':S,'9':S,'10':S,'1':S},
    '19': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':S,'8':S,'9':S,'10':S,'1':S},
    '18': {'2':H,'3':D,'4':D,'5':D,'6':D,'7':H,'8':H,'9':H,'10':H,'1':H},
    '17': {'2':H,'3':D,'4':D,'5':D,'6':D,'7':H,'8':H,'9':H,'10':H,'1':H},
    '16': {'2':H,'3':H,'4':D,'5':D,'6':D,'7':H,'8':H,'9':H,'10':H,'1':H},
    '15': {'2':H,'3':H,'4':D,'5':D,'6':D,'7':H,'8':H,'9':H,'10':H,'1':H},
    '14': {'2':H,'3':H,'4':H,'5':D,'6':D,'7':H,'8':H,'9':H,'10':H,'1':H},
    '13': {'2':H,'3':H,'4':H,'5':H,'6':D,'7':H,'8':H,'9':H,'10':H,'1':H},
    '12': {'2':Sp,'3':Sp,'4':Sp,'5':Sp,'6':Sp,'7':Sp,'8':Sp,'9':Sp,'10':Sp,'1':Sp}
}
player_logic_split = {
    'A': {'2':Sp,'3':Sp,'4':Sp,'5':Sp,'6':Sp,'7':Sp,'8':Sp,'9':Sp,'10':Sp,'1':Sp}, 
    'K': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':S,'8':S,'9':S,'10':S,'1':S},
    'Q': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':S,'8':S,'9':S,'10':S,'1':S},
    'J': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':S,'8':S,'9':S,'10':S,'1':S},
    '10': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':S,'8':S,'9':S,'10':S,'1':S},
    '9': {'2':Sp,'3':Sp,'4':Sp,'5':Sp,'6':Sp,'7':H,'8':Sp,'9':Sp,'10':H,'1':H},
    '8': {'2':Sp,'3':Sp,'4':Sp,'5':Sp,'6':Sp,'7':Sp,'8':Sp,'9':Sp,'10':Sp,'1':Sp},
    '7': {'2':Sp,'3':Sp,'4':Sp,'5':Sp,'6':Sp,'7':Sp,'8':H,'9':H,'10':H,'1':H},
    '6': {'2':Sp,'3':Sp,'4':Sp,'5':Sp,'6':Sp,'7':H,'8':H,'9':H,'10':H,'1':H},
    '5': {'2':H,'3':H,'4':H,'5':H,'6':H,'7':H,'8':H,'9':H,'10':H,'1':H},
    '4': {'2':H,'3':H,'4':Sp,'5':Sp,'6':Sp,'7':H,'8':H,'9':H,'10':H,'1':H},
    '3': {'2':Sp,'3':Sp,'4':Sp,'5':Sp,'6':Sp,'7':Sp,'8':H,'9':H,'10':H,'1':H},
    '2': {'2':Sp,'3':Sp,'4':Sp,'5':Sp,'6':Sp,'7':Sp,'8':H,'9':H,'10':H,'1':H}
}
player_logic_hard_totals = {
    '21': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':S,'8':S,'9':S,'10':S,'1':S},
    '20': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':S,'8':S,'9':S,'10':S,'1':S},
    '19': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':S,'8':S,'9':S,'10':S,'1':S},
    '18': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':S,'8':S,'9':S,'10':S,'1':S},
    '17': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':S,'8':S,'9':S,'10':S,'1':S},
    '16': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':H,'8':H,'9':H,'10':H,'1':H},
    '15': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':H,'8':H,'9':H,'10':H,'1':H},
    '14': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':H,'8':H,'9':H,'10':H,'1':H},
    '13': {'2':S,'3':S,'4':S,'5':S,'6':S,'7':H,'8':H,'9':H,'10':H,'1':H},
    '12': {'2':H,'3':H,'4':S,'5':S,'6':S,'7':H,'8':H,'9':H,'10':H,'1':H},
    '11': {'2':D,'3':D,'4':D,'5':D,'6':D,'7':D,'8':D,'9':D,'10':D,'1':H},
    '10': {'2':D,'3':D,'4':D,'5':D,'6':D,'7':D,'8':D,'9':D,'10':H,'1':H},
    '9': {'2':H,'3':D,'4':D,'5':D,'6':D,'7':H,'8':H,'9':H,'10':H,'1':H},
    '8': {'2':H,'3':H,'4':H,'5':H,'6':H,'7':H,'8':H,'9':H,'10':H,'1':H},
    '7': {'2':H,'3':H,'4':H,'5':H,'6':H,'7':H,'8':H,'9':H,'10':H,'1':H},
    '6': {'2':H,'3':H,'4':H,'5':H,'6':H,'7':H,'8':H,'9':H,'10':H,'1':H},
    '5': {'2':H,'3':H,'4':H,'5':H,'6':H,'7':H,'8':H,'9':H,'10':H,'1':H},
    '4': {'2':H,'3':H,'4':H,'5':H,'6':H,'7':H,'8':H,'9':H,'10':H,'1':H},
    '3': {'2':H,'3':H,'4':H,'5':H,'6':H,'7':H,'8':H,'9':H,'10':H,'1':H},
    '2': {'2':H,'3':H,'4':H,'5':H,'6':H,'7':H,'8':H,'9':H,'10':H,'1':H}
}

CARD_VALS = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']

class Shoe:
    card_array = []
    def __init__(self, decks):
        self.decks = decks
        self.card_array = [Card(x) for x in (CARD_VALS * 4 * self.decks)]
        self.new_shoe = False
        self.cut_loc = 0
    
    def shuffle(self): random.shuffle(self.card_array)

    def deal_one(self, verbose = False): 
        card = self.card_array.pop()
        if card != 'CUT':
            return card
        else:
            self.new_shoe = True
            print "TIME TO SHUFFLE"
            return self.card_array.pop()

    def insert_cut_card(x=20,y=40):
        place = len(self.card_array) - random.randint(x,y)
        self.card_array.insert(place, 'CUT') 
        self.cut_loc = place

    def summarize_shoe(self):
        print "Shoe is %s decks"%(self.decks)
        print "Shoe has %s remaining cards"%(len(self.card_array))
        print "Shoe is cut at %s"%(self.cut_loc)

class Card:
    face_vals = {'J':10,'Q':10,'K':10,'A':1}
    def __init__(self, card):
        self.value = self.parse_card(card)
        self.card = card

    def parse_card(self, card):
        try:
            x = int(card)
        except ValueError:
            x = self.face_vals[card]
        return x

    def show_card(self): 
        print self.card, self.value

class Hand:
    def __init__(self, card_array, bet):
        self.card_array = card_array 
        self.has_ace = False
        self.soft_value = -1
        self.hard_value = 0
        self.bust = False
        self.blackjack = False
        self.bet = bet
        self.pair = False

    def set_bet(self, bet):
        print "Current bet %s"%(self.bet)
        self.bet = bet 
        print "NEW BET %s"%(self.bet)

    def set_pair(self):
        cards = [x.card for x in self.card_array]
        if len(cards) == cards.count(cards[0]) == 2:
            self.pair = cards[0]
        else: self.pair = False

    def set_has_ace(self):
        for x in self.card_array:
            if x.card == 'A':
                self.has_ace = True

    def check_ace(self):
        self.set_has_ace()
        return self.has_ace

    def set_blackjack(self):
        if len(self.card_array) == 2:
            if self.soft_value == 21:
                self.blackjack = True        

    def set_bust(self):
        self.bust = True if self.hard_value > 21 else False

    def set_hard_value(self):
        self.hard_value = sum(x.value for x in self.card_array)

    def set_soft_value(self):
        if self.check_ace():
            if self.hard_value + 10 > 21:
                self.soft_value = -1
            else:
                self.soft_value = self.hard_value + 10

    def accept_new_card(self, card): 
        self.card_array.append(card)
        self.compute_score()

    def compute_score(self):
        self.set_has_ace()
        self.set_pair()
        self.set_hard_value()
        self.set_soft_value()
        self.set_blackjack()
        self.set_bust()

    def ret_hand_total(self):
        if self.bust:
            return -1
        else: 
            return max(self.soft_value, self.hard_value)

class Dealer:
    def __init__(self):
        self.hand = Hand([], None)
        self.name = 'Jimmy'

    def up_card(self):
        if len(self.hand.card_array) > 1:
            return str(self.hand.card_array[1].value)

    def clear_hands(self):
        self.hand = Hand([], None)
        self.split_hand = None

class Player:
    def __init__(self, name, money=1000):
        self.name = name
        self.money = money 
        self.bet = 5 
        self.hand = Hand([], self.bet)
        self.split_hand = None

    def make_bet(self, hand, x=5):
        self.bet = x
        self.hand.bet = x

    def check_strategy(self, hand_value, dealer_up, strategy_table, debug):
        print "Looking up %s"%(debug)
        try:
            decision = strategy_table[str(hand_value)][dealer_up]
        except KeyError:
            print "Look up failed for\n Value: %s\n Lookup: %s"%(hand_value,
                                                                    debug)
            decision = None
        return decision

    def decide_play(self, dealer):
        num_cards = len(self.hand.card_array)
        dealer_up = dealer.up_card()
        decision = None

        self.hand.compute_score()

        if self.hand.soft_value > 0:
            decision = self.check_strategy(self.hand.soft_value, dealer_up, player_logic_soft_totals, "SOFT")
        elif self.hand.pair:
            decision = self.check_strategy(self.hand.pair, dealer_up, player_logic_split, "SPLIT")
        else:
            decision = self.check_strategy(self.hand.hard_value, dealer_up, player_logic_hard_totals, "HARD")
        
        print "PLAYER DECIDES TO %s"%(decision)
        return decision

    def split(self):
        pre_split = self.hand.card_array
        self.split_hand = Hand([self.hand.card_array[1]], self.bet)
        self.hand = Hand([self.hand.card_array[0]], self.bet)
        print "SPLIT PSLIT\n"
        print len(self.split_hand.card_array)
        print len(self.hand.card_array)

    def clear_hands(self):
        self.hand = Hand([], self.bet)
        self.split_hand = None

class Game:
    def __init__(self, dealer, players, shoe):
        self.dealer = dealer
        self.players = players 
        self.shoe = shoe

    def deal_dealer(self, dealer):
        new_card = self.shoe.deal_one()
        dealer.hand.accept_new_card(new_card)
        print "DEALER CARD DEALT %s"%(new_card.card)

    def deal_player(self, hand):
        new_card = self.shoe.deal_one()
        hand.accept_new_card(new_card)
        print "PLAYER CARD DEALT %s"%(new_card.card)

    def start_hand(self):
        count = 0
        while count < 2:
            self.deal_dealer(self.dealer)
            for p in self.players:
                self.deal_player(p.hand)
            count += 1

    def play_hand(self, player, hand):
        hand.compute_score()

        if not(hand.bust or hand.blackjack):
            d = player.decide_play(self.dealer)
            if d == H:
                self.deal_player(hand)
                self.play_hand(player, hand)
            elif d == S:
                print "%s stands with"%(player.name)
                print ' '.join([str(x.card) for x in hand.card_array])
                print hand.ret_hand_total()
            elif d == D:
                hand.set_bet(hand.bet * 2)
                print "%s has doubled on %s"%(player.name,
                            ' '.join([str(x.card) for x in hand.card_array]))
                self.deal_player(hand)
            elif d == Sp: 
                player.split()
                hand = player.hand
                split_hand = player.split_hand
                print "\t\n SPLIT HAND 1"
                self.deal_player(hand)
                self.play_hand(player, hand)
                print "\t\n SPLIT HAND 2"
                self.deal_player(split_hand)
                self.play_hand(player, split_hand)
        elif hand.bust:
            print 'player bust with %s'%(' '.join([str(x.card) for x in player.hand.card_array]))
        elif hand.blackjack:
            print 'player blackjack'

    def play_dealer(self, dealer):
        dealer.hand.compute_score()
        if not (dealer.hand.blackjack or dealer.hand.bust) :
            if dealer.hand.has_ace & (dealer.hand.soft_value <= 17):
                self.deal_dealer(self.dealer)
                self.play_dealer(dealer)
            elif (not dealer.hand.has_ace) & (dealer.hand.hard_value < 17):
                self.deal_dealer(self.dealer)
                self.play_dealer(dealer)
        else:
            if dealer.hand.blackjack:
                print 'dealer blackjack'
            elif dealer.hand.bust:
                print 'dealer bust' 

    def win_lose(self, dealer, player):
        winner = None
        loser = None

        if player.hand.bust:
            winner, loser = dealer, player
        elif dealer.hand.bust:
            winner, loser = player, dealer
        else:
            if dealer.hand.ret_hand_total() > player.hand.ret_hand_total():
                winner, loser = dealer, player
            elif dealer.hand.ret_hand_total == player.hand.ret_hand_total():
                winner = None
                loser = None
            elif dealer.hand.ret_hand_total() < player.hand.ret_hand_total(): 
                winner, loser = player, dealer

        if winner:
            print "%s has won with %d"%(winner.name, winner.hand.ret_hand_total())
            print "%s has lost with %d"%(loser.name, loser.hand.ret_hand_total())
            print "----\n"*2
        else:
            print "%s PUSHes with %d"%(player.name, player.hand.ret_hand_total())
        return winner


card_test_array = {x: Card(x) for x in CARD_VALS}
def check_scores(player):
    player.hand.compute_score()
    print player.hand.soft_value
    print player.hand.hard_value

foo = Shoe(8)
foo.shuffle()
tyler = Player('tyler')
d = Dealer()

if __name__ == "__main__":
    tyler_win = 0
    dealer_win = 0
    for x in range(1,55):
    #GENERAL TEST GAME
        bar = Game(d, [tyler], foo)
        bar.start_hand()
        for x in bar.players:
            bar.play_hand(x, x.hand)
        bar.play_dealer(bar.dealer)
        for x in bar.players:
            winner = bar.win_lose(d, x)
            if winner and winner.name == 'tyler':
                tyler_win += 1
            else: dealer_win += 1
        d.clear_hands()
        for x in bar.players:
            x.clear_hands()
    print 'tyler %d'%(tyler_win)
    print 'dealer %d'%(dealer_win)

    p = bar.players[0]
    d = bar.dealer 

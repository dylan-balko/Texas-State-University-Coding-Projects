## Dylan Balko, Alaina Adcox, Mariana Valdez 
##imports random to be able to shuffle the deck later on
import random

## creates the deck by assigning every suit one of the values in the value array
## uses random function to shuffle the cards
def create_deck():
    suits = ['Hearts','Diamonds','Clubs','Spades']
    values = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
    deck = [f'{value} of {suit}' for suit in suits for value in values]
    random.shuffle(deck)
    return deck

## draws a card from top of deck if the deck is not empty
def draw_card(deck):
    if deck:
        return deck.pop()
    else:
        print("The deck is empty, shuffling again...")
        return None

## asks user for a bet amount and validates that it is a valid monetary value ie. not negative or a string 
def get_bet():
    while True:
        try:
            bet = float(input("How much money would you like to bet in each of the three cirlces? "))
            if bet > 0:
                return bet
            else:
                print("Can't bet a negative amount")
        except ValueError:
            print("Invalid input. Try again please. ")

## allows user to change their total bet amount by pulling one of the three circles after seeing their first hand and first community car
def get_bet_decision(total_bet,bet):
    while True:
        decision = input("After seeing your hand, would you like to let it ride or pull back a bet? Ride or Pull? ").upper()
        if decision == "RIDE":
            return None
        elif decision == "PULL":
            return total_bet - bet
        else:
            print("Invalid decision. Please choose 'Ride' or 'Pull'.")

## adds original three cards player got dealt to the community cards to create their final hand to be evaluated
def evaluate_hand(hand, community_cards):
    final_hand = hand + community_cards
    return final_hand

## count how many ranks are in each hand
def count_ranks(final_hand):
    rank_count = {}
    for card in final_hand:
        rank = card.split()[0]
        rank_count[rank] = rank_count.get(rank, 0) + 1
    return rank_count

## sorts ranks to see if there is a straight
def is_straight(rank_count):
    ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}
    sorted_ranks = sorted(rank_count.keys(), key=lambda x: ranks.get(x, 0), reverse=True)
    return ranks.get(sorted_ranks[0], 0) - ranks.get(sorted_ranks[4], 0) == 4

## reads the second half of the card to see if all suits are the same equaling a flush
def is_flush(final_hand):
    return len(set(card.split()[2] for card in final_hand)) == 1

## checks for if all the suits are in the array filled with royal suits
def is_royal_flush(rank_count):
    royal_ranks = {'Ace', 'King', 'Queen', 'Jack', '10'}
    return set(rank_count.keys()) == royal_ranks

## calls all the previous methods to check for different hand combos
## based on the outputs in a nested decision structure the payout multiplier is set and returns payout
def calculate_payout(rank_count, total_bet,final_hand):
    payout_multiplier = 0
    if is_royal_flush(rank_count):
        payout_multiplier = 1000  ## Royal Flush pays 1000:1
    ## Check for four of a kind
    elif 4 in rank_count.values():
        payout_multiplier = 50  ## Four of a Kind pays 50:1
    ## Check for three of a kind
    elif 3 in rank_count.values():
        payout_multiplier = 3  ## Three of a Kind pays 3:1
    ## Check for two pairs or one pair
    elif 2 in rank_count.values():
        # Count the number of pairs
        num_pairs = sum(count == 2 for count in rank_count.values())
        if num_pairs == 2:
            payout_multiplier = 2  ## Two Pair pays 2:1
        elif num_pairs == 1:
            payout_multiplier = 1  ## One Pair pays 1:1
    ## Check for other hands
    else:
        if len(rank_count) == 1:
            if is_flush(final_hand):
                payout_multiplier = 8  ## Flush pays 8:1
            elif is_straight(rank_count):
                payout_multiplier = 5  ## Straight pays 5:1
    
    return payout_multiplier


def payout_bet(final_hand, total_bet):
    rank_count = count_ranks(final_hand)
    return calculate_payout(rank_count, total_bet,final_hand) * total_bet

## main function and controls the flow of the game by calling methods and outputting 
def main():
    print("Welcome to let it ride.\n")
    bet = get_bet()
    total_bet = bet * 3
    print("\n")
    deck = create_deck()
    hand = [draw_card(deck) for num in range(3)]
    print(f"Here is your hand: \n{hand[0]}, {hand[1]}, {hand[2]}")
    new_total_bet = get_bet_decision(total_bet, bet)
    if new_total_bet is not None:
        total_bet = new_total_bet
    community_cards = [draw_card(deck) for _ in range(2)]
    print(f"\nCommunity Card: {community_cards[0]}")
    new_total_bet = get_bet_decision(total_bet, bet)
    if new_total_bet is not None:
        total_bet = new_total_bet
    print(f"\nCommunity Card: {community_cards[1]}")
    final_hand = evaluate_hand(hand, community_cards)
    print(f"\nFinal hand: {final_hand}")
    payout = payout_bet(final_hand,total_bet)
    print(f"Payout: {payout}")
    
    
main()

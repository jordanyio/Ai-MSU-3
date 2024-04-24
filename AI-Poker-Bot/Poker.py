from treys import Card, Evaluator, Deck
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from itertools import combinations
import json
import pickle
import multiprocessing


class Poker:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.evaluator = Evaluator()
        self.board = []
        self.hero_hand = None
        self.villian_hand = None
        self.pot = 0


    def generate_hands():
        return list(combinations(Deck.GetFullDeck(), 2))    
    

    def deal_villian_hands(self, n_hands):
        hands = []
        for i in range(n_hands):
            hands.append(self.deck.draw(2))
        return hands
 
    def deal_hand(self):
        return self.deck.draw(2)
    
    def deal_hero_hand(self):
        return self.deck.draw(2)

    def deal_flop(self):
        if len(self.board) > 0: 
            return
        self.board.extend(self.deck.draw(3))
    def deal_street(self):
        if len(self.board) > 4: 
            return
        self.board.extend(self.deck.draw(1))   


    def make_action(self, hero_hand, villians):
        self.deal_flop()
        self.deal_street()
        self.deal_street()
        print(f"Board: {Card.print_pretty_cards(self.board)}")

        hero_score = self.evaluator.evaluate(self.board, hero_hand)
        print(f"Hero hand: {Card.print_pretty_cards(hero_hand)}, score: {hero_score}")
        scores = []
        for hand in villians:
            villian_score = self.evaluator.evaluate(self.board, hand)
            scores.append(villian_score)
            print(f"Villian hand: {Card.print_pretty_cards(hand)}, score: {villian_score}")

        # Evaluate 
        hands_hero_beats = sum(1 for score in scores if hero_score <= score)

        print(f"Hands hero beats: {hands_hero_beats}")

        action_ratio = hands_hero_beats / (len(villians) + 1)
        if action_ratio > 0.80:
            return "Call or Raise"
        elif action_ratio > 0.70:
            return "Call or Check"
        else:
            return "Check or Fold"
        

    def generate_all_possible_hands(self):
    # Generate all possible combinations of two cards from a full deck
        full_deck = self.deck.GetFullDeck()
        return list(combinations(full_deck, 2))

 
    def make_pickle(self):
        all_possible_hands = self.generate_all_possible_hands()

        # Initialize the rainbow dictionary
        rainbow_dict = {}

        # Populate the dictionary with all possible hands
        for hand in all_possible_hands:
            hand_key = tuple(sorted(hand))  # Use tuple of integers as key
            rainbow_dict[hand_key] = {1: 0.5, 2: 0.5}

        # Write the dictionary to a pickle file
        with open('rainbow_dict.pkl', 'wb') as file:
            pickle.dump(rainbow_dict, file)


    def get_win_odds(self, hand, n_villians):
        # Load the pickle file containing the rainbow dictionary
        with open('rainbow_dict.pkl', 'rb') as file:
            rainbow_dict = pickle.load(file)

        # Convert random_hand to a tuple if not already (ensure it's hashable)
        hand_key = tuple(hand) if isinstance(hand, list) else hand
        #print(f"Drawn Hand:{hand_key}", [Card.int_to_pretty_str(card) for card in hand_key])

        # Check if the drawn hand is in the dictionary and access its value
        if hand_key in rainbow_dict:
            nested_value = rainbow_dict[hand_key].get(n_villians)  # Get the value associated with key n_villians
            return f"The odds of winning against {n_villians} villians with the hand {hand_key} is: {nested_value}"
        elif hand_key[::-1] in rainbow_dict:
            nested_value = rainbow_dict[hand_key[::-1]].get(n_villians) 
            return f"The odds of winning against {n_villians} villians with the hand {hand_key} is: {nested_value}"
        else:
            return "Hand not found in the dictionary."


    def worker(self, args):
        main_key, rainbow_dict = args
        pretty_hand = ', '.join(Card.int_to_pretty_str(card) for card in list(main_key))
        #print(f"Worker is proccessing hand: {pretty_hand}")
        
        if not isinstance(rainbow_dict[main_key], dict):
            rainbow_dict[main_key] = {}
        for dict_key in range(1, 9):
            value = self.populate(main_key, dict_key)
            rainbow_dict[main_key][dict_key] = value  

        return (main_key, rainbow_dict[main_key])


    def update_rainbow_dict(self, file_path):
        with open(file_path, 'rb') as file:
            rainbow_dict = pickle.load(file)

        pool = multiprocessing.Pool(processes=8)
        results = pool.map(self.worker, [(key, rainbow_dict) for key in list(rainbow_dict.keys())])
        pool.close()
        pool.join()

        # Update the original dictionary with the processed results
        for main_key, sub_dict in results:
            rainbow_dict[main_key] = sub_dict

        # Write the updated dictionary back to the pickle file
        with open(file_path, 'wb') as file:
            pickle.dump(rainbow_dict, file)

        print("Rainbow dictionary has been updated.")


    def populate(self, hand, n_villians, simulations=10000):
        wins = 0
        hands = 0

        for _ in range(simulations):
            self.deck.shuffle()
            current_deck = [card for card in self.deck.cards if card not in hand]
            self.deck.cards = current_deck 
            self.board = []

            villians = [self.deck.draw(2) for _ in range(n_villians)]
            
            self.deal_flop()
            self.deal_street()
            self.deal_street()

            try:
                hero_score = self.evaluator.evaluate(self.board, list(hand))
            except Exception as e:
                print(f"Failed to evaluate hero hand: {list(hand)} on board: {self.board}")
                print(f"Exception: {e}")
                continue  # Skip this round

            scores = []
            for v_hand in villians:
                try:
                    villian_score = self.evaluator.evaluate(self.board, v_hand)
                    scores.append(villian_score)
                except KeyError:
                    print(f"Failed to evaluate villain hand: {v_hand} on board: {self.board}")
                    continue  # Skip this villain

            hands_hero_beats = sum(1 for score in scores if hero_score <= score)
            if hands_hero_beats == n_villians:
                wins += 1
            hands += 1

        return wins / hands if hands > 0 else 0 


    def pickle_to_json(self, pickle_file_path, json_file_path):
    # Load the data from the pickle file
        with open(pickle_file_path, 'rb') as file:
            data = pickle.load(file)

        # Convert the keys to strings if they are not already
        string_data = {str(key): value for key, value in data.items()}

        # Write the data to a JSON file
        with open(json_file_path, 'w') as file:
            json.dump(string_data, file, indent=4)

        print(f"Data has been written from {pickle_file_path} to {json_file_path} in JSON format.")

            
    def list_all_cards():
        card_map = {}

        suits = ['c', 'd', 'h', 's']  
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        
        for suit in suits:
            for rank in ranks:
                card_str = rank + suit
                card_int = Card.new(card_str)
                card_map[card_str] = card_int

        card_values = card_map
        for card_str, card_int in card_values.items():
            print(f"{card_str} (integer: {card_int})")
        
        return card_map        


# pp = Poker()

# villians = pp.deal_villian_hands(7)
# hero = pp.deal_hero_hand()

# print(pp.make_action(hero, villians))


# hand = pp.deck.draw(2)
# opponent = pp.deck.draw(2)
# board = pp.deck.draw(4)
# player_score = pp.evaluator.evaluate(board, hand)
# bogey = pp.evaluator.evaluate(board, opponent)

# print(Card.print_pretty_cards(board))
# print(player_score)
# print(Card.print_pretty_cards(hand))
# print(bogey)
# print(Card.print_pretty_cards(opponent))
#print(pp.deck)
#print(Poker.generate_hands())
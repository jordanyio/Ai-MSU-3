from treys import Card, Evaluator, Deck
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from itertools import combinations
import random

class PokerHandOdds:
    def __init__(self):
        self.evaluator = Evaluator()
        self.model = DecisionTreeClassifier()
        self.features = []
        self.labels = []

    def generate_all_hands(self):
        deck = Deck.GetFullDeck()
        return list(combinations(deck, 2))

    def simulate_hand_against_opponents(self, player_hand):
        wins = 0
        trials = 0
        all_hands = self.generate_all_hands()
        opponents_hands = [hand for hand in all_hands if set(hand) != set(player_hand)]

        for _ in range(1000):
            deck = Deck()
            deck.shuffle()
            board = [deck.draw() for _ in range(5)]  # Draw 5 cards for the board

            # Make sure hands are correctly formatted as lists of integers
            player_hand_integers = [card for card in player_hand]
            player_score = self.evaluator.evaluate(board, player_hand_integers)

            for opponent_hand in random.sample(opponents_hands, 10):
                opponent_hand_integers = [card for card in opponent_hand]
                opponent_score = self.evaluator.evaluate(board, opponent_hand_integers)
                if player_score < opponent_score:
                    wins += 1
                trials += 1

        return wins / trials  # Probability of winning

    def train_model(self):
        all_hands = self.generate_all_hands()
        for hand in all_hands:
            features = self.hand_to_features(hand)
            probability_of_winning = self.simulate_hand_against_opponents(hand)
            self.features.append(features)
            self.labels.append(probability_of_winning)

        self.model.fit(self.features, self.labels)

    def hand_to_features(self, hand):
        features = []
        for card in hand:
            rank = Card.get_rank_int(card)
            suit = Card.get_suit_int(card)
            features.extend([rank, suit])
        return features

    def predict_odds(self, hand):
        features = np.array([self.hand_to_features(hand)])
        return self.model.predict_proba(features)[0][1]

if __name__ == "__main__":
    poker_odds = PokerHandOdds()
    poker_odds.train_model()  # This will take a significant amount of time
    hand = [Card.new('Ah'), Card.new('Kh')]
    print(f"Odds of winning with {Card.int_to_pretty_str(hand[0])} and {Card.int_to_pretty_str(hand[1])}: {poker_odds.predict_odds(hand)}")

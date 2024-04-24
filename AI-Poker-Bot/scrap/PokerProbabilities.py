from treys import Deck, Evaluator, Card
from sklearn.tree import DecisionTreeClassifier
import numpy as np

class PokerProbabilities:
    def __init__(self):
        self.deck = Deck()
        self.evaluator = Evaluator()
        self.preflop_tree = DecisionTreeClassifier()
        self.postflop_tree = DecisionTreeClassifier()

    def simulate_hands(self, player_hand, community_cards=None):
        community_cards = community_cards or []
        deck = Deck()
        deck.shuffle()
        
        player_hand_cards = [Card.new(card) for card in player_hand]
        community_cards_cards = [Card.new(card) for card in community_cards]
        
        results = []
        for _ in range(1000):  # Simulate 1000 hands
            deck.shuffle()
            opponent_hand = deck.draw(2)
            board = community_cards_cards + [deck.draw(1) for _ in range(5 - len(community_cards_cards))]
            
            player_score = self.evaluator.evaluate(board, player_hand_cards)
            opponent_score = self.evaluator.evaluate(board, opponent_hand)
            
            # 1 for player win, 0 for player loss
            results.append(1 if player_score < opponent_score else 0)
        return results

    def train_decision_tree(self, tree, player_hand_samples, results):
        tree.fit(player_hand_samples, results)

    def prepare_features(self, player_hand):
        ranks = '23456789TJQKA'
        suits = 'cdhs'
        features = []
        for card in player_hand:
            rank = ranks.index(card[0]) + 2  # Numerical value of rank
            suit = suits.index(card[1])  # Numerical value of suit
            features.extend([rank, suit])
        return features

    def make_decision(self, tree, player_hand):
        features = np.array([self.prepare_features(player_hand)])
        return tree.predict(features)[0]  # Return '0' for fold, '1' for play

    def example_training(self):
        player_hands = [['Ah', 'Kh'], ['8c', '8s'], ['2d', '7d']]
        results = []
        for hand in player_hands:
            results.extend(self.simulate_hands(hand))

        player_hand_features = [self.prepare_features(hand) for hand in player_hands]
        self.train_decision_tree(self.preflop_tree, player_hand_features, results)

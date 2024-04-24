from deuces import Deck, Evaluator, Card
from treelib import Tree, Node
import itertools

def simulate_hand(player_hand, board, num_opponents):
    deck = Deck()
    deck.shuffle()
    
    # Convert both player_hand and board to lists to avoid type issues
    player_hand = list(player_hand)
    board = list(board)
    
    # Remove known cards from deck
    for card in player_hand + board:
        deck.cards.remove(card)
    
    evaluator = Evaluator()
    
    # Ensure there are enough cards for evaluation
    if len(board) + len(player_hand) >= 5:
        player_score = evaluator.evaluate(board, player_hand)
    else:
        player_score = float('inf')  # Use a high score for an invalid hand
    
    wins = 0
    trials = 1000  # Number of simulations per state
    
    for _ in range(trials):
        deck.shuffle()
        # Ensure there are enough cards on the board
        simulated_board = board[:]
        while len(simulated_board) < 3:
            simulated_board.append(deck.draw(1))

        opponents_hands = [deck.draw(2) for _ in range(num_opponents)]
        opponents_scores = [evaluator.evaluate(simulated_board, hand) for hand in opponents_hands]
        
        if all(player_score <= opponent_score for opponent_score in opponents_scores):
            wins += 1
    
    return wins / trials

def build_decision_tree(num_opponents):
    tree = Tree()
    tree.create_node("Root", "root", data="Root Node Data")

    deck = Deck()
    all_possible_hands = list(itertools.combinations(deck.cards, 2))
    possible_board_states = [
        (),
        tuple(deck.draw(3)) if len(deck.cards) >= 3 else (),
        tuple(deck.draw(4)) if len(deck.cards) >= 4 else (),
        tuple(deck.draw(5)) if len(deck.cards) >= 5 else (),
    ]

    for hand in all_possible_hands:
        for board in possible_board_states:
            hand_cards = Card.print_pretty_cards(hand) if hand else "Empty Hand"
            board_cards = Card.print_pretty_cards(board) if board else "Empty Board"
            hand_str = hand_cards + " | " + board_cards
            win_prob = simulate_hand(hand, board, num_opponents)
            tree.create_node(hand_str, hand_str, parent="root", data=f"Win Probability: {win_prob:.2f}")

    return tree



def decide_action(player_hand, board, decision_tree):
    if player_hand and all(player_hand):  # Ensure there are no None values in player_hand
        hand_str = Card.print_pretty_cards(player_hand) + " | " + Card.print_pretty_cards(board)
    else:
        print("Invalid player hand or board.")
        return 'Check'  # Safeguard against invalid input
    
    node = decision_tree.get_node(hand_str)
    if node and node.data:
        win_probability = float(node.data.split(": ")[1])
        if win_probability > 0.6:
            return 'Raise or Call'
        elif win_probability > 0.4:
            return 'Check or Call'
        else:
            return 'Fold'
    else:
        print(f"Node not found for hand: {hand_str}")  # Log missing node
        return 'Check'  # Default action if no data found






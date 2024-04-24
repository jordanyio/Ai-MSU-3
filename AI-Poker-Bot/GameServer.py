from flask import Flask, jsonify, request
from flask_cors import CORS
from Poker import Poker
from Bot import Bot

app = Flask(__name__)
CORS(app) 

poker = Poker()
bot = Bot()

# Mock data to represent game state
game_state = {
    "player_hand": [],
    "opponent_hand": [],
    "community_cards": [],
    "pot": 0
}

# Endpoint to get a new hand
@app.route('/GetNewHand', methods=['GET'])
def get_new_hand():
    # Mocked new hands for simplicity
    game_state['community_cards'] = [] 
    poker.board = [] # Clear community cards
    poker.deck.shuffle()
    game_state['player_hand'] = poker.deal_hand()
    game_state['opponent_hand'] = poker.deal_hand()
    game_state['pot'] = 0  # Resetting pot for a new game
  
    return jsonify(game_state)

# Endpoint to get the flop (first three community cards)
@app.route('/GetFlop', methods=['GET'])
def get_flop():
    poker.deal_flop()
    game_state['community_cards'] = poker.board
    print(f"Game state: {game_state}, board: {poker.board}")
   
    return jsonify(poker.board)

# Endpoint to get the turn (fourth community card)
@app.route('/GetTurn', methods=['GET'])
def get_turn():
    if len(game_state['community_cards']) < 3:
        return jsonify({"error": "Flop must be dealt first"}), 400
    poker.deal_street()
    game_state['community_cards'] = poker.board
    # Example turn card
    return jsonify(poker.board)

# Endpoint to get the river (fifth community card)
@app.route('/GetRiver', methods=['GET'])
def get_river():
    if len(game_state['community_cards']) < 4:
        return jsonify({"error": "Turn must be dealt first"}), 400
    poker.deal_street()
    game_state['community_cards'] = poker.board
    return jsonify(poker.board)

# Endpoint to update the state (for simplicity, accepting changes via query parameters)
@app.route('/UpdateState', methods=['POST'])
def update_state():
    chips = request.json.get('chips')
    if chips is not None:
        game_state['pot'] += chips
    return jsonify(game_state)

@app.route('/EvaluateHands', methods=['POST'])
def evaluate_hand():
    data = request.json  # Access the JSON data sent by the client
    player_hand = data['playerHand']
    opponent_hand = data['opponentHand']
    community_cards = data['communityCards']

    # Logic to evaluate hands
    # This is a placeholder for whatever logic you need to apply
    player_score = poker.evaluator.evaluate(community_cards, player_hand)
    bot_score = poker.evaluator.evaluate(community_cards, opponent_hand)

   
    result = {'playerScore': player_score, 'botScore': bot_score}
    return jsonify(result), 200


@app.route('/GetBotAction', methods=['POST'])
def get_bot_action():
    try:
        # Parse the incoming data as JSON
        
        game_state = request.get_json()
        print(f"game state {game_state}")
        # Process the game state through your function
        result = bot.get_action(game_state)  # Check this method for the error
        
        # Logging the result for debugging
        print(f"BOT RESULT SERVER: {result}")
        
        # Return the result as JSON
        return jsonify(result), 200
    except Exception as e:
        # Log the full error message for debugging
        print("Error processing request:", str(e))
        
        # Return an error message
        return jsonify({'error': 'Failed to process request', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

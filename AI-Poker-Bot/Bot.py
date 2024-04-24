import openai
import appsettings
from Poker import Poker as p
from treys import Card
import json
import re
import ast



class Bot:
  def __init__(self):
    self.model="gpt-4-turbo"
    self.temperature = 0.9
    self.max_tokens = 150
    self.top_p = 1
    self.frequency_penalty = 0
    self.presence_penalty = 0.6
    self.api_key = appsettings.API_KEY
    self.systemPrompt = appsettings.systemPrompt
    self.messages=[
      {"role": "system", "content": f"{self.systemPrompt}"},
      {"role": "user", "content": "Welcome to the game, the dealer is about to begin soon. Good Luck!"},
      {"role": "assistant", "content": "Thank you, good luck to you as well!"}
    ]


  def _add_user_message(self, content):
        """
        Adds a user message to the messages list.
        
        Parameters:
            content (str): The content of the user message.
        """
        self.messages.append({"role": "user", "content": content})

  def _add_assistant_message(self, content):
      """
      Adds an assistant message to the messages list.
      
      Parameters:
          content (str): The content of the assistant message.
      """
      self.messages.append({"role": "assistant", "content": content.content})  




  def parse_response(self, data):
    
    content = data.get("content", "")
    # Define the pattern to extract the key-value pairs
    pattern = r"Action: (.*), Amount: (\d+), LLM_Note: (.*)"
    
    # Use regular expression to find the matches
    match = re.search(pattern, content)
    if match:
        # Construct the dictionary from the matched groups
        result = {
            "Action": match.group(1),
            "Amount": int(match.group(2)),
            "LLM_Note": match.group(3)
        }
        return result
    else:
        return "No valid data found"



  def _call_llm(self, messages: list):
    openai.api_key = self.api_key

    response = openai.ChatCompletion.create(
      model=self.model,
      temperature = self.temperature,
      max_tokens = self.max_tokens,
      top_p = self.top_p,
      frequency_penalty = self.frequency_penalty,
      presence_penalty = self.presence_penalty,
      messages=messages
    )
    return response
  
  def _process_game_state(self, game_state):
    """
    Constructs a descriptive paragraph from the game state dictionary.
    
    Parameters:
        game_state (dict): A dictionary containing various attributes of the current poker game state.
        
    Returns:
        str: A descriptive paragraph summarizing the current game state.
    """
    current_betting_round = ''
    if (game_state['currentBettingRound'] == 0):
      current_betting_round = 'preflop action'
    elif (game_state['currentBettingRound'] == 1):
      current_betting_round = 'flop action'
    elif (game_state['currentBettingRound'] == 2):
      current_betting_round = 'turn action'
    elif (game_state['currentBettingRound'] == 3):
      current_betting_round = 'river action'


    hand = game_state['botHand']
    pretty_hand = ', '.join(Card.int_to_str(card) for card in hand)

    board = game_state['communityCards']
    pretty_board = ', '.join(Card.int_to_str(card) for card in board)

    description = (
        "A new action is required. Here is previous action logs, and the current game state in which you must make an action based on. The logs will refer to you as Bot, and the opponent as Player."
        f"Actions taken this hand and many previous hands include: {game_state['playerActionsThisHand']}. "
        f"The current game is in the {current_betting_round} round. "
        f"The bot has the following cards: {pretty_hand}. "
        f"Community cards on the table are: {pretty_board}. "
        f"There are currently {game_state['potSize']} chips in the pot. "
        f"The bot's stack size is {game_state['botStackSize']} chips, while the opponent's stack size is {game_state['opponentStackSize']} chips. "
        f"The current bet to match is {game_state['currentBet']} chips. "
        f"The dealer is on {'the bot' if game_state['dealer'] == 'bot' else 'the opponent'}."
    )
    
    return description
  
  def get_action(self, game_state):
     
     user_message = self._process_game_state(game_state)
     self._add_user_message(user_message)
     print(f"Messages: {self.messages}")

     bot_response = self._call_llm(self.messages)
     print(f"Bot response: {bot_response}")
     self._add_assistant_message(bot_response.choices[0].message)
     print(f"Bot response idx: {bot_response.choices[0].message}")
    

     action_extract = self.parse_response(bot_response.choices[0].message)
     print(f"Bot response Extract: {action_extract}")
     
     return action_extract









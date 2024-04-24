from Poker import Poker as p
from treys import Card
from itertools import combinations
import time as t
import json

# p = p()







import openai
import appsettings

openai.api_key = appsettings.API_KEY

response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)

print(response)



# start = t.time()

# #p.update_rainbow_dict('rainbow_dict.pkl')
# # p.pickle_to_json('rainbow_dict.pkl', 'rainbow_dict.json')
# end = t.time()

# print(f"Time elapsed: {end - start}")

# hand = p.deck.draw(2)
# pretty_hand = ', '.join(Card.int_to_pretty_str(card) for card in hand)
# print(f"Get winning odds for {pretty_hand}, odds: {p.get_win_odds(hand, 1)}")




# from treys import Card



# # Get all cards and their integer representations









# # used these to confirm the pickle file was proccessed coreectly after multiproccessing was added

# #p.update_rainbow_dict('rainbow_dict.pkl')
# #p.pickle_to_json('rainbow_dict.pkl', 'rainbow_dict.json')



# def update_json_values(json_file_path, new_value=0.50):
#     # Step 1: Read the JSON file
#     try:
#         with open(json_file_path, 'r') as file:
#             data = json.load(file)
#     except FileNotFoundError:
#         print(f"No file found at {json_file_path}")
#         return
#     except json.JSONDecodeError:
#         print(f"File {json_file_path} is not a valid JSON file.")
#         return

#     # Step 2: Modify the data
#     for main_key in data:
#         for sub_key in data[main_key]:
#             data[main_key][sub_key] = new_value

#     # Step 3: Write the changes back to the JSON file
#     with open(json_file_path, 'w') as file:
#         json.dump(data, file, indent=4)

#     print(f"All nested dictionary values in {json_file_path} have been updated to {new_value}.")

# # Example usage
# #update_json_values('rainbow_dict.json')


# def count_keys_in_json(json_file_path):
#     # Load the data from the JSON file
#     with open(json_file_path, 'r') as file:
#         data = json.load(file)

#     # Count the main keys in the dictionary
#     num_keys = len(data.keys())

#     print(f"The number of main keys in the JSON file is: {num_keys}")
#     return num_keys

# # # Example usage
# # count_keys_in_json('rainbow_dict.json')
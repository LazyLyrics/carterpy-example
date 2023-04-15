import os
from dotenv import load_dotenv
from termcolor import colored
from art import text2art
from carterpy import Carter

# Print logo
print(colored(text2art("carter-py"), "magenta"))
print(colored("A Python wrapper for the Carter API", "magenta"))
print()
# Print links
print("Carter")
print("------")
print(colored("Get your API key: https://www.carterlabs.ai/", "blue"))
print(colored("Documentation: https://docs.carterlabs.ai/", "blue"))
print()
print("carter-py")
print("--------")
print(colored("carterpy on GitHub: https://github.com/LazyLyrics/carterpy", "blue"))
print(colored("This example on GitHub: https://github.com/LazyLyrics/carterpy-example", "blue"))
print()

# Load API key and player_id from .env
load_dotenv()
api_key = os.getenv("CARTER_API_KEY")
player_id = os.getenv("PLAYER_ID")
char_name = os.getenv("CHAR_NAME")

# Check if API key and player_id are set
if not api_key:
    api_key = input("Please enter your API key: ")
if not player_id:
    player_id = input("Please enter your player_id (leave blank for random): ")
    if player_id == "":
        player_id = None
if not char_name:
    char_name = input("Please enter your character name: ")
opener_needed = input("Do you want a conversation opener? (yes/no): ").lower()

# Initialize Carter
carter = Carter(api_key)

print()
print(colored(f"Welcome to the Carter API example! Use /help for guidance. You can set variables using the .env_example provided and renaming it to '.env'", "magenta"))
print()

# Ask if the user wants a conversation opener
if opener_needed == "yes":
    interaction = carter.opener(player_id)
    print(colored(f"{char_name}: {interaction.output_text}", "green"))

# Main loop
while True:
    user_input = input("You: ")

    if user_input == "/help":
        print("Available commands:")
        print("/quit - Quit the program")
        print("/history - Show the history of interactions")
        print("/avg_time - Show the average response time over the session")
        print("/avg_time_last_5 - Show the average response time over the last 5 interactions")

    elif user_input == "/quit":
        break

    elif user_input == "/history":
        for interaction in carter.history:
            print(interaction)

    elif user_input == "/avg_time":
        avg_time = sum([interaction.time_taken for interaction in carter.history]) / len(carter.history)
        print(f"Average response time: {avg_time} ms")

    elif user_input == "/avg_time_last_5":
        last_5 = carter.history[:5]
        avg_time = sum([interaction.time_taken for interaction in last_5]) / len(last_5)
        print(f"Average response time (last 5 interactions): {avg_time} ms")

    elif user_input[0] != "/":
        interaction = carter.say(user_input, player_id)
        if interaction.ok:
            print(colored(f"{char_name}: " + interaction.output_text, "green"))
        else:
            print(colored(f"Error [{interaction.status_code}]: " + interaction.status_message, "red"))

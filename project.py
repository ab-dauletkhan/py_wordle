import requests
from prohibited import prohibited_words


def get_random_word():
    while True:
        try:
            response = requests.get(
                "https://random-word-api.herokuapp.com/word?length=5"
            )
            response.raise_for_status()
            random_word = response.json()[0]

            # print(random_word)
            if random_word not in prohibited_words:
                return random_word

        except requests.exceptions.RequestException as e:
            print(f"Error fetching random word: {e}")
            continue


def game_instruction():
    print(
        """Welcome to Wordle, a single-player word guessing game!

Instructions:
1. You have six attempts to guess a hidden five-letter word.
2. Each letter of the word is represented by a cell in the table.
3. After each attempt, the table will show your progress:
    - \033[92mGreen\033[0m cell indicates a correct letter in the correct position.
    - \033[93mYellow\033[0m cell indicates a correct letter in the wrong position.
    - \033[91mRed\033[0m cell indicates an incorrect letter.
5. Your goal is to guess the hidden word correctly within the given attempts.

Let's get started!"""
    )


def display_table(table):
    for row in table:
        print("+---" * (len(row) - 1) + "+")
        print("| " + " | ".join(str(cell).center(1) for cell in row[:-1]) + " |")
    print("+---" * (len(row) - 1) + "+")


def play_game(hidden_word):
    attempt = 6
    word_length = len(hidden_word)
    table = [[" " for _ in range(word_length + 1)] for _ in range(attempt)]

    while attempt > 0:
        guess = str(
            input(f"Attempt {7 - attempt}: Guess the {word_length}-letter word: ")
        )

        if len(guess) != word_length:
            print(f"Please enter a {word_length}-letter word.")
            continue

        for i, (char, word) in enumerate(zip(hidden_word, guess)):
            if word == char:
                table[6 - attempt][i] = (
                    "\033[92m" + word + "\033[0m"
                )  # Green for correct
            elif word in hidden_word:
                table[6 - attempt][i] = (
                    "\033[93m" + word + "\033[0m"
                )  # Yellow for partially correct
            else:
                table[6 - attempt][i] = (
                    "\033[91m" + word + "\033[0m"
                )  # Red for incorrect

        display_table(table)
        attempt -= 1
        if guess == hidden_word:
            print("You guessed the word correctly! WIN 🕺🕺🕺 ")
            break

        if attempt == 0:
            print("Game over !!!! ")
            print(f"The hidden word was: {hidden_word}")


def main():
    print("Welcome to Wordle!")
    while True:
        print("\nChoose an option:")
        print("1) Play")
        print("2) Read the instructions")
        print("3) Quit")

        choice = input("Enter your choice (1, 2, or 3): ")

        match choice:
            case "1":
                hidden_word = get_random_word()
                play_game(hidden_word)
            case "2":
                game_instruction()
            case "3":
                print("Goodbye! Thanks for playing.")
                break
            case _:
                print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()

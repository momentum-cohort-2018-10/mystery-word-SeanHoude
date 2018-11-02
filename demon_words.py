import os
import sys
import random


# import words.txt
dictionary_file = open("words.txt", 'r')
dictionary = dictionary_file.readlines()
dictionary_file.close()


remaining_tries = 8
word_bank = []
game_loop = "Y"
unguessed = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
mystery_word = ""
win_condition = False
has_letter = []
not_has_letter = []


wordbank = ['heal', 'love', 'toes', 'cast', 'heel', 'deer', 'reel', 'healthy', 'reel', 'plea', 'peal', 'fast', 'east', 'hull', 'will', 'ship', 'peel']

def accept_letter(guess, word_bank):
    for word in word_bank:
        if guess in word:
            has_letter.append(word)
        else:
            not_has_letter.append(word)
    if len(has_letter) > len(not_has_letter):
        word_bank = has_letter
    else:
        word_bank = not_has_letter

    print(word_bank, "from accept_letter")
    return word_bank


def check_num_letters(guess, word_bank):
    print(f"inside checknum {word_bank}")
    for word in word_bank:
        print(word)
        num_letters = 0
        for letter in word:
            if letter == guess:
                num_letters += 1
                print(num_letters)
        if num_letters > 1:
            print(f'removing {word}')
            word_bank.remove(word)
    return word_bank


letter_guess = "e"

print(check_num_letters(letter_guess, accept_letter(letter_guess, wordbank)))

def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def grab_words(length):
    """Select words with a specified range of lengths from the dictionary. Clean and store them in word_bank."""
    for word in dictionary:
        word = word.strip()
        if len(word) == int(length):
            word_bank.append(word)


def display():
    """Prints the remaining letters, The hidden and revealed characters, the num of guesses remaining, """
    clearscreen()
    print(" ".join(unguessed))
    revealed = ""
    for letter in mystery_word.upper():
        if letter in unguessed:
            revealed += " _"
        else:
            revealed += " " + letter
    print(f"\n{revealed}\n")
    if remaining_tries > 1:
        print(f"You have {remaining_tries} guesses left\n")
    else:
        print(f"You have {remaining_tries} guess left\n")
    # print(f"debug mode: the answer is **  {mystery_word}  **\n")
    if remaining_tries == 0:
        print("You have lost!!!\n")
        print(f"the answer was *** {mystery_word} ***\n")
    if win_condition:
        print("You have won the game!!!\n")


def accept_letter(guess):
    for word in wordbank:
        if guess in word:
            has_letter.append(word)
        else:
            not_has_letter.append(word)
    if len(has_letter) > len(not_has_letter):
        word_bank = has_letter
    else:
        word_bank = not_has_letter

def check_num_letters(guess):
    for word in word_bank:
        for letter in word:
            num_letters = 0
            if letter == guess:
                num_letters += 1
        if num_letters > 1:
            word_bank.remove(word)

    guess.lower() not in mystery_word:
                    remaining_tries -= 1
                unguessed.remove(guess)
# Choose difficulty and create list of words with appropriate lengths
while game_loop == "Y":
    while True:
        clearscreen()
        difficulty = input("Welcome to the game of ** Demon Word ** ! Please select a difficulty level:\n( 1 / 2 / 3 ): ")
        if difficulty not in "123" or len(difficulty) > 1:
            print("Please try again")
            continue
        else:
            print(f"You've selected difficulty level: {difficulty}\n")
            if difficulty == "1":
                print("Easy mode - Please enjoy a relaxing game ( *evil grin* )")
                grab_words(4)
                break
            elif difficulty == "2":
                print("Normal mode - A moderate difficulty for an even-paced experience ( *evil grin* )")
                grab_words(6)
                break
            else:
                print("Hard mode - I see you like a challenge. Alright! Game on!!! ( *evil grin* )")
                grab_words(8)
                break
    input("\nPress enter to continue...")

# move on if game won or lost, else recycle display and resume game
    while True:
        display()
        if remaining_tries == 0 or win_condition:
            break


# Game logic for when win or lose conditions are met
        while True:
            if remaining_tries == 0:
                break
            answer = [x for x in mystery_word.upper()]
            win = (set(unguessed) & set(answer))
            if not win:
                win_condition = True
                break

# request and accept user guesses
            guess = input("Please enter a letter: ").upper()
            if guess not in unguessed or len(guess) > 1:
                print("That's not a valid answer. Please try again!!!")
                continue
            else:
                if guess.lower() not in mystery_word:
                    remaining_tries -= 1
                unguessed.remove(guess)
                break

# After game win/loss, ask player if they would like to play again.
# If yes, re-initialize variables and return to top of loop
    while game_loop == "Y":
        game_loop = input("Would you like to play again? (y/n): ").upper()
        if game_loop not in "YN" or len(game_loop) > 1:
            print("please enter a valid answer")
            continue
        elif game_loop == "N":
            print("Thanks for playing!")
            sys.exit()
        else:
            win_condition = False
            difficulty_loop = "Y"
            remaining_tries = 8
            unguessed = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
            break

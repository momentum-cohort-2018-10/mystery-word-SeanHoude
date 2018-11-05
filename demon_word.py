import os
from collections import defaultdict

# Grab words from words.txt, copy them line by line, stripping whitespace and uppercasing into a list
with open("words.txt", 'r', buffering=20000000) as f:
    all_words = [line.strip('\n').upper() for line in f]

word_bank = all_words.copy()
unguessed = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
remaining_tries = 8
revealed = defaultdict(list)
sublibraries = defaultdict(int)
# Control flow variables
playing = True
not_won = True
resume_algorithm = False


def grab_words(_word_bank):
    """ Filter words in word_bank by length """
    selected_words = []
    temp = (x for x in _word_bank if len(x) == difficulty)
    for word in temp:
        selected_words.append(word)
    return selected_words


def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display():
    """ Prints unguessed letters, and hidden and revealed characters """
    clearscreen()
    print(" ".join(unguessed))
    reveal = "\n "
    for i in range(0, difficulty):
        if i in revealed:
            reveal += f" {revealed[i]}"
        else:
            reveal += " _"
    print(reveal, "\n")


def accept_letter(_word_bank, _remaining_tries, _unguessed, _resume_algorithm):
    """ 
    creates two lists, one of words containing the guess, one 
    without and compares length. If more without letter, player
    loses a guess and loop starts over, else return with letter
    """
    has_letter = []
    missing_letter = []
    temp = (x for x in _word_bank if guess in x)
    for word in temp:
        has_letter.append(word)
    temp2 = (x for x in _word_bank if guess not in x)
    for word in temp2:
        missing_letter.append(word)
    if len(has_letter) > len(missing_letter):
        _unguessed.remove(guess)
        _resume_algorithm = True
        return has_letter, _remaining_tries, _unguessed, _resume_algorithm
    else:
        print(f"""There are no " {guess}'s " in the word. *evil grin*""")
        _remaining_tries -= 1
        _unguessed.remove(guess)
        _resume_algorithm = False
        return missing_letter, _remaining_tries, _unguessed, _resume_algorithm


def generate_sublibraries(_word_bank, _sublibraries):
    """ Populate sublibraries dictionary with keys matching revealed letters and the number of times seen """
    magical_words_generator = (x for x in _word_bank)
    _sublibraries = defaultdict(int)
    for word in magical_words_generator:
        sublibrary_key = ""
        for letter in word:
            if letter in guess:
                sublibrary_key += guess
            else:
                sublibrary_key += "_"
        _sublibraries[sublibrary_key] += 1
    return _sublibraries


def apply_sublibrary(choose_sublibrary, _word_bank, _revealed):
    """
    Re-iterates through list to find the words which match the
    sublibrary key with most words and overwrites them to word_bank.
    Also appends revealed letters and their indexes to 'revealed'
    """
    magical_words_generator = (x for x in _word_bank)
    key_to_match = choose_sublibrary()
    matches_key = []
    for word in magical_words_generator:
        sublibrary_key = ""
        for letter in word:
            if letter in guess:
                sublibrary_key += guess
            else:
                sublibrary_key += "_"
        if key_to_match == sublibrary_key:
            matches_key.append(word)
    for i in range(0, difficulty):
        if key_to_match[i] != "_":
            _revealed[i] = key_to_match[i]
    print(key_to_match)
    return matches_key, _revealed


def choose_sublibrary():
    """ Compares length of values in sublibraries. returns key with highest lengths """
    most_words_key = ""
    most_words_value = 0
    for key, value in sublibraries.items():
        if value > most_words_value:
            most_words_value = value
            most_words_key = key
    return most_words_key


def show_remaining_guesses():
    """ 
    Prints remaining guesses to screen, checks for win/loss
    and prints appropriate message. returns False when game is
    won, else True. Used with the not_won variable
    """
    if remaining_tries == 0:
        print("You have lost!!!\n")
        if len(word_bank) == 1:
            print(f"The answer was {word_bank[0]}")
        else:
            print("You weren't even close to finding out the word!!! *maniacal cackle*")
        return False
    else:
        if win_condition():
            print("You have won the game!!! Quite frankly I don't know how you did it... \n")
            return False
        if remaining_tries > 1:
            print(f"You have {remaining_tries} guesses left\n")
            return True
        else:
            print(f"You have {remaining_tries} guess left\n")
            return True
        
    
def win_condition():
    """ Check if word bank has only 1 possible word in it. If so, checks if all letters in word have been guessed """
    if len(word_bank) == 1:
        answer = [x for x in word_bank[0].upper()]
        print("".join(answer))
        print("".join(unguessed))
        if (set(unguessed) & set(answer)):
            return False
        else:
            return True
    else:
        return False


# Master loop for if player wants to continue playing
while playing:
    # request user to input a difficulty, grab words of specified length from word_bank
    while True:
        print("\nWelcome to the game of Demon Word. Please enjoy this totally 'fair' experience... *evil grin*\n")
        difficulty = input("Please select the length of word to guess (3-15): ")
        try:
            difficulty = int(difficulty)
            if difficulty not in list(range(3, 16)):
                print("Please enter a valid response. I'll wait...\n")
                continue
            else:
                display()
                not_won = show_remaining_guesses()
                word_bank = grab_words(word_bank)
                break
        except:
            print("Please enter a valid response. I'll wait...\n")
            continue


# while game not won, request user to input guess and run algorithm to choose words and display letters
    while not_won:
        guess = input("Please enter a letter: ").upper()
        if guess not in "".join(unguessed) or len(guess) > 1:
            print("Please enter a valid response. I'll wait...\n")
            continue
        else:
            (word_bank, remaining_tries, unguessed, resume_algorithm) = accept_letter(word_bank, remaining_tries, unguessed, resume_algorithm)
            if resume_algorithm:
                sublibraries = generate_sublibraries(word_bank, sublibraries)
                (word_bank, revealed) = apply_sublibrary(choose_sublibrary, word_bank, revealed)
            display()
            not_won = show_remaining_guesses()

    while True:
        play_again_input = input("Would you like to play again? (y/n): ").upper()
        if play_again_input == "Y":
            # Re-initialize variables and word bank so new game starts fresh!
            clearscreen()
            word_bank = all_words.copy()
            unguessed = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            remaining_tries = 8
            revealed.clear()
            revealed = defaultdict(list)
            sublibraries.clear()
            sublibraries = defaultdict(int)
            not_won = True
            break
        elif play_again_input == "N":
            print("Thanks for playing!!\n\n*evil grin*")
            playing = False
            break
        else:
            print("Please enter a valid response. I'll wait...")
            continue

# The following are notes on the difficulties I faced while working on this program. They are rambles and are intended to remind me of what was going on in my head. I intend to reference them when I build my portfolio.
# --- Problems ---
# - MemoryErrors - solved by looking up the term and then learning and implementing buffering and generators.
# - variables not available inside functions - solved by return statements and had to determine how to return two values. Remembered tuple unpacking and tried to see if i could unpack two return values into a tuple. you can!
# - terminal emulation issues with clearscreen function - solved by using a different terminal
# - constant issues with calculations not returning expected values - debugged using print statements inside of each level of loops, sometimes by inspecting libraries themselves. moving counter variables to different levels of the loop usually solved the issues.
# - struggled to find a way to return both the letter and the index value when a guess was revealed. thought about using tuples and tuple unpacking again, but then realized i could just use a dictionary! So much simpler.
# - could not make a function that removes words with the same letter more than once. Every time i ran the function it would remove words, but always left some behind which got skipped. Tried about 10 different things, rewrote multiple times, used append vs/remove. Nothing worked. had to scrap the idea and come up with some other way to pick words. decided to count the num of instances of each letter and their indexes using a dictionary and counting.
# - Struggled a lot with control flow. Had to rearrange statements and function calls to make sure that the right functions were being run at the right time. Lots of diagnostic print statements and painstakingly scanning code helped to find the issues. Will seriously need to work on code organization!

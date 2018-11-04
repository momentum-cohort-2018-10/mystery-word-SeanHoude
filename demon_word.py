import sys
from collections import defaultdict


with open("words.txt", 'r', buffering=20000000) as f:
    all_words = [line.strip('\n').upper() for line in f]

word_bank = all_words.copy()
unguessed = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
remaining_tries = 12
revealed = defaultdict(list)
sublibraries = defaultdict(int)
playing = True
# guess = None
not_won = True
resume_algorithm = None


def grab_words(difficulty_length, remaining_words):
    """ Filter words in word_bank by length """
    selected_words = []
    temp = (x for x in remaining_words if len(x) == difficulty_length)
    for word in temp:
        selected_words.append(word)
    print(f"Grabbed {len(selected_words)} words from inside *grab_words* function")
    return selected_words


def generate_sublibraries(letter_guess, remaining_words, sublibrary_dict):
    """ Populate sublibraries dictionary with keys matching revealed letters, then counting each time that key is seen """
    magical_words_generator = (x for x in remaining_words)
    sublibrary_dict = defaultdict(int)
    for word in magical_words_generator:
        sublibrary_key = ""
        for letter in word:
            if letter in letter_guess:
                sublibrary_key += letter_guess
            else:
                sublibrary_key += "_"
        sublibrary_dict[sublibrary_key] += 1
    print(f"sublibraries: {sublibrary_dict}")
    return sublibrary_dict


def display():
    """ Prints unguessed letters, and hidden and revealed characters """
    # clearscreen()
    print(" ".join(unguessed))
    reveal = "\n "
    for i in range(0, difficulty):
        if i in revealed:
            reveal += f" {revealed[i]}"
        else:
            reveal += " _"
    print(reveal, "\n")
    # show_remaining_guesses()


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
        return False
    else:
        if remaining_tries > 1:
            print(f"You have {remaining_tries} guesses left\n")
            return True
        else:
            print(f"You have {remaining_tries} guess left\n")
            return True
        if win_condition():
            print("You have won the game!!!\n")
            return False
    


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


def accept_letter(guessed_letter, remaining_words, guesses_left, remaining_guesses, resume):
    """ 
    creates two lists, one of words containing the guess, one 
    without and compares length. If more without letter, player
    loses a guess and loop starts over, else return with letter
    """
    has_letter = []
    missing_letter = []
    temp = (x for x in remaining_words if guessed_letter in x)
    for word in temp:
        has_letter.append(word)
    temp2 = (x for x in remaining_words if guessed_letter not in x)
    for word in temp2:
        missing_letter.append(word)
    print(len(has_letter), "has letter - from inside *accept_letter* function")
    print(len(missing_letter), "missing letter - from inside *accept_letter* function")
    if len(has_letter) > len(missing_letter):
        remaining_guesses.remove(guessed_letter)
        resume = True
        return has_letter, guesses_left, remaining_guesses, resume
    else:
        print(f"""There are no "{guessed_letter}'s" in the word. *evil grin*""")
        guesses_left -= 1
        remaining_guesses.remove(guessed_letter)
        resume = False
        return missing_letter, guesses_left, remaining_guesses, resume


def choose_sublibrary():
    """ Compares length of values in sublibraries. returns highest lengths key """
    most_words_key = ""
    most_words_value = 0
    for key, value in sublibraries.items():
        if value > most_words_value:
            most_words_value = value
            most_words_key = key
    return most_words_key


def apply_sublibrary(choose_sublibrary_function, letter_guess, remaining_words, revealed_letters):
    """
    Re-iterates through list to find the words which match the
    sublibrary key with most words and overwrites them to word_bank.
    Also pastes revealed letters and their indexes to revealed
    """
    magical_words_generator = (x for x in remaining_words)
    key_to_match = choose_sublibrary_function()
    print(f"from apply_sublibrary, key to match = {key_to_match}")
    matches_key = []
    for word in magical_words_generator:
        sublibrary_key = ""
        for letter in word:
            if letter in letter_guess:
                sublibrary_key += letter_guess
            else:
                sublibrary_key += "_"
        if key_to_match == sublibrary_key:
            matches_key.append(word)
    for i in range(0, difficulty):
        if key_to_match[i] != "_":
            revealed[i] = key_to_match[i]
    return matches_key, revealed_letters


while playing:
    while True:
        difficulty = input("Please select the length of word to guess (3-15): ")
        try:
            difficulty = int(difficulty)
            print("")
            if difficulty not in list(range(3, 16)):
                print("Please enter a valid response!!\n")
                continue
            else:
                display()
                break
        except:
            print("Please enter a valid response!!\n")
            continue

    word_bank = grab_words(difficulty, word_bank)

    while not_won:
        guess = input("Please enter a letter: ").upper()
        if guess not in "".join(unguessed) or len(guess) > 1:
            print("Please enter a valid response!!\n")
            continue
        else:
            (word_bank, remaining_tries, unguessed, resume_algorithm) = accept_letter(guess, word_bank, remaining_tries, unguessed, resume_algorithm)
            print(len(word_bank), "current length of word_bank")
            if resume_algorithm:
                sublibraries = generate_sublibraries(guess, word_bank, sublibraries)
                (word_bank, revealed) = apply_sublibrary(choose_sublibrary, guess, word_bank, revealed)
            display()
            not_won = show_remaining_guesses()

    while True:
        play_again_input = input("Would you like to play again? (y/n): ").lower()
        if play_again_input == "y":
            word_bank = all_words.copy()
            unguessed = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            remaining_tries = 12
            revealed.clear()
            revealed = defaultdict(list)
            sublibraries.clear()
            sublibraries = defaultdict(int)
            # difficulty = None
            not_won = True
            break
        if play_again_input == "n":
            print("Thanks for playing!!\n\n*evil grin*")
            playing = False
            break
        else:
            continue


###### accept letter needs to call the next function only if it is a winning guess.

# print(word_bank)



# word_bank_gen = (x for x in word_bank)

# word_bank_generator = word_bank_gen
# print(list(word_bank_gen))

# for word in word_bank_gen:
#     print(word)


# Problems
# - MemoryErrors - solved by looking up the term and then learning and implementing buffering and generators.
# - variables not available inside functions - solved by return statements and had to determine how to return two values. Remembered tuple unpacking and tried to see if i could unpack two return values into a tuple. you can!
# - terminal emulation issues with clearscreen function - solved by using a different terminal
# - constant issues with calculations not returning expected values - debugged using print statements inside of each level of loops, sometimes by inspecting libraries themselves. moving counter variables to different levels of the loop usually solved the issues.
# - struggled to find a way to return both the letter and the index value when a guess was revealed. thought about using tuples and tuple unpacking again, but then realized i could just use a dictionary! So much simpler.
# - could not make a function that removes words with the same letter more than once. Every time i ran the function it would remove words, but always left some behind which got skipped. Tried about 10 different things, rewrote multiple times, used append vs/remove. Nothing worked. had to scrap the idea and come up with some other way to pick words. decided to count the num of instances of each letter and their indexes using a dictionary and counting.
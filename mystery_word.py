import random
import os

dictionary_file = open("words.txt", 'r')
dictionary = dictionary_file.readlines()
dictionary_file.close()

remaining_tries = 8
hidden_words = []
game_loop = "Y"
not_guessed = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
difficulty_loop = "Y"
exit_program = False
input_loop = True
mystery_word = ""
win_condition = False

def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def grab_words(lower_limit, upper_limit):
    for word in dictionary:
        word = word.strip()
        if len(word) in range(lower_limit, upper_limit):
            hidden_words.append(word)

def display():
    print(" ".join(not_guessed))
    revealed = ""
    for letter in mystery_word.upper():
        if letter in not_guessed:
            revealed += " _"
        else:
            revealed += " " + letter
    print(revealed)



# def win_lose():
#     pass


while game_loop.upper() == "Y":
    while difficulty_loop.upper() == "Y":
        difficulty = input("Welcome to the game of Mystery Word! Please select a difficulty level (1/2/3): ")
        if difficulty not in "123" or len(difficulty) > 1:
            print("Please try again")
            continue
        else:
            print(f"you've selected difficulty level: {difficulty}")
            if difficulty == "1":
                grab_words(4,6)
                mystery_word = random.choice(hidden_words)
                difficulty_loop = "N"
            elif difficulty == "2":
                grab_words(6,8)
                mystery_word = random.choice(hidden_words)
                difficulty_loop = "N"
            else:
                print("Uh oh, things are about to get real!!!")
                grab_words(8,20)
                mystery_word = random.choice(hidden_words)
                difficulty_loop = "N"

    while remaining_tries > 0:
        if win_condition == True:
            break

        print(f"debug mode: the answer is **  {mystery_word}  **")
        clearscreen()
        display()

        while True:
            if remaining_tries == 0:
                print("You have lost!!!")
                break
            answer = [x for x in mystery_word.upper()]
            win = ((set(not_guessed) & set(answer)))
            if not win:
                print("You have won the game!!!")
                win_condition = True
                break
            print(f"You have {remaining_tries} guesses left")
            guess = input("Please enter a letter: ")
            if guess.upper() not in not_guessed or len(guess) > 1:
                print("That's not a valid answer. Please try again!!!")
                continue
            else:
                if guess.lower() not in mystery_word:
                    remaining_tries -= 1
                not_guessed.remove(guess.upper())
                break


    while True:
        game_loop = input("Would you like to play again? (y/n): ")
        if game_loop.upper() not in "YN" or len(game_loop) > 1:
            print("please enter a valid answer")
            continue
        else:
            win_condition = False
            difficulty_loop = "Y"
            remaining_tries = 8
            not_guessed = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
            break

print("Final message")
clearscreen()

#tell me ive lost



# dictionary_file.close()
#
# # look up with content manager
# # for really large files
# students = []
# with open('students.txt') as student_file:
#     student = student_file.readline()
#     while student:
#         students.append(student)
#         student = student_file.readline()
#
#
# # for smaller files
# with open('students.txt') as student_file:
#     for student in student_file.readlines():
#         students.append(student.strip())
#
# print(random.choice(students))

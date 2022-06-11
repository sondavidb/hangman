# CLI game for Hangman

import logic.hangman as hangman
import time

# Plays a singular game of hangman 
def playGame():

    #
    # Setup
    #

    print("\nHow long is your word?")
    length = input()
    valid = False

    while not valid:
        if length.isdigit():
            length = int(length)
            if length > 0:
                valid = True
            else:
                print("Please give a valid input (integer greater than 0)")
                length = input()
        else:
            print("Please give a valid input (integer greater than 0)")
            length = input()

    print("How many mistakes am I allowed? (standard is 6)")
    maxMistakes = input()
    valid = False

    while not valid:
        if maxMistakes.isdigit():
            maxMistakes = int(maxMistakes)
            if maxMistakes > 0:
                valid = True
            else:
                print("Please give a valid input (integer greater than 0)")
                maxMistakes = input()
        else:
            print("Please give a valid input (integer greater than 0)")
            maxMistakes = input()

    print("Setting up. Please stand by...")
    start = time.time()

    hangman.resetWordChoices(length)
    hangman.resetLetterChoices()

    # guessedWord is some combination of the actual word and the * character
    # Actual letters are put where they should be, 
    # and *s are put in place of when we don't know
    # e.g. if the word was "apple", but we only knew the letters 
    # 'a' and 'l', word would be represented as "a**l*"
    # By default it's a string of stars that is the length of the word 
    # Long explanation for a simple concept but wording is hard
    guessedWord = '*' * length
    mistakes = 0

    print("Setup finished in " + str(time.time() - start) + " seconds.")
    
    #
    # Game Start
    #

    print("Let's get started!")

    # Each loop is one round of the game
    while '*' in guessedWord \
            and len(hangman.wordChoices) > 1 and mistakes < maxMistakes:
        print("\nCurrent word: " + str(guessedWord))
        print("Mistakes made: " + str(mistakes))
        
        print("Guessing best letter...")
        start = time.time()
        letter = hangman.guess()
        print("Figured optimal letter to guess in " +
            str(time.time() - start) + " seconds.")

        print("Does your word have the letter " + letter + 
            "? (type y or yes for yes, n or no for no)")
        isCorrect = input().lower()

        while (isCorrect != "y" and isCorrect != "yes"
            and isCorrect != "n" and isCorrect != "no"):
            print("Invalid input. Please type y or yes for yes, "\
                "n or no for no")
            isCorrect = input().lower()

        if isCorrect == "y" or isCorrect == "yes":
            print("Please tell me in what position(s) your letter is in. " \
                "When you're done, type done.\n(e.g. if your word is 'apple' " \
                "and I guessed p, you would enter 2, then 3, then done)")
            pos = input().lower()
            posArr = [] # Keep track of the positions of where the letter is

            while pos != "done":
                if pos.isdigit():
                    pos = int(pos)

                    if pos > 0 and pos <= length:
                        pos -= 1
                        if guessedWord[pos] != "*" or pos in posArr:
                            print("That position is already filled in!")
                        else:
                            posArr.append(pos)
                    else:
                        print("Please give a valid input (integer greater " \
                            "than 0 " "and less than " + str(length + 1) + ")")
                else:
                    print("Please give a valid input (integer greater than 0 " \
                            "and less than " + str(length + 1) + ")")

                pos = input()

            for i in range(length):
                if i in posArr:
                    guessedWord = guessedWord[:i] + letter \
                        + guessedWord[i + 1:]
                    hangman.setWordChoices( \
                        hangman.makeListWithLetter(letter, i))
                else:
                    hangman.setWordChoices( \
                        hangman.makeListWithoutLetter(letter, i))
            
        else:
            hangman.setWordChoices( \
                hangman.makeListWithoutLetter(letter, -1))
            mistakes += 1

    #
    # Game end
    #

    if not hangman.wordChoices:
        print("Sorry, your word wasn't in the dictionary.")
    elif mistakes >= maxMistakes:
        print("Ran out of tries! You win!")
    else:
        if len(hangman.wordChoices) == 1:
            guessedWord = hangman.wordChoices[0]
        print("Your word is " + guessedWord + "! I win!")

    print("\nGame over!")
    print("Mistakes made: " + str(mistakes))

# Master function. Starts hangman and keeps playing
# till the user doesn't want to anymore.
def playHangman():
    hangman.initializeDictionary() # Create the initial dictionary
    play = "y" # Will be anything besides "y" when user no longer wants to play
    print("Welcome to hangman! Think of a word and I'll try to guess it.")
    
    while play == "y":
        playGame()
        print("\nWanna play again? (Type y for yes, anything else for no.")
        play = input().lower()

    input("Thanks for playing!\nPress enter to exit.")

# Play the game
def main():
    playHangman()

if __name__ == "__main__":
    main()

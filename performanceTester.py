# Analysis of the algorithm's performance with the following metrics:
# time spent to guess word
# number of correct and incorrect guesses

import logic.hangman as hangman

import pandas as pd
import random
import time

wordInfo = []

# Runs guesses on the word and adds to the global list of dicts
def guessWord(word):

    #
    # Setup
    #

    length = len(word)
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
    correctGuesses = 0
    incorrectGuesses = 0
    
    #
    # Game Start
    #

    # Each loop is one guess
    while '*' in guessedWord and len(hangman.wordChoices) > 1:
        letter = hangman.guess()
        if letter in word:
            correctGuesses += 1
            for i in range(length):
                if word[i] == letter:
                    guessedWord = guessedWord[:i] + letter \
                        + guessedWord[i + 1:]
                    hangman.setWordChoices( \
                        hangman.makeListWithLetter(letter, i))
                else:
                    hangman.setWordChoices( \
                        hangman.makeListWithoutLetter(letter, i))
            
        else:
            incorrectGuesses += 1
            hangman.setWordChoices( \
                hangman.makeListWithoutLetter(letter, -1))

    #
    # Game end
    #

    if not hangman.wordChoices:
        wordInfo.append({
            "word": word,
            "time elapsed": time.time() - start,
            "letters guessed correctly": "N/A",
            "letters guessed incorrectly": "N/A"
            })
    else:
        wordInfo.append({
            "word": word,
            "time elapsed": time.time() - start,
            "letters guessed correctly": correctGuesses,
            "letters guessed incorrectly": incorrectGuesses
            })

# Master function. Starts hangman and keeps playing
# till the user doesn't want to anymore.
def performAnalysis():
    hangman.initializeDictionary() # Create the initial dictionary
    print("Welcome to hangman benchmark tool!" \
        "This script is to see the effectiveness of the algorithm used.\n" \
        "All data will be output to data.csv. " \
        "Each line represents one word. ")

    print("How many words would you like to do? " \
        "(Enter max to do whole dictionary)")
    numWords = input().lower()
    valid = False
    maxLen = len(hangman.dictionary)

    while not valid:
        if numWords.isdigit():
            numWords = int(numWords)
            if numWords > 0:
                valid = True
            else:
                print("Please give a valid input (integer greater than 0 " \
                    "and less than " + str(maxLen) + ")")
                numWords = input()
        elif numWords == "max":
            numWords = maxLen
        else:
            print("Please give a valid input (integer greater than 0 " \
                "and less than " + str(maxLen) + ")")
            numWords = input()

    wordsTested = random.sample(hangman.dictionary, numWords)

    csvCols = ["word", "time elapsed", \
        "letters guessed correctly", "letters guessed incorrectly"]
    
    start = time.time()
    print("Performing analysis...")

    for word in wordsTested:
        guessWord(word)

    print("Analysis complete in " + str(time.time() - start) + " seconds!")
    print("Writing to data.csv...")

    test = time.time()

    df = pd.DataFrame.from_dict(wordInfo) 
    df.to_csv (r'data.csv', index = False, header=True)

    print("Written to file in " + str(time.time() - test) + " seconds!")
    input("Done! Press enter to exit.")

# Play the game
def main():
    performAnalysis()

if __name__ == "__main__":
    main()

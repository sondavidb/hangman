# Logic behind hangman

import copy
import time

#
# Constants
#

# Most commonly used letters in words the English alphabet, 
# from most common to least common (how many words contain these letters, 
# not how often they appear in words)
FREQUENCY = ['e', 'i', 'a', 'n', 'o', 'r', 's', 't', 'l', 'c', 'u', 'd',
    'p', 'm', 'h', 'g', 'y', 'b', 'f', 'v', 'k', 'w', 'z', 'x', 'q', 'j']

#
# Variables
#

# Should I use global variables in normal settings? No.
# Should I refactor it? Yes!
# Will I? Probably not : ^)

# Our comprehensive dictionary (something something
# this isn't a dictionary in Python terms - I know
# but bear with me pls :>)
dicitonary = []
wordChoices = [] # Possible words based on the information given from the word

# alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
#   'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] 
letterChoices = [] # Letter candidates for removing

# ----------------------------------------------------------------------

#
# Helper functions
#

# Creates initial dictionary and returns it
def initializeDictionary():
    global dictionary
    fin = open("logic/dictionary.txt", "r") # 370104 words!!
    dictionary = [word.strip() for word in fin.readlines()]
    fin.close()

# Resets list of word choices to only have
# words of length length (taken from dictionary)
def resetWordChoices(length):
    global wordChoices
    wordChoices = []
    for word in dictionary:
        if len(word) == length:
            wordChoices.append(word)

# Reset list of letters to its original state
# (the entire alphabet in order of FREQUENCY)
def resetLetterChoices():
    global letterChoices
    letterChoices = copy.deepcopy(FREQUENCY)

# Changes the global wordChoices variable
# The letter choices are always removed individually so 
# it's less intuitive to make a separate function for those
def setWordChoices(lst):
    global wordChoices
    wordChoices = lst


# The next two functions take the same parameters.
# letter - character type. Letter to be used for list pruning
# pos - integer type. Position to remove letter from.
# If -1, remove any instance of it.

# Make a list of words without given letter
def makeListWithoutLetter(letter, pos):
    newlst = []

    if pos == -1:
        for word in wordChoices:
            if letter not in word:
                newlst.append(word)
    
    else:
        for word in wordChoices:
            if letter != word[pos]:
                newlst.append(word)

    return newlst

# Make a list of word with given letter
def makeListWithLetter(letter, pos):
    newlst = []

    if pos == -1:
        for word in wordChoices:
            if letter in word:
                newlst.append(word)
    else:
        for word in wordChoices:
            if letter == word[pos]:
                newlst.append(word)

    return newlst

# ----------------------------------------------------------------------

#
# Logic functions
#

# Based on the available choices, 
# finds the best letter to guess and returns it
def findOptimalLetter():
    global letterChoices
    listSizes = {} # The length of each list made by removing
    # any words with the given letter
    removeList = []

    # TODO - find a more efficient method xd
    for letter in letterChoices:
        lst = makeListWithoutLetter(letter, -1)
        
        if len(lst) == len(wordChoices):
            # Letter does not show up in remaining words
            removeList.append(letter)
        else:
            listSizes[letter] = len(lst)

    for letter in removeList:
        letterChoices.remove(letter)
    # Sorts by num words left in ascending order
    listSizes = sorted(listSizes.items(), key=lambda item: item[1])

    # Get the smallest value
    bestLetter = listSizes[0][0]

    return bestLetter

# Guesses a letter and removes it from the list of possible letters, 
# then returns the letter
def guess():
    global letterChoices
    letter = findOptimalLetter()
    letterChoices.remove(letter)
    return letter

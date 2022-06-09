# Inspired by the following video:
# https://www.youtube.com/watch?v=le5uGqHKll8

# This program is the guesser in a game of hangman.
# Give it the length of your word, and it will guess
# which word you're thinking of.

# Make sure your is in the following dictionary:
# https://github.com/dwyl/english-words/blob/master/words_alpha.txt

# In the future I plan to optimize the algorithm used
# and make a more intuitive interface
# bc a console-line game is really not that fun

# ----------------------------------------------------------------------

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
#	'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] 
letterChoices = [] # Letter candidates for removing

# ----------------------------------------------------------------------

#
# Helper functions
#

# Creates initial dictionary and returns it
def initializeDictionary():
	global dictionary
	fin = open("dictionary.txt", "r") # 370104 words!!
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

# Fully resets the list of word choices to be the original dictionary.
# Never used as of now so commented out
# def fullResetWordChoices():
# 	global wordChoices
# 	wordChoices = dictionary.deepcopy()

# Reset list of letters to its original state
# (the entire alphabet in order of frequency)
def resetLetterChoices():
	global letterChoices
	letterChoices = copy.deepcopy(frequency)

# Changes the global wordChoices variable
# The letter choices are always removed individually so 
# it's less intuitive to make a separate function for those
def setWordChoices(lst):
	global wordChoices
	wordChoices = lst

# TODO - The below functions could definitely be consolidated
# to 1-2 functions

# Makes a list of words without the given letter and returns it
def makeListWithoutLetter(letter):
	newlst = []
	for word in wordChoices:
		if letter not in word:
			newlst.append(word)

	return newlst

# Makes a list of words without the given letter 
# in the given position and returns it
def makeListWithoutLetter(letter, pos):
	newlst = []
	for word in wordChoices:
		if letter != word[pos]:
			newlst.append(word)

	return newlst

# Makes a list of words with the given letter and returns it
def makeListWithLetter(letter):
	newlst = []
	for word in wordChoices:
		if letter in word:
			newlst.append(word)

	return newlst

# Makes a list of words with the given letter 
# in the given position and returns it
def makeListWithLetter(letter, pos):
	newlst = []
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
	global letterChoices # The length of each list made by removing
	# any words with the given letter
	listSizes = {}

	# TODO - find a more efficient method xd
	for letter in letterChoices:
		lst = makeListWithoutLetter(letter)
		if len(lst) == len(wordChoices):
			# Letter does not show up in remaining words
			letterChoices.remove(letter)
		else:
			listSizes[letter] = len(lst)

	# Sorts by num words left in ascending order
	listSizes = {k: v for k, v in sorted(listSizes.items(),
		key=lambda item: item[1])}
	# Get the smallest value
	bestLetter = next(iter(listSizes))

	return bestLetter

# Guesses a letter and removes it from the list of possible letters, 
# then returns the letter
def guess():
	global letterChoices
	start = time.time()
	letter = findOptimalLetter()
	letterChoices.remove(letter)

	print("Figured optimal letter to guess in " +
		str(time.time() - start) + " seconds.")
	return letter

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

	resetWordChoices(length)
	resetLetterChoices()

	# guessedWord is some combination of the actual word and the * character
	# Actual letters are put where they should be, 
	# and *s are put in place of when we don't know
	# e.g. if the word was "apple", but we only knew the letters 
	# 'a' and 'l', word would be represented as "a**l*"
	# By default it's a string of stars that is the length of the word 
	# Long explanation for a simple concept but wording is hard
	guessedWord = '*' * length
	mistakes = 0

	print("Setup finished in " + str(time.time() - start) + "seconds.")
	
	#
	# Game Start
	#

	print("Let's get started!")

	# Each loop is one round of the game
	while '*' in guessedWord and len(wordChoices) > 1 and mistakes < maxMistakes:
		print("\nCurrent word: " + str(guessedWord))
		print("Mistakes made: " + str(mistakes))
		
		print("Guessing best letter...")
		letter = guess()
		print("Does your word have the letter " + letter + 
			"? (type y or yes for yes, n or no for no)")
		isCorrect = input().lower()

		while (isCorrect != "y" and isCorrect != "yes"
			and isCorrect != "n" and isCorrect != "no"):
			print("Invalid input. Please type y or yes for yes, n or no for no")
			isCorrect = input().lower()

		if isCorrect == "y" or isCorrect == "yes":
			setWordChoices(makeListWithLetter(letter))
			print("Please tell me in what position(s) your letter is in." \
				"When you're done, type done.\n(e.g. if your word is 'apple'" \
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
						print("Please give a valid input (integer greater than 0 " \
							"and less than " + str(length + 1) + ")")
				else:
					print("Please give a valid input (integer greater than 0" \
							" and less than " + str(length + 1) + ")")

				pos = input()

			for i in range(length):
				if i in posArr:
					guessedWord = guessedWord[:i] + letter + guessedWord[i + 1:]
					setWordChoices(makeListWithLetter(letter, i))
				else:
					setWordChoices(makeListWithoutLetter(letter, i))
			
		else:
			setWordChoices(makeListWithoutLetter(letter))
			mistakes += 1

	#
	# Game end
	#

	if not wordChoices:
		print("Sorry, your word wasn't in the dictionary.")
	elif mistakes >= maxMistakes:
		print("Ran out of tries! You win!")
	else:
		if len(wordChoices) == 1:
			guessedWord = wordChoices[0]
		print("Your word is " + guessedWord + "! I win!")

	print("\nGame over!")
	print("Mistakes made: " + str(mistakes))

# Master function. Starts hangman and keeps playing
# till the user doesn't want to anymore.
def playHangman():
	initializeDictionary() # Create the initial dictionary
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

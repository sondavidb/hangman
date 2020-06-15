import copy
import time

# Inspired by the following video: https://www.youtube.com/watch?v=le5uGqHKll8
# This program is the guesser in a game of hangman. Give it the length of your word, and it will guess which word you're thinking of.
# Make sure your is in the following dictionary: https://github.com/dwyl/english-words/blob/master/words_alpha.txt
# In the future I plan to optimize the algorithm used and make a more intuitive interface

#
# variables
#

wordList = [] # Our comprehensive dictionary (something something this isn't a dictionary in Python terms - I know but bear with me pls :>)
wordChoices = [] # Possible words

# alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] 
letterChoices = [] # Candidates for removing 
frequency = ['e', 'i', 'a', 'n', 'o', 'r', 's', 't', 'l', 'c', 'u', 'd', 'p', 'm', 'h', 'g', 'y', 'b', 'f', 'v', 'k', 'w', 'z', 'x', 'q', 'j']
# Most commonly used letters in words the english alphabet, from most common to least common (how many words contain these letters, not how often they appear in words)

#
# functions`+
#

# Creates initial dictionary and returns it
def initializeWordList():
	global wordList
	fin = open("dictionary.txt", "r") # 370104 words!!
	wordList = [word.strip() for word in fin.readlines()]
	fin.close()

# Reset list of word choices to only have words of length length (taken from dictionary)
def resetWordChoices(length):
	global wordChoices
	wordChoices = []
	for word in wordList:
		if len(word) == length:
			wordChoices.append(word)


# Reset list of letters to its original state (the entire alphabet in order of frequency)
def resetLetterChoices():
	global letterChoices
	letterChoices = copy.deepcopy(frequency)

'''
# Limits wordChoices to only include words of length length
def getWordsOfLength():
	global wordChoices
	for word in wordChoices:
		if len(word) != length:
			wordChoices.remove(word)
'''

# Changes the global wordChoices variable 
def setWordChoices(lst):
	global wordChoices
	wordChoices = lst

# Removes any word if it has the given letter in it
def removeLetter(letter):
	global wordChoices
	for word in wordChoices:
		if letter in word:
			wordChoices.remove(word)

# Makes a list of words without the given letter and returns it
def makeListWithoutLetter(letter, pos):
	newlst = []
	for word in wordChoices:
		if letter != word[pos]:
			newlst.append(word)

	return newlst

# Makes a list of words without the given letter in the given position and returns it
def makeListWithoutLetterNoPos(letter):
	newlst = []
	for word in wordChoices:
		if letter not in word:
			newlst.append(word)

	return newlst

# Makes a list of words with the given letter in the given position and returns it
def makeListWithLetter(letter, pos):
	newlst = []
	for word in wordChoices:
		if letter == word[pos]:
			newlst.append(word)

	return newlst

# Makes a list of words with the given letter and returns it
def makeListWithLetterNoPos(letter):
	newlst = []
	for word in wordChoices:
		if letter in word:
			newlst.append(word)

	return newlst

# Based on the available choices, finds the best letter to guess and returns it
def findOptimalLetter():
	global letterChoices
	listSizes = {} # The length of each list made by removing any words with the given letter

	# TODO - find a more efficient method xd
	for letter in letterChoices:
		lst = makeListWithoutLetterNoPos(letter)
		if len(lst) == len(wordChoices): # This means the letter is not in any of the words
			letterChoices.remove(letter)
		else:
			listSizes[letter] = len(lst)

	listSizes = {k: v for k, v in sorted(listSizes.items(), key=lambda item: item[1])} # Sorts by key in ascending order
	bestLetter = next(iter(listSizes)) # Gets the first key in the newly sorted by length list
	# print(listSizes)

	return bestLetter

# Guesses a letter and removes it from the list of possible letters, then returns the letter
def guess():
	global letterChoices
	start = time.time()
	letter = findOptimalLetter()
	letterChoices.remove(letter)

	print("Figured optimal letter to guess in " + str(time.time() - start) + " seconds.")
	return letter

# Master function
def main():
	initializeWordList() # Create the initial dictionary
	play = "y" # Will be anything besides "Y" when user no longer wants to play
	print("Welcome to hangman! Think of a word and I'll try to guess it.")
	
	while play == "y":
		# Setup
		print("\nHow long is your word?")
		length = input()
		valid = False
		while not valid:
			if length.isdigit():
				length = int(length)
				if length > 0:
					valid = True
				else:
					print("Please give a valid input (integer greater than 0) ")
					length = input()
			else:
				print("Please give a valid input (integer greater than 0) ")
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
					print("Please give a valid input (integer greater than 0) ")
					maxMistakes = input()
			else:
				print("Please give a valid input (integer greater than 0) ")
				maxMistakes = input()

		print("Setting up. Please stand by...")
		start = time.time()

		resetWordChoices(length)
		resetLetterChoices()

		# guessedWord is some combination of the actual word and the * character
		# Actual letters are put where they should be, and *s are put in place of when we don't know
		# e.g. if the word was "apple", but we only knew the letters 'a' and 'l', word would be represented as "a**l*"
		# By default it's a string of stars that is the length of the word 
		# Long explanation for a simple concept but wording is hard

		guessedWord = '*' * length
		mistakes = 0

		print("Setup finished in " + str(time.time() - start) + "seconds.")
		
		# Game Start
		print("Let's get started!")

		while '*' in guessedWord and len(wordChoices) > 1 and mistakes < maxMistakes:
			print("\nCurrent word: " + str(guessedWord))
			print("Mistakes made: " + str(mistakes))
			print("Guessing best letter...")

			# print(wordChoices)
			letter = guess()
			print("Does your word have the letter " + letter + "? (type y for yes, anything else for no)")
			isCorrect = input().lower()

			if isCorrect == "y":
				setWordChoices(makeListWithLetterNoPos(letter))
				# print(wordChoices)
				print("Please tell me in what position(s) your letter is in. When you're done, type done.\n(e.g. if your word is 'apple' and I guessed p, you would enter 2, then 3, then done)")
				pos = input().lower()
				posArr = [] # Keep track of the positions of where the letter is

				# TODO: Make this look 10 times prettier god this hurts to look at
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
							print("Please give a valid input (integer greater than 0 and less than " + str(length + 1) + ")")
					else:
						print("Please give a valid input (integer greater than 0 and less than " + str(length + 1) + ")")

					pos = input()

				# print(posArr)
				for i in range(length):
					if i in posArr:
						guessedWord = guessedWord[:i] + letter + guessedWord[i + 1:]
						setWordChoices(makeListWithLetter(letter, i))
						# print(wordChoices)
					else:
						setWordChoices(makeListWithoutLetter(letter, i))
				
			else:
				setWordChoices(makeListWithoutLetterNoPos(letter))
				mistakes += 1


		# Game end
		# print(wordChoices)
		if not wordChoices:
			print("Sorry, your word wasn't in the dictionary.")
		elif mistakes >= maxMistakes:
			print("Ran our of tries! You win!")
		else:
			if len(wordChoices) == 1:
				guessedWord = wordChoices[0]
			print("Your word is " + guessedWord + "! I win!")

		print("\nGame over!")
		print("Mistakes made: " + str(mistakes))
		print("\nWanna play again? (Type y for yes, anything else for no.")
		play = input().lower()

	input("Thanks for playing!\nPress enter to exit.")

if __name__ == "__main__":
	main()

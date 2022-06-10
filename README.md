# hangman
Play hangman with your computer! Think of a word, give the computer its length, and it will try to guess your word.

Make sure your word only contains alphabet characters (no hyphens, spaces, colons, etc) and is in this file: https://github.com/dwyl/english-words/blob/master/words_alpha.txt

Based on the algorithm presented in this video (timestamped at 2:58): https://youtu.be/le5uGqHKll8?t=178

The process behind each guess can be summarized as follows:

1. Have list of all available words (in our case, the entire English dictionary)
2. Get all of the available letters to guess
3. For each letter:
    - Assume letter is not in word
    - Copy word list and prune it based on this assumption
4. Guess the letter that minimizes length of pruned word list

Also definitely looking into making this an actual interface and not a command-line game.

Prerequisites: Python 3.7+

06/15/20 - First push  
06/09/22 - Cleaned more code and separated logic and playfield into separate files  

Future plans:

- Add faster way to consider all possibilities
- Create graphical version
- Allow users to use their own dictionary or add words to an existing dictionary

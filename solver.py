# Solves a wordle using this api for wordle guesses
# https://github.com/k2bd/wordle-api

from apigrabber import guess_word
import re
import pandas as pd

allowed_words = open("allowed_words.txt", "r")
word_list = allowed_words. readlines()
word_list = [x.strip() for x in word_list]

letter_frequencies = pd.read_csv('letter_frequencies.txt', names=['letter', 'freq'], header=None)


initial_guess = 'crane'

state = ['.', '.', '.', '.', '.']
present = set()
absent = set()

def evaluate_guess(response):
	correct = 0
	for letter_data in response.json():
		if letter_data['result'] == 'present':
			present.add(letter_data['guess'])
		if letter_data['result'] == 'absent':
			absent.add(letter_data['guess'])
		if letter_data['result'] == 'correct':
			correct += 1
			state[letter_data['slot']] = '(' + letter_data['guess'] + ')'
	if correct == 5:
		return True
	return False

def list_new_guesses():
	r = re.compile(''.join(state))
	filtered_guesses = list(filter(r.match, word_list))
	for letter in present:
		filtered_guesses = list(filter(lambda x: letter in x, filtered_guesses))
	for letter in absent:
		filtered_guesses = list(filter(lambda x: letter not in x, filtered_guesses))
	
	guess_scores = []
	for guess in filtered_guesses:
		guess_scores.append((guess, score_guess(guess)))
		guess_scores.sort(key=lambda x: x[1], reverse=True)

	return guess_scores

def score_guess(guess):
	score = 0
	alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	for letter in alphabet:
		if letter not in absent and ('('+letter+')') not in state:
			if letter in guess:
				score += float(letter_frequencies[letter_frequencies.letter == letter].freq)
	return score


response = guess_word(initial_guess)
evaluate_guess(response)
new_guesses = list_new_guesses()



correct = False
while not correct:
	print('='*40)
	print('Guessing...', new_guesses[0])
	print('Present Letters:', present)
	print('Absent Letters:', absent)
	print('State:', state)
	current_guess = new_guesses[0][0]
	response = guess_word(current_guess) 					# Guesses from api
	correct = evaluate_guess(response)						# updates internal states
	new_guesses = list_new_guesses()						# generates a list of possible next words

print('='*40)
print('Word Guessed:', new_guesses[0][0])

# Solves a wordle using this api for wordle guesses
# https://github.com/k2bd/wordle-api

from apigrabber import guess_word
import re
import pandas as pd
from apigrabber import WordleScraper

class Solver():

	def __init__(self, initial_guess, headless=False, state=['.', '.', '.', '.', '.'], present=set(), absent=set(), guessed=set()):

		allowed_words = open("allowed_words.txt", "r")
		word_list = allowed_words.readlines()
		self.word_list = [x.strip() for x in word_list]

		self.letter_frequencies = pd.read_csv('letter_frequencies.txt', names=['letter', 'freq'], header=None)


		self.initial_guess = initial_guess

		self.state = state
		self.present = present
		self.absent = absent
		self.guessed_words = guessed

		self.guess_api = WordleScraper(headless)

	def evaluate_guess(self, response):
		correct = 0
		for letter_data in response:
			# print(letter_data)
			if letter_data['result'] == 'present':
				self.present.add(letter_data['guess'])
			if letter_data['result'] == 'absent':
				self.absent.add(letter_data['guess'])
			if letter_data['result'] == 'correct':
				correct += 1
				self.state[letter_data['slot']] = '(' + letter_data['guess'] + ')'
		if correct == 5:
			return True
		return False

	def score_guess(self, guess):
		score = 0
		alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
		for letter in alphabet:
			if letter not in self.absent and ('('+letter+')') not in self.state:
				if letter in guess:
					score += float(self.letter_frequencies[self.letter_frequencies.letter == letter].freq)
		return score

	def list_new_guesses(self):
		r = re.compile(''.join(self.state))
		filtered_guesses = list(filter(r.match, self.word_list))
		for letter in self.present:
			filtered_guesses = list(filter(lambda x: letter in x, filtered_guesses))
		for letter in self.absent:
			filtered_guesses = list(filter(lambda x: letter not in x, filtered_guesses))
		for word in self.guessed_words:
			filtered_guesses = list(filter(lambda x: word not in x, filtered_guesses))
		
		guess_scores = []
		for guess in filtered_guesses:
			guess_scores.append((guess, self.score_guess(guess)))
			guess_scores.sort(key=lambda x: x[1], reverse=True)

		return guess_scores


	def run(self):
		print('='*40)
		print('Guessing...', self.initial_guess)
		print('Present Letters:', self.present)
		print('Absent Letters:', self.absent)
		print('State:', self.state)
		# response = guess_word(self.initial_guess)
		guess_count = 1
		response = self.guess_api.guess_word(self.initial_guess, guess_count)
		correct = self.evaluate_guess(response)
		new_guesses = self.list_new_guesses()

		while not correct:
			guess_count += 1
			print('='*40)
			print('Guessing...', new_guesses[0])
			current_guess = new_guesses[0][0]
			# response = guess_word(current_guess) 					# Guesses from api
			response = self.guess_api.guess_word(current_guess, guess_count)
			print('evaluating guess...')
			correct = self.evaluate_guess(response)						# updates internal states
			print('generating list of new guesses...')
			new_guesses = self.list_new_guesses()						# generates a list of possible next words
			print('Present Letters:', self.present)
			print('Absent Letters:', self.absent)
			print('State:', self.state)
			if guess_count == 6:
				return new_guesses, self.state, self.present, self.absent, self.guessed_words


		print('='*40)
		print('Word Guessed in {} attempts:'.format(guess_count), new_guesses[0][0])
		# return new_guesses[0][0]
		return False,new_guesses[0][0],False,False,False




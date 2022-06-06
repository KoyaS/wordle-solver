import requests

def guess_word(word):
	if len(word) == 5:
		# payload = 'https://v1.wordle.k2bd.dev/daily?guess={}'.format(word)
		payload = 'https://v1.wordle.k2bd.dev/word/depth?guess={}'.format(word)
		response = requests.get(payload)
	else:
		print('word not 5 letters')

	return response




# guess_word('crane')
import requests
from selenium.webdriver.common.by import By
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def guess_word(word):
	if len(word) == 5:
		# payload = 'https://v1.wordle.k2bd.dev/daily?guess={}'.format(word)
		payload = 'https://v1.wordle.k2bd.dev/word/depth?guess={}'.format(word)
		response = requests.get(payload)
	else:
		print('word not 5 letters')

	return response


class WordleScraper():

	def __init__(self, headless=False):

		self.board = [
			[None, None, None, None, None],
			[None, None, None, None, None],
			[None, None, None, None, None],
			[None, None, None, None, None],
			[None, None, None, None, None],
			[None, None, None, None, None]
		]

		chrome_options = Options()
		if headless:
			chrome_options.add_argument("--headless")
		chrome_options.add_experimental_option("useAutomationExtension", False)
		chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
		driver_location = '/Users/koya/Documents/Development/Python/wordle-solver/chromedriver'
		self.driver = webdriver.Chrome(driver_location, options=chrome_options)
		self.driver.get("https://www.nytimes.com/games/wordle/index.html")

		actions = ActionChains(self.driver)
		actions.move_by_offset(100, 100).click().perform()

	def update_board_state(self):
		for i in range(6):
			for j in range(5):
				# print('='*40)
				
				# letter = self.driver.execute_script("return document.querySelector('html>body>game-app').shadowRoot.querySelector('game-theme-manager>div>div>div>:nth-child({row})').shadowRoot.querySelector('div>:nth-child({letter})')".format(row=i+1, letter=j+1)).get_attribute('letter')
				# letter = self.driver.execute_script("return document.querySelector('html>body>#wordle-app-game>div>div>:nth-child({row})').querySelector('div>:nth-child({letter})>div')".format(row=i+1, letter=j+1))
				letter = self.driver.execute_script("return document.querySelector('html>body>#wordle-app-game>div>div>:nth-child({row})').querySelector('div>div>:nth-child({l})>div')".format(row=i+1, l=j+1))
				# print(self.driver.execute_script("return document.querySelector('html>body>#wordle-app-game>div>div>:nth-child({row})')".format(row=i+1)).get_attribute('innerHTML'))
				# print(letter.get_attribute('innerHTML'))
				# print(letter.get_attribute('data-state'))

				if i == j:
					row_html = self.driver.execute_script("return document.querySelector('html>body>#wordle-app-game>div>div>:nth-child({row})')".format(row=i+1)).get_attribute('innerHTML')

					letter_html = row_html
					for z in range(j):
						letter_html = letter_html[letter_html.index('</div></div>')+12:]
					
					letter = letter_html[letter_html.index('</div></div>')-1]
					
					state_start_pos = letter_html.index('data-state="')
					half_cut = letter_html[state_start_pos + 12:]
					state = half_cut[:half_cut.index('"')]

					if state == 'empty':
						letter = ''
				else:
					state = letter.get_attribute('data-state')
					letter = letter.get_attribute('innerHTML')

					


				# print(letter.get_attribute('innerHTML'))
				# print(letter.get_attribute('data-state'))
				# print(letter)
				# print(state)
				# print('='*40)

				# Row-module_row__dEHfN <- row classname
				# class="App-module_game__NSc-J" <- this is the root of the game board, for future reference
				
				# state = self.driver.execute_script("return document.querySelector('html>body>game-app').shadowRoot.querySelector('game-theme-manager>div>div>div>:nth-child({row})').shadowRoot.querySelector('div>:nth-child({letter})').shadowRoot.querySelector('div')".format(row=i+1, letter=j+1)).get_attribute('data-state')
				# state = self.driver.execute_script("return document.querySelector('html>body>game-app').querySelector('game-theme-manager>div>div>div>:nth-child({row})').querySelector('div>:nth-child({letter})').querySelector('div')".format(row=i+1, letter=j+1)).get_attribute('data-state')
				# state = self.driver.execute_script("return document.querySelector('html>body>game-app')")
				# print(state.get_attribute('innerHTML'))
				# state = letter.get_attribute('data-state')
				# letter = letter.get_attribute('innerHTML')
				self.board[i][j] = (letter, state)

	def guess_word(self, word, guess_number):

		for i in range(5):
			ActionChains(self.driver).key_down(Keys.BACKSPACE).key_up(Keys.BACKSPACE).perform()
		ActionChains(self.driver).send_keys(word).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
		time.sleep(2)

		# click to reset cursor
		actions = ActionChains(self.driver)
		actions.move_by_offset(100, 100).click().perform()

		self.update_board_state()
		response = []
		for i in range(5):
			response.append({
					'slot': i,
					'guess': self.board[guess_number-1][i][0],
					'result': self.board[guess_number-1][i][1]
				})

		return response

# s = WordleScraper()
# print(s.guess_word('crane', 1))
# s.guess_word('olive')
# s.get_board()







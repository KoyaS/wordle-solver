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


class WordleScraper()

	def __init__(self, headless=False):
		chrome_options = Options()
		if headless:
			chrome_options.add_argument("--headless")
		chrome_options.add_experimental_option("useAutomationExtension", False)
		chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
		driver_location = '/Users/koya/Documents/Development/Python/wordle-solver/chromedriver'
		driver = webdriver.Chrome(driver_location, options=chrome_options)

		start_url = "https://www.nytimes.com/games/wordle/index.html"
		driver.get(start_url)

		# time.sleep(0.5)

		# time.sleep(1.5)
		# myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'svg')))
		# print(myElem)
		actions = ActionChains(driver)
		actions.move_by_offset(100, 100).click().perform()
		# time.sleep(500)
		# time.sleep(0.5)


def scrape_wordle():

	# click "x" button on popup
	# driver.find_element_by_css_selector('svg').click()
	# driver.find_element_by_xpath('//*[@id="game"]/game-modal//div/div/div/game-icon//svg').click()
	# driver.find_element_by_xpath('/html/body/game-app//game-theme-manager/div/game-modal//div/div/div/game-icon//svg').click()
	# driver.find_element_by_class_name('game-app>game-theme-manager>game-modal>div>div>.close-icon').click()
	# driver.find_element_by_css_selector('.close-icon').click()

	# time.sleep(1.5)

	# print(driver.page_source)

	# print(driver.find_element(By.CLASS_NAME, 'tile'))
	# print(driver.find_element_by_class_name('tile'))
	# print(driver.find_element_by_css_selector('div>game-tile:nth-child(1)'))
	# print(driver.find_element_by_css_selector('html'))
	# print(driver.find_element(By.CSS_SELECTOR, 'html>body>game-app').shadowRoot)

	# ActionChains(driver).send_keys("depth").key_down(Keys.ENTER).perform()
	# time.sleep(5)


	element = driver.execute_script("return document.querySelector('html>body>game-app').shadowRoot.querySelector('game-theme-manager>div>div>div')")
	# print(element.find_element(By.CLASS_NAME, 'tile'))
	# print(element.get_attribute('innerHTML'))
	for i in range(6):
		print(element.find_element(By.CSS_SELECTOR, ':nth-child({})'.format(i+1)))

	# delay=3
	# myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'tile')))
	# print(myElem)

scrape_wordle()







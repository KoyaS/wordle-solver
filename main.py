from solver import Solver
from textapi import sendMessage
import datetime as dt
import time

now = dt.datetime.now()
current_day = now.strftime('%d')

while True:
    print('waiting...')
    time.sleep(100)
    now = dt.datetime.now()
    if current_day != now.strftime('%d'):

        s = Solver('crane', False)

        new_guesses, state, present, absent, guessed_words = s.run()
        print(new_guesses)
        while new_guesses:
            backup = Solver(new_guesses[0][0], headless=False, state=state, present=present, absent=absent, guessed=guessed_words)
            new_guesses, state, present, absent, guessed_words = backup.run()

        sendMessage("Today's wordle is:" + state + ". suck it.")

        current_day = now.strftime('%d')

# Twilio recovery: l3cldUSn6q9tXS3os3dRnwoYp1jO1CJtfdJgY8CW


import game_logic
from bots import random_bot
from screen_utils import screen_utils
from game_logic import game_logic
from data import data_utils
import time
import keyboard
import os
from PIL import Image


CHAMP_LIST = ['Archer', 'Fighter', 'Knight', 'Monk', 'Ninja', 'Priestess',
            'Pyromancer', 'Swordsman', 'Shrine Maiden', 'Berserker', 'Sniper',
            'Ice Mage', 'Magic Knight', 'Shield Bearer', 'Ghost',
            'Lightning Mage', 'Necromancer', 'Boomerang Hunter',
            'Plague Doctor', 'Poison Dart Hunter', 'Barrier Mage', 'Vampire',
            'Devil', 'Gambler', 'Lancer', 'Dual Blader', 'Executioner',
            'Bard', 'Gunner', 'Illusionist', 'Shadowmancer', 'Cook',
            'Exorcist', 'Clown', 'Ogre', 'Werewolf', 'Taoist',
            'Mystic Dancer', 'Dark Mage', 'Cold Corpse']

DATA_FILE = os.path.join(os.path.dirname(__file__), 
                         'data', 'data.json')

def set_false(var):
    return False

def stop_program(test_var):
    print('Program Stopped')
    keyboard.unhook_all()
    test_var = set_false(test_var)

def main():
    game = game_logic.GameLogic()
    screen_util = screen_utils.ScreenUtils()
    data_util = data_utils.DataUtils()
    r_bot = random_bot.RandomBot()

    # Add hotkey
    continue_testing = True
    keyboard.add_hotkey('q', stop_program, args=(continue_testing,))

    time.sleep(5)

    numTests = 0
    while numTests < 1000 and continue_testing == True:
        char_pool = CHAMP_LIST[:]
        # Run Draft for teams
        draft = game.bot_draft(char_pool, r_bot, r_bot)
        b_team = draft[0]
        r_team = draft[1]
        print(b_team, r_team)

        # Click new test to start a new test
        screen_util.click_new_test()

        # Click on characters for simulation
        for char in b_team:
            screen_util.find_and_click_char(char)
        for char in r_team:
            screen_util.find_and_click_char(char)
        
        # Start Test
        time.sleep(0.5)
        screen_util.click_start_test()
        
        # Check for simulation complete
        screen_util.find_score()
        time.sleep(0.2)

        # Screenshot score to find winner
        pic = Image.open('screenshot.png')
        game_result = screen_util.find_winner(pic)

        # Add data to json file
        scrim_chars = []
        scrim_chars = b_team + r_team
        data_util.append_data(scrim_chars, game_result, DATA_FILE)

        # Close simulation
        screen_util.click_close()
        
        # Increment test
        numTests += 1


if __name__ == '__main__':
    main()
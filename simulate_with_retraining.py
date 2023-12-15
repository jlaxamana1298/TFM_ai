import game_logic
from bots import random_bot, mcts_bot
from screen_utils import screen_utils
from game_logic import game_logic
from data import data_utils
import time
import keyboard
from PIL import Image
import random
import os
import nn_training


CHAMP_LIST = ['Archer', 'Fighter', 'Knight', 'Monk', 'Ninja', 'Priestess',
            'Pyromancer', 'Swordsman', 'Shrine Maiden', 'Berserker', 'Sniper',
            'Ice Mage', 'Magic Knight', 'Shield Bearer', 'Ghost',
            'Lightning Mage', 'Necromancer', 'Boomerang Hunter',
            'Plague Doctor', 'Poison Dart Hunter', 'Barrier Mage', 'Vampire',
            'Devil', 'Gambler', 'Lancer', 'Dual Blader', 'Executioner',
            'Bard', 'Gunner', 'Illusionist', 'Shadowmancer', 'Cook',
            'Exorcist', 'Clown', 'Ogre', 'Werewolf', 'Taoist',
            'Mystic Dancer', 'Dark Mage', 'Cold Corpse']


TURN_ORDER = ['b_ban', 'r_ban', 'b_ban', 'r_ban',
              'b_pick', 'r_pick', 'r_pick', 'b_pick',
              'r_ban', 'b_ban',
              'r_pick', 'b_pick', 'b_pick', 'r_pick']


RUNNING = True
DATA_FILE = 'data.json'


def stop_program():
    global RUNNING
    print('Stopping the program')
    RUNNING = False


def run_simulations(b_team, r_team):
    screen_util = screen_utils.ScreenUtils()
    data_util = data_utils.DataUtils()
    # Click new test to start a new test
    screen_util.click_new_test()

    # Click on characters for simulation
    for char in b_team:
        screen_util.find_and_click_char(char)
    for char in r_team:
        screen_util.find_and_click_char(char)

    # Start test
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


def main():
    game = game_logic.GameLogic()
    screen_util = screen_utils.ScreenUtils()
    r_bot = random_bot.RandomBot()
    m_bot = mcts_bot.MctsBotLogic()
    bots_list = ['random', 'mcts']

    # Add hotkey
    keyboard.add_hotkey('q', stop_program)
    time.sleep(5)

    nn_training.main()

    num_tests = 0
    while num_tests < 1000 and RUNNING == True:
        char_pool = CHAMP_LIST[:]

        # Randomly select bot
        choice1 = random.choice(bots_list)
        if choice1 == 'random':
            print('Blue is Random')
            blue_bot = r_bot
        elif choice1 == 'mcts':
            print('Blue is MCTS')
            blue_bot = m_bot
        choice2 = random.choice(bots_list)
        if choice2 == 'random':
            print('Red is Random')
            red_bot = r_bot
        elif choice2 == 'mcts':
            print('Red is MCTS')
            red_bot = m_bot

        # Run draft for selected bots
        draft = game.bot_draft(char_pool, blue_bot, red_bot)
        drafted_b_team = draft[0]
        drafted_r_team = draft[1]
        b_team_bans = draft[2]
        r_team_bans = draft[3]
        print(drafted_b_team, drafted_r_team)
        print(b_team_bans, r_team_bans)

        # Run simulations for games
        for i in range(3):
            run_simulations(drafted_b_team, drafted_r_team)

        # Retrain Neural Network every 30 simulated matches
        if num_tests % 30 == 0:
            nn_training.main()

        num_tests += 1


if __name__ == '__main__':
    main()
import game_logic
from bots import random_bot, mcts_bot
from screen_utils import screen_utils
from game_logic import game_logic
import time
import keyboard
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


TURN_ORDER = ['b_ban', 'r_ban', 'b_ban', 'r_ban',
              'b_pick', 'r_pick', 'r_pick', 'b_pick',
              'r_ban', 'b_ban',
              'r_pick', 'b_pick', 'b_pick', 'r_pick']


def main():
    game = game_logic.GameLogic()
    screen_util = screen_utils.ScreenUtils()
    r_bot = random_bot.RandomBot()
    m_bot = mcts_bot.MctsBotLogic()

    champ_pool = CHAMP_LIST[:]
    '''
    b_team = ['Archer', 'Fighter', 'Knight']
    r_team = ['Ogre', 'Exorcist','Cold Corpse']
    for char in b_team:
        champ_pool.remove(char)
    for char in r_team:
        champ_pool.remove(char)

    print(m_bot.ban_choice(champ_pool, b_team, r_team))
    '''

    b_team = []
    r_team = []
    b_bans = []
    r_bans = []
    char_pool = CHAMP_LIST[:]

    for turn_num, turn in enumerate(TURN_ORDER):
        if turn == 'b_ban':
            b_ban_choice = r_bot.ban_choice(char_pool, b_team, r_team, turn_num)
            b_bans.append(b_ban_choice)
            char_pool.remove(b_ban_choice)
        elif turn == 'r_ban':
            r_ban_choice = m_bot.ban_choice(char_pool, b_team, r_team, turn_num)
            r_bans.append(r_ban_choice)
            char_pool.remove(r_ban_choice)
        elif turn == 'b_pick':
            b_pick_choice = r_bot.pick_choice(char_pool, b_team, r_team,
                                              turn_num)
            b_team.append(b_pick_choice)
            char_pool.remove(b_pick_choice)
        elif turn == 'r_pick':
            r_pick_choice = m_bot.pick_choice(char_pool, b_team, r_team,
                                              turn_num)
            r_team.append(r_pick_choice)
            char_pool.remove(r_pick_choice)
    print(b_bans, r_bans)
    print(b_team, r_team)





'''
    # Run Draft for teams
    draft = game.bot_draft(CHAMP_LIST, r_bot, r_bot)
    b_team = draft[0]
    r_team = draft[1]
    print(b_team, r_team)

    print(m_bot.ban_choice(CHAMP_LIST, b_team, r_team))
'''


if __name__ == '__main__':
    main()
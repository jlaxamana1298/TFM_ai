class GameLogic:
    def __init__(self):
        # Turn order for 4v4 draft
        self.turn_order = ['b_ban', 'r_ban', 'b_ban', 'r_ban',
                           'b_pick', 'r_pick', 'r_pick', 'b_pick',
                           'r_ban', 'b_ban',
                           'r_pick', 'b_pick', 'b_pick', 'r_pick']
        
    # Simulate 2 bots drafting
    def bot_draft(cls, full_pool, b_bot, r_bot):
        # Initialize teams
        b_team = []
        r_team = []
        char_pool = full_pool

        # Simulate Draft
        for turn in cls.turn_order:
            if turn == 'b_ban':
                b_ban_choice = b_bot.ban_choice(char_pool, b_team, r_team)
                char_pool.remove(b_ban_choice)
            elif turn == 'r_ban':
                r_ban_choice = r_bot.ban_choice(char_pool, b_team, r_team)
                char_pool.remove(r_ban_choice)
            elif turn == 'b_pick':
                b_pick_choice = b_bot.pick_choice(char_pool, b_team, r_team)
                b_team.append(b_pick_choice)
                char_pool.remove(b_pick_choice)
            elif turn == 'r_pick':
                r_pick_choice = r_bot.pick_choice(char_pool, b_team, r_team)
                r_team.append(r_pick_choice)
                char_pool.remove(r_pick_choice)
        
        return [b_team, r_team, char_pool]
    
    # Click on characters for test simulations
    def sim_click_characters(cls):
        pass

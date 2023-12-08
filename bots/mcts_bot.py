import random
import numpy as np
from collections import defaultdict
from tensorflow.keras.models import load_model
import tensorflow as tf
import pandas as pd


CHAMP_LIST = ['Archer', 'Fighter', 'Knight', 'Monk', 'Ninja', 'Priestess',
            'Pyromancer', 'Swordsman', 'Shrine Maiden', 'Berserker', 'Sniper',
            'Ice Mage', 'Magic Knight', 'Shield Bearer', 'Ghost',
            'Lightning Mage', 'Necromancer', 'Boomerang Hunter',
            'Plague Doctor', 'Poison Dart Hunter', 'Barrier Mage', 'Vampire',
            'Devil', 'Gambler', 'Lancer', 'Dual Blader', 'Executioner',
            'Bard', 'Gunner', 'Illusionist', 'Shadowmancer', 'Cook',
            'Exorcist', 'Clown', 'Ogre', 'Werewolf', 'Taoist',
            'Mystic Dancer', 'Dark Mage', 'Cold Corpse']


class MctsBotLogic:
    def __init__(self):
        pass

    def ban_choice_test(self, char_pool, b_team, r_team):
        # Load model
        model_file = 'my_model.h5'
        draft_state = DraftState(b_team, r_team, char_pool, turn_num = 12)
        mcts_node = MctsNode(state = draft_state, model = model_file)
        #print(mcts_node.get_legal_actions())
        #print(mcts_node.move('Knight').remaining_pool)
        #print([mcts_node.best_action().state.team1,
        #        mcts_node.best_action().state.team2])
        
        team1_new = mcts_node.best_action().state.team1[:]
        #team1_new = ['Archer', 'Fighter', 'Knight', 'Ninja']
        print(team1_new)
        char_pool_new = char_pool[:]
        char_pool_new.remove(team1_new[3])
        draft_state2 = DraftState(team1_new, r_team, 
                                  char_pool_new, turn_num = 13)
        mcts_node2 = MctsNode(state = draft_state2, model = model_file)
        team2_new = mcts_node2.best_action().state.team2
        print(team2_new)
        return team2_new
        
    
    def ban_choice(self, char_pool, b_team, r_team, turn_num):
        b_states = [0,2,4,7,9,11,12]
        model_file = tf.keras.models.load_model('my_model.h5')
        draft_state = DraftState(b_team, r_team, char_pool, turn_num)
        if turn_num in b_states:
            top_node = MctsNode(state = draft_state, model = model_file,
                                team = 'blue')
        else:
            top_node = MctsNode(state = draft_state, model = model_file,
                                team = 'red')
        best_action = top_node.best_action().parent_action
        return best_action

    def pick_choice(self, char_pool, b_team, r_team, turn_num):
        b_states = [0,2,4,7,9,11,12]
        model_file = tf.keras.models.load_model('my_model.h5')
        draft_state = DraftState(b_team, r_team, char_pool, turn_num)
        if turn_num in b_states:
            top_node = MctsNode(state = draft_state, model = model_file,
                                team = 'blue')
        else:
            top_node = MctsNode(state = draft_state, model = model_file,
                                team = 'red')
        best_state = top_node.best_action().state
        if turn_num in b_states:
            return best_state.team1[-1]
        else:
            return best_state.team2[-1]


class MctsNode:
    def __init__(self, state, parent = None, parent_action = None,
                model = None, team = None):
        self.state = state
        self.team = team
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self.number_of_visits = 0
        self.results = defaultdict(int)
        self.results[1] = 0
        self.results[-1] = 0
        self.untried_actions = None
        self.untried_actions = self.get_untried_actions()
        self.model = model
        return

    def get_untried_actions(self):
        self.untried_actions = self.get_legal_actions()
        return self.untried_actions
    
    def q(self):
        wins = self.results[1]
        losses = self.results[-1]
        return wins - losses
    
    def n(self):
        return self.number_of_visits
    
    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.move(action, self.state)
        child_node = MctsNode(state = next_state, parent = self,
                              parent_action = action, model = self.model,
                              team = self.team)
        self.children.append(child_node)
        return child_node
    
    def is_terminal_node(self):
        return self.state.is_game_over()
    
    def rollout(self):
        current_rollout_state = self.state
        
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = self.move(action, current_rollout_state)
        return self.game_result()
    
    def backpropagate(self, result):
        self.number_of_visits += 1
        self.results[result] += 1
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0
    
    def best_child(self, c_param=0.1):
        choices_weights = [(c.q() / c.n()) + c_param * 
                        np.sqrt((2 * np.log(self.n()) / c.n())) 
                        for c in self.children]
        if self.team == 'blue':
            return self.children[np.argmax(choices_weights)]
        else:
            return self.children[np.argmin(choices_weights)]
    
    def rollout_policy(self, possible_moves):
        if possible_moves:
            return possible_moves[np.random.randint(0,len(possible_moves)-1)]
        else:
            return None
    
    def tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node
    
    def best_action(self):
        simulation_no = 100
        for i in range(simulation_no):
            v = self.tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        return self.best_child(c_param=0)
    
    def get_legal_actions(self):
        # Returns a list
        legal_actions = self.state.remaining_pool[:]
        return legal_actions

    def is_game_over(self):
        # Returns True or False
        return self.state.is_game_over()
    
    def game_result(self):
        # Returns 1 or 0 or -1 for win, tie, loss
        # Load model
        model = self.model

        # Encode teams
        encoded_teams = np.zeros(len(CHAMP_LIST), dtype = int)
        team1 = self.state.team1[:]
        team2 = self.state.team2[:]
        for char in team1:
            char_index = CHAMP_LIST.index(char)
            encoded_teams[char_index] = 1
        for char in team2:
            char_index = CHAMP_LIST.index(char)
            encoded_teams[char_index] = -1
        
        # Make predictions
        predictions = model.predict(np.expand_dims(encoded_teams, axis=0))
        predicted_class = np.argmax(predictions[0])
        
        if predicted_class == 0:
            return 1
        else:
            return -1

    def move(self, action, state):
        # Returns new state after making move
        team1 = state.team1[:]
        team2 = state.team2[:]
        updated_pool = state.remaining_pool[:]
        next_turn_num = state.turn_num + 1
        if self.state.current_action == 'b_pick':
            team1.append(action)
            updated_pool.remove(action)
        elif self.state.current_action == 'r_pick':
            team2.append(action)
            updated_pool.remove(action)
        else:
            updated_pool.remove(action)
            #pass
        new_state = DraftState(team1 = team1, team2 = team2, 
                               remaining_pool = updated_pool, 
                               turn_num = next_turn_num)
        return new_state


class DraftState:
    def __init__(self, team1, team2, remaining_pool, turn_num = 0):
        self.turn_order = ['b_ban', 'r_ban', 'b_ban', 'r_ban',
                           'b_pick', 'r_pick', 'r_pick', 'b_pick',
                           'r_ban', 'b_ban',
                           'r_pick', 'b_pick', 'b_pick', 'r_pick']
        self.turn_num = turn_num
        if self.turn_num <= 13:
            self.current_action = self.turn_order[self.turn_num]
        else:
            self.current_action = None
        self.team1 = team1[:]
        self.team2 = team2[:]
        self.remaining_pool = remaining_pool[:]

    def is_game_over(self):
        if self.turn_num == 14:
            return True
        if len(self.team1) == 4 and len(self.team2) == 4:
            return True
        else:
            return False
        
    def get_legal_actions(self):
        legal_actions = self.remaining_pool[:]
        return legal_actions
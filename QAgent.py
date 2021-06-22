# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 16:59:48 2021

@author: Harold
"""


import random
import torch
import matplotlib.pyplot as plt
import IPython
import numpy as np
from Snake_AI import directions, Snake_QL
from collections import deque
from DQL_Model import DQN, DQ_train

max_memory = 100000
batch = 1000



class QAgent():
    
    def __init__(self, eps = 0.4, gamma = 0.9):
        self.num_game = 0
        # Exploration rate
        self.eps = eps
        # Discounted reward rate
        self.gamma = gamma
        
        # Initialize replay memory variable to story past experience
        self.replay_memory = deque(maxlen = max_memory)
        
        
        self.model = DQN(11, 3, 256)
        self.training = DQ_train(self.model, lr = 0.001, gamma = self.gamma)
        
        
        
        
    def add_memory(self, curr_state, action, reward, next_state, game):
        """
        Add experience to replay_memory variable
        Parameters
        ----------
        curr_state : numpy array
        action : numpy array
        reward : int
        next_state : numpy array
        game : boolean
            true if game over, else otherwise.

        Returns
        -------
        None.

        """
        self.replay_memory.append((curr_state, action, reward, next_state, game))
        

        
    def get_state(self, game):
        """
        Parameters
        ----------
        game : Object of Snake_QL

        Returns
        -------
        Vectorized form of current form.
        
        [danger straight, danger right, danger left, Left, Up, Right, Down, food left, food up, food right, food down]

        """
        # First get the danger state
        danger = self.helper_danger(game)
        
        # Second get the direction state
        dir_l = int(game.Direction == 1)
        dir_u = int(game.Direction == 2)
        dir_r = int(game.Direction == 3)
        dir_d = int(game.Direction == 4)
        
        dir_ = [dir_l, dir_u, dir_r, dir_d]
        
        # Third get the food state
        food = [game.food[0] <game.snake[0][0], \
                game.food[1] < game.snake[0][1], \
                game.food[0] > game.snake[0][0], \
                    game.food[1] > game.snake[0][1]]
        
        
        
        # Concatenate all the lists above together to get state
        state= danger + dir_ + food
            
        return np.array(state, dtype=int)
        
    def helper_danger(self, game):
        """
        Helper function to determine the danger state of the snake

        Parameters
        ----------
        game : Snake_QL()
            Object of Snake_QL.

        Returns
        -------
        danger: list of 3 elements to indicate direction of danger
                [straight, right, left]

        """
        # Initialize danger status
        
        danger = [0, 0, 0]
        
        # First create additional 'snake-body' around the head in all direction
        
        pt_L = [game.snake[0][0] - 10, game.snake[0][1]]
        pt_U = [game.snake[0][0], game.snake[0][1] - 10]
        pt_R = [game.snake[0][0] + 10, game.snake[0][1]]
        pt_D = [game.snake[0][0], game.snake[0][1] + 10]
        
        if (game.Direction == 1 and game.collision(pt_L)) or \
            (game.Direction == 2 and game.collision(pt_U)) or \
            (game.Direction == 3 and game.collision(pt_R)) or \
            (game.Direction == 4 and game.collision(pt_D)) :
            # Update danger status as straight
            danger[0] = 1
        
        if (game.Direction == 1 and game.collision(pt_U)) or \
            (game.Direction == 2 and game.collision(pt_R)) or \
            (game.Direction == 3 and game.collision(pt_D)) or \
            (game.Direction == 4 and game.collision(pt_L)):
            danger[1] = 1
        
        if (game.Direction == 1 and game.collision(pt_D)) or \
            (game.Direction == 2 and game.collision(pt_L)) or \
            (game.Direction == 3 and game.collision(pt_U)) or \
            (game.Direction == 4 and game.collision(pt_R)):
            danger[2] = 1
        
        return danger
    
    def long_train(self):
        """

        Parameters
        ----------
        curr_state : numpy array
        action : numpy array
        reward : int
        next_state : numpy array
        game : boolean
            true if game over, else otherwise.

        Returns
        -------
        None.

        """
        # If we have more memory than the batch, take random sample
        if len(self.replay_memory) > batch:
            sample1 = random.sample(self.replay_memory, batch)
        else:
            sample1 = self.replay_memory
        
        
        # Group by variable and train using q network
            
        states = []
        actions = []
        rewards = []
        next_states = []
        games = []
        for i in range(len(sample1)):
            states.append(sample1[i][0])
            actions.append(sample1[i][1])
            rewards.append(sample1[i][2])
            next_states.append(sample1[i][3])
            games.append(sample1[i][4])
        
        self.training.learn(states, actions, rewards, next_states, games)
        

        
    def short_train(self, curr_state, action, reward, next_state, game):
        """

        Parameters
        ----------
        curr_state : numpy array
        action : numpy array
        reward : int
        next_state : numpy array
        game : boolean
            true if game over, else otherwise.

        Returns
        -------
        None.

        """
        self.training.learn(curr_state, action, reward, next_state, game)
            
            
    def get_action(self, state):

        # Create default action
        action = [0, 0, 0]
        

        # We will use decaying epsilon greedy algorithm.
        # Essentially, more games -> less exploration
        # Start with 40% exploration rate that decays by 0.004% every game.
        # After 100 games, the snake will make it's own decision based on experience.

        prob = np.random.uniform(0, 1)
        self.eps = 0.4 - 0.004 * self.num_game

        
        # Check exploration
        if prob < self.eps:
            act = random.randint(0, 2)
            action[act] = 1
        
        # Otherwise get optimal action
        else:
            curr_state = torch.tensor(state, dtype=torch.float)
            pred = self.model(curr_state)
            
            act_inx = torch.argmax(pred).item()
            action[act_inx] = 1
            
            
        return action
        
        
        

def train():
    # Make some variables to store score, number of games, etc
    
    list_score = []
    
    Q_agent = QAgent()
    snake_game = Snake_QL()
    
    
    while True:
        # Get current state
        current_state = Q_agent.get_state(snake_game)
        
        # Get action
        move = Q_agent.get_action(current_state)
        
        # Perform the action
        game_over, score, reward = snake_game.game_move(move)
    
        # Get the new state
        new_state = Q_agent.get_state(snake_game)
    
        # Train DQN
        Q_agent.short_train(current_state, move, reward, new_state, game = game_over)
        
        # Add this experience to our deque
        
        Q_agent.add_memory(current_state, move, reward, new_state, game_over)
        
        
        if game_over:
            # Reset the game then train long memory
            snake_game.reset()
            Q_agent.num_game += 1
            Q_agent.long_train()
            
            # print generation number and the score
            print("{}: {} and {}: {}".format("Generation", Q_agent.num_game, "Score", score))
            list_score.append(score)
            num = list(i for i in range(1, len(list_score) + 1))
            
            
            # Plotting to visualize the progress of Q network
            plt.plot(num, list_score)
            plt.title("Score against number of games")
            plt.xlabel("Game number")
            plt.ylabel("Score")
            
    

if __name__ == '__main__':
    train()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

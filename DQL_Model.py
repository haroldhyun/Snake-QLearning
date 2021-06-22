# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 17:01:39 2021

@author: Harold
"""
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import os

class DQN(nn.Module):
    
    def __init__(self, state_size, action_size, hidden_size):
        
        super().__init__()
        
        self.input = nn.Linear(state_size, hidden_size)
        self.output = nn.Linear(hidden_size, action_size)
        
        # 1 input, 1 hidden, 1 output layer


    def forward(self, x):
        """
        Network that maps state to action pair
        
        Parameters
        ----------
        state : numpy array of current state

        Returns
        -------
        Action

        """
        # x = state
        
        x = F.relu(self.input(x))
        x = self.output(x)
        
        return x
    

        
class DQ_train():
    
    def __init__(self, model, lr, gamma):
        # Model is DQN model
        # lr is learning rate
        # gamma is discount rate
        self.gamma = gamma
        self.model = model
        self.lr = lr
        
        # Loss function is MSE
        self.criterion = nn.MSELoss()
        
        # We will use Adam optimizer (most general)
        self.optimizer = optim.Adam(model.parameters(), lr = self.lr)
        
        
        
    def learn(self, curr_state, action, reward, next_state, game):
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
        # Convert to torch variables.
        curr_state = torch.tensor(curr_state, dtype = torch.float)
        action = torch.tensor(action, dtype = torch.long)
        reward = torch.tensor(reward, dtype = torch.float)
        next_state = torch.tensor(next_state, dtype = torch.float)
        
        
        # If we are only passing dim 1 variables to learn then we need to unsqueeze.
        
        if len(curr_state.shape) == 1:
            curr_state = torch.unsqueeze(curr_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            next_state = torch.unsqueeze(next_state, 0)
            game = (game, )
        
        
        
        # Get the predicted q value
        pred = self.model(curr_state)
        
        labels = pred.clone()
        
        # Update q values according to simplified bellman equation
        # Q(s, a) = R(s, a) + gamma * max(Q'(s', a'))
        
        # Check if the game is done first
        
        for ele in range(len(game)):
            newQ = reward[ele]
            if not game[ele]:
                newQ = reward[ele] + self.gamma*torch.max(self.model(next_state[ele]))
                                                 
            labels[ele][torch.argmax(action[ele]).item()] = newQ
        
        
        self.optimizer.zero_grad()
        loss = self.criterion(pred,labels)
        loss.backward()
        self.optimizer.step()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
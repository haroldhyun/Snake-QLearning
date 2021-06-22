# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 14:52:27 2021

@author: Harold
"""


import random
import torch
import matplotlib
import IPython
import pygame
import numpy as np


pygame.init()


snake_col = (255, 255, 255)
food_col = (255, 0, 0)

#directions
class directions():
    L = 1
    U = 2
    R = 3
    D = 4
    
class Snake_QL:
    
    def __init__(self, width = 500, height = 500):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode(size = (self.width, self.height))
        pygame.display.set_caption("The Iconic Snake")
        
        self.clock = pygame.time.Clock()

        self.reset()
        
        
        
    def reset(self):
        """to initialize/reset the game when snake hits boundary or itself
        """
        self.score = 0
        
        #initialize Snake body, directions, settings
        
        #moving to the right initially
        self.Direction = directions.R
        
        self.snake = [[100,100], [90,100], [80,100]]
        
        self.score = 0
        self.food = None
        self.clock_speed = 120
        self.generation = 0
        self.new_food()
        
    def new_food(self):
        """
        random food placement on the screen

        Returns
        -------
        None.

        """
        # Initialize random x and y coordinate for the food
        food_x = np.random.randint(self.width/10)*10
        food_y = np.random.randint(self.height/10)*10
        self.food = [food_x, food_y]
        
        #this will make sure that food never appears in snake body.
        if self.food in self.snake:
            self.new_food()
        else:
            pass
        
    def game_move(self, action):
        """
        action: array of 3 elements to indicate a new action instead of 
        user based input.
        
        Returns
        -------
        collision: Bool - True if snake dies, false if else
        score: int - number of fruits eaten by the snake
        reward: int - reward gained by the Q learning agent
        """
        self.generation += 1
        
        # Check for user input to close the game.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        # Move the snake according to our action.
        self.action_move(action)
        
        # Insert new snake heading.
        self.snake.insert(0, self.new_head)
        
        # Initialize reward at 0
        reward = 0
        
        # Check if snake collides with itself or the display
        collision = False
        
        
        if self.collision() or self.generation > 100*len(self.snake):
            collision = True
            reward = -10
            return collision, self.score, reward
        
        # Check if snake gets the food.
        if self.snake[0] == self.food:
            self.score += 1
            
            # Reward the snake for eating the fruit
            reward = 10
            
            # we need new food now.
            self.new_food()
        else:
            # must remove the tail of the snake.
            self.snake.pop()
        
        
        # Display the screen using helper
        self.display()
        self.clock.tick(self.clock_speed)
        
        return collision, self.score, reward
    

    
    
    def action_move(self, action):
        """
        Move the snake accordingly to the action
        action: array of 3 elements indicating which way to move. [straight, right, left]
        
        
        Returns
        -------
        None.

        """
        self.snake_head = self.snake[0]
        self.snake_headx = self.snake[0][0]
        self.snake_heady = self.snake[0][1]
        
        heading_type = [directions.L, directions.U, directions.R, directions.D]
        inx = heading_type.index(self.Direction)
        
        
        # Action is straight
        # No changes to the direction of the snake.
        if np.array_equal(action, np.array([1, 0, 0])):
            new_dir = self.Direction
        
        # Action is right
        # Direction will change accordingly. ie) U -> R, R -> D, D -> L, L -> U
        elif np.array_equal(action, np.array([0, 1, 0])):
            new_dir = heading_type[(inx + 1) % 4]
    
        # Action is left
        # Direction will change accordingly. ie) U -> L, L -> D, D -> R, R -> U
        else:
            new_inx = 3 - inx
            new_dir = heading_type[new_inx]
        
        
        if new_dir == 1:
            new_headx = self.snake_headx - 10
            new_heady = self.snake_heady
        elif new_dir == 2:
            new_heady = self.snake_heady - 10
            new_headx = self.snake_headx    
        elif new_dir == 3:
            new_headx = self.snake_headx + 10
            new_heady = self.snake_heady
        elif new_dir == 4:
            new_heady = self.snake_heady + 10
            new_headx = self.snake_headx
            
        # Get the next snake head
        self.new_head = [new_headx, new_heady]
        
        # Finally, change the direction of the snake
        self.Direction = new_dir
        
        
        
        
    def collision(self, point = None):
        """
        point: list of 2 indicating [x, y] coordinates to check for collision\
            
        two ways of collision.
        1) snake head collides with the boundary of the screen
        2) snake head collides with the body        

        Returns
        -------
        bool
            If snake collides return True, else False.

        """
        if point == None:
            point = self.snake[0]

        # Check if snake head hits the boundary of the screen
        if point[0] > self.width or point[0] < 0 or point[1] > self.height or point[1] < 0:
            return True
        
        # Check if snake hits its body
        elif self.snake[0] in self.snake[1:]:
            return True
        
        # Otherwise return False
        return False
    
    def display(self):
        """
        Draw in the rectangles for food and snake.

        Returns
        -------
        None.

        """
        self.screen.fill("black")
        
        # Draw all the snake body
        for body in self.snake:
            pygame.draw.rect(self.screen, snake_col, [body[0], body[1], 10, 10])

        # Draw the food
        pygame.draw.rect(self.screen, food_col, [self.food[0], self.food[1], 10, 10])
        
        # Put up a scoreboard metric
        pygame.font.init()
        font = pygame.font.SysFont('calibri', 15)
        img = font.render("Score: {0}".format(self.score), True, (0, 255, 150))
        self.screen.blit(img, (280, 10))
        
        pygame.display.flip()
    

    

        
        
        
        
        
        
        
        
        
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 12:35:42 2021

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
    R = 2
    U = 3
    D = 4
    
class Snake:
    
    def __init__(self, width = 600, height = 600):
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
        
        #initialize Snake body & directions
        
        #moving to the right initially
        self.Direction = directions.R
        
        self.snake = [[100,100], [90,100], [80,100]]
        #self.food = None
        self.score = 0
        self.food = None
        self.new_food()
        self.clock_speed = 20

        
    def new_food(self):
        """
        random food placement on the screen

        Returns
        -------
        None.

        """
        food_x = np.random.randint(self.width/10)*10
        food_y = np.random.randint(self.height/10)*10
        self.food = [food_x, food_y]
        
        #this will make sure that food never appears in snake body.
        if self.food in self.snake:
            self.new_food()
        else:
            pass
        
    def game_move(self):
        """
        

        Returns
        -------
        None.

        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.Direction = directions.L
                elif event.key == pygame.K_RIGHT:
                    self.Direction = directions.R
                elif event.key == pygame.K_UP:
                    self.Direction = directions.U
                elif event.key == pygame.K_DOWN:
                    self.Direction = directions.D
        

        self.action_move(self.Direction)
        
        # Insert new snake heading.
        self.snake.insert(0, self.new_head)
        
        # Check if snake collides with itself or the display
        
        game = False
        
        if self.collision():
            
            #this will indicate when to stop the game.
            game = self.continue_quit()
            
            if game:
                return game, self.score
            else:
                self.reset()
        
        # Check if snake gets the food.
        
        if self.snake[0] == self.food:
            self.score += 1
            self.clock_speed += 0.5
            # we need new food now.
            self.new_food()
        else:
            # must remove the tail of the snake.
            self.snake.pop()
        
        
        # Display the screen using helper

        self.display()
        self.clock.tick(self.clock_speed)
        return game, self.score
    
    def continue_quit(self):
        """
        checks user input for either continue or quit the game when collision happens.
        Assumes that collision happened.
        Returns
        -------
        None.

        """
        pygame.font.init()
        font = pygame.font.SysFont('javanesetext', 30)
        img = font.render("Press any Key to Continue or Q to Quit", True, (255, 255, 0))
        self.screen.blit(img, (30, 100))
        
        
        pygame.display.flip()
        
        game_status = None
        
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                game_status = True
                return(game_status)
            elif event.key == pygame.K_RETURN:
                game_status = False
                return(game_status)
        if event.type == pygame.QUIT:
            pygame.quit()
    
    
    def action_move(self, heading):
        """
        move the snake accordingly.

        Returns
        -------
        None.

        """
        self.snake_head = self.snake[0]
        self.snake_headx = self.snake[0][0]
        self.snake_heady = self.snake[0][1]
        
        if heading == 1:
            new_headx = self.snake_headx - 10
            new_heady = self.snake_heady
        elif heading == 2:
            new_headx = self.snake_headx + 10
            new_heady = self.snake_heady
        elif heading == 3:
            new_heady = self.snake_heady - 10
            new_headx = self.snake_headx
        elif heading == 4:
            new_heady = self.snake_heady + 10
            new_headx = self.snake_headx
        
        self.new_head = [new_headx, new_heady]
        
        
        
        
    def collision(self, box = None):
        """
        two ways of collision.
        1) snake head collides with the boundary of the screen
        2) snake head collides with the body        

        Returns
        -------
        bool
            DESCRIPTION.

        """
        if self.snake[0][0] > self.width or self.snake[0][0] < 0 or self.snake[0][1] > self.height or self.snake[0][1] < 0:
            return True
        elif self.snake[0] in self.snake[1:]:
            return True
    
    def display(self):
        """
        Draw in the rectangles for food and snake.

        Returns
        -------
        None.

        """
        self.screen.fill("black")
        for body in self.snake:
            pygame.draw.rect(self.screen, snake_col, [body[0], body[1], 10, 10])

            
        pygame.draw.rect(self.screen, food_col, [self.food[0], self.food[1], 10, 10])

    
        pygame.font.init()
        font = pygame.font.SysFont('calibri', 15)
        img = font.render("Score: {0}".format(self.score), True, (0, 255, 150))
        self.screen.blit(img, (280, 10))
        
        pygame.display.flip()
        
if __name__ == '__main__':
    start_game = Snake()
    
    game = True
    
    while True:
        game, high_score = start_game.game_move()
        
        if game == True:
            break
        
    #print(score?)
    print("You're score is:", high_score)
    pygame.quit()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
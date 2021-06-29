# Snake-QLearning

This repository contains the code for running and visualizing the classic arcade game 'Snake', controlled by deep Q learning agent.

The ``Snake`` file contains the core of this project, and includes 4 packages. First ``Snake_human`` for building the classic **Snake** game controlled by user input. ``Snake_AI.py`` very much clones the human controlled version of the game, instead is only controlled by computer inputs. Third, ``QAgent.py`` is the Q agent that will try to learn the game. Lastly, ``DQL_Model.py`` is the deep q learning algorithm.

Next, ``video`` file contains the sample learning videos and other miscellaneous example videos that will help visualize how the Q learning behaves as generation increases. 

## Installation

Summary of all the required packages/libraries to install before running:
- pygame
- numpy
- Random
- matplotlib
- pytorch

To install these packages simply go to https://packaging.python.org/tutorials/installing-packages/

Or type "pip install <package>" in your command prompt.
  
## Running Script
To run and visualize the Deep Q learning network, simply run ``QAgent.py`` file. 

If you would like to end the algorithm, just close the pygame.
  
At the end of the algorithm, it will output a single image file showing performance against number of generations.
  
If you would like to change some of the parameters used in the algorithm, feel free to change them.
  Some of these include:
  - height, width of the game
  - number of layers, neuros in neural network
  - learning rate, gamma, epsilon
  - batch size
  - maximum memory
  
**For Example**
  
  
  ![Plot](https://user-images.githubusercontent.com/67341452/123872151-ab2dce80-d902-11eb-89e9-f56c15e08025.png)

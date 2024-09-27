Aim Trainer Game
This is a simple Aim Trainer Game built with Python and Pygame to help you improve your reaction time and aiming accuracy. The game generates random targets of various shapes and colors on the screen, which grow and shrink over time. Your goal is to click as many targets as possible before you run out of lives.

Features
Randomized Targets: Targets are generated with random shapes (circle, square, triangle, star) and random colors (red, green, blue, yellow, purple).
Dynamic Growth: Targets grow and shrink over time, adding challenge to the gameplay.
Score Tracking: The game tracks your hit count, click accuracy, and target speed.
End Game Options: When the game ends, you can choose to either restart the game or quit.
Three Lives: You have 3 lives. If you miss too many targets, the game is over.
Gameplay
A variety of targets will appear randomly on the screen. You need to click on them before they disappear.
The game tracks the number of successful hits, missed targets, and your overall accuracy.
Once you miss 3 targets, the game will display your final score and give you the option to play again or quit.
Controls
Mouse Click: Click on the targets to hit them.
R Key: Press R to restart the game after it ends.
Q Key: Press Q to quit the game after it ends.
Installation and Setup
Install Python: Make sure you have Python installed. You can download it from python.org.

Install Pygame: You need to install Pygame to run the game. Use the following command to install it via pip:

bash
pip install pygame
Download the Code: Clone or download this repository to your local machine.

Run the Game: Navigate to the folder where the code is located and run the main.py file:

bash
python main.py
How to Play
Run the game by executing main.py.
Targets will start appearing on the screen.
Click on the targets before they disappear to earn points.
You lose a life for every missed target.
Once all lives are lost, the game will end and display your stats.
Press R to restart the game or Q to quit.
Game Stats
Time: The total time spent in the game.
Speed: The number of targets hit per second.
Hits: The total number of targets you successfully clicked.
Accuracy: The percentage of your clicks that hit a target.
Code Overview
Target Class: Handles target creation, random color and shape assignment, and growth/shrinking behavior.
Main Game Loop: Controls the flow of the game, target generation, mouse click detection, and screen updates.
End Screen: Displays the final score and stats when the game ends. Offers options to restart or quit.
Requirements
Python 3.x
Pygame 2.x or later
License
This project is open-source and free to use for personal or educational purposes.

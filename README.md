# BaseFibonacciDivisionGame
Make dividing in base Fibonacci a game

# Environment
conda create --name py310_game python=3.10
pip install -r requirements.txt

# Clicking on Cells

Grid object that is a list of list of Cell objects
Initialize Cell Object
 - value: 
 - rectangle object inside of it
 - position (x,y)
 - top-left (x,y)
 - top-right (x,y)
 - bot-right (x,y)
 - bot-left (x,y)
 - [skip] color (whenever value changes, automatically trigger a change in color)
    - if value is 0: background is gray
    - if value is 1:

Hover effect on clickable objects to indicate they're clickable
Handle user clicks (and drags) to cell objects
- on click, highlight valid moves


If they click on a red cell
-> then 
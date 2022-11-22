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

# Event Class (handle dragging)
  - If button pressed down and collides with some rectangle


# Initial setup for dragging
0. Helper Methods:
  -> For a given cell, return the row/column its in
  -> For a given cell, return the (x,y) co-ordinate of its center position
  -> For a (x,y) position, return the cell that it falls within
    -> this should be something
    -> [After this is done,can then use is_valid_move as we can pass in 
    cell_x, cell_y indices

0. Want to show the cell (row #, col #) that the mouse is currently in. If its not on top of a cell
then we want to show that as well

1. HELPER Methods

# Next Steps for Dragging

3. Can likely refactor to be comprehensive in regards to grid building

0. Integrate general dragging of arbitrary element

1. Enable dragging for any of the red cells

2. Constrain dragging to only be able to go up one or right one
    -> can have various "constraints" be added/passed so its easy 
    to quickly add/remove constraints to be  
[organize/refactor classes]

3. Use the Cell Class effectively

4. Want a function that when given a cell, it returns the positions that the cell can be moved to. Another functionw will take these positions (or cells) and reflect it on the GUI. After the cell is no longer hovered over 



# REFACTORING
Grid should not be in charge of validation











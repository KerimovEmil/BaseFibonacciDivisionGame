# Potentially want to pass cell object
# rather than cell_x, cell_y
class Move:

	direction_handler = {
		"LEFT":  self.move_left,
		"RIGHT": self.move_right,
		"UP": self.move_up,
		"DOWN": self.move_down
	}
	
	def __init__(self,grid: 'Grid', cell_x:int,cell_y:int, direction:str) -> None:
		"""
		Change the board position based on the move.
		Args:
		    cell_x: x index location of array
		    cell_y: y index location of array
		    direction: 'DOWN', 'UP', 'LEFT', 'RIGHT'

		Returns: boolean if the move was valid

		"""
		self.grid = grid
		self.cell_x = cell_x
		self.cell_y = cell_y
	
	def is_valid(self, cell_x: int, cell_y: int, direction: str) -> bool:
	    """
	    Computes if the move is valid
	    Args:
	        cell_x: x index location of array
	        cell_y: y index location of array
	        direction: 'DOWN', 'UP', 'LEFT', 'RIGHT'

	    Returns: boolean if the move was valid
	    """
	    # todo confirm that the bottom left is self.width, self.height and not 0,0
	    if direction == 'LEFT':
	        if cell_x == self.grid_width:
	            # special case
	            return self.array[cell_y][cell_x].value > 1
	        return self.array[cell_y][cell_x + 1].value > 1

	    if direction == 'RIGHT':
	        return cell_x != self.grid_width

	    if direction == 'DOWN':
	        return cell_y != self.grid_height

	    if direction == 'UP':
	        if cell_y == self.grid_height:
	            # special case
	            return self.array[cell_y][cell_x].value > 1
	        else:
	            return self.array[cell_y + 1][cell_x].value > 1


	def make_move(self) -> bool:
		if not self.is_valid(cell_x, cell_y, direction):
		    return False
	    
	    direction_handler[direction]()

		return True

	def move_left(self):
		if cell_x == self.grid_width:
		    # special case
		    if self.array[cell_y][cell_x].value > 1:
		        self.array[cell_y][cell_x].change_value(-2)
		        self.array[cell_y][cell_x - 1].change_value(1)
		self.array[cell_y][cell_x].change_value(-1)
		self.array[cell_y][cell_x+1].change_value(-1)
		self.array[cell_y][cell_x-1].change_value(1)
	
	def move_right(self):
		if cell_x == self.grid_width - 1:
		    self.array[cell_y][cell_x].change_value(-1)
		    self.array[cell_y][cell_x+1].change_value(2)
		else:
		    self.array[cell_y][cell_x].change_value(-1)
		    self.array[cell_y][cell_x + 1].change_value(1)
		    self.array[cell_y][cell_x + 2].change_value(1)
	
	def move_up(self):
		if cell_y == self.grid_height:
		    # special case
		    if self.array[cell_y][cell_x].value > 1:
		        self.array[cell_y][cell_x].change_value(-2)
		        self.array[cell_y-1][cell_x].change_value(1)
		else:
		    self.array[cell_y+1][cell_x].change_value(1)
		    self.array[cell_y][cell_x].change_value(-1)
		    self.array[cell_y-1][cell_x].change_value(-1)
	
	def move_down(self):
		if cell_y == self.grid_height - 1:
		    self.array[cell_y][cell_x].change_value(-1)
		    self.array[cell_y - 1][cell_x].change_value(2)
		else:
		    self.array[cell_y][cell_x].change_value(-1)
		    self.array[cell_y - 1][cell_x].change_value(1)
		    self.array[cell_y - 2][cell_x].change_value(1)
		return cell_y != self.grid_height




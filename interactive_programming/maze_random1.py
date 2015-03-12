""" A rotational, computational maze created collaboratively.

@authors: Mackenzie, Jaime, Anisha

"""

import pygame
import random


class Maze():
  """ Main maze class
  """
  def __init__(self):
    """ Initialize the rotating maze game.  Use Maze.run to
        start the game """
    width = 500   #we can change later if needed
    height = 500  #we can change later if needed
    self.model = MazeModel(width, height)
    self.view = MazeView(self.model, width, height)
    self.controller = MazeController(self.model)
    self.clock = pygame.time.Clock()

  def run(self):
    """ the main runloop... loop until death """
    while not(self.model.board.at_end()):
      self.view.draw()
      self.controller.process_events()
      self.model.update()
      self.clock.tick(60)
    print ("You Win!")
    pygame.quit()


class MazeController():
  """Keyboard Posiitons"""
  def __init__(self, model):
    self.model = model
    self.down_pressed = False
    self.up_pressed = False
    self.right_pressed = False
    self.left_pressed = False

  def process_events(self):
    """ process keyboard events.  This must be called periodically
        in order for the controller to have any effect on the game """
    for event in pygame.event.get():
      # If the user pressed a key
      if event.type == pygame.KEYDOWN:
        # Figure out if it was an arrow key. If so, adjust speed.
        if event.key == pygame.K_LEFT:
          self.model.board.x_speed =- 3
        elif event.key == pygame.K_RIGHT:
          self.model.board.x_speed = 3
        elif event.key == pygame.K_UP:
          self.model.board.y_speed =- 3
        elif event.key == pygame.K_DOWN:
          self.model.board.y_speed = 3
      # User let up on a key
      elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
        if event.key == pygame.K_LEFT:
          self.model.board.x_speed=0
        elif event.key == pygame.K_RIGHT:
          self.model.board.x_speed=0
        elif event.key == pygame.K_UP:
          self.model.board.y_speed=0
        elif event.key == pygame.K_DOWN:
          self.model.board.y_speed=0
    # Get the next coordinates of the object according to the speed vector.
    new_point_x = self.model.board.fixed_point.x - self.model.board.x_speed
    new_point_y = self.model.board.fixed_point.y - self.model.board.y_speed
    self.model.board.update()
    # See if moving to the next position will cause the point and walls to collide
    if not self.model.board.will_collide(new_point_x, new_point_y):
      self.model.board.x_coord = self.model.board.x_coord + self.model.board.x_speed
      self.model.board.y_coord = self.model.board.y_coord + self.model.board.y_speed

class MazeModel():
  """represents the game state of our maze"""
  def __init__(self, width, height):
    """ Initialize the maze model """
    self.width = width
    self.height = height
    self.board = Board(width, height)

  def update(self):
    """ Updates the model and its constituent parts """
    self.board.update()

  def is_dead(self):
    running = True
    while running == True:
      for event in pygame.event.get():
        if event.type == QUIT:
          running = False   #Exiting the while loop
      screen.blit(background, (0,0))
      pygame.display.update()
      pygame.quit() #Call the quit() method outside the while loop to end the application

class MazeView():
  def __init__(self, model, width, height):
    """ Initialize the view for the maze.  The input model
        is necessary to find the position of relevant objects
        to draw. """
    pygame.init()
    # to retrieve width and height use screen.get_size()
    self.screen = pygame.display.set_mode((width, height))
    # this is used for figuring out where to draw stuff
    self.model = model
    self.width = width
    self.height = height

  def draw(self):
    """ Redraw the full game window """
    self.screen.fill((0,0,0))

    # Draw board with rects from a list of tuples, where the
    # first value is the rect object, and the second value is the color
    tuple_rects = self.model.board.get_rects()
    for t in tuple_rects:
      pygame.draw.rect(self.screen, t[1], t[0])

    # Draw fixed point with rectangle
    color = pygame.Color(255, 238, 0) #a nice violet color
    rect = self.model.board.fixed_point
    pygame.draw.rect(self.screen, color, rect)
    pygame.display.update()

class Board():
  """ Describes the board maze """
  def __init__(self, width, height):
    self.width = width
    self.heigth = height
    self.box_width = 32
    self.background = pygame.Surface((int(width), int(height)))
    self.fixed_point = pygame.Rect(width/2 + 5, height/2 + 5, self.box_width - 10, self.box_width - 10)
    self.walls = []
    self.rects = []
    self.matrix = Matrix(5, 5)
    self.matrix.make_random_maze()

    # Speed in pixels per frame
    self.x_speed = 0
    self.y_speed = 0
    # Starting position
    self.x_coord = width/2 - self.box_width
    self.y_coord = height/2 - self.box_width

  def update(self):
    self.rects = self.get_rects()
    
  def get_rects(self):
    """ Gets a list of rects that represent the positions
        in the board of free space and walls.

        returns: rects, which is a list of tuples, storing
        the rect objects and the corresponding colors
    """
    rects = []
    self.walls = []
    for r in range(len(self.matrix.matrix)): #loop through rows
      for c in range(len(self.matrix.matrix[r])): # loop through columns
        # get image depending on what number is in the matrix
        is_wall = False
        is_end = False
        if self.matrix.matrix[r][c] == 1: #free
          color = pygame.Color(0, 0, 0)
        elif self.matrix.matrix[r][c] == 0: #wall
          is_wall = True
          color = pygame.Color(0, 0, 255)
        elif self.matrix.matrix[r][c] == 2: #start
          color = pygame.Color(0, 255, 0)
        else: #end
          is_end = True
          color = pygame.Color(255, 0, 0)
        # get the absolute positions for the point at which to draw the squares
        width = self.box_width
        left = self.x_coord + (width * c)
        top = self.y_coord + (width * r)
        rectt = pygame.Rect(left, top, width, width)
        rects.append((rectt, color))
        if is_wall:
          self.walls.append(rectt)
        elif is_end:
          self.end = rectt
    return rects

  def will_collide(self, temp_x, temp_y):
    """generates temp x and y pos to check if a collision will occur"""
    new_point = pygame.Rect(temp_x, temp_y, self.box_width - 10, self.box_width - 10)
    self.update()
    for wall in self.walls:
      if wall.colliderect(new_point):
        return True
    return False

  def at_end(self):
    """ Checks whether the fixed point is at the end """
    self.update()
    return self.end.contains(self.fixed_point)

class Matrix():
    """ Randomly creates a matrix that serves as the maze """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = []
        # The set of units with which the maze will be built
        # Each is a two by two matrix, with one block of "wall"
        self.units = [[[0,1],[1,1]],[[1,0],[1,1]],[[1,1],[0,1]],[[1,1],[1,0]]]

    def make_random_maze(self):
        # Empty the matrix
        self.matrix = []
        # Fill the matrix randomly with the redefined units
        for r in range(0, self.height*2, 2):
            self.matrix.append([])
            self.matrix.append([])
            for c in range(0, self.width*2, 2):
                unit = self.units[random.randrange(4)]
                self.matrix[r] += unit[0]
                self.matrix[r+1] += unit[1]

        # Add a border of walls
        self.matrix.insert(0, [])
        self.matrix.insert(len(self.matrix), [])
        for i in range(len(self.matrix[1])):
          self.matrix[0].append(0)
          self.matrix[len(self.matrix)-1].append(0)
        for r in self.matrix:
          r.insert(0, 0)
          r.append(0)

        # Set the starting and stopping points
        self.matrix[1][1] = 2
        self.matrix[-2][-2] = 3
        self.matrix[-2][-3] = 1
        self.matrix[-3][-2] = 1
        self.matrix[-3][-3] = 1

if __name__ == '__main__':
    maze = Maze()
    maze.run()

""" A rotational, computational maze created collaboratively.

@authors: Mackenzie, Jaime, Anisha

"""

import pygame 


class Maze():
  """ Main maze class
  """
  def __init__(self):
    """ Initialize the rotating mazae game.  Use Maze.run to
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
    print "You Win!"


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
      if event.type == pygame.QUIT:
        self.model.is_dead() == True

        
      elif event.type == pygame.KEYDOWN:
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
          
    # Move the object according to the speed vector.
    new_point_x = None
    new_point_y = None
    new_point_x = self.model.board.fixed_point.x - self.model.board.x_speed
    new_point_y = self.model.board.fixed_point.y - self.model.board.y_speed
    self.model.board.update()
    if self.model.board.will_collide(new_point_x, new_point_y):
      pass
    else:
      self.model.board.x_coord = self.model.board.x_coord + self.model.board.x_speed
      self.model.board.y_coord = self.model.board.y_coord + self.model.board.y_speed
    #Initiates collision detection 


class MazeModel():
  """represents the game state of our maze"""
  
  def __init__(self, width, height):
    """ Initialize the flappy model """
    self.width = width
    self.height = height
    self.board = Board(width, height)


  def get_drawables(self):
    """ Return a list of DrawableSurfaces for the model """
    return self.board.get_drawables()

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
    self.screen.fill((0,0,0)) # COLOR is midnihgt blue
    
    # Draw board with rects
    tuple_rects = self.model.board.get_rects()
    for t in tuple_rects:
      pygame.draw.rect(self.screen, t[1], t[0])
    
    # Draw fixed point with rectangle
    color = pygame.Color(255,238,0) #a nice violet color
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
    #self.fixed_point = FixedPoint(width/2, height/2)
    self.fixed_point = pygame.Rect(width/2 + 5, height/2 + 5, self.box_width - 10, self.box_width - 10)
    self.walls = []
    self.rects = []
    self.matrix = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
                   [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                   [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                   [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                   [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
                   [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
                   [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
                   [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1],
                   [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                   [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 3, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
                   
    

    # Speed in pixels per frame
    self.x_speed = 0
    self.y_speed = 0
    # Current position
    self.x_coord = width/2 - self.box_width
    self.y_coord = height/2 - self.box_width
  
  def update(self):
    self.rects = self.get_rects()
  
  def get_rects(self):
    # rects is a dictionary of tuples, where the keys are
    # rect objects and the values are the colors of the rects
    rects = []
    self.walls = []
    for r in range(len(self.matrix)): #loop through rows
      for c in range(len(self.matrix[r])): # loop through columns
        # get image depending on what number is in the matrix
        is_wall = False
        is_end = False
        if self.matrix[r][c] == 0: #free
          color = pygame.Color(0,0,0)
        elif self.matrix[r][c] == 1: #wall
          is_wall = True
          color = pygame.Color(0, 0, 255)
        elif self.matrix[r][c] == 2: #startt
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

#need to define positions and velocities below as generated in controller
  def will_collide(self, temp_x, temp_y):
    """generates temp x and y pos to check if a collision will occur"""
    new_point = pygame.Rect(temp_x, temp_y, self.box_width - 10, self.box_width - 10)
    self.update()
    for wall in self.walls:
      if wall.colliderect(new_point):
        return True
    return False
  
  def at_end(self):
    """generates temp x and y pos to check if a collision will occur"""
    self.update()
    if self.end.contains(self.fixed_point):
      return True
    else:
      return False
    

if __name__ == '__main__':
    maze = Maze()
    maze.run()

pygame.quit()

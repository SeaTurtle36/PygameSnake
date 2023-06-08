# Snake made with pygame
import pygame
import random
pygame.font.init()

WINDOW = pygame.display.set_mode((410, 410))
FPS = 60
score = 1
snake_length = []
game_start = False
game_started = False

animation_time_prev = 0
animation_trigger = False
animation_time = 200


#########################################################

class Snake:
    def __init__(self, colour, x_pos, y_pos, width, height):
        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.colour = colour
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.speed = 25
        self.snake_length = []
        self.head = False
        self.visible = False

  
    def draw(self):
        if self.visible == True:
          self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
          pygame.draw.rect(WINDOW, self.colour, self.rect)

#########################################################

class Snack:
  def __init__(self, colour, x_pos, y_pos, width, height):
    self.rect = pygame.Rect(x_pos, y_pos, width, height)
    self.colour = colour
    self.x_pos = x_pos
    self.y_pos = y_pos
    self.width = width
    self.height = height
    self.visible = True

  
  def draw(self):
    pygame.draw.rect(WINDOW, self.colour, self.rect)


  def pos(self, x_pos, y_pos):
    self.x_pos = x_pos
    self.y_pos = y_pos

#########################################################

def draw_window():
    WINDOW.fill((0, 0, 10))
    for x in range(0, 410, 16):
        pygame.draw.line(WINDOW, (0, 0, 255), (1, x), (400, x), 1)
        pygame.draw.line(WINDOW, (0, 0, 255), (x, 1), (x, 400), 1)


def check_animation_time():
    global animation_time_prev
    global animation_trigger
    global animation_time

    animation_trigger = False

    time_now = pygame.time.get_ticks()

    if time_now - animation_time_prev > animation_time:
      animation_time_prev = time_now
      animation_trigger = True


def move_snake(direction):
    global snake_length
    global game_start
    global game_started

    new_x = 0
    new_y = 0
    temp_x = 0
    temp_y = 0

    for bug in snake_length:
        temp_x = bug.x_pos
        temp_y = bug.y_pos
        bug.visible = True

        if bug.head == True:
            if direction == "left":
                bug.x_pos = bug.x_pos - 16

            if direction == "right":
                bug.x_pos = bug.x_pos + 16

            if direction == "up":
                bug.y_pos = bug.y_pos - 16

            if direction == "down":
                bug.y_pos = bug.y_pos + 16

        else:
            bug.x_pos = new_x
            bug.y_pos = new_y

        new_x = temp_x
        new_y = temp_y

        if bug.head == True:
            for other_bug in snake_length:
                if other_bug.head == False:
                    if bug.rect.colliderect(other_bug.rect):
                        game_start = False
                        game_started = True


def handle_snack(snack_list, bug):
  global score
  global animation_time
  for bug in snake_length:
    for snack in snack_list:
      snack.draw()
      if bug.rect.colliderect(snack.rect) and bug.head == True:
        snack_list.remove(snack)
        snack = Snack((255, 0, 0), 16 * random.randint(0, 24), 16 * random.randint(0, 24), 16, 16)
        snack_list.append(snack)
        score += 1
        new_bug = Snake((0, 255, 0), 100, 100, 16, 16)
        new_bug.visible = False
        snake_length.append(new_bug)
        animation_time -= 10


def handle_borders():
  global game_start
  global game_started
  for bug in snake_length:
    if bug.rect.x >= 400 and bug.head == True or bug.rect.x <= -25 and bug.head == True:
      game_start = False
      game_started = True

    if bug.rect.y >= 400 and bug.head == True or bug.rect.y <= -25 and bug.head == True:
      game_start = False
      game_started = True

text_font = pygame.font.SysFont("monospace", 15)


def display_text(text, text_font, text_col, x, y):
  img = text_font.render(text, True, text_col)
  WINDOW.blit(img, (x, y))


def entry_screen(keys_pressed):
  global game_start
  display_text("Snake \r press LCTRL to play", text_font, (255, 255, 255), 25, 350)
  if keys_pressed[pygame.K_LCTRL]:
    game_start = True


def end_screen(keys_pressed):
  global game_start
  display_text(f"Game over \r score: {score - 1}", text_font, (255, 255, 255), 25, 350)

def main():
    global snake_length
    global score
    global game_start
    global game_started

    direction = "left"
    clock = pygame.time.Clock()
    run = True
    snack_list = []

    for i in range(score):
        bug = Snake((0, 255, 0), 208, 112, 16, 16)
        if i == 0:
            bug.head = True

        snake_length.append(bug)

    snack_list.append(Snack((255, 0, 0), 16 * random.randint(0, 16), 16 * random.randint(0, 16), 16, 16))

    while run:
        clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()


        if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]) and direction != "right":
            direction = "left"

        if (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]) and direction != "left":
            direction = "right"

        if (keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]) and direction != "up":
            direction = "down"

        if (keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]) and direction != "down":
            direction = "up"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()
        if game_start == False and game_started == False:
          entry_screen(keys_pressed)
        if game_start == True:
          handle_snack(snack_list, bug)
          check_animation_time()
          if animation_trigger == True:
            move_snake(direction)
          for bug in snake_length:
            bug.draw()
          handle_borders()

        if game_start == False and game_started == True:
          end_screen(keys_pressed)
        
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()


main()

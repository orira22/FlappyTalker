import pygame
import random

pygame.init()

def main():
    #Screen define
    WIDTH, HEIGHT = 864, 768
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird!")

    #Game variables
    clock = pygame.time.Clock()
    FPS = 60
    ground_movement = 0
    ground_speed = 4
    flying = False
    game_over = False
    PIPE_GAP = 150
    PIPE_FREQUENCY = 1500 #In milliseconds
    last_pipe = pygame.time.get_ticks() - PIPE_FREQUENCY
    score = 0
    pass_pipe = False

    FONT = pygame.font.SysFont("Bauhaus 93", 60)
    WHITE = (255, 255, 255)

    #Load images
    BG = pygame.image.load("Bird/Stuff/back3.png")
    GROUND = pygame.image.load("Bird/Stuff/ground.png")
    RESTART_BUTTON = pygame.image.load("Bird/Stuff/restart.png")

    #Drawing score function
    def draw_score(text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        WIN.blit(img, (x, y))

    def reset_game():
        pipe_group.empty()
        flappy.rect.x = 100
        flappy.rect.y = HEIGHT // 2
        return 0

    #Bird class
    class Bird(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            self.index = 0
            self.counter = 0
            for num in range(1, 4):
                img = pygame.image.load(f"Bird/Stuff/bird{num}.png")
                self.images.append(img)
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            self.velocity = 0
            self.clicked = False

        def update(self):
            if flying:
                #Set up the gravity
                self.velocity += 0.5
                if self.velocity > 8:
                    self.velocity = 8
                if self.rect.bottom < 600:
                    self.rect.y += int(self.velocity)
            #Jump, animation and rotation of the bird if game is not over
            if not game_over:
                #Jumping
                if pygame.mouse.get_pressed()[0] == 1 and not(self.clicked):
                    self.clicked = True
                    self.velocity = -10
                elif pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False

                #Controls the animation
                self.counter += 1
                flap_cooldawn = 5
                if self.counter > flap_cooldawn:
                    self.counter = 0
                    self.index += 1
                    if self.index >= 2:
                        self.index = 0
                self.image = self.images[self.index]

                #Rotation in rise and fall
                self.image = pygame.transform.rotate(self.images[self.index], -2 * self.velocity)
            else:
                self.image = pygame.transform.rotate(self.images[self.index], -90)
    
    #Pipe class
    class Pipe(pygame.sprite.Sprite):
        def __init__(self, x, y, position):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("Bird/Stuff/pipe.png")
            self.rect = self.image.get_rect()
            #Position 1 is from the top, and -1 is from the bottom
            if position == 1:
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect.bottomleft = [x, y - int(PIPE_GAP / 2)]
            if position == -1:
                self.rect.topleft = [x, y + int(PIPE_GAP / 2)]

        def update(self):
            self.rect.x -= ground_speed
            if self.rect.right < 0:
                self.kill()

    class Button():
        def __init__(self, x, y, img):
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

        def draw(self):
            restart_action = False

            #Draw the restart button on the screen
            WIN.blit(self.image, (self.rect.x, self.rect.y))

            #Check mouse position
            pos = pygame.mouse.get_pos()

            #Bumping check
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    restart_action = True
            return restart_action




    bird_group = pygame.sprite.Group()
    pipe_group = pygame.sprite.Group()

    flappy = Bird(100, int(HEIGHT / 2))
    bird_group.add(flappy)

    button = Button(WIDTH // 2 - 50, HEIGHT // 2 - 100, RESTART_BUTTON)

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
                flying = True

        #Draw background
        WIN.blit(BG, (0, 0))
        
        #Bird animation
        bird_group.draw(WIN)
        bird_group.update()
        pipe_group.draw(WIN)

        #Draw the ground
        WIN.blit(GROUND, (ground_movement, 600))

        #Score check
        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
                pass_pipe = True
            elif pass_pipe:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False

        draw_score(str(score), FONT, WHITE, int(WIDTH / 2), 20)


        #Check if the bird bumped into a pipe
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            game_over = True

        #Check hit the floor
        if flappy.rect.bottom >= 600:
            game_over = True
            flying = False

        if not game_over and flying:
            #Pipes generating
            current_time = pygame.time.get_ticks()
            if current_time - last_pipe > PIPE_FREQUENCY:
                pipe_height = random.randint(-125, 100)
                bottom_pipe = Pipe(WIDTH, int(HEIGHT / 2) + pipe_height, -1)
                top_pipe = Pipe(WIDTH, int(HEIGHT / 2) + pipe_height, 1)
                pipe_group.add(bottom_pipe)
                pipe_group.add(top_pipe)
                last_pipe = current_time

            #Move the ground
            ground_movement -= ground_speed
            if abs(ground_movement) > 35:
                ground_movement = 0
            pipe_group.update()

        #Reset the game when it's over
        if game_over:
            if button.draw():
                game_over = False
                score = reset_game()
        
        pygame.display.update()

if __name__ == "__main__":
    main()
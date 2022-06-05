import pygame, time, math , random, sys, requests
from pypresence import Presence #pip install pypresence

pygame.mixer.init()
pygame.init()

def main():
    #Screen define
    WIDTH, HEIGHT = 864, 768
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_icon(pygame.image.load("Stuff/icon.png"))
    pygame.display.set_caption("Flappy Talker!")

    #Game variables
    clock = pygame.time.Clock()
    diccord_client_id = "982617952325074954"
    FPS = 60
    ground_movement = 0
    ground_speed = 4
    flying = False
    game_over = False
    PIPE_GAP = 160
    PIPE_FREQUENCY = 1500 #In milliseconds
    last_pipe = pygame.time.get_ticks() - PIPE_FREQUENCY
    score = 0
    pass_pipe = False
    best_world_score = 0
    last_score = 0
    
    FONT = pygame.font.SysFont("Bauhaus 93", 60)
    INTRO_FONT = pygame.font.SysFont("Bauhaus 93", 90)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LIGHT_GREEN = (18, 242, 120)
    INTRO_COLOR = "#55c0cb"

    #Load images
    BG = pygame.image.load("Stuff/back.png")
    GROUND = pygame.image.load("Stuff/ground.png")
    START_BUTTON = pygame.image.load("Stuff/StartButton.png")
    RESTART_BUTTON = pygame.image.load("Stuff/restart.png")
    tutorial = pygame.image.load("Stuff/tutorial.png") 

    #sounds
    game_over_sound = pygame.mixer.Sound('Stuff/gameOverSound.wav')
    JUMP_SOUND = pygame.mixer.Sound('Stuff/jump.wav')


    def update_server(score_var=None):
        if score_var:
            try:
                requests.get(f'https://flappytalker.herokuapp.com/score?score={score_var}')
            except:
                pass
        else:
            try:
                return requests.get('https://flappytalker.herokuapp.com/score').text.split('\n', 1)[0]
            except:
                return -1
    def update_discord_status(large_image,large_text,details,state):
        RPC.update(
            large_image = large_image, #name of your asset
            large_text = large_text,
            details = details,
            state = state,
            start = start
        )



    def loading_screen():
        update_discord_status("logo","Flappy Talker","on loading screen","loading")
        LOADING_BG = pygame.image.load("Stuff/LoadingBarBackground.png")
        LOADING_BAR = pygame.image.load("Stuff/LoadingBar.png")
        LOADING_BG_RECT = LOADING_BG.get_rect(center=(425, 450))
        LOADING_BAR_RECT = LOADING_BAR.get_rect(midleft=(0, 450))
        loading_finished = True
        loading_progress = 0
        loading_bar_width = 8
        JUMP_SOUND.set_volume(0.2)

        while loading_finished:
            WIN.fill("#0d0e2e")
            draw_score("Flappy Talker", INTRO_FONT, LIGHT_GREEN, 150, 200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            loading_progress += 0.7
            loading_bar_width = math.ceil(loading_progress)
            LOADING_BAR = pygame.transform.scale(LOADING_BAR, (int(loading_bar_width), 150))
            LOADING_BAR_RECT = LOADING_BAR.get_rect(midleft = (60, 450))
            WIN.blit(LOADING_BG, LOADING_BG_RECT)
            WIN.blit(LOADING_BAR, LOADING_BAR_RECT)
            pygame.display.update()
            color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(30)]
            if loading_progress >= 730:
                for i in range(20):
                    time.sleep(0.1)
                    WIN.fill(color[i])
                    loading_progress = random.randint(0, 730)
                    loading_bar_width = math.ceil(loading_progress)
                    LOADING_BAR = pygame.transform.scale(LOADING_BAR, (int(loading_bar_width), 150))
                    WIN.blit(LOADING_BG, LOADING_BG_RECT)
                    WIN.blit(LOADING_BAR, LOADING_BAR_RECT)
                    draw_score("Flappy Talker", INTRO_FONT, BLACK, 150, 200)
                    pygame.display.update()


                loading_finished = False
        best_world_score = int(update_server()) or -1
        print(best_world_score)
        intro()

    def death():
        global death_sound_counter
        update_discord_status("logo","Flappy Talker","on the fild","dead")
        if death_sound_counter == 0:
            game_over_sound.play()
            death_sound_counter += 1

    def intro():
        update_discord_status("logo","Flappy Talker","on main screen screen","last score: "+str(last_score))
        best_world_score = int(update_server())
        global death_sound_counter
        death_sound_counter = 0
        WIN.fill(INTRO_COLOR)
        intro = True
        ANIMATION_IMGS = []
        for i in range (1, 20):
            ANIMATION_IMGS.append(pygame.image.load(f"Stuff/intro{i}.png"))
        if best_world_score != -1:
            best_world_score = int(update_server())
        index = 0
        counter = 0
        cooldawn = 27
        current_img = ANIMATION_IMGS[0]
        pygame.mixer.music.load('Stuff/intromusic.wav')
        pygame.mixer.music.set_volume(float(0.1)) # 0.0 - 1.0
        pygame.mixer.music.play(-1)
        while intro:
            WIN.fill(INTRO_COLOR)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            counter += 1
            if counter > cooldawn:
                counter = 0
                index += 1
                if index >= 19:
                    index = 0
            current_img = ANIMATION_IMGS[index]
            WIN.blit(current_img, (300, -20))
            draw_score("Flappy Talker", INTRO_FONT, BLACK, 150, 200)
            draw_score("world's best score:", INTRO_FONT, LIGHT_GREEN, 80, 530)
            draw_score(str(best_world_score), INTRO_FONT, LIGHT_GREEN, WIDTH//2-70, 650)
            if start_button.draw():
                intro = False
            pygame.display.update()
        pygame.mixer.music.stop()

        

    #Drawing score function
    def draw_score(text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        WIN.blit(img, (x, y))

    def reset_game(score):
        global clicks
        update_server(score)
        pipe_group.empty()
        flappy.rect.x = 100
        flappy.rect.y = HEIGHT // 2
        intro()
        clicks = 0

    #Bird class
    class Bird(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            self.index = 0
            self.counter = 0
            for num in range(1, 4):
                img = pygame.image.load(f"Stuff/bird{num}.png")
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
                global clicks
                #Jumping
                if pygame.mouse.get_pressed()[0] == 1 and not(self.clicked):
                    self.clicked = True
                    self.velocity = -10
                    if intro != True:
                        JUMP_SOUND.play()
                    clicks += 1
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
            self.image = pygame.image.load("Stuff/pipe2.png")
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

    #The class of all the buttons used in the game
    class Button():
        def __init__(self, x, y, img):
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

        def draw(self):
            action = False

            #Draw the restart button on the screen
            WIN.blit(self.image, (self.rect.x, self.rect.y))

            #Check mouse position
            pos = pygame.mouse.get_pos()

            #Bumping check
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    action = True
            return action




    bird_group = pygame.sprite.Group()
    pipe_group = pygame.sprite.Group()

    flappy = Bird(100, int(HEIGHT / 2))
    bird_group.add(flappy)

    start_button = Button(WIDTH // 2 - 170, HEIGHT // 2 - 40, START_BUTTON)
    restart_button = Button(WIDTH // 2 - 50, HEIGHT // 2 - 100, RESTART_BUTTON)

    loading_screen()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
                flying = True

        #Draw background
        WIN.blit(BG, (0, 0))
        if clicks == 1:
            WIN.blit(tutorial, (100, 300))
        
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
                update_discord_status("logo","Flappy Talker","on the field","score: "+str(score))

            #Move the ground
            ground_movement -= ground_speed
            if abs(ground_movement) > 35:
                ground_movement = 0
            pipe_group.update()

        #Reset the game when it's over
        if game_over:
            death()
            if restart_button.draw():
                game_over = False
                reset_game(score)
                last_score = score
                score = 0  
        
        pygame.display.update()

if __name__ == "__main__":
    try: requests.get('https://flappytalker.herokuapp.com/score')
    except: pass
    start = int(time.time())
    RPC = Presence("982617952325074954")
    RPC.connect()
    clicks = 0
    main()
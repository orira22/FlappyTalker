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
    last_score = 0


    #Fonts and colors definition
    SCORE_FONT = pygame.font.SysFont("Bauhaus 93", 60)
    INTRO_FONT = pygame.font.SysFont("Bauhaus 93", 90)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    LIGHT_GREEN = (18, 242, 120)
    INTRO_COLOR = "#55c0cb"

    #Images loading
    BG = pygame.image.load("Stuff/back.png")
    GROUND = pygame.image.load("Stuff/ground.png")
    START_BUTTON = pygame.image.load("Stuff/StartButton.png")
    RESTART_BUTTON = pygame.image.load("Stuff/restart.png")
    TUTORIAL = pygame.image.load("Stuff/tutorial.png")
    MUTE_BUTTON = pygame.image.load("Stuff/mute.png")
    UNMUTE_BUTTON = pygame.image.load("Stuff/unmute.png")
    

    #Sounds 
    GAME_OVER_SOUND = pygame.mixer.Sound('Stuff/gameOverSound.wav')
    JUMP_SOUND = pygame.mixer.Sound('Stuff/jump.wav')
    #Sounds volume 0.0 -- 1.0
    JUMP_SOUND.set_volume(float(0.1))
    pygame.mixer.music.set_volume(float(0.1))
    GAME_OVER_SOUND.set_volume(float(0.2))

    #Drawing text to the window function
    def draw_text(text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        WIN.blit(img, (x, y))

    #The function which updates the server with the highest score
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

    #The function which displays in discord when you play the game 
    def update_discord_status(large_image, large_text, details,state):
        try:
            RPC.update(
                large_image = large_image,
                large_text = large_text,
                details = details,
                state = state,
                start = start
            )
        except:
            pass

    #The function which displays the fake loading screen before the game starts
    def loading_screen():
        update_discord_status("logo", "Flappy Talker", "On loading screen", "loading...")
        LOADING_BG = pygame.image.load("Stuff/LoadingBarBackground.png")
        LOADING_BAR = pygame.image.load("Stuff/LoadingBar.png")
        LOADING_BG_RECT = LOADING_BG.get_rect(center=(425, 450))
        LOADING_BAR_RECT = LOADING_BAR.get_rect(midleft=(0, 450))
        loading_finished = True
        loading_progress = 0
        loading_bar_width = 8

        while loading_finished:
            WIN.fill("#0d0e2e")
            draw_text("Flappy Talker", INTRO_FONT, LIGHT_GREEN, 150, 200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            loading_progress += 0.7
            loading_bar_width = math.ceil(loading_progress)
            LOADING_BAR = pygame.transform.scale(LOADING_BAR, (loading_bar_width, 150))
            LOADING_BAR_RECT = LOADING_BAR.get_rect(midleft = (60, 450))
            WIN.blit(LOADING_BG, LOADING_BG_RECT)
            WIN.blit(LOADING_BAR, LOADING_BAR_RECT)
            pygame.display.update()
            color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(30)]
            if loading_progress >= 730:
                for i in range(20):
                    time.sleep(0.1)
                    WIN.fill(color[i]) #Changes the color in the screen
                    loading_progress = random.randint(0, 730)
                    loading_bar_width = math.ceil(loading_progress) 
                    LOADING_BAR = pygame.transform.scale(LOADING_BAR, (loading_bar_width, 150)) #Make the loading bar move
                    WIN.blit(LOADING_BG, LOADING_BG_RECT)
                    WIN.blit(LOADING_BAR, LOADING_BAR_RECT)
                    draw_text("Flappy Talker", INTRO_FONT, BLACK, 150, 200)
                    pygame.display.update()

                loading_finished = False 
        best_world_score = int(update_server()) or -1
        print(best_world_score)
        intro()

    def change_volume(vol):
        JUMP_SOUND.set_volume(float(vol))
        pygame.mixer.music.set_volume(float(vol))
        GAME_OVER_SOUND.set_volume(float(vol*2))

    #The function which draws the lobby of the game
    def intro():
        global mute
        mute = False
        update_discord_status("logo", "Flappy Talker","In lobby","Last score: " + str(last_score))
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
        index = 0 #Used for creating the animation - for taking photo after a photo by the index in the list
        counter = 0 #Used for gradually increase the variable until it reaches the animation speed 
        ANIMATION_SPEED = 27
        current_img = ANIMATION_IMGS[0]
        pygame.mixer.music.load('Stuff/introMusic.wav')
        pygame.mixer.music.play(-1)
        while intro:
            WIN.fill(INTRO_COLOR) #Erases the previous images of the animation from the screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    quit()
            counter += 1
            if counter > ANIMATION_SPEED:
                counter = 0
                index += 1
                if index >= 19:
                    index = 0
            current_img = ANIMATION_IMGS[index]
            WIN.blit(current_img, (300, -20))
            draw_text("Flappy Talker", INTRO_FONT, BLACK, 150, 200)
            draw_text("world's best score:", INTRO_FONT, LIGHT_GREEN, 80, 530)
            draw_text(str(best_world_score), INTRO_FONT, LIGHT_GREEN, WIDTH // 2 - 70, 650)
            if mute_button.draw2():
                if mute == False:
                    mute_button.change_image(MUTE_BUTTON)
                    mute = True
                    change_volume(0)
                else:
                    mute_button.change_image(UNMUTE_BUTTON)
                    mute = False
                    change_volume(0.1)
            if start_button.draw():
                intro = False
            pygame.display.update()
        pygame.mixer.music.stop()

    #The function which play the game over sound when it is required, and ensures it won't be played over and over again
    def death():
        global death_sound_counter
        update_discord_status("logo","Flappy Talker","On the field","dead :(")
        if death_sound_counter == 0:
            GAME_OVER_SOUND.play()
            death_sound_counter += 1

    #The function which resets the things that should be resetted to their initial settings 
    def reset_game(score):
        global clicks
        update_server(score) #Updates the server with a new world high score(if there is one)
        pipe_group.empty() #Cleans the screen from old pipes
        flappy.rect.x = 100 #Resets talker's position
        flappy.rect.y = HEIGHT // 2 
        intro() #Returning to the lobby
        clicks = 0

    #Bird class
    class Bird(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            self.index = 0
            self.counter = 0
            for num in range(1, 4):
                img = pygame.image.load(f"Stuff/bird{num}.png") #Creates a list with the images required for talker wings' animation
                self.images.append(img)
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            self.velocity = 0 #The velocity of falling to the ground(gravity)
            self.clicked = False

        def update(self):
            if flying:
                #Sets up the gravity
                self.velocity += 0.5
                if self.velocity > 8:
                    self.velocity = 8
                if self.rect.bottom < 600:
                    self.rect.y += int(self.velocity)
            #Jumping, animation and rotation of the bird if the game is not over
            if not game_over:
                global clicks,event
                #Jumping
                if pygame.mouse.get_pressed()[0] == 1 and not(self.clicked): #If the mouse has been left-clicked...
                    self.clicked = True
                    self.velocity = -10 #Makes the bird jump by 10 pixels
                    if intro != True: #If currently you are not in the lobby...
                        JUMP_SOUND.play()
                    clicks += 1
                elif pygame.mouse.get_pressed()[0] == 0: #If the left button of the mouse is released...
                    self.clicked = False #Ensures the bird won't jump infinity times

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
                self.image = pygame.transform.rotate(self.images[self.index], -2 * self.velocity) #Positive number rotates left, and negative right
            else:
                self.image = pygame.transform.rotate(self.images[self.index], -90)
    
    #Pipe class
    class Pipe(pygame.sprite.Sprite):
        def __init__(self, x, y, position):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("Stuff/pipe2.png")
            self.rect = self.image.get_rect()
            #Position 1 is a pipe from the top, and -1 is a pipe from the bottom
            if position == 1:
                self.image = pygame.transform.flip(self.image, False, True) #Flips the pipe to the top of the screen
                self.rect.bottomleft = [x, y - int(PIPE_GAP / 2)]
            if position == -1:
                self.rect.topleft = [x, y + int(PIPE_GAP / 2)]

        def update(self):
            self.rect.x -= ground_speed #Moves the pipes with the ground
            if self.rect.right < 0:
                self.kill() #Remove the pipes from the game when the player can't see them

    #The class of all the buttons used in the game
    class Button():
        def __init__(self, x, y, img):
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)

        def draw(self):
            action = False

            #Draws the button on the screen
            WIN.blit(self.image, (self.rect.x, self.rect.y))

            #Checks mouse position
            pos = pygame.mouse.get_pos()

            #Checks if the mouse is on the button
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1: #Checks if the mouse pressed while it's on the button
                    action = True
            return action
            
        def change_image(self, img): #Used for changing the mute and unmuted images when clicked
            self.image = img
            
        def draw2(self): #An advanced version of the original draw function, in adjustment to the mute and unmute buttons
            ev = pygame.event.get()
            action = False

            #Draw the button on the screen
            WIN.blit(self.image, (self.rect.x, self.rect.y))

            #Check mouse position
            pos = pygame.mouse.get_pos()

            #Bumping check
            for event in ev:
                if self.rect.collidepoint(pos):
                    if event.type == pygame.MOUSEBUTTONUP: #Ensures that the buttons won't be clicked more than 1 time in a few moments
                        action = True
            return action

    bird_group = pygame.sprite.Group()
    pipe_group = pygame.sprite.Group()

    flappy = Bird(100, int(HEIGHT / 2))
    bird_group.add(flappy)

    #Buttons definition
    mute_button = Button(10, 10, UNMUTE_BUTTON)
    start_button = Button(WIDTH // 2 - 170, HEIGHT // 2 - 40, START_BUTTON)
    restart_button = Button(WIDTH // 2 - 50, HEIGHT // 2 - 100, RESTART_BUTTON)

    loading_screen()
    run = True
    while run:
        clock.tick(FPS) #Sets the max FPS of the game to 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
                flying = True

        WIN.blit(BG, (0, 0)) #Draws the background
        if clicks == 1:
            WIN.blit(TUTORIAL, (100, 300))
        
        bird_group.draw(WIN) #Draws talker's animation
        bird_group.update()
        pipe_group.draw(WIN) 

        #Draws the ground
        WIN.blit(GROUND, (ground_movement, 600))

        #Score checking
        if len(pipe_group) > 0:
            #Checks if talker passed the left side of a pipe, but hasn't passed the right side of it yet
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
                pass_pipe = True
            elif pass_pipe:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right: #If all talker has passed the whole pipe
                    score += 1
                    pass_pipe = False

        draw_text(str(score), SCORE_FONT, WHITE, int(WIDTH / 2), 20) #Updates the latest score on the screen(top-mid)


        #Checks if talker has bumped into a pipe
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0: #The booleans' purpose is to kill the instance of a group which was involved in the collision
            game_over = True

        #Checks if talker has hit the floor
        if flappy.rect.bottom >= 600:
            game_over = True
            flying = False

        if not game_over and flying: #If the game is running...
            #Pipes generating
            current_time = pygame.time.get_ticks()
            if current_time - last_pipe > PIPE_FREQUENCY:
                pipe_height = random.randint(-125, 100) #Chooses a random height for the new pipes
                bottom_pipe = Pipe(WIDTH, int(HEIGHT / 2) + pipe_height, -1)
                top_pipe = Pipe(WIDTH, int(HEIGHT / 2) + pipe_height, 1)
                pipe_group.add(bottom_pipe) #Adds the new pipes to the pipe group
                pipe_group.add(top_pipe)    #...
                last_pipe = current_time #Sets when the last pipe has been generated
                update_discord_status("logo", "Flappy Talker", "On the field", "score: " + str(score))

            #Makes the ground move
            ground_movement -= ground_speed
            if abs(ground_movement) > 35: #Ensures it won't run off the screen
                ground_movement = 0
            pipe_group.update() #Draws the pipes on the screen and ensures they will move with the ground

        #Reset the game when it's over
        if game_over:
            death()
            if restart_button.draw(): #If the restart button has been clicked...
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
    try: RPC.update(start)
    except: pass
    print(pygame.event.get())
    clicks = 0
    main()
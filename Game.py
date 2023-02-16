import pygame
import button
import crosshair
import dice

# Initialize Pygame
import draw_board

pygame.init()
# Set screen size and title
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catan")
# load the icon for the game
icon = pygame.image.load('icon.png').convert_alpha()
# add the icon
pygame.display.set_icon(icon)
###################### Universal instances ##################################################

# crosshair
pygame.mouse.set_visible(False)
# load crosshair image & create a crosshair object and add it to a sprite group
crosshair = crosshair.crosshair("cursor_fist.gif", "cursor.gif")
crosshair_group = pygame.sprite.Group(crosshair)
crosshair_group.add(crosshair)

# load button images
start_img = pygame.image.load('Play.png').convert_alpha()
quit_img = pygame.image.load('Quit.png').convert_alpha()
start_img2 = pygame.image.load('Play2.png').convert_alpha()
quit_img2 = pygame.image.load('Quit2.png').convert_alpha()

#################### Main menu Stage #####################################################
# load the background image for the main menu
background = pygame.image.load('landscape.jpg').convert_alpha()
# Scale the background image to fit the screen size
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# create button instance
start_button = button.Button(SCREEN_WIDTH/5, SCREEN_HEIGHT/2.5, start_img, start_img2)
quit_button = button.Button(SCREEN_WIDTH/1.8, SCREEN_HEIGHT/2.5, quit_img, quit_img2)
#################### Main menu Stage END#######################################################


#################### Game Stage ###############################################################
quit_button2 = button.Button(SCREEN_WIDTH*0, SCREEN_HEIGHT*0, quit_img, quit_img2)

dice = dice.Dice(1078, 539)#define dice


######################## Game Stage END #######################################################

#################### Game Stage Function ######################################################
def game():
    clock = pygame.time.Clock()
    running = True
    diceRolling = False #boolean for event loop
    while running:
        screen.fill((79, 129, 189))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseX, mouseY = pygame.mouse.get_pos()
                if (dice.d1X <= mouseX <= dice.d2X+dice.dimens) and (dice.d1Y <= mouseY <= dice.d1Y+dice.dimens):
                    if diceRolling == False:
                        pygame.time.set_timer(dice.EVENT, 100)
                        diceRolling = True #so you can't retrigger dice roll when its already rolling
                        dRollCount = 0 #counting for animation of dice roll

            elif event.type == dice.EVENT:
                if dRollCount == 10: #num of seconds for animation x10
                    dRoll = dice.roll(screen) #gets value of roll
                    pygame.time.set_timer(dice.EVENT, 0)
                    diceRolling = False
                
                else:
                    dice.roll(screen) #temp display of dice while rolling
                    dRollCount += 1
        ####################################################################
        
        #display static dice when not rolling
        dice.display(screen)

        draw_board.main(screen)

        if quit_button2.draw(screen):
            print('QUIT')
            running = False


        # crosshair
        crosshair_group.draw(screen)
        crosshair_group.update()
        #########################################################################
        clock.tick(60)
        pygame.display.flip()

############################# Main Game Loop #################################################
# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    ####################################################################
    # buttons
    screen.blit(background, (0, 0))
    if start_button.draw(screen):
        print('START')
        game()
    if quit_button.draw(screen):
        print('QUIT')
        running = False

    # crosshair
    crosshair_group.draw(screen)
    crosshair_group.update()
    crosshair.switch_image([start_button, quit_button])
    #########################################################################
    pygame.display.update()
# Quit Pygame
pygame.quit()


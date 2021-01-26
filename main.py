import pygame
import os
pygame.font.init()

from pygame.constants import DOUBLEBUF #the operative system will help me define the path of my images and other files
#FIRST we set the width and the height of the window of the game
WIDTH, HEIGHT= 900, 500
#after that we input the window 
WIN= pygame.display.set_mode((WIDTH, HEIGHT))
#lets give a name to our game
pygame.display.set_caption("Galaxy")
SPACESHIP_WIDTH, SPACESHIP_HEIGHT=55,40
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)
VEL= 5
MAX_BULLETS=3
BULLETS_VEL= 7
#we have to define at how many frames the game will run
FPS=60

#we need a separation border for the 2 screens
BORDER=pygame.Rect(WIDTH//2,0,10,HEIGHT)

HEALTH_FONT= pygame.font.SysFont("comicsans", 40)
#we need to create a new event when the ship has been hit by a bullet
YELLOW_HIT=pygame.USEREVENT+1 #+1 and 2 are a way to separate events, if they were bot +1 they would be considered the same event
RED_HIT=pygame.USEREVENT+2

SPACE=pygame.transform.scale(pygame.image.load(os.path.abspath("/Users/Akihiko/Documents/Pygame/Assets/space.png")), (WIDTH, HEIGHT))
YELLOW_SPACESHIP_IMAGE=pygame.image.load(os.path.abspath("/Users/Akihiko/Documents/Pygame/Assets/spaceship_yellow.png"))
RED_SPACESHIP_IMAGE=pygame.image.load(os.path.abspath("/Users/Akihiko/Documents/Pygame/Assets/spaceship_red.png"))
#We have to readjust the images dimension
YELLOW_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90 )
RED_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

#We define a function that handles the main loops of the game

def main():
    #We need to code the movement of the ships, to do so we draw some rectanngles
    red=pygame.Rect(700,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow=pygame.Rect(100,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    #now well'pass the 2 rects as arguments in the draw window function
    clock=pygame.time.Clock()
    run=True
    red_bullets= []
    yellow_bullets=[]
    red_health=10
    yellow_health=10
    #this it the main loop, the game will be played as long as it runs, if run=False the game will close
    while run:
        clock.tick(FPS) #speed at which the loop will refresh
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            
            # we are gonna handle bullets movement in a different and alternative way compared to the ships movement
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and len(yellow_bullets)< MAX_BULLETS:
                            bullet=pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                            yellow_bullets.append(bullet)

                    if event.key == pygame.K_RCTRL and len(red_bullets)< MAX_BULLETS:
                            bullet=pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                            red_bullets.append(bullet)
        

            if event.type == RED_HIT:
                    red_health -=1

            if event.type == YELLOW_HIT:
                    yellow_health -=1
        
        winner_text=""
        if red_health <=0:
                winner_text="Yellow wins"
        
        if yellow_health <=0:
                winner_text="Red wins"
        
        if winner_text != "":
                pass
        
        
        print(red_bullets, yellow_bullets)
        #we need to make the ships move when we press a button, by storing my code in 2 separate functions
        keys_pressed= pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red,yellow,red_bullets, yellow_bullets, red_health, yellow_health)
        

    pygame.quit()

#function for the content of the window, all the elements that we are going to draw in the window
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health): #the order of the elements matters
    WIN.blit(SPACE, (0, 0))
    #WIN.fill(WHITE) #color of the content of the window
    pygame.draw.rect(WIN,BLACK,BORDER) #This is the code to draw the rectangle for the border
    
    red_health_text= HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text= HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width()- 10, 10))
    WIN.blit(yellow_health_text, (10,10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))   #draws a surface(a element of text or image), and takes two parameters: the actual element and its position(position coordinates start from top left)
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    # well draw the bullets with a for loop
    for bullet in red_bullets:
            pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update() # no changes will happen unless we update the display with this line of code


#function for the characters
#def characters():

def yellow_handle_movement(keys_pressed, yellow):

    if keys_pressed[pygame.K_a] and yellow.x -VEL >0:
            yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
            yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
            yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT:
            yellow.y += VEL
        
def red_handle_movement(keys_pressed, red):

    if keys_pressed[pygame.K_LEFT] and red.x -VEL > BORDER.x + BORDER.width:
            red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
            red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
            red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:
            red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
        for bullet in yellow_bullets:
                bullet.x += BULLETS_VEL
                if red.colliderect(bullet): 
                        pygame.event.post(pygame.event.Event(RED_HIT))
                        yellow_bullets.remove(bullet)
                elif bullet.x > WIDTH:
                        yellow_bullets.remove(bullet)
        for bullet in red_bullets:
                bullet.x -= BULLETS_VEL
                if yellow.colliderect(bullet): 
                        pygame.event.post(pygame.event.Event(YELLOW_HIT))
                        red_bullets.remove(bullet)
                elif bullet.x < 0:
                        red_bullets.remove(bullet)
if __name__ == "__main__":
    main()
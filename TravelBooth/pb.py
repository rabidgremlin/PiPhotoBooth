import pygame
import time
import pygame.camera


#pygame.display.init()
pygame.font.init()
pygame.camera.init()

cameras = pygame.camera.list_cameras()
print "Using camera %s ..." % cameras[0]

webcam = pygame.camera.Camera(cameras[0],(1280,720))
#webcam.start()
#img = webcam.get_image()

#size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
size = (1184,624)
print "Framebuffer size: %d x %d" % (size[0], size[1])
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

# Clear the screen to start
screen.fill((0, 0, 0))        





font_super = pygame.font.Font("tt0105m_.TTF", 140)
font_big = pygame.font.Font("tt0105m_.TTF", 75)
font_mid = pygame.font.Font("tt0106m0.TTF", 40)

blank = pygame.image.load('blank.png').convert()
withlogo = pygame.image.load("withlogo.png").convert()
#results = pygame.image.load("results.png").convert()

text_star_fleet_enrollment = font_big.render("PASSPORT PHOTO CHECK", True, (0, 0, 0))
text_press_space = font_mid.render("PRESS SPACE TO BEGIN", True, (11, 1, 56))

text_pose = font_big.render("PREPARE FOR PHOTO CHECK", True, (0, 0, 0))
text_3 = font_super.render("3", True, (11, 1, 56))
text_2 = font_super.render("2", True, (11, 1, 56))
text_1 = font_super.render("1", True, (11, 1, 56))
text_hold = font_big.render("HOLD", True, (11, 1, 56))

def draw_welcome():
        screen.blit(withlogo, (0, 0))
        
        textpos = text_star_fleet_enrollment.get_rect(centerx=screen.get_width()/2,centery=screen.get_height()/2+70)
        screen.blit(text_star_fleet_enrollment, textpos)
        
        textpos = text_press_space.get_rect(centerx=screen.get_width()/2,centery=screen.get_height()/2+170)
        screen.blit(text_press_space, textpos)
        
        pygame.display.flip()
        
def draw_message(message):
        screen.blit(blank, (0, 0))
        
        textpos = message.get_rect(centerx=screen.get_width()/2,centery=screen.get_height()/2)
        screen.blit(message, textpos)
                        
        pygame.display.flip()        


def count_and_snap():
        draw_message(text_3)
        pygame.time.wait(500)
        draw_message(text_2)
        pygame.time.wait(500)
        draw_message(text_1)
        pygame.time.wait(500)
        draw_message(text_hold)
        
        #res = subprocess.Popen(["sudo", "fswebcam", "-r 640x480", "grab.jpeg"])
        webcam.start()
        img = webcam.get_image()
        screen.fill((255, 255, 255))
        pygame.display.flip()
        
        screen.fill((0, 0, 0))
        pygame.display.flip()
        webcam.stop()
        return img

pygame.mouse.set_visible(False)
        
game_exit = False
doing_capture = False
last_capture = 0

# main loop
while game_exit == False :
    for event in pygame.event.get():
        # terminate the loop when esc key is pressed or user exits
        if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)  : game_exit=True
        
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)  : doing_capture=True

    if (time.time() - last_capture > 30):
        draw_welcome()

        
    if doing_capture:
        doing_capture = False
        draw_message(text_pose)
        pygame.time.wait(1000)
        
        img1 = count_and_snap()
        img2 = count_and_snap()
        img3 = count_and_snap()
        img4 = count_and_snap()
        
        snap1 = pygame.transform.scale(img1,(400,225))
        snap2 = pygame.transform.scale(img2,(400,225))
        snap3 = pygame.transform.scale(img3,(400,225))
        snap4 = pygame.transform.scale(img4,(400,225))
        
        screen.blit(blank, (0, 0))
        screen.blit(snap1,(150,69))
        screen.blit(snap2,(610,69))
        screen.blit(snap3,(150,331))
        screen.blit(snap4,(610,331))
        pygame.display.flip()
        
        last_capture = time.time()
        
        millis = int(round(last_capture * 1000))
        fileprefix = "images/" + str(millis)
        
        pygame.image.save(img1, fileprefix +"_01.jpg")
        pygame.image.save(img2, fileprefix +"_02.jpg")
        pygame.image.save(img3, fileprefix +"_03.jpg")
        pygame.image.save(img4, fileprefix +"_04.jpg")
        
        #draw_welcome()
        
    # use this to limit the CPU load of the while loop, 
    # the less the wait the faster the loop runs and thus the more cpu it consumes   
    pygame.time.wait(10) 


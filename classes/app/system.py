from classes.util.sounds import Sounds
from classes.util.stopwatch import Stopwatch
import os
import pygame


class System(object):

    IMAGES = {
        'active_start_button': os.path.join("images", "active_start_button.png"),
        'asteroid': os.path.join("images", "asteroid.png"),
        'background': os.path.join("images", "background.png"),
        'explosion': [os.path.join("images", "explosion", "explosion_%i.png" % i) for i in range(7)],
        'icon': os.path.join("images", "icon.ico"),
        'spaceship': os.path.join("images", "spaceship.png"),
        'start_button': os.path.join("images", "start_button.png")
    }

    FONTS = {
        'autumn':os.path.join("fonts", "Autumn.ttf"),
        'space_age':os.path.join("fonts", "Space Age.ttf")
    }

    SOUNDS = {
        'explosion':os.path.join("sounds", "explosion.mp3"),
        'music':os.path.join("sounds", "music.mp3")
        }


    def __init__(self, window_geometry, title):

        for image in self.IMAGES:

            if type(self.IMAGES[image]) is list:
                for img in self.IMAGES[image]:
                    if not os.path.exists(img):
                        raise FileNotFoundError('ERROR: Could not find file "%s".' % img)

            elif not os.path.exists(self.IMAGES[image]):
                raise FileNotFoundError('ERROR: Could not find file "%s".' % self.IMAGES[image])

        for font in self.FONTS:
            if not os.path.exists(self.FONTS[font]):
                raise FileNotFoundError('ERROR: Could not find file "%s".' % self.FONTS[font])

        for sound in self.SOUNDS:
            if not os.path.exists(self.SOUNDS[sound]):
                raise FileNotFoundError('ERROR: Could not find file "%s".' % self.SOUNDS[sound])

        pygame.init()
        pygame.display.set_mode(window_geometry)
        pygame.display.set_caption(title)
        pygame.display.set_icon(pygame.image.load(self.IMAGES["icon"]))

        self.clock = pygame.time.Clock() 
        self.sounds = Sounds()  
        self.stopwatch = Stopwatch()


    def updateWindow(self):
        pygame.display.flip()
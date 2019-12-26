from pygame import display
from pygame import image
from pygame import time


class Animation(object):

    def __init__(self, window, images):

        self.__window = window
        self.__images = [ image.load(img) for img in images ]
        self.__WIDTH, self.__HEIGHT = self.__images[0].get_size()
        self.__clock = time.Clock()


    def draw(self, x, y, updateFunction, fps = 30):

        for image in self.__images:
            updateFunction()
            self.__window.blit(image, [ x - self.width // 2, y - self.height // 2 ])
            self.__clock.tick(fps)
            display.flip()


    @property
    def height(self):
        return self.__HEIGHT


    @property
    def width(self):
        return self.__WIDTH
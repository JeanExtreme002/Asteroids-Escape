from classes.util.animation import Animation
from pygame import image
from pygame import mouse


class Spaceship(object):
    
    __rect = None


    def __contains__(self,rect):

        if self.__rect:
            return self.__rect.colliderect(rect)


    def __init__(self, window, image_fn, explosion_images, margin = (0,0,0,0)):

        self.__window = window
        self.__window_width, self.__window_height = window.get_size()
        self.__explosionAnimation = Animation(window, explosion_images)
        self.__image = image.load(image_fn)
        self.__WIDTH, self.__HEIGHT = self.__image.get_size()
        self.__margin = margin


    def centralize(self):

        mouse.set_pos(self.__rect.x + self.width // 2 , self.__rect.y + self.height // 2)


    def cursor(self,bool_):

        mouse.set_visible(bool_)


    def draw(self, x, y):

        self.__rect = self.__window.blit(self.__image,[x,y])


    def explode(self, updateFunction):

        # Realiza explosão no centro e no nariz da nave.
        self.__explosionAnimation.draw(
            self.x + self.width // 2, 
            self.y + self.height // 2, 
            updateFunction, 15
            )

        self.__explosionAnimation.draw(
            self.x + self.width, 
            self.y + self.height // 2, 
            updateFunction, 10
            )


    @property
    def height(self):

        return self.__HEIGHT


    def move(self):

        cursor_x, cursor_y = mouse.get_pos()

        if cursor_x < self.__margin[0]:
            cursor_x = self.__margin[0]

        elif cursor_x > self.__window_width - self.__margin[2]:
            cursor_x = self.__window_width - self.__margin[2]

        if cursor_y < self.__margin[1]:
            cursor_y = self.__margin[1]
            
        elif cursor_y > self.__window_height - self.__margin[3]:
            cursor_y = self.__window_height - self.__margin[3]

        x = cursor_x - self.width // 2
        y = cursor_y - self.height // 2

        self.__rect.x = x
        self.__rect.y = y


    @property
    def x(self):
        return self.__rect.x


    @property
    def y(self):
        return self.__rect.y


    @property
    def width(self):
        return self.__WIDTH
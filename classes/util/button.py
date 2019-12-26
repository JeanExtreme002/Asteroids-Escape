from pygame import image
from pygame import mouse


class Button(object):

    __rect = None


    def __init__(self, window, image_fn):

        self.__window = window

        if type(image_fn) is tuple and len(image_fn) > 1:
            self.__image = image.load(image_fn[0])
            self.__active_image = image.load(image_fn[1])
        else:
            self.__image = image.load(image_fn)
            self.__active_image = None

        self.__WIDTH, self.__HEIGHT = self.__image.get_size()


    def draw(self, x, y):
        
        x -= self.width // 2
        y -= self.height // 2

        if self.__rect and self.__active_image and self.pressed: 
            self.__rect = self.__window.blit(self.__active_image, [x,y])
        else:
            self.__rect = self.__window.blit(self.__image, [x,y])


    @property
    def height(self):
        return self.__HEIGHT


    @property
    def pressed(self):

        cursor_x, cursor_y = mouse.get_pos()

        if self.__rect.x <= cursor_x <= self.__rect.x + self.width:
            if self.__rect.y <= cursor_y < self.__rect.y + self.height:
                return True
        return False


    
    @property
    def width(self):
        return self.__WIDTH


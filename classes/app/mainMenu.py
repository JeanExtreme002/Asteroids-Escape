from pygame import display
from pygame import image


class MainMenu(object):

    def __init__(self, window, spaceship, titleText, startButton):

        self.__window = window
        self.__window_width, self.__window_height = window.get_size()

        self.spaceship = spaceship
        self.spaceship.draw(self.__window_width // 2 - self.spaceship.width // 2, self.__window_height // 2)
        self.__velocity = 5

        self.__title = display.get_caption()[0] 
        self.__titleText = titleText
        self.__startButton = startButton


    def draw(self):

        if self.spaceship.y <= self.__window_height // 2 - 100:
            self.__velocity = 5

        elif self.spaceship.y >= self.__window_height // 2:
            self.__velocity = -5

        y = self.spaceship.y + self.__velocity

        self.spaceship.draw(self.__window_width // 2 - self.spaceship.width // 2, y)
        self.__startButton.draw(self.__window_width // 2, self.__window_height // 100 * 80)

        self.__titleText.draw(self.__title, self.__window_width // 2, 50)     

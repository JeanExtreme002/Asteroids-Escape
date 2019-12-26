from pygame import image
import random


class Asteroids(object):

    __asteroids = []
    __index = 0


    def __getitem__(self,index):
        return self.__asteroids[index]


    def __init__(self, window, image_fn, margin = (0,0)):

        self.__window = window
        self.__window_width, self.__window_height = self.__window.get_size()
        self.__image = image.load(image_fn)
        self.__WIDTH, self.__HEIGHT = self.__image.get_size()
        self.__margin = margin


    def __iter__(self):
        return self


    def __next__(self):

        if self.__index >= len(self.__asteroids):
            self.__index = 0
            raise StopIteration

        else:
            try:
                return self.__asteroids[self.__index]
            finally:
                self.__index += 1


    def clear(self):
        self.__asteroids.clear()


    def createNewAsteroid(self, amount = (1,1)):

        # Obtém uma lista com todas as posições disponíveis para criar os asteróides.
        start = self.__margin[0]
        stop = self.__window_height - self.__margin[1] - self.height
        pos_list = [ num for num in range(start, stop) ]

        for i in range(random.randint(*amount)):

            if not pos_list: break

            # Obtém uma posição X e Y aleatóriamente.
            pos_y = random.choice(pos_list)
            pos_x = random.randint(self.__window_width + 50, self.__window_width + 50 + self.width)
            
            # Remove as posições usadas pelo asteróide.
            index = pos_list.index(pos_y)

            part1 = 0 if index - self.height < 0 else index - self.height + 1
            part2 = index + 1 if index + self.height >= len(pos_list) else index + self.height + 1

            pos_list = pos_list[:part1] + pos_list[part2:]
            self.__asteroids.append(self.__window.blit(self.__image,[pos_x, pos_y]))


    def draw(self):

        index = 0

        for asteroid in self.__asteroids:

            x = asteroid.x
            y = asteroid.y

            # Após desenhar, o objeto rect.Rect contido na lista de asteróides, será atualizado
            # por um novo objeto, afim de evitar conflitos futuros.
            self.__asteroids[index] = self.__window.blit(self.__image, [x, y] )
            self.__asteroids[index].x = x

            index += 1


    @property
    def empty(self):
        return False if self.__asteroids else True


    @property
    def height(self):
        return self.__HEIGHT


    def move(self, px, scoreFunction = None):

        index = 0

        for asteroid in self.__asteroids:
            asteroid.x -= px

        # Percorre cada asteróide verificando se algum já saiu da tela do jogo.
        for asteroid in self.__asteroids:
            if asteroid.x < -self.width:
                self.__asteroids.remove(asteroid)
                if scoreFunction: scoreFunction()
    

    @property
    def width(self):
        return self.__WIDTH
            
            


            

    
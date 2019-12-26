from pygame import image


class Background(object):

    __surface = None
    __images = []


    def __init__(self, window, image_fn):

        self.__window = window
        self.__image = image.load(image_fn)
        self.__WIDTH, self.__HEIGHT = self.__image.get_size()


    @property
    def surface(self):
        return self.__image


    def draw(self, velocity = 1):

        # Cria duas imagens caso a lista esteja vazia.
        if not self.__images:
            self.__images.append(self.__window.blit(self.__image, [0,0]))
            self.__images.append(self.__window.blit(self.__image, [self.width,0]))

        # Se a primeira imagem passar da tela, ela será colocada no final da lista 
        # e será desenhada depois da outra imagem, criando assim um loop.
        if self.__images[0].x <= -self.width:
            self.__images.append(self.__images.pop(0))
            self.__images[-1].x = self.__images[0].x + self.width

        index = 0

        for image in self.__images:
            x = image.x - velocity
            y = image.y

            self.__images[index] = self.__window.blit(self.__image,[image.x,image.y])
            self.__images[index].x = x
            index += 1


    @property
    def height(self):
        return self.__HEIGHT

    
    @property
    def width(self):
        return self.__WIDTH


    
        
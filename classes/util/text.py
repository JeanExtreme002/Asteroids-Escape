from pygame import font


class Text(object):

    def __init__(self, window, text_font):

        self.__window = window
        self.__font = font.Font(*text_font)


    def draw(self, text, x, y , color = [255,255,255], place = "center", outline = None):

        place = place.lower()

        if place != "left":
            w , h = self.size(text)

            if place == "center":
                x -= w // 2
                y -= h // 2
            else:
                x -= w

        size = 2

        if outline:
            self.__window.blit(self.__font.render(text,False,outline),[x - size,y])
            self.__window.blit(self.__font.render(text,False,outline),[x + size,y])
            self.__window.blit(self.__font.render(text,False,outline),[x,y - size])
            self.__window.blit(self.__font.render(text,False,outline),[x,y + size])
        self.__window.blit(self.__font.render(text,False,color),[x,y])


    def size(self, text):
        return self.__font.size(text)



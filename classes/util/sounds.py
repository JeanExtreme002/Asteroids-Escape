from pygame import mixer

mixer.init(buffer=1024)


class Sounds(object):

    def play(self, filename, loop = 1):

        mixer.music.load(filename)
        mixer.music.play(loop)


    def pause(self):

        mixer.music.pause()
    
    
    def unpause(self):

        mixer.music.unpause()

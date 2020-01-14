from classes.app.mainMenu import MainMenu
from classes.app.system import System
from classes.entities.asteroids import Asteroids
from classes.entities.spaceship import Spaceship
from classes.util.background import Background
from classes.util.button import Button
from classes.util.text import Text
import pygame


class App(System):

    FRAMES_PER_SECOND = 60
    MARGIN = (50,100,50,50)
    WINDOW_GEOMETRY = (900,600)
    WINDOW_TITLE = "Asteroids Escape"


    def __init__(self):

        try:
            super().__init__(self.WINDOW_GEOMETRY, self.WINDOW_TITLE)
        except FileNotFoundError as error:
            raise error

        self.__window = pygame.display.get_surface()

        self.__bigTitleText = Text(self.__window, ( self.FONTS["autumn"], 100 ))
        self.__infoText = Text(self.__window, (self.FONTS["autumn"],35) )
        self.__titleText = Text(self.__window, (self.FONTS["space_age"],50) )
        self.__startButton = Button(self.__window, (self.IMAGES["start_button"], self.IMAGES["active_start_button"]))

        self.asteroids = Asteroids(self.__window, self.IMAGES["asteroid"], self.MARGIN)
        self.background = Background(self.__window, self.IMAGES["background"])
        self.spaceship = Spaceship(self.__window, self.IMAGES["spaceship"], self.IMAGES["explosion"], self.MARGIN)
        self.__reset()


    def __captureEvents(self):
        """
        Método para realizar ações com base nos eventos.
        """

        for event in pygame.event.get():
            
            if event.type == pygame.BUTTON_X1:
                if self.__startButton.pressed:
                    self.__playing = True

            elif event.type == pygame.QUIT:
                self.__stop = True

            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    self.__stop = True

                # Pausa ou despausar jogo.
                elif event.key == pygame.K_p and self.__playing:
                    self.__pause = not self.__pause
                    if self.__pause:
                        self.sounds.pause()
                    else:
                        self.sounds.unpause()

                # Inicia o jogo.
                elif event.key == pygame.K_RETURN:
                    self.__playing = True


    def __collided(self):
        """
        Método para verificar se a nave colidiu com os asteróides.
        """

        for asteroid in self.asteroids:
            if asteroid in self.spaceship:
                return True
        return False


    def __reset(self):
        """
        Método para resetar o jogo.
        """

        self.__asteroids_limit = 2
        self.__distance = 400
        self.__fps = self.FRAMES_PER_SECOND
        self.__game_over = False
        self.__pause = False
        self.__playing = False
        self.__score = 0
        self.__stop = False
        self.__time = None
        self.__velocity = 5

        # Apaga todos os asteróides, centraliza a nave na tela e reinicia o cronômetro.
        self.asteroids.clear()
        self.spaceship.draw(self.WINDOW_GEOMETRY[0] // 2, self.WINDOW_GEOMETRY[1] // 2)
        self.stopwatch.start()


    def run(self):
        """
        Método para inicializar o jogo.
        """
        
        # Cria o menu inicial e aguarda o usuário apertar o botão "start" ou fechar o programa.
        mainMenu = MainMenu(self.__window, self.spaceship, self.__titleText, self.__startButton)
        
        while not self.__playing and not self.__stop:
            self.__captureEvents()

            if self.__playing: break

            self.__update()
            mainMenu.draw()
            self.updateWindow()
            self.clock.tick(self.FRAMES_PER_SECOND)

        # Fecha a janela caso o usuário queira sair.
        if self.__stop:
            pygame.quit()
            return

        # Inicia a sessão. 
        self.__start()
        pygame.quit()


    @property
    def score(self):
        return self.__score


    def __start(self):
        """
        Método para iniciar um novo jogo.
        """

        # Reseta os dados do jogo anterior.
        self.__reset()
        self.__playing = True

        # Reproduz uma música de fundo.
        self.sounds.play(self.SOUNDS["music"], loop = -1)

        # Esconde o cursor durante o jogo e define a posição do mouse no centro da tela.
        self.spaceship.cursor(False)
        self.spaceship.centralize()

        while not self.__stop:
            self.__time = self.stopwatch.get()

            # Verifica se a nave colidiu.
            if self.__collided(): break

            self.__captureEvents()

            # Atualiza o jogo.
            self.__update(updateEntities = True)
            self.updateWindow()

            # Se o jogo estiver pausado, o mouse ficará centralizado 
            # na nave e nenhum objeto poderá se mover.
            if self.__pause:
                self.spaceship.centralize()
                continue

            # Caso o último asteróide criado tenha uma distância X maior ou igual 
            # do que o seu ponto de criação, um novo asteróide será criado.
            if self.asteroids.empty or self.WINDOW_GEOMETRY[0] - self.asteroids[-1].x > self.__distance: 
                self.asteroids.createNewAsteroid((1, self.__asteroids_limit))

                if self.__distance > 200:
                    self.__distance -= 10
            
            # Move os asteróides e a nave.
            self.asteroids.move(self.__velocity, self.__increaseScore)
            self.spaceship.move()

        if self.__stop: return

        # Reproduz som de explosão e gera sua animação.
        self.sounds.play(self.SOUNDS["explosion"])
        self.spaceship.explode(lambda: self.__update(updateEntities = True))

        self.__captureEvents()
        self.spaceship.cursor(True)
        self.__playing = False
        self.__game_over = True

        # Aguarda o usuário apertar o botão "start" ou fechar o programa.
        while not self.__stop and not self.__playing:
            self.__captureEvents()
            self.__update(updateEntities = True)
            self.__startButton.draw(self.WINDOW_GEOMETRY[0] // 2, self.WINDOW_GEOMETRY[1] // 100 * 80)
            self.updateWindow()
        
        # Começa um novo jogo.
        if self.__playing:
            self.__start()


    def __increaseScore(self):
        """
        Método para aumentar a pontuação do usuário.
        """

        self.__score += 1
        if self.__score % 10 == 0:
            self.__increaseDifficulty()


    def __increaseDifficulty(self):
        """
        Método para aumentar o nível de dificuldade do jogo.
        """

        # Aumenta o FPS até no máximo 200 a cada 10 pontos obtidos.
        if self.__score % 10 == 0 and self.__fps < 200:
            self.__fps += 10

        # Aumenta a velocidade ao obter 10 pontos.
        if self.__score == 10:
            self.__velocity += 1

        # A cada 40 pontos obtidos, a velocidade aumentará em 1 pixel.
        if self.__score % 20 == 0 and self.__velocity < 15:
            self.__velocity += 1


    def __update(self, updateEntities = False):
        """
        Método para atualizar a tela do jogo.
        """
        
        # Limpa a tela e deseja um plano de fundo. 
        # Se o usuário não estiver jogando no momento, o plano de fundo será estático.
        self.__window.fill([0,0,0])
        self.background.draw( 2 if self.__playing and not self.__pause else 0 )

        # Atualiza a entidades.
        if updateEntities:
            self.spaceship.draw(self.spaceship.x, self.spaceship.y)
            self.asteroids.draw()

        if self.__pause:
            self.__bigTitleText.draw("PAUSED", self.WINDOW_GEOMETRY[0] // 2, 100, color = [255,0,0], outline = [0,0,0])

        elif self.__game_over:
            self.__bigTitleText.draw("GAME OVER", self.WINDOW_GEOMETRY[0] // 2, 100, color = [255,0,0], outline = [0,0,0])

        # Mostra a pontuação e o tempo de jogo.
        if self.__playing or self.__game_over:
            self.__infoText.draw("Score: %i" % self.__score, 30, 10, place = "left")
            self.__infoText.draw("Time: %s" % self.__time, self.WINDOW_GEOMETRY[0] - 30, 10, place = "right")
            self.clock.tick(self.FRAMES_PER_SECOND)


    @property
    def window(self):
        return self.window
    

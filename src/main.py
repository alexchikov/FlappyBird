import pygame as pg
import random as rnd

pg.init()

TEMP = 0
WIDTH, HEIGHT = 800, 600
SCORE = 0
FPS = 60

sprites = pg.sprite.Group()
screen = pg.display.set_mode(size=(WIDTH, HEIGHT))
clock = pg.time.Clock()

pg.display.set_caption("Flappy Bird")

surface = pg.image.load('./img/background.png')
background = pg.transform.scale(surface, size=(WIDTH, HEIGHT))

class Pipe(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, file: str, size: tuple=(110,600,), type: bool = True) -> None:
        pg.sprite.Sprite.__init__(self, sprites)
        self.surface = pg.image.load(file)
        if type:
            self.image = pg.transform.scale(self.surface, size)
            self.image.set_colorkey(self.image.get_at((0,0)))
        else:
            self.surface = pg.transform.scale(self.surface, size)
            self.image = pg.transform.rotate(self.surface, 180)
            self.image.set_colorkey(self.image.get_at((0,200)))
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = 3
        self.score = 0
    
    def update(self):
        if self.rect.x < -100:
            self.rect.x = 800
            if type:
                self.score += 1
        else:
            self.rect.x -= self.speed
            
class Bird(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, size: tuple = (80, 60)):
        pg.sprite.Sprite.__init__(self, sprites)
        self.surface = pg.image.load('./img/bird.png')
        self.image = pg.transform.scale(self.surface, size)
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = 3 
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 600:
            pg.quit()
            exit()
        if self.rect.y <   0:
            self.rect.y += 50

def render_score(score: int): # функция для рендеринга надписи с счетом игрока 
    global score_text, record_text
    score_font = pg.font.Font('./font/ARCADECLASSIC.TTF', 34)
    score_text = score_font.render(f'Score {score}', False, 'Red')
        
upper_pipe = Pipe(800, 725, './img/pipe_2.png', type=False)
lower_pipe = Pipe(800, 0, './img/pipe_2.png')
bird = Bird(300, 220)
render_score(upper_pipe.score)
sprites.add(upper_pipe, lower_pipe, bird)
while True:
    screen.fill('Black')
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
            
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE or event.key == pg.K_UP:
                bird.rect.y -= 40
        
    if pg.sprite.collide_rect(bird, upper_pipe) or pg.sprite.collide_rect(bird, lower_pipe):
        pg.quit()
        exit()
        
    if upper_pipe.rect.x < -100:
        y = rnd.randint(200, 550)
        lower_pipe.rect.y = -y
        upper_pipe.rect.y = 725-y 
        
    render_score(upper_pipe.score)
    
    sprites.update()     
    screen.blit(background,(0,0,))
    screen.blit(upper_pipe.image, upper_pipe.rect)
    screen.blit(lower_pipe.image, lower_pipe.rect)
    screen.blit(bird.image, bird.rect)
    screen.blit(score_text, (0,0))
    
    pg.display.update()
    clock.tick(FPS)
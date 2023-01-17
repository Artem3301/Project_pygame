import random

import pygame


# Класс для музики
class AudioSource:
    def __init__(self, sound_track, volume, active, looping):
        self.sound_track = sound_track
        self.active = active
        self.looping = looping
        self.audio = pygame.mixer.Sound(self.sound_track)
        self.volume = volume
        self.audio.set_volume(self.volume)
        if self.active:
            self.play()

    def play(self):
        if not self.looping:
            self.audio.play()
        else:
            self.audio.play(-1)


# Класс панели
class Panel:
    def __init__(self, x, y, w, h, txt='', deleted=False, is_game_obj=False, is_table=False, img=None, colorf=(0, 0, 0),
                 color=None, count=0, active=True):
        self.color = color
        self.colorf = colorf
        self.txt = txt
        self.start_pos = (x, y)
        # Самоудаление при нажатии
        self.deleted = deleted
        self.is_game_obj = is_game_obj
        self.is_table = is_table
        self.text = shrift.render(txt, 1, self.colorf)
        self.rect_txt = self.text.get_rect()
        self.rect_txt.center = (x, y)
        self.rect = pygame.Rect(x, y, w, h)
        self.rect.center = (x, y)
        self.in_table = False
        self.count = count
        self.active = active
        self.img = img
        if self.img:
            self.image = pygame.image.load(img)
            self.image = pygame.transform.scale(self.image, (w, h))
            self.img_rect = self.image.get_rect()

    def draw(self):
        if self.active:
            if self.color:
                pygame.draw.rect(screen, self.color, self.rect)
            if self.txt:
                screen.blit(self.text, (self.rect_txt[0], self.rect_txt[1]))
            if self.img:
                screen.blit(self.image, (self.rect[0], self.rect[1]))

    # Отображение текста
    def set_text(self, txt):
        self.text = shrift.render(txt, 1, self.colorf)

    # Функция передвижения
    def click(self, code_=None):
        global made_move, start_game, made_move_start, count_object
        b = pygame.mouse.get_pressed()[0]
        if b and self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            if self.deleted:
                start_game = True
            elif self.is_game_obj and (
                    type(code_) != Panel or (type(code_) == Panel and not code_.is_game_obj)) and not made_move:
                self.rect.center = pygame.mouse.get_pos()
                return self
            elif self.is_table and type(code_) == Panel and code_.is_game_obj and not made_move:
                code_.rect.center = pos_1
                code_.in_table = True
                count_object = code_.count
                made_move = True
                made_move_start = True
            return True
        if self.is_game_obj and not self.in_table:
            self.rect.center = self.start_pos
        return False


# Отрисовка движения
def move():
    global made_move_start, score_player, score_enemy
    made_move_start = False
    r = random.randint(1, 3)
    buttons[r + 3].rect.center = pos_2
    if count_object == r:
        panel_draw.active = True
    elif (count_object == 1 and r == 3) or (count_object == 2 and r == 1) or (count_object == 3 and r == 2):
        panel_win.active = True
        score_player += 1
        score_pl.set_text(f'Ваш Счёт:{score_player}')
    elif (count_object == 3 and r == 1) or (count_object == 1 and r == 2) or (count_object == 2 and r == 3):
        panel_loss.active = True
        score_enemy += 1
        score_en.set_text(f'Счёт Врага:{score_enemy}')


# Обновление
def update():
    code_ = None
    buts = [b for b in buttons]
    buts.reverse()

    for b in buts:
        c = b.click(code_)
        if type(c) == Panel and c.is_game_obj:
            code_ = c


# Запись в панели
def get_panels():
    return [table,
            Panel(200 + 75, 700, 150, 150, img='data/n.png', is_game_obj=True, count=1),
            Panel(500, 700, 150, 150, img='data/k.png', is_game_obj=True, count=2),
            Panel(650 + 75, 700, 150, 150, img='data/b.png', is_game_obj=True, count=3),
            Panel(200 + 75, 200, 150, 150, img='data/n.png'),
            Panel(500, 200, 150, 150, img='data/k.png'),
            Panel(650 + 75, 200, 150, 150, img='data/b.png')
            ]


# Отрисовка панелей
def draw():
    screen.blit(back, (0, 0))
    score_pl.draw()
    score_en.draw()
    for b in buttons:
        b.draw()
    if not start_game:
        button_play.draw()
    panel_draw.draw()
    panel_win.draw()
    panel_loss.draw()


# Делаем панели неактивными
def reset():
    global buttons, made_move_start, made_move
    buttons = get_panels()
    panel_draw.active = False
    panel_win.active = False
    panel_loss.active = False
    made_move = False
    made_move_start = True


if __name__ == '__main__':
    pygame.init()
    # Цвета
    cor = (165, 38, 10)
    yellow = (255, 225, 76)
    # Позиции на столе
    pos_1 = (400, 450)
    pos_2 = (600, 450)
    # Счёт
    score_player = 0
    score_enemy = 0
    count_object = 0
    shrift = pygame.font.SysFont("Arial", 50)
    made_move = False
    made_move_start = True
    size = width, height = 1000, 900
    screen = pygame.display.set_mode(size)
    back = pygame.transform.scale(pygame.image.load('data/back.jpg'), size)
    back.set_alpha(90)
    # Отрисовка результатов
    panel_draw = Panel(500, 450, 400, 200, txt="Ничья", active=False)
    panel_win = Panel(500, 450, 400, 200, txt="Победа", active=False, colorf=(51, 162, 21))
    panel_loss = Panel(500, 450, 400, 200, txt="Поражение", active=False, colorf=(194, 10, 16))
    table = Panel(500, 450, 400, 200, img='data/table.png', is_table=True)
    button_play = Panel(500, 450, 300, 100, 'Играть', True, colorf=yellow, color=(34, 56, 50))
    score_pl = Panel(115, 60, 220, 100, txt=f'Ваш Счёт:{score_player}', colorf=(0, 255, 0))
    score_en = Panel(875, 60, 240, 100, txt=f'Счёт Врага:{score_player}', colorf=(255, 0, 0))
    buttons = get_panels()
    start_game = False
    # Музыка
    back_music = AudioSource('back_mus.ogg', 1, True, True)
    # Процесс игры
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and made_move and not made_move_start:
                reset()

        if made_move and made_move_start:
            move()

        if start_game:
            update()
        else:
            button_play.click()
        draw()

        pygame.display.flip()
    pygame.quit()

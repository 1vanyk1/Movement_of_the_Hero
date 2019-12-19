import pygame
import os
pygame.init()
width, height = 400, 300
screen = pygame.display.set_mode((width, height))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    image = image.convert_alpha()
    return image


tile_width = tile_height = 50


tile_images = {'#': 'box.png', '.': 'grass.png', '@': 'mar.png'}
player_image = load_image('mar.png')


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(-int(self.left // 50 + 1), -int(self.left // 50 - width // 50)):
            for j in range(-int(self.top // 50 + 1), -int(self.top // 50 - height // 50)):
                image = load_image(tile_images[self.board[j % self.height][i % self.width]])
                rect = image.get_rect().move(self.left + self.cell_size * i, self.top + self.cell_size * j)
                screen.blit(image, rect)

    def get_cell(self, mouse_pos):
        if not(self.left <= mouse_pos[0] < self.left + self.cell_size * self.width and
               self.top <= mouse_pos[1] < self.top + self.cell_size * self.height):
            return None
        return (mouse_pos[0] - self.left) // self.cell_size, \
               (mouse_pos[1] - self.top) // self.cell_size

    def on_click(self, cell_coords):
        if cell_coords is not None:
            if self.board[cell_coords[1]][cell_coords[0]] == 1:
                self.board[cell_coords[1]][cell_coords[0]] = 0
            else:
                self.board[cell_coords[1]][cell_coords[0]] = 1

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def set_board(self, board):
        self.board = board
        self.height = len(board)
        self.width = len(board[0])
        t = False
        for i in range(self.width):
            for j in range(self.height):
                if board[j][i] == '@':
                    x, y = j, i
                    t = True
                    board[j][i] = '.'
                    break
            if t:
                break
        return Player(x, y)


def open_file(filename):
    filename = 'data/levels/' + filename
    with open(filename, 'r') as mapfile:
        level_map = [line.strip() for line in mapfile]
    max_level = max(map(len, level_map))
    return [list(i.ljust(max_level, '.')) for i in level_map]


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_y, pos_x):
        super().__init__()
        self.image = player_image
        self.pos = (pos_x, pos_y)
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15, tile_height * self.pos[1] + 5)

    def render(self):
        screen.blit(self.image, (self.rect[0] + board.left, self.rect[1] + board.top))


def move(hero, movement):
    x, y = hero.pos
    if movement == pygame.K_UP:
        if board.height > y > 0 and board.board[y - 1][x] == '.':
            hero.move(x, y - 1)
        elif board.board[-1][x] == '.':
            hero.move(x, board.height - 1)
            board.top -= board.cell_size * board.height
    if movement == pygame.K_DOWN:
        if 0 <= y < board.height - 1 and board.board[y + 1][x] == '.':
            hero.move(x, y + 1)
        elif board.board[0][x] == '.':
            hero.move(x, 0)
            board.top += board.cell_size * board.height
    if movement == pygame.K_LEFT:
        if x > 0 and board.board[y][x - 1] == '.':
            hero.move(x - 1, y)
        elif board.board[y][-1] == '.':
            hero.move(board.width - 1, y)
    if movement == pygame.K_RIGHT:
        if x < len(board.board) and board.board[y][x + 1] == '.':
            hero.move(x + 1, y)
        elif board.board[y][0] == '.':
            hero.move(0, y)
            board.left += board.cell_size * board.width


def change_camera_pos():
    res = player.pos[0] * board.cell_size + board.left - width / 2
    if res > 10:
        board.left -= res / 50
        if board.left > board.cell_size * board.width + width:
            board.left = 0
    elif res < -10:
        board.left -= res / 50
        if board.left < -width:
            board.left = -(board.cell_size * board.width - width)
    res = player.pos[1] * board.cell_size + board.top - height / 2
    if res > 10:
        board.top -= res / 50
        if board.top > board.cell_size * board.height + height:
            board.top = 0
    elif res < -10:
        board.top -= res / 50
        if board.top < -height:
            board.top = -(board.cell_size * board.height - height)


def draw():
    if if_started:
        return None
    files = os.listdir(os.path.abspath('data/levels'))
    c = 0
    files_of_levels.clear()
    for i in files:
        files_of_levels.append(i)
        font = pygame.font.Font(None, 50)
        text = font.render(i[:-4], 1, (100, 255, 100))
        text_x = width // 2 - text.get_width() // 2
        text_y = sprite.rect.y + 35 + c * 60 - buttons_y
        pygame.draw.rect(screen, (0, 0, 0), (50, sprite.rect.y + 25 + c * 60 - buttons_y, 300, 50), 0)
        screen.blit(text, (text_x, text_y))
        c += 1


buttons_y = 0
running = True

all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = pygame.transform.scale(load_image("fon.jpg"), (width, height))
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
sprite.rect.x = int(-(sprite.rect.width - width) / 2)
sprite.rect.y = 0

board = Board(4, 3)
player = board.set_board(open_file('level.txt'))
board.set_view(0, 0, 50)

files_of_levels = []
game_start = False
if_started = False

MYEVENTTYPE = 30
pygame.time.set_timer(MYEVENTTYPE, 10)
t = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and 50 <= event.pos[0] <= 350 and \
                    sprite.rect.y + 25 - buttons_y <= event.pos[1] <= \
                    sprite.rect.y + len(files_of_levels) * 60 + 15 - buttons_y:
                num = files_of_levels[(event.pos[1] - sprite.rect.y - 25 + buttons_y) // 60]
                player = board.set_board(open_file(num))
                board.set_view(0, 0, 50)
                if_started = True
            elif event.button == 4 and buttons_y > 0:
                buttons_y -= 10
            elif event.button == 5 and buttons_y < len(files_of_levels) * 60 - height + 40:
                buttons_y += 10
        if event.type == MYEVENTTYPE:
            change_camera_pos()
            if if_started:
                if sprite.rect.y < height:
                    sprite.rect.y += 2
                else:
                    game_start = True
        if event.type == pygame.KEYDOWN:
            if game_start:
                move(player, event.key)
    screen.fill((0, 0, 255))
    board.render()
    player.render()
    all_sprites.draw(screen)
    draw()
    pygame.display.flip()
pygame.quit()
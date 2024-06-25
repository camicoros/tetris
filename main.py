import copy
import pygame as pg
import random

# размеры игрового поля
COLUMNS = 11
STRINGS = 21
# размеры окна в пикселях
SCREEN_X = 50
SCREEN_Y = 100
# частота кадров в секунду
FPS = 60


# ширина одной ячейки сетки
cell_x = SCREEN_X / (COLUMNS - 1)
# высота одной ячейки сетки
cell_y = SCREEN_Y / (STRINGS - 1)

pg.init()
screen = pg.display.set_mode((SCREEN_X, SCREEN_Y))
pg.display.set_caption("Tetris CODE")
clock = pg.time.Clock()

# создаём сетку игрового поля
grid = []
for i in range(COLUMNS):
    grid.append([])
    for j in range(STRINGS):
        # 1 - ячейка свободна
        grid[i].append([1])
        # задаём координаты и размеры ячейки
        grid[i][j].append(pg.Rect(i * cell_x, j * cell_y, cell_x, cell_y))
        # задаём цвет ячейки
        grid[i][j].append(pg.Color("Gray"))

# создаём фигуры
details = [
    # линия
    [[-2, 0], [-1, 0], [0, 0], [1, 0]],
    # L-образная
    [[-1, 1], [-1, 0], [0, 0], [1, 0]],
    # обратная L-образная
    [[1, 1], [-1, 0], [0, 0], [1, 0]],
    # квадрат
    [[-1, 1], [0, 1], [0, 0], [-1, 0]],
    # Z-образная
    [[1, 0], [1, 1], [0, 0], [-1, 0]],
    # обратная Z-образная
    [[0, 1], [-1, 0], [0, 0], [1, 0]],
    # T-образная
    [[-1, 1], [0, 1], [0, 0], [1, 0]]
]

det = [[] for _ in details]

for i in range(len(details)):
    for j in range(len(details[i])):
        det[i].append(
            pg.Rect(details[i][j][0] * cell_x + cell_x * (COLUMNS // 2),  # отрисовываем по X в центре
                    details[i][j][1] * cell_y,
                    cell_x,
                    cell_y))

detail = pg.Rect(0, 0, cell_x, cell_y)

det_choice = copy.deepcopy(random.choice(det))
# счётчик для управления скоростью падения фигур
count = 0
# флаг для управления игровым циклом
game = True
# флаг для управления поворотом фигур
rotate = False

while game:
    # смещение по оси X
    delta_x = 0
    # смещение по оси Y
    delta_y = 1

    for event in pg.event.get():
        # выход
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            # движение влево
            if event.key == pg.K_LEFT:
                delta_x = -1
            # движение вправо
            elif event.key == pg.K_RIGHT:
                delta_x = 1
            # поворот
            if event.key == pg.K_UP:
                rotate = True
    # получаем состояние всех клавиш на клавиатуре
    key = pg.key.get_pressed()
    if key[pg.K_DOWN]:
        count = 31 * FPS

    # заполняем фон цветом
    screen.fill(pg.Color("Yellow"))
    # рисуем сетку поверх фона
    for i in range(COLUMNS):
        for j in range(STRINGS):
            pg.draw.rect(screen, grid[i][j][2], grid[i][j][1], grid[i][j][0])

    # проверяем границы движения фигуры
    for i in range(len(det_choice)):
        # по горизонтали
        if ((det_choice[i].x + delta_x * cell_x < 0) or (det_choice[i].x + delta_x * cell_x >= SCREEN_X)):
            delta_x = 0
        # по вертикали
        if ((det_choice[i].y + cell_y >= SCREEN_Y) or (grid[int(det_choice[i].x // cell_x)][int(det_choice[i].y // cell_y) + 1][0] == 0)):
            delta_y = 0

            # отмечаем занятые ячейки, перекрашиваем фигуры
            for i in range(len(det_choice)):
                x = int(det_choice[i].x // cell_x)
                y = int(det_choice[i].y // cell_y)
                grid[x][y][0] = 0
                grid[x][y][2] = pg.Color("Brown")

            # сбрасываем координаты новой фигуры
            detail.x = 0
            detail.y = 0

            # выбираем новую фигуру
            det_choice = copy.deepcopy(random.choice(det))

    # перемещение по x
    for i in range(len(det_choice)):
        det_choice[i].x += delta_x * cell_x

    # каждый цикл увеличиваем счётчик количества кадров на 1 секунду
    count += FPS

    # перемещение по y
    if count > 30 * FPS:
        for i in range(len(det_choice)):
            det_choice[i].y += delta_y * cell_y
        count = 0

    # отрисовка текущей фигуры
    for i in range(len(det_choice)):
        detail.x = det_choice[i].x
        detail.y = det_choice[i].y
        pg.draw.rect(screen, pg.Color("White"), detail)

    # поворот фигуры
    # определяем центр фигуры
    det_center = det_choice[2]
    if rotate:
        for i in range(len(det_choice)):
            # считаем новые координаты
            x = det_choice[i].y - det_center.y
            y = det_choice[i].x - det_center.x
            # присваиваем их
            det_choice[i].x = det_center.x - x
            det_choice[i].y = det_center.y + y
        rotate = False

    # обнуление рядов
    # проходим снизу вверх, считаем заполненные ячейки
    for j in range(STRINGS-1, -1, -1):
        count_cells = 0
        for i in range(COLUMNS):
            if grid[i][j][0] == 0:
                count_cells += 1
            elif grid[i][j][0] == 1:
                break
        # если весь ряд заполнен
        if count_cells == (COLUMNS - 1):
            # стираем заполненные ячейки
            for l in range(COLUMNS):
                grid[l][j][0] = 1
            # сдвигаем ячейки вниз
            for k in range(j, -1, -1):
                for l in range(COLUMNS):
                    grid[l][k][0] = grid[l][k-1][0]
                    grid[l][k][2] = grid[l][k-1][2]

    pg.display.flip()
    clock.tick(FPS)
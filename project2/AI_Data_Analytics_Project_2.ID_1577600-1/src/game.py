import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def animate(step):
    grid = game.update()
    img.set_data(grid)
    return [img]


class GameOfLife:
    def __init__(self, size: int = 50, p: float = 0.2):
        self.size = size
        self.p = p
        self.grid = np.random.choice([0, 1], size=(size, size), p=[p, 1 - p])  # Инициализируем начальную позицию.

    def count_neighbors(self, grid):
        """Подсчет количества живых соседей для каждой клетки"""
        # Создай пустой массив для подсчета соседей.
        # Для каждой клетки проверь ее 8 соседей.
        # Используй модульную арифметику для циклических границ.
        # Не учитывай саму клетку при подсчете.
        size = self.size
        indexes = {(-1, -1), (0, -1), (1, -1),
                   (-1, 0),           (1, 0),
                   (-1, 1), (0, 1), (1, 1)}
        neighbours = np.zeros((size, size), dtype=int)

        for i in range(size):
            for j in range(size):
                count = 0
                for dx, dy in indexes:
                    ni = (i + dx) % size
                    nj = (j + dy) % size
                    count += grid[ni][nj]
                neighbours[i, j] = count
        
        return neighbours


    def update(self):
        """Обновление состояния игры по правилам"""
        # Получи количество соседей для каждой клетки.
        # Примени правила рождения, выживания и смерти.
        # Используй булевы операции Numpy для эффективности.
        neighbours = self.count_neighbors(self.grid)

        new_grid = (
            ((self.grid == 1) & ((neighbours == 2) | (neighbours == 3))) | # если клетка живая и у неё 2 или 3 живых соседа, то она остаётся живой
            ((self.grid == 0) & (neighbours == 3)) # если клетка мертвая и у неё ровно 3 живых соседа, то она становится живой
        )

        self.grid = new_grid.astype(int)
        return self.grid


if __name__ == "__main__":
    size = 100
    frames = 100
    game = GameOfLife(size=size, p=0.5)

    fig, ax = plt.subplots()
    img = plt.imshow(game.grid, cmap="binary")
    ax.axis("off")

    anim = FuncAnimation(fig, animate, frames=frames, interval=100)

    writer = PillowWriter(fps=5)
    anim.save("game_of_life.gif", writer=writer)

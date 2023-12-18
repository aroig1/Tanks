from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

matrix = [
    [1, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1]
]

grid = Grid(matrix = matrix)

start = grid.node(5, 0)
end = grid.node(0, 2)

print(start)

finder = AStarFinder()

path, runs = finder.find_path(start, end, grid)

grid.cleanup()

print(path[0].x)
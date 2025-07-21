from .models import GRID_SIZE, Cell, Robot, Base
import random
import time

class Simulator:
    def __init__(self, trash_count=50, robot_count=3):
        self.grid = [[Cell(x, y) for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]
        self.turns = 0

        
        self.base = Base(15, 15)
        self.grid[15][15] = self.base

        
        #self.robot = Robot(1, 1)
        #self.grid[1][1].has_robot = True
        shared_trash_cells = set()
        self.robots = []
        for _ in range(robot_count):
            while True:
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                if not self.grid[x][y].is_base and not self.grid[x][y].has_robot:
                    robot = Robot(x, y, trash_cells=shared_trash_cells)
                    self.grid[x][y].has_robot = True
                    self.robots.append(robot)
                    break
        
        placed = 0
        while placed < trash_count:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if not self.grid[x][y].is_base and not self.grid[x][y].has_robot and not self.grid[x][y].has_trash:
                self.grid[x][y].has_trash = True
                placed += 1

    def step(self):
        #self.robot.act(self.grid, (self.base.x, self.base.y), self.base)
        for robot in self.robots:
            robot.act(self.grid, (self.base.x, self.base.y), self.base)
        self.turns += 1
        #print(f"STEP: robot at ({self.robot.x}, {self.robot.y}), base at ({self.base.x}, {self.base.y})")

    def get_state(self):
        return {
            "turn": self.turns,
            #"robot": {
            #    "x": self.robot.x,
            #    "y": self.robot.y,
            #    "carrying": self.robot.carrying,
            #},
            "robots": [
                {
                    "x": robot.x,
                    "y": robot.y,
                    "carrying": robot.carrying
                }
                for robot in self.robots
            ],
            "base": self.base.collected_trash,
            "remaining_trash": sum(cell.has_trash for row in self.grid for cell in row),
            "grid": [
                [{"trash": c.has_trash, "base": c.is_base, "robot": c.has_robot} for c in row]
                for row in self.grid
            ]
        }

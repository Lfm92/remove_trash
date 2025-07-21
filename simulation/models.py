import random, math, asyncio, time
from dataclasses import dataclass, field

GRID_SIZE = 32
DIST_VISION = 5

@dataclass
class Cell:
    x: int
    y: int
    has_trash: bool = False
    is_base: bool = False
    has_robot: bool = False

@dataclass
class Base(Cell):
    collected_trash: int = 0

    def __post_init__(self):
        self.is_base = True

    def deposit_trash(self):
        self.collected_trash += 1

@dataclass
class Robot:
    x: int
    y: int
    carrying: bool = False
    visited: set = field(default_factory=set)
    trash_cells: set = field(default_factory=set)

    def move(self, grid, base_pos, base):

        if self.carrying:
            self.visited.clear()
            return self.return_to_base(grid, base_pos, base)

        #def __post_init__(self):
         #   self.visited.add((self.x, self.y))
        #if self.trash_cells:
        #    vision_cells = list(self.trash_cells)
        #else:
        vision_cells = []
        for a in range(GRID_SIZE):
            for b in range(GRID_SIZE):
                dist = math.sqrt((a - self.x)**2 + (b - self.y)**2)
                if dist < DIST_VISION and grid[a][b].has_trash:
                    vision_cells.append((dist, a, b))
                    self.trash_cells.add((dist, a, b))

        if not vision_cells:
            vision_cells = list(self.trash_cells)

        if vision_cells:
            vision_cells.sort(key=lambda k: k[0])
            _, x_togo, y_togo = vision_cells[0]
            delta_x, delta_y = x_togo - self.x, y_togo - self.y

            if abs(delta_x) > abs(delta_y):
                step_x = 1 if delta_x > 0 else -1
                step_y = 0
            else:
                step_y = 1 if delta_y > 0 else -1
                step_x = 0

            nx, ny = self.x + step_x, self.y + step_y
            cell = grid[nx][ny]
            if not cell.has_robot:
                grid[self.x][self.y].has_robot = False
                self.x, self.y = nx, ny
                self.visited.add((self.x, self.y))
                cell.has_robot = True
                time.sleep(0.05)
                return

        else: #aucun trash dans le champ de vision
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and (nx, ny) not in self.visited and (nx, ny) != base_pos:
                    cell = grid[nx][ny]
                    if not cell.has_robot:
                        grid[self.x][self.y].has_robot = False
                        self.x, self.y = nx, ny
                        self.visited.add((self.x, self.y))
                        cell.has_robot = True
                        time.sleep(0.05)
                        return
            #Si le robot est bloqué
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                cell = grid[nx][ny]
                if not cell.has_robot:
                    grid[self.x][self.y].has_robot = False
                    self.x, self.y = nx, ny
                    cell.has_robot = True
                    time.sleep(0.05)
            return

    def return_to_base(self, grid, base_pos, base):
        base_x, base_y = base_pos
        delta_x = base_x - self.x
        delta_y = base_y - self.y

        if delta_x == 0 and delta_y == 0:
            base.deposit_trash()
            self.carrying = False
            self.visited.clear()
            time.sleep(0.05)
            return

        if abs(delta_x) > abs(delta_y):
            step_x = 1 if delta_x > 0 else -1
            step_y = 0
        else:
            step_x = 0
            step_y = 1 if delta_y > 0 else -1

        nx, ny = self.x + step_x, self.y + step_y
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            cell = grid[nx][ny]
            if not cell.has_robot:
                grid[self.x][self.y].has_robot = False
                self.x, self.y = nx, ny
                cell.has_robot = True
                time.sleep(0.05)
            

    def act(self, grid, base_pos, base):
        current = grid[self.x][self.y]
        print("Robot acting", self.x, self.y, "carrying =", self.carrying)

        if self.carrying and current.is_base:
            self.carrying = False
            base.deposit_trash()
            self.visited.clear()

        elif not self.carrying and current.has_trash:
            self.carrying = True
            current.has_trash = False
            self.trash_cells = {t for t in self.trash_cells if not (t[1] == self.x and t[2] == self.y)}

        else:
            self.move(grid, base_pos, base)

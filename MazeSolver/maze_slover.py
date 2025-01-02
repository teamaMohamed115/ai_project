import tkinter as tk
from random import choice

RES = WIDTH, HEIGHT = 600, 800  # Adjusted for a vertical maze
TILE = 40
cols, rows = WIDTH // TILE, HEIGHT // TILE

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw(self, canvas):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            canvas.create_rectangle(x, y, x + TILE, y + TILE, fill='#1e1e1e', outline='')

        if self.walls['top']:
            canvas.create_line(x, y, x + TILE, y, fill='white', width=2)
        if self.walls['right']:
            canvas.create_line(x + TILE, y, x + TILE, y + TILE, fill='white', width=2)
        if self.walls['bottom']:
            canvas.create_line(x, y + TILE, x + TILE, y + TILE, fill='white', width=2)
        if self.walls['left']:
            canvas.create_line(x, y, x, y + TILE, fill='white', width=2)
            
    def check_cell(self, x, y):
        """Retrieve a cell by its coordinates."""
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]
    
    def check_neighbors(self):
        """Find unvisited neighbors."""
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False 

# Initialize maze grid
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []

# Player setup
player_pos = [0, 0]  # Player starts at the top-left corner
goal_pos = [cols - 1, rows - 1]  # Goal is at the bottom-right corner
path = []  # Store the path for the green line

def reset_game_state():
    global grid_cells, current_cell, stack
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    stack = []

reset_game_state()

# Tkinter setup
root = tk.Tk()
root.title("Maze Game")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Generate the maze
while True:
    canvas.delete("all")
    for cell in grid_cells:
        cell.draw(canvas)
    next_cell = current_cell.check_neighbors()
    
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()
    else:
        break

# Game loop
speed = 8  # Movement speed (higher = faster)
player_progress = 0  # Tracks progress in moving between cells
moving = False  # Whether the player is currently moving
direction = None  # Direction of movement

def game_loop():
    global player_progress, moving, direction

    canvas.delete("all")
    
    for cell in grid_cells:
        cell.draw(canvas)

    # Handle movement
    if moving:
        player_progress += speed
        if direction == 'UP':
            path.append((player_pos[0] * TILE + TILE // 2, player_pos[1] * TILE + TILE // 2 - player_progress))
        elif direction == 'DOWN':
            path.append((player_pos[0] * TILE + TILE // 2, player_pos[1] * TILE + TILE // 2 + player_progress))
        elif direction == 'LEFT':
            path.append((player_pos[0] * TILE + TILE // 2 - player_progress, player_pos[1] * TILE + TILE // 2))
        elif direction == 'RIGHT':
            path.append((player_pos[0] * TILE + TILE // 2 + player_progress, player_pos[1] * TILE + TILE // 2))
        
        if player_progress >= TILE:
            player_progress = 0
            moving = False
            if direction == 'UP':
                player_pos[1] -= 1
            elif direction == 'DOWN':
                player_pos[1] += 1
            elif direction == 'LEFT':
                player_pos[0] -= 1
            elif direction == 'RIGHT':
                player_pos[0] += 1
            path.append((player_pos[0] * TILE + TILE // 2, player_pos[1] * TILE + TILE // 2))
            direction = None

    # Draw the path
    if len(path) > 1:
        canvas.create_line(path, fill="green", width=4)

    # Draw player
    canvas.create_oval(player_pos[0] * TILE + TILE // 4, player_pos[1] * TILE + TILE // 4,
                       player_pos[0] * TILE + 3 * TILE // 4, player_pos[1] * TILE + 3 * TILE // 4,
                       fill="red")

    # Draw goal
    canvas.create_oval(goal_pos[0] * TILE + TILE // 3, goal_pos[1] * TILE + TILE // 3,
                       goal_pos[0] * TILE + 2 * TILE // 3, goal_pos[1] * TILE + 2 * TILE // 3,
                       fill="blue")

    # Check for victory
    if player_pos == goal_pos:
        print("Congratulations! You reached the goal!")
        root.quit()

    root.after(1000 // 60, game_loop)

# Key events
def key_pressed(event):
    global moving, direction
    current_index = player_pos[0] + player_pos[1] * cols
    current_cell = grid_cells[current_index]
    if not moving:
        if event.keysym == 'Up' and not current_cell.walls['top']:
            moving = True
            direction = 'UP'
        if event.keysym == 'Down' and not current_cell.walls['bottom']:
            moving = True
            direction = 'DOWN'
        if event.keysym == 'Left' and not current_cell.walls['left']:
            moving = True
            direction = 'LEFT'
        if event.keysym == 'Right' and not current_cell.walls['right']:
            moving = True
            direction = 'RIGHT'

root.bind("<KeyPress>", key_pressed)
game_loop()
root.mainloop()

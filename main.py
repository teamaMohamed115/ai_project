import tkinter as tk
from tkinter import messagebox, ttk
import heapq
import time
import math
import random
from random import choice

class GameManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game Collection")
        self.create_main_menu()

    def create_main_menu(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        # Configure the main menu
        self.root.geometry("400x400")
        
        # Title
        title_label = tk.Label(self.root, text="Game Collection", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)
        # Game buttons
        games = [
            ("Towers of Hanoi", self.start_towers_of_hanoi),
            ("Connect Four", self.start_connect_four),
            ("Maze Solver", self.start_maze_solver)
        ]
        for game_name, game_func in games:
            button = tk.Button(
                self.root,
                text=game_name,
                font=("Arial", 14),
                width=20,
                height=2,
                command=game_func
            )
            button.pack(pady=10)
        # Quit button
        quit_button = tk.Button(
            self.root,
            text="Quit",
            font=("Arial", 14),
            width=20,
            height=2,
            command=self.root.quit
        )
        quit_button.pack(pady=20)

    def back_to_main_menu(self):
        # Hide the current game window
        self.root.withdraw()
        # Show the main menu window
        self.create_main_menu()
        self.root.deiconify()

    def start_towers_of_hanoi(self):
        self.root.withdraw()  # Hide the main window instead of destroying it
        start_gui(self.root, self)  # Pass the existing root window and self

    def start_connect_four(self):
        self.root.withdraw()  # Hide the main window instead of destroying it
        root = tk.Tk()
        ConnectFourGUI(root, self)  # Pass self reference for back functionality

    def start_maze_solver(self):
        self.root.withdraw()  # Hide the main window instead of destroying it
        root = tk.Tk()
        MazeSolverGUI(root, self)  # Pass self reference for back functionality

# class GameManager:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("Game Collection")
#         self.create_main_menu()

#     def create_main_menu(self):
#         # Clear existing widgets
#         for widget in self.root.winfo_children():
#             widget.destroy()

#         # Configure the main menu
#         self.root.geometry("400x400")
        
#         # Title
#         title_label = tk.Label(self.root, text="Game Collection", font=("Arial", 24, "bold"))
#         title_label.pack(pady=20)

#         # Game buttons
#         games = [
#             ("Towers of Hanoi", self.start_towers_of_hanoi),
#             ("Connect Four", self.start_connect_four),
#             ("Maze Solver", self.start_maze_solver)
#         ]

#         for game_name, game_func in games:
#             button = tk.Button(
#                 self.root,
#                 text=game_name,
#                 font=("Arial", 14),
#                 width=20,
#                 height=2,
#                 command=game_func
#             )
#             button.pack(pady=10)

#         # Quit button
#         quit_button = tk.Button(
#             self.root,
#             text="Quit",
#             font=("Arial", 14),
#             width=20,
#             height=2,
#             command=self.root.quit
#         )
#         quit_button.pack(pady=20)

#     def back_to_main_menu(self):
#         # Destroy current game window
#         self.root.destroy()
#         # Create new root window and menu
#         self.__init__()

#     def start_towers_of_hanoi(self):
#         # self.root.destroy()
#         # root = tk.Tk()
#         # start_gui(root, self)  # Pass self reference for back functionality
            
#         self.root.withdraw()  # Hide the main window instead of destroying it
#         start_gui(self.root, self)  # Pass the existing root window and self

#     def start_connect_four(self):
#         self.root.destroy()
#         root = tk.Tk()
#         ConnectFourGUI(root, self)  # Pass self reference for back functionality

#     def start_maze_solver(self):
#         self.root.destroy()
#         root = tk.Tk()
#         MazeSolverGUI(root, self)  # Pass self reference for back functionality

# [Original Towers of Hanoi code remains the same, except modify the start_gui function to accept game_manager parameter]

scores = {3: [], 4: [], 5: [], 6: []}  # Global dictionary to track scores

# Towers of Hanoi logic using A*
def a_star_towers_of_hanoi(num_disks):
    initial_state = (tuple(range(num_disks, 0, -1)), (), ())
    goal_state = ((), (), tuple(range(num_disks, 0, -1)))

    def heuristic(state):
        return sum(disk != peg[-1] if peg else True for peg in state for disk in peg)

    def get_neighbors(state):
        neighbors = []
        for from_peg in range(3):
            if state[from_peg]:
                for to_peg in range(3):
                    if from_peg != to_peg:
                        if not state[to_peg] or state[from_peg][-1] < state[to_peg][-1]:
                            new_state = list(map(list, state))
                            disk = new_state[from_peg].pop()
                            new_state[to_peg].append(disk)
                            neighbors.append(tuple(map(tuple, new_state)))
        return neighbors

    open_set = []
    heapq.heappush(open_set, (heuristic(initial_state), 0, initial_state, []))
    closed_set = set()

    while open_set:
        _, g, current_state, path = heapq.heappop(open_set)

        if current_state == goal_state:
            return path

        if current_state in closed_set:
            continue

        closed_set.add(current_state)

        for neighbor in get_neighbors(current_state):
            if neighbor not in closed_set:
                move = (current_state, neighbor)
                heapq.heappush(
                    open_set,
                    (g + 1 + heuristic(neighbor), g + 1, neighbor, path + [move])
                )

    return None

def start_gui(root, game_manager):

    def start_game(level):
        num_disks = level
        solution = a_star_towers_of_hanoi(num_disks)

        def reset_game():
            nonlocal start_time, state, selected_peg, timer_running, history
            start_time = time.time()
            state = [list(range(num_disks, 0, -1)), [], []]
            selected_peg = None
            timer_running = True
            history = []
            draw_game()
            update_timer()

        def draw_game():
            canvas.delete("all")
            peg_width = 20
            peg_height = 200

            # Draw pegs
            for i in range(3):
                x = 100 + i * 200
                y = 300
                canvas.create_rectangle(x - peg_width / 2, y - peg_height, x + peg_width / 2, y, fill="black")

            # Draw disks
            for peg_index, peg in enumerate(state):
                for disk_index, disk in enumerate(reversed(peg)):
                    width = 50 + (disk - 1) * 30
                    height = 20
                    x = 100 + peg_index * 200
                    y = 300 - (len(peg) - disk_index) * height
                    canvas.create_rectangle(x - width / 2, y - height, x + width / 2, y, fill="blue")

        def on_click(event):
            nonlocal selected_peg, timer_running

            x = event.x
            peg_width = 20

            for i in range(3):
                peg_x = 100 + i * 200
                if peg_x - peg_width / 2 <= x <= peg_x + peg_width / 2:
                    if selected_peg is None:
                        if state[i]:
                            selected_peg = i
                            status_label.config(text=f"Selected Rod {chr(65 + i)}.", fg="blue")
                    else:
                        if not state[i] or state[selected_peg][-1] < state[i][-1]:
                            history.append([list(peg) for peg in state])  # Save current state
                            state[i].append(state[selected_peg].pop())
                            draw_game()
                            status_label.config(text=f"Moved disk to Rod {chr(65 + i)}", fg="green")
                            # if state[2] == list(range(num_disks, 0, -1)):
                            #     elapsed_time = time.time() - start_time
                            #     timer_running = False
                            #     messagebox.showinfo("Congratulations!", f"You solved the puzzle in {elapsed_time:.2f} seconds!")
                            #     best_scores[level] = min(best_scores[level], elapsed_time)

                            if state[2] == list(range(num_disks, 0, -1)):
                                elapsed_time = time.time() - start_time
                                timer_running = False
                                num_moves = len(history)
                                scores[level].append((elapsed_time, num_moves))  # Store time and moves
                                messagebox.showinfo("Congratulations!", f"You solved the puzzle in {elapsed_time:.2f} seconds and {num_moves} moves!")

                        else:
                            status_label.config(text="Invalid move! Cannot place a larger disk on a smaller one.", fg="red")
                        selected_peg = None
                        return

        def update_timer():
            if not timer_running:
                return
            elapsed_time = time.time() - start_time
            if elapsed_time >= 60:
                messagebox.showinfo("Game Over", "Time's up! Here's the solution:")
                show_solution()
            else:
                timer_label.config(text=f"Time: {elapsed_time:.2f} s")
                root.after(100, update_timer)

        def show_solution():
            solution_text = "\n".join([str(move) for move in solution])
            messagebox.showinfo("Solution", solution_text)

        def back_to_menu():
            root.destroy()
            menu()

        def undo_move():
            if history:
                nonlocal state
                state = history.pop()
                draw_game()
                status_label.config(text="Undid the last move.", fg="orange")
            else:
                status_label.config(text="No moves to undo!", fg="red")

        def show_scores():
            if scores[level]:
                score_text = "\n".join([f"Time: {time:.2f}s, Moves: {moves}" for time, moves in scores[level]])
                messagebox.showinfo("Achieved Scores", f"Scores for Level {level}:\n\n{score_text}")
            else:
                messagebox.showinfo("Achieved Scores", "No scores recorded yet for this level.")

        root = tk.Tk()
        root.title(f"Towers of Hanoi - Level {level}")

        start_time = time.time()
        selected_peg = None
        state = [list(range(num_disks, 0, -1)), [], []]
        timer_running = True
        history = []

        # best_scores = {3: float('inf'), 4: float('inf'), 5: float('inf'), 6: float('inf')}

        status_label = tk.Label(root, text="Select a disk to move.", font=("Arial", 12), fg="blue")
        status_label.pack()

        timer_label = tk.Label(root, text="Time: 0.00 s", font=("Arial", 14))
        timer_label.pack()

        canvas = tk.Canvas(root, width=600, height=400, bg="white")
        canvas.pack()
        canvas.bind("<Button-1>", on_click)

        button_frame = tk.Frame(root)
        button_frame.pack()

        reset_button = tk.Button(button_frame, text="Reset", command=reset_game)
        reset_button.grid(row=0, column=0)

        solution_button = tk.Button(button_frame, text="Show Solution", command=show_solution)
        solution_button.grid(row=0, column=1)

        back_button = tk.Button(button_frame, text="Back", command=back_to_menu)
        back_button.grid(row=0, column=2)

        undo_button = tk.Button(button_frame, text="Undo", command=undo_move)
        undo_button.grid(row=0, column=3)

        scores_button = tk.Button(button_frame, text="Achieved Scores", command=show_scores)
        scores_button.grid(row=0, column=4)

        draw_game()
        update_timer()

        root.mainloop()


    def menu():
        menu_root = tk.Tk()
        menu_root.title("Select a Level of Difficulty")

        title_label = tk.Label(menu_root, text="Select a Level of Difficulty", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        buttons = [
            ("Easy (3 disks)", 3),
            ("Medium (4 disks)", 4),
            ("Hard (5 disks)", 5),
            ("Level الوحش (6 disks)", 6),
        ]

        for text, level in buttons:
            button = tk.Button(menu_root, text=text, font=("Arial", 14), 
                             command=lambda l=level: [menu_root.destroy(), start_game(l)])
            button.pack(pady=5)

        # Add back to main menu button
        back_button = tk.Button(menu_root, text="Back to Main Menu", font=("Arial", 14, "bold"),
                              command=lambda: [menu_root.destroy(), game_manager.back_to_main_menu()])
        back_button.pack(pady=10)

        menu_root.mainloop()

    # [Rest of the Towers of Hanoi code remains the same]
    menu()










#############################################################################################################################










# [Original Connect Four code remains the same, except modify the ConnectFourGUI class to accept game_manager parameter]

# Constants (existing ones remain the same)
ROWS = 6
COLUMNS = 7
PLAYER_1 = "X"  # Human
PLAYER_2 = "O"  # AI
PLAYER_COLORS = {PLAYER_1: "red", PLAYER_2: "yellow"}
EMPTY_COLOR = "white"
BOARD_COLOR = "#003366"
WINNER_COLOR = "#FFD700"
SLOT_OUTLINE = "#CCCCCC"
ANIMATION_INTERVAL = 300


class ConnectFourGame:
    def __init__(self, difficulty="medium"):
        self.board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_player = PLAYER_1
        self.difficulty = difficulty
        self.depth_map = {
            "easy": 2,
            "medium": 4,
            "hard": 6
        }

    def drop_piece(self, column):
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][column] == " ":
                self.board[row][column] = self.current_player
                return row, column
        return None

    def check_winner(self, piece):
        winning_positions = []

        # Horizontal check
        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                if all(self.board[row][col + i] == piece for i in range(4)):
                    winning_positions = [(row, col + i) for i in range(4)]
                    return True, winning_positions

        # Vertical check
        for row in range(ROWS - 3):
            for col in range(COLUMNS):
                if all(self.board[row + i][col] == piece for i in range(4)):
                    winning_positions = [(row + i, col) for i in range(4)]
                    return True, winning_positions

        # Diagonal checks
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                if all(self.board[row + i][col + i] == piece for i in range(4)):
                    winning_positions = [(row + i, col + i) for i in range(4)]
                    return True, winning_positions
        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                if all(self.board[row - i][col + i] == piece for i in range(4)):
                    winning_positions = [(row - i, col + i) for i in range(4)]
                    return True, winning_positions

        return False, []

    def is_draw(self):
        return all(self.board[0][col] != " " for col in range(COLUMNS))

    def switch_player(self):
        self.current_player = PLAYER_2 if self.current_player == PLAYER_1 else PLAYER_1

    def get_valid_moves(self):
        return [col for col in range(COLUMNS) if self.board[0][col] == " "]

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = PLAYER_1 if piece == PLAYER_2 else PLAYER_2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(" ") == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(" ") == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(" ") == 1:
            score -= 4

        return score

    def evaluate_window_simple(self, window, piece, opp_piece):
        score = 0

        if window.count(piece) == 4:
            score += 100  # Winning move
        elif window.count(piece) == 3 and window.count(" ") == 1:
            score += 10  # Good potential move
        elif window.count(piece) == 2 and window.count(" ") == 2:
            score += 5  # Decent potential move

        if window.count(opp_piece) == 3 and window.count(" ") == 1:
            score -= 50  # Block opponent's winning move

        return score

    def evaluate_position(self):
        score = 0
        piece = PLAYER_2  # AI piece

        # Score center column
        center_array = [self.board[row][COLUMNS // 2] for row in range(ROWS)]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Horizontal
        for row in range(ROWS):
            row_array = self.board[row]
            for col in range(COLUMNS - 3):
                window = row_array[col:col + 4]
                score += self.evaluate_window(window, piece)

        # Vertical
        for col in range(COLUMNS):
            col_array = [self.board[row][col] for row in range(ROWS)]
            for row in range(ROWS - 3):
                window = col_array[row:row + 4]
                score += self.evaluate_window(window, piece)

        # Diagonal
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                # Positive diagonal
                window = [self.board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

                # Negative diagonal
                window = [self.board[row + 3 - i][col + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def evaluate_position_simple(self):
        score = 0
        piece = PLAYER_2
        opp_piece = PLAYER_1

        # Score center column
        center_array = [self.board[row][COLUMNS // 2] for row in range(ROWS)]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Horizontal
        for row in range(ROWS):
            row_array = self.board[row]
            for col in range(COLUMNS - 3):
                window = row_array[col:col + 4]
                score += self.evaluate_window_simple(window, piece, opp_piece)

        # Vertical
        for col in range(COLUMNS):
            col_array = [self.board[row][col] for row in range(ROWS)]
            for row in range(ROWS - 3):
                window = col_array[row:row + 4]
                score += self.evaluate_window_simple(window, piece, opp_piece)

        # Diagonal
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                # Positive diagonal
                window = [self.board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window_simple(window, piece, opp_piece)

                # Negative diagonal
                window = [self.board[row + 3 - i][col + i] for i in range(4)]
                score += self.evaluate_window_simple(window, piece, opp_piece)

        return score

    def is_terminal_node(self):
        return self.check_winner(PLAYER_1)[0] or self.check_winner(PLAYER_2)[0] or len(self.get_valid_moves()) == 0

    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        valid_moves = self.get_valid_moves()
        is_terminal = self.is_terminal_node()

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_winner(PLAYER_2)[0]:
                    return (None, 100000000000000)
                elif self.check_winner(PLAYER_1)[0]:
                    return (None, -100000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.evaluate_position())

        if maximizing_player:
            value = -math.inf
            column = valid_moves[0]
            for col in valid_moves:
                row = -1
                for r in range(ROWS - 1, -1, -1):
                    if self.board[r][col] == " ":
                        row = r
                        break
                if row != -1:
                    self.board[row][col] = PLAYER_2
                    new_score = self.alpha_beta(depth - 1, alpha, beta, False)[1]
                    self.board[row][col] = " "
                    if new_score > value:
                        value = new_score
                        column = col
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = valid_moves[0]
            for col in valid_moves:
                row = -1
                for r in range(ROWS - 1, -1, -1):
                    if self.board[r][col] == " ":
                        row = r
                        break
                if row != -1:
                    self.board[row][col] = PLAYER_1
                    new_score = self.alpha_beta(depth - 1, alpha, beta, True)[1]
                    self.board[row][col] = " "
                    if new_score < value:
                        value = new_score
                        column = col
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
            return column, value

    def get_ai_move(self):
        if self.difficulty == "easy":
            return self.get_easy_move()

        depth = self.depth_map[self.difficulty]
        column, _ = self.alpha_beta(depth, -math.inf, math.inf, True)
        return column

    def get_easy_move(self):
        valid_moves = self.get_valid_moves()
        scores = []

        for col in valid_moves:
            # Simulate dropping a piece in the column
            row = self.get_next_row(col)
            if row is not None:
                self.board[row][col] = PLAYER_2
                # Evaluate the board using a simplified heuristic
                score = self.evaluate_position_simple()
                # Undo the move
                self.board[row][col] = " "
                scores.append((col, score))

        # Sort moves by score (best first)
        scores.sort(key=lambda x: x[1], reverse=True)

        # Add randomness factor: Occasionally choose from lower-ranked options
        if len(scores) > 1 and random.random() < 0.3:  # 30% chance to pick a less optimal move
            move = random.choice(scores[1:])[0]
        else:
            move = scores[0][0]  # Choose the best move

        return move

    def get_next_row(self, col):
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == " ":
                return row
        return None

class ConnectFourGUI:

    def __init__(self, root, game_manager):
        # self.game_manager = game_manager
        # self.root = root
        # self.root.title("Connect Four vs AI")

        # # Create main container frame
        # self.main_frame = tk.Frame(root)
        # self.main_frame.grid(row=0, column=0, sticky="nsew")

        # # Create button frame with right alignment
        # self.button_frame = tk.Frame(self.main_frame)
        # self.button_frame.grid(row=0, column=0, columnspan=COLUMNS, sticky="e", padx=10, pady=5)

        # # Modify the back button to properly return to main menu
        # self.back_button = tk.Button(
        #     self.button_frame,
        #     text="Back to Main Menu",
        #     font=("Arial", 12),
        #     command=lambda: [self.root.withdraw(), game_manager.back_to_main_menu()]
        # )
        # self.back_button.pack(side="right")

        self.game_manager = game_manager
        self.root = root
        self.root.title("Connect Four vs AI")
        # Create main container frame
        self.main_frame = tk.Frame(root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        # Create button frame with right alignment
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=0, column=0, columnspan=COLUMNS, sticky="e", padx=10, pady=5)
        # Modify the back button to properly return to main menu
        self.back_button = tk.Button(
            self.button_frame,
            text="Back to Main Menu",
            font=("Arial", 12),
            command=self.back_to_main_menu
        )
        self.back_button.pack(side="right")

    # def back_to_main_menu(self):
    #     # Destroy current game window
    #     self.root.destroy()
    #     # Create new root window and menu
    #     self.__init__()

        # # Add back to main menu button
        # back_button = tk.Button(menu_root, text="Back to Main Menu", font=("Arial", 14, "bold"),
        #                       command=lambda: [menu_root.destroy(), game_manager.back_to_main_menu()])

        # Difficulty selector
        self.difficulty_frame = tk.Frame(self.main_frame)
        self.difficulty_frame.grid(row=1, column=0, columnspan=COLUMNS, pady=5)

        tk.Label(self.difficulty_frame, text="Difficulty:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.difficulty_var = tk.StringVar(value="medium")
        self.difficulty_combo = ttk.Combobox(
            self.difficulty_frame,
            textvariable=self.difficulty_var,
            values=["easy", "medium", "hard"],
            state="readonly",
            width=10
        )
        self.difficulty_combo.pack(side=tk.LEFT, padx=5)

        self.game = ConnectFourGame(self.difficulty_var.get())
        self.buttons = []
        self.animation_running = False

        # Game Canvas
        self.canvas = tk.Canvas(self.main_frame, width=COLUMNS * 100, height=ROWS * 80, bg=BOARD_COLOR, highlightthickness=0)
        self.canvas.grid(row=2, column=0, columnspan=COLUMNS)

        # Add column buttons
        self.buttons = []
        for col in range(COLUMNS):
            button = tk.Button(
                self.main_frame, text="↓", font=("Arial", 18, "bold"), bg="#4CAF50", fg="white",
                activebackground="#45a049", command=lambda c=col: self.human_move(c)
            )
            button.grid(row=3, column=col, sticky="nsew", padx=2, pady=2)
            self.buttons.append(button)

        # Status Label
        self.status_label = tk.Label(self.main_frame, text="Your Turn (Red)", font=("Arial", 14), bg="white")
        self.status_label.grid(row=4, column=0, columnspan=COLUMNS, pady=10, sticky="nsew")

        # Restart Button
        self.restart_button = tk.Button(
            self.main_frame, text="Restart", font=("Arial", 14, "bold"), bg="gray", fg="white",
            command=self.reset_game
        )
        self.restart_button.grid(row=5, column=0, columnspan=COLUMNS, pady=5)

        # Add mode selector
        self.mode_frame = tk.Frame(self.main_frame)
        self.mode_frame.grid(row=6, column=0, columnspan=COLUMNS, pady=5)

        tk.Label(self.mode_frame, text="Mode:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.mode_var = tk.StringVar(value="Human vs AI")
        self.mode_combo = ttk.Combobox(
            self.mode_frame,
            textvariable=self.mode_var,
            values=["Human vs AI", "AI vs AI"],
            state="readonly",
            width=15
        )
        self.mode_combo.pack(side=tk.LEFT, padx=5)

        self.difficulty_combo.bind('<<ComboboxSelected>>', lambda e: self.reset_game())
        self.mode_combo.bind('<<ComboboxSelected>>', lambda e: self.reset_game())

        self.draw_board()

    def back_to_main_menu(self):
        self.root.destroy()
        self.game_manager.root.deiconify()

    # def back_to_main_menu(self):
    #     # Hide this window
    #     self.root.withdraw()
    #     # Show the main menu
    #     self.game_manager.root.deiconify()
    #     # Schedule the destruction of this window after showing main menu
    #     self.root.after(100, self.root.destroy)

    def human_move(self, column):
        if self.mode_var.get() != "Human vs AI" or self.game.current_player != PLAYER_1:
            return

        result = self.game.drop_piece(column)
        if result is None:
            messagebox.showwarning("Invalid Move", "Column is full! Try a different column.")
            return

        self.draw_board()

        if self.check_game_end():
            return

        # AI's turn
        self.game.switch_player()
        self.update_status()
        self.root.after(500, self.ai_move)

    def ai_move(self):
        ai_column = self.game.get_ai_move()
        result = self.game.drop_piece(ai_column)
        self.draw_board()

        if self.check_game_end():
            return

        self.game.switch_player()
        self.update_status()

    def check_game_end(self):
        has_winner, winning_positions = self.game.check_winner(self.game.current_player)
        if has_winner:
            self.animate_winner(winning_positions)
            winner = "You win!" if self.game.current_player == PLAYER_1 else "AI wins!"  # Display winner
            messagebox.showinfo("Game Over", winner)  # Show the winner's name
            self.disable_buttons()
            return True

        if self.game.is_draw():
            self.status_label.config(text="It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")  # Show draw message
            return True

        return False

    def draw_board(self, highlight=[]):
        self.canvas.delete("all")
        for row in range(ROWS):
            for col in range(COLUMNS):
                x0 = col * 100 + 10
                y0 = row * 100 + 10
                x1 = x0 + 80
                y1 = y0 + 80
                color = EMPTY_COLOR
                outline = SLOT_OUTLINE
                if self.game.board[row][col] == PLAYER_1:
                    color = PLAYER_COLORS[PLAYER_1]
                elif self.game.board[row][col] == PLAYER_2:
                    color = PLAYER_COLORS[PLAYER_2]
                if (row, col) in highlight:
                    color = WINNER_COLOR
                self.canvas.create_oval(x0, y0, x1, y1, fill=color, outline=outline, width=2)

    def update_status(self):
        if self.game.current_player == PLAYER_1:
            player_text = "Your Turn (Red)" if self.game.difficulty != "ai_vs_ai" else "Player 1's Turn (Red)"
            player_color = PLAYER_COLORS[PLAYER_1]  # Red
        else:
            player_text = "AI's Turn (Yellow)" if self.game.difficulty != "ai_vs_ai" else "Player 2's Turn (Yellow)"
            player_color = PLAYER_COLORS[PLAYER_2]  # Yellow

        self.status_label.config(text=player_text, bg=player_color)

    def disable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)

    def reset_game(self):
        self.animation_running = False
        self.game = ConnectFourGame(difficulty=self.difficulty_var.get())
        self.draw_board()
        self.update_status()
        for button in self.buttons:
            button.config(state=tk.NORMAL)

        # Disable buttons if in AI vs AI mode
        if self.mode_var.get() == "AI vs AI":
            for button in self.buttons:
                button.config(state=tk.DISABLED)
            self.start_ai_vs_ai()

    def start_ai_vs_ai(self):
        def play_turn():
            if self.game.is_terminal_node():
                self.check_game_end()
                return

            current_difficulty = "easy" if self.game.current_player == PLAYER_1 else "hard"
            self.game.difficulty = current_difficulty

            ai_move = self.game.get_ai_move()
            self.game.drop_piece(ai_move)
            self.draw_board()

            if self.check_game_end():
                return

            self.game.switch_player()
            self.update_status()
            self.root.after(500, play_turn)  # Add delay for better simulation effect

        play_turn()

    def animate_winner(self, positions):
        self.animation_running = True

        def toggle_color():
            if not self.animation_running:
                return
            current_color = self.canvas.itemcget("highlight", "fill")
            new_color = WINNER_COLOR if current_color == BOARD_COLOR else BOARD_COLOR
            for row, col in positions:
                x0 = col * 100 + 10
                y0 = row * 100 + 10
                x1 = x0 + 80
                y1 = y0 + 80
                self.canvas.create_oval(x0, y0, x1, y1, fill=new_color, outline=SLOT_OUTLINE, tags="highlight")
            self.root.after(ANIMATION_INTERVAL, toggle_color)

        toggle_color()










#############################################################################################################################










# [Original Maze Solver code remains the same, except create a new class to handle the GUI]

class MazeSolverGUI:

    def __init__(self, root, game_manager):
        # self.game_manager = game_manager
        # self.root = root
        # self.root.title("Maze Game")
        
        # # Constants
        # self.WIDTH = 600
        # self.HEIGHT = 600
        # self.TILE = 40
        # self.cols = self.WIDTH // self.TILE
        # self.rows = self.HEIGHT // self.TILE
        
        # # Create frame for buttons
        # self.button_frame = tk.Frame(self.root)
        # self.button_frame.pack(pady=5)
        
        # # Modified back button with proper navigation
        # self.back_button = tk.Button(
        #     self.button_frame,
        #     text="Back to Main Menu",
        #     font=("Arial", 12),
        #     command=self.back_to_main_menu
        # )
        # self.back_button.pack(pady=5)

        self.game_manager = game_manager
        self.root = root
        self.root.title("Maze Game")
        
        # Constants
        self.WIDTH = 600
        self.HEIGHT = 600
        self.TILE = 40
        self.cols = self.WIDTH // self.TILE
        self.rows = self.HEIGHT // self.TILE
        
        # Create frame for buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)
        
        # Modified back button with proper navigation
        self.back_button = tk.Button(
            self.button_frame,
            text="Back to Main Menu",
            font=("Arial", 12),
            command=self.back_to_main_menu
        )
        self.back_button.pack(pady=5)

        # Create canvas
        self.canvas = tk.Canvas(self.root, width=self.WIDTH, height=self.HEIGHT, bg="black")
        self.canvas.pack()
        
        # Game state variables
        self.speed = 8
        self.player_progress = 0
        self.moving = False
        self.direction = None
        self.path = []
        
        # Initialize game
        self.reset_game_state()
        self.generate_maze()
        
        # Start game loop
        self.game_loop()
        
        # Bind keys
        self.root.bind("<KeyPress>", self.key_pressed)

    def create_ui(self):
        # Create back button
        back_button = tk.Button(
            self.root,
            text="Back to Main Menu",
            command=lambda: [self.root.destroy(), self.game_manager.root.deiconify()]
        )
        back_button.pack()

        # Create canvas
        self.canvas = tk.Canvas(self.root, width=self.WIDTH, height=self.HEIGHT, bg="black")
        self.canvas.pack()

    def reset_game_state(self):
        self.grid_cells = [Cell(col, row) for row in range(self.rows) for col in range(self.cols)]
        self.current_cell = self.grid_cells[0]
        self.stack = []
        self.player_pos = [0, 0]  # Player starts at top-left
        self.goal_pos = [self.cols - 1, self.rows - 1]  # Goal at bottom-right
        self.path = []

    def generate_maze(self):
        self.current_cell.visited = True
        while True:
            self.canvas.delete("all")
            for cell in self.grid_cells:
                cell.draw(self.canvas)
            
            next_cell = self.current_cell.check_neighbors(self.grid_cells, self.cols, self.rows)
            
            if next_cell:
                next_cell.visited = True
                self.stack.append(self.current_cell)
                self.remove_walls(self.current_cell, next_cell)
                self.current_cell = next_cell
            elif self.stack:
                self.current_cell = self.stack.pop()
            else:
                break

    def remove_walls(self, current, next):
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

    # def back_to_main_menu(self):
    #     self.root.withdraw()
    #     self.game_manager.back_to_main_menu()

    def back_to_main_menu(self):
        self.root.destroy()
        self.game_manager.root.deiconify()

    def game_loop(self):
        self.canvas.delete("all")
        
        for cell in self.grid_cells:
            cell.draw(self.canvas)

        # Handle movement
        if self.moving:
            self.player_progress += self.speed
            if self.direction == 'UP':
                self.path.append((self.player_pos[0] * self.TILE + self.TILE // 2,
                                self.player_pos[1] * self.TILE + self.TILE // 2 - self.player_progress))
            elif self.direction == 'DOWN':
                self.path.append((self.player_pos[0] * self.TILE + self.TILE // 2,
                                self.player_pos[1] * self.TILE + self.TILE // 2 + self.player_progress))
            elif self.direction == 'LEFT':
                self.path.append((self.player_pos[0] * self.TILE + self.TILE // 2 - self.player_progress,
                                self.player_pos[1] * self.TILE + self.TILE // 2))
            elif self.direction == 'RIGHT':
                self.path.append((self.player_pos[0] * self.TILE + self.TILE // 2 + self.player_progress,
                                self.player_pos[1] * self.TILE + self.TILE // 2))
            
            if self.player_progress >= self.TILE:
                self.player_progress = 0
                self.moving = False
                if self.direction == 'UP':
                    self.player_pos[1] -= 1
                elif self.direction == 'DOWN':
                    self.player_pos[1] += 1
                elif self.direction == 'LEFT':
                    self.player_pos[0] -= 1
                elif self.direction == 'RIGHT':
                    self.player_pos[0] += 1
                self.path.append((self.player_pos[0] * self.TILE + self.TILE // 2,
                                self.player_pos[1] * self.TILE + self.TILE // 2))
                self.direction = None

        # Draw the path
        if len(self.path) > 1:
            self.canvas.create_line(self.path, fill="green", width=4)

        # Draw player
        self.canvas.create_oval(
            self.player_pos[0] * self.TILE + self.TILE // 4,
            self.player_pos[1] * self.TILE + self.TILE // 4,
            self.player_pos[0] * self.TILE + 3 * self.TILE // 4,
            self.player_pos[1] * self.TILE + 3 * self.TILE // 4,
            fill="red"
        )

        # Draw goal
        self.canvas.create_oval(
            self.goal_pos[0] * self.TILE + self.TILE // 3,
            self.goal_pos[1] * self.TILE + self.TILE // 3,
            self.goal_pos[0] * self.TILE + 2 * self.TILE // 3,
            self.goal_pos[1] * self.TILE + 2 * self.TILE // 3,
            fill="blue"
        )

        # # Check for victory
        # if self.player_pos == self.goal_pos:
        #     messagebox.showinfo("Victory!", "Congratulations! You reached the goal!")
        #     self.root.destroy()
        #     self.game_manager.back_to_main_menu()
        #     return
        
        # Check for victory
        if self.player_pos == self.goal_pos:
            messagebox.showinfo("Victory!", "Congratulations! You reached the goal!")
            if messagebox.askyesno("Play Again?", "Would you like to play again?"):
                self.reset_game_state()
                self.generate_maze()
                self.game_loop()
                self.root.bind("<KeyPress>", self.key_pressed)
            else:
                self.back_to_main_menu()
            return

        self.root.after(1000 // 60, self.game_loop)

    def key_pressed(self, event):
        if not self.moving:
            current_index = self.player_pos[0] + self.player_pos[1] * self.cols
            current_cell = self.grid_cells[current_index]
            
            if event.keysym == 'Up' and not current_cell.walls['top']:
                self.moving = True
                self.direction = 'UP'
            if event.keysym == 'Down' and not current_cell.walls['bottom']:
                self.moving = True
                self.direction = 'DOWN'
            if event.keysym == 'Left' and not current_cell.walls['left']:
                self.moving = True
                self.direction = 'LEFT'
            if event.keysym == 'Right' and not current_cell.walls['right']:
                self.moving = True
                self.direction = 'RIGHT'

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw(self, canvas):
        TILE = 40  # Need to match the TILE size from MazeSolverGUI
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

    def check_neighbors(self, grid_cells, cols, rows):
        def check_cell(x, y):
            if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
                return False
            return grid_cells[x + y * cols]

        neighbors = []
        top = check_cell(self.x, self.y - 1)
        right = check_cell(self.x + 1, self.y)
        bottom = check_cell(self.x, self.y + 1)
        left = check_cell(self.x - 1, self.y)
        
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
            
        return choice(neighbors) if neighbors else False



def main():
    game_manager = GameManager()
    game_manager.root.mainloop()

if __name__ == "__main__":
    main()
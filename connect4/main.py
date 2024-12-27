import tkinter as tk
from tkinter import messagebox, ttk
import math
import random
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
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four vs AI")

        # Difficulty selector
        self.difficulty_frame = tk.Frame(root)
        self.difficulty_frame.grid(row=0, column=0, columnspan=COLUMNS, pady=5)

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
        self.canvas = tk.Canvas(root, width=COLUMNS * 100, height=ROWS * 100, bg=BOARD_COLOR, highlightthickness=0)
        self.canvas.grid(row=1, column=0, columnspan=COLUMNS)

        # Add buttons
        self.buttons = []
        for col in range(COLUMNS):
            button = tk.Button(
                root, text="↓", font=("Arial", 18, "bold"), bg="#4CAF50", fg="white",
                activebackground="#45a049", command=lambda c=col: self.human_move(c)
            )
            button.grid(row=2, column=col, sticky="nsew", padx=2, pady=2)
            self.buttons.append(button)

        # Status Label
        self.status_label = tk.Label(root, text="Your Turn (Red)", font=("Arial", 14), bg="white")
        self.status_label.grid(row=3, column=0, columnspan=COLUMNS, pady=10, sticky="nsew")

        # Restart Button
        self.restart_button = tk.Button(
            root, text="Restart", font=("Arial", 14, "bold"), bg="gray", fg="white",
            command=self.reset_game
        )
        self.restart_button.grid(row=4, column=0, columnspan=COLUMNS, pady=5)

        self.difficulty_combo.bind('<<ComboboxSelected>>', lambda e: self.reset_game())
        self.draw_board()

        # Add mode selector
        self.mode_frame = tk.Frame(root)
        self.mode_frame.grid(row=0, column=0, columnspan=COLUMNS, pady=5)

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
        self.mode_combo.bind('<<ComboboxSelected>>', lambda e: self.reset_game())

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
            winner = "You win!" if self.game.current_player == PLAYER_1 else "AI wins!"
            messagebox.showinfo("Game Over", winner)
            self.disable_buttons()
            return True

        if self.game.is_draw():
            self.status_label.config(text="It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
            return True

        return False

    # [Rest of the GUI methods remain the same as in your original code]
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


def main():
    root = tk.Tk()
    ConnectFourGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
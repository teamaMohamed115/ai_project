import tkinter as tk
from tkinter import messagebox
import heapq
import time

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

# GUI for Towers of Hanoi
def start_gui():
    def start_game(level):
        num_disks = level
        solution = a_star_towers_of_hanoi(num_disks)

        def reset_game():
            nonlocal start_time, state, selected_peg
            start_time = time.time()
            state = [list(range(num_disks, 0, -1)), [], []]
            selected_peg = None
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
                for disk_index, disk in enumerate(peg):
                    width = 50 + (disk - 1) * 30
                    height = 20
                    x = 100 + peg_index * 200
                    y = 300 - (disk_index + 1) * height  # Adjust position based on the disk index
                    canvas.create_rectangle(x - width / 2, y - height, x + width / 2, y, fill="blue", outline="black")

        def on_click(event):
            nonlocal selected_peg

            x = event.x
            peg_width = 20

            for i in range(3):
                peg_x = 100 + i * 200
                if peg_x - peg_width / 2 <= x <= peg_x + peg_width / 2:
                    if selected_peg is None:
                        # Select the peg only if it's not empty
                        if state[i]:
                            selected_peg = i
                            status_label.config(text=f"Selected disk from Rod {chr(65 + i)}", fg="green")
                        else:
                            status_label.config(text=f"Rod {chr(65 + i)} is empty! Select another rod.", fg="red")
                    else:
                        # Move disk only if the target peg is empty or its top disk is larger
                        if not state[i] or state[selected_peg][-1] < state[i][-1]:
                            state[i].append(state[selected_peg].pop())
                            draw_game()
                            status_label.config(text=f"Moved disk to Rod {chr(65 + i)}", fg="green")

                            # Check for game completion
                            if state[2] == list(range(num_disks, 0, -1)):
                                elapsed_time = time.time() - start_time
                                messagebox.showinfo("Congratulations!", f"You solved the puzzle in {elapsed_time:.2f} seconds!")
                                best_scores[level] = min(best_scores[level], elapsed_time)
                        else:
                            status_label.config(text=f"Invalid move! You can't place a larger disk on a smaller one.", fg="red")

                        # Deselect the source peg after the move
                        selected_peg = None
                        return

        def update_timer():
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

        root = tk.Tk()
        root.title(f"Towers of Hanoi - Level {level}")

        start_time = time.time()
        selected_peg = None
        state = [list(range(num_disks, 0, -1)), [], []]

        best_scores = {3: float('inf'), 4: float('inf'), 5: float('inf'), 6: float('inf')}

        timer_label = tk.Label(root, text="Time: 0.00 s", font=("Arial", 14))
        timer_label.pack()

        canvas = tk.Canvas(root, width=600, height=400, bg="white")
        canvas.pack()
        canvas.bind("<Button-1>", on_click)
        #################
        status_label = tk.Label(root, text="Select a disk to move.", font=("Arial", 12), fg="blue")
        status_label.pack()
        #################

        button_frame = tk.Frame(root)
        button_frame.pack()

        reset_button = tk.Button(button_frame, text="Reset", command=reset_game)
        reset_button.grid(row=0, column=0)

        solution_button = tk.Button(button_frame, text="Show Solution", command=show_solution)
        solution_button.grid(row=0, column=1)

        back_button = tk.Button(button_frame, text="Back", command=back_to_menu)
        back_button.grid(row=0, column=2)

        draw_game()
        update_timer()

        root.mainloop()

    def menu():
        menu_root = tk.Tk()
        menu_root.title("Select a Level of Difficulty")

        title_label = tk.Label(menu_root, text="Select a Level of Difficulty", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        buttons = [
            ("Level 1: Easy (3 disks)", 3),
            ("Level 2: Medium (4 disks)", 4),
            ("Level 3: Hard (5 disks)", 5),
            ("Level 4: Level الوحش", 6),
            ("Level 5: Solve and take 1 million dollar", -1),
        ]

        for text, level in buttons:
            button = tk.Button(menu_root, text=text, font=("Arial", 14), command=lambda l=level: [menu_root.destroy(), start_game(l)] if l > 0 else None)
            button.pack(pady=5)

        menu_root.mainloop()

    menu()

if __name__ == "__main__":
    start_gui()

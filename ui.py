import customtkinter as ctk
from tkinter import Canvas, messagebox
from game_logic import GameLogic
from hanoi_solver import HanoiSolver
import time
import threading
import math

class HanoiUI:
    def __init__(self, root, num_disks, on_home_callback):
        self.root = root
        self.num_disks = num_disks
        self.on_home_callback = on_home_callback
        self.game = GameLogic()
        self.solver = HanoiSolver(self.game)
        self.selected_peg = None
        self.selected_disk = None
        self.move_counter = 0
        self.start_time = None
        self.timer_running = False
        self.auto_solving = False

        # Modern UI Setup
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Main container
        self.main_frame = ctk.CTkFrame(root, fg_color="#1a1a1a")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="#2d2d2d", corner_radius=15)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))

        self.title_label = ctk.CTkLabel(self.header_frame, text="🗼 Tower of Hanoi", font=("Helvetica", 28, "bold"), text_color="#00ff88")
        self.title_label.pack(pady=(15, 5))

        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="Move all disks to the rightmost tower!", font=("Helvetica", 12), text_color="#cccccc")
        self.subtitle_label.pack(pady=(0, 15))

        # Game controls - simplified
        self.controls_frame = ctk.CTkFrame(self.main_frame, fg_color="#2d2d2d", corner_radius=15)
        self.controls_frame.pack(fill="x", padx=20, pady=10)

        # Left controls - Home and Restart
        self.left_controls = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.left_controls.pack(side="left", padx=20, pady=15)

        self.home_button = ctk.CTkButton(self.left_controls, text="🏠 Home", command=self.go_home,
                                       font=("Helvetica", 12, "bold"), fg_color="#666666", hover_color="#888888",
                                       width=80, height=35)
        self.home_button.pack(side="left", padx=(0, 10))

        self.restart_button = ctk.CTkButton(self.left_controls, text="🔄 Restart", command=self.restart_game,
                                          font=("Helvetica", 12, "bold"), fg_color="#00ff88", hover_color="#00cc66",
                                          width=80, height=35)
        self.restart_button.pack(side="left")

        # Center controls - Game info
        self.center_controls = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.center_controls.pack(side="left", padx=20, pady=15, expand=True)

        self.game_info_label = ctk.CTkLabel(self.center_controls, text=f"🗼 Tower of Hanoi - {self.num_disks} Discs",
                                          font=("Helvetica", 14, "bold"), text_color="#ffffff")
        self.game_info_label.pack()

        # Right controls - Auto solve and stats
        self.right_controls = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.right_controls.pack(side="right", padx=20, pady=15)

        self.solve_button = ctk.CTkButton(self.right_controls, text="🤖 Auto Solve", command=self.auto_solve,
                                        font=("Helvetica", 12, "bold"), fg_color="#ff8800", hover_color="#cc6600",
                                        width=100, height=35)
        self.solve_button.pack(side="top", pady=(0, 5))

        self.stats_frame = ctk.CTkFrame(self.right_controls, fg_color="transparent")
        self.stats_frame.pack(side="top")

        self.timer_label = ctk.CTkLabel(self.stats_frame, text="⏱️ 00:00", font=("Helvetica", 10, "bold"), text_color="#ffffff")
        self.timer_label.pack()

        self.moves_label = ctk.CTkLabel(self.stats_frame, text="🎯 0", font=("Helvetica", 10, "bold"), text_color="#ffffff")
        self.moves_label.pack()

        min_moves = (2 ** self.num_disks) - 1
        self.min_moves_label = ctk.CTkLabel(self.stats_frame, text=f"⭐ {min_moves}", font=("Helvetica", 10, "bold"), text_color="#cccccc")
        self.min_moves_label.pack()

        # Game canvas
        self.canvas_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a", corner_radius=15)
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        self.canvas = Canvas(self.canvas_frame, width=700, height=400, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(pady=20, padx=20)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Instructions
        self.instruction_label = ctk.CTkLabel(self.main_frame, text="Click a disk to select it, then click a destination tower to move it!",
                                           font=("Helvetica", 11), text_color="#888888")
        self.instruction_label.pack(pady=(0, 20))

        self.draw_pegs()
        self.start_game()  # Initialize the game

    def start_game(self):
        self.game.initialize(self.num_disks)
        self.move_counter = 0
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
        self.update_move_counter()
        self.draw_disks()
        self.instruction_label.configure(text="Click a disk to select it, then click a destination tower to move it!")

    def go_home(self):
        self.on_home_callback()

    def restart_game(self):
        self.start_game()

    def update_move_counter(self):
        self.moves_label.configure(text=f"🎯 {self.move_counter}")

    def update_timer(self):
        if self.timer_running and self.start_time:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.timer_label.configure(text=f"⏱️ Time: {minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)

    def draw_pegs(self):
        # Draw 3 clean 2D pegs
        self.canvas.delete("all")
        peg_positions = [150, 350, 550]

        for i, x in enumerate(peg_positions):
            # Simple rectangular peg
            self.canvas.create_rectangle(x-8, 60, x+8, 340, fill="#666666", outline="#999999", width=2)

            # Base
            self.canvas.create_rectangle(x-20, 340, x+20, 360, fill="#444444", outline="#666666", width=2)

            # Peg number
            self.canvas.create_text(x, 375, text=str(i+1), font=("Helvetica", 12, "bold"), fill="#ffffff")

    def draw_disks(self):
        self.draw_pegs()
        # Modern 2D color palette
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F"]
        peg_positions = [150, 350, 550]
        disk_height = 28

        for peg_idx, peg in enumerate(self.game.pegs):
            x = peg_positions[peg_idx]
            for i, disk in enumerate(peg):
                width = 40 + disk * 20
                y_top = 335 - (i + 1) * disk_height
                y_bottom = 335 - i * disk_height
                color = colors[disk % len(colors)]

                # Draw clean 2D disk
                self.canvas.create_rectangle(x - width//2, y_top, x + width//2, y_bottom,
                                           fill=color, outline="#ffffff", width=3)

                # Simple border highlight
                self.canvas.create_rectangle(x - width//2 + 2, y_top + 2, x + width//2 - 2, y_bottom - 2,
                                           outline=self.lighten_color(color, 0.3), width=1)

                # Disk number
                disk_number = disk + 1
                self.canvas.create_text(x, (y_top + y_bottom)/2, text=str(disk_number),
                                      font=("Helvetica", 12, "bold"), fill="#000000")

    def lighten_color(self, color, factor):
        """Lighten a hex color by factor (0-1)"""
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return f"#{r:02x}{g:02x}{b:02x}"

    def darken_color(self, color, factor):
        """Darken a hex color by factor (0-1)"""
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        r = max(0, int(r * (1 - factor)))
        g = max(0, int(g * (1 - factor)))
        b = max(0, int(b * (1 - factor)))
        return f"#{r:02x}{g:02x}{b:02x}"

    def on_canvas_click(self, event):
        if not self.game.pegs or self.auto_solving:
            return

        peg_positions = [150, 350, 550]
        clicked_peg = None

        # Check if clicked on a peg area
        for i, x in enumerate(peg_positions):
            if abs(event.x - x) < 60:  # Wider click area
                clicked_peg = i
                break

        if clicked_peg is None:
            return

        if self.selected_peg is None:
            # Select top disk from clicked peg
            if self.game.pegs[clicked_peg]:
                self.selected_peg = clicked_peg
                self.selected_disk = self.game.pegs[clicked_peg][-1]
                self.draw_disks()  # Redraw to show selection
                self.instruction_label.configure(text="Now click on the destination tower!")
                # Highlight selected disk
                self.highlight_selected_disk(clicked_peg)
        else:
            # Try to move to clicked peg
            if self.game.move_disk(self.selected_peg, clicked_peg):
                self.move_counter += 1
                self.update_move_counter()
                self.draw_disks()
                if self.game.is_solved():
                    self.show_win_message()
                else:
                    self.instruction_label.configure(text="Great move! Select another disk to continue.")
            else:
                self.instruction_label.configure(text="Invalid move! Try a different tower.")
                # Flash invalid move feedback
                self.flash_invalid_move(clicked_peg)

            self.selected_peg = None
            self.selected_disk = None

    def highlight_selected_disk(self, peg_idx):
        peg_positions = [150, 350, 550]
        x = peg_positions[peg_idx]
        peg = self.game.pegs[peg_idx]
        if not peg:
            return

        disk = peg[-1]
        width = 40 + disk * 20  # Match the width calculation from draw_disks
        disk_height = 28  # Match the disk_height from draw_disks
        i = len(peg) - 1
        y_top = 335 - (i + 1) * disk_height
        y_bottom = 335 - i * disk_height

        # Draw glowing border around selected disk - exact same size as the disc
        self.canvas.create_rectangle(x - width//2, y_top, x + width//2, y_bottom,
                                   outline="#00ff88", width=3, fill="")

    def flash_invalid_move(self, peg_idx):
        peg_positions = [150, 350, 550]
        x = peg_positions[peg_idx]

        # Flash red border around invalid destination
        flash_rect = self.canvas.create_rectangle(x - 30, 50, x + 30, 360, outline="#ff4444", width=3, fill="")
        self.root.after(300, lambda: self.canvas.delete(flash_rect))

    def auto_solve(self):
        if self.auto_solving or not self.game.pegs:
            return

        self.auto_solving = True
        self.solve_button.configure(state="disabled", text="🤖 Solving...")
        self.instruction_label.configure(text="Watch the automatic solution!")

        # Get moves to solve from current state
        moves = self.solver.get_remaining_moves()

        if not moves:
            # Already solved
            self.auto_solving = False
            self.solve_button.configure(state="normal", text="🤖 Auto Solve")
            self.instruction_label.configure(text="Puzzle is already solved!")
            return

        self.execute_moves(moves, 0)

    def execute_moves(self, moves, index):
        if index >= len(moves):
            # Solution complete
            self.auto_solving = False
            self.solve_button.configure(state="normal", text="🤖 Auto Solve")
            if self.game.is_solved():
                self.show_win_message()
            else:
                self.instruction_label.configure(text="Solution complete! Try solving manually next time.")
            return

        from_peg, to_peg = moves[index]
        if self.game.move_disk(from_peg, to_peg):
            self.move_counter += 1
            self.update_move_counter()
            self.draw_disks()  # Instant redraw instead of animation

        # Schedule next move after longer delay for slower animation
        self.root.after(800, lambda: self.execute_moves(moves, index + 1))



    def show_win_message(self):
        self.timer_running = False
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60

        min_moves = (2 ** len(self.game.pegs[2])) - 1
        efficiency = "⭐ Perfect!" if self.move_counter == min_moves else "👍 Good job!"

        message = f"🎉 Congratulations!\n\nTime: {minutes:02d}:{seconds:02d}\nMoves: {self.move_counter}\nMinimum: {min_moves}\n\n{efficiency}"

        # Create celebration popup
        win_window = ctk.CTkToplevel(self.root)
        win_window.title("Puzzle Solved!")
        win_window.geometry("350x250")
        win_window.resizable(False, False)

        # Center the window on screen
        win_window.transient(self.root)
        win_window.grab_set()

        # Calculate center position
        win_window.update_idletasks()
        width = win_window.winfo_width()
        height = win_window.winfo_height()
        x = (win_window.winfo_screenwidth() // 2) - (width // 2)
        y = (win_window.winfo_screenheight() // 2) - (height // 2)
        win_window.geometry(f"{width}x{height}+{x}+{y}")

        frame = ctk.CTkFrame(win_window, fg_color="#2d2d2d", corner_radius=15)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(frame, text="🎉 PUZZLE SOLVED! 🎉",
                                 font=("Helvetica", 20, "bold"), text_color="#00ff88")
        title_label.pack(pady=(20, 10))

        stats_label = ctk.CTkLabel(frame, text=message, font=("Helvetica", 12), text_color="#ffffff")
        stats_label.pack(pady=10)

        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=(10, 20))

        play_again_btn = ctk.CTkButton(button_frame, text="🎮 Play Again", command=lambda: [win_window.destroy(), self.start_game()],
                                     font=("Helvetica", 12, "bold"), fg_color="#00ff88", hover_color="#00cc66")
        play_again_btn.pack(side="left", padx=5)

        close_btn = ctk.CTkButton(button_frame, text="🏠 Home", command=lambda: [win_window.destroy(), self.go_home()],
                                font=("Helvetica", 12, "bold"), fg_color="#666666", hover_color="#888888")
        close_btn.pack(side="right", padx=5)


class HomeScreen:
    def __init__(self, root, on_start_game):
        self.root = root
        self.on_start_game = on_start_game
        self.selected_disks = 3

        # Modern UI Setup
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Main container
        self.main_frame = ctk.CTkFrame(root, fg_color="#0a0a0a")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title section
        self.title_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a", corner_radius=20)
        self.title_frame.pack(fill="x", padx=30, pady=(30, 20))

        self.title_label = ctk.CTkLabel(self.title_frame, text="🗼 Tower of Hanoi",
                                      font=("Helvetica", 36, "bold"), text_color="#00ff88")
        self.title_label.pack(pady=(25, 10))

        self.subtitle_label = ctk.CTkLabel(self.title_frame, text="Classic Puzzle Game",
                                         font=("Helvetica", 16), text_color="#cccccc")
        self.subtitle_label.pack(pady=(0, 25))

        # Game setup section
        self.setup_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a", corner_radius=20)
        self.setup_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Difficulty selection
        self.difficulty_label = ctk.CTkLabel(self.setup_frame, text="Select Difficulty and Number of Disks",
                                           font=("Helvetica", 20, "bold"), text_color="#ffffff")
        self.difficulty_label.pack(pady=(30, 20))

        # Disk count buttons
        self.button_frame = ctk.CTkFrame(self.setup_frame, fg_color="transparent")
        self.button_frame.pack(pady=20)

        self.disk_buttons = []
        difficulties = [
            ("3", "Easy", "#4CAF50"),
            ("4", "Medium", "#FF9800"),
            ("5", "Hard", "#FF5722"),
            ("6", "Expert", "#9C27B0"),
            ("7", "Master", "#607D8B"),
            ("8", "Legend", "#E91E63")
        ]

        for i, (num, diff, color) in enumerate(difficulties):
            btn = ctk.CTkButton(self.button_frame, text=f"{num}\n{diff}",
                              command=lambda n=int(num): self.select_disks(n),
                              font=("Helvetica", 12, "bold"), fg_color=color,
                              hover_color=self.darken_color(color, 0.2),
                              width=80, height=60)
            btn.grid(row=0, column=i, padx=5, pady=5)
            self.disk_buttons.append(btn)

        self.selected_disks = 3
        self.update_button_selection()

        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.setup_frame, fg_color="transparent")
        self.buttons_frame.pack(pady=(20, 30))

        # Help button
        self.help_button = ctk.CTkButton(self.buttons_frame, text="❓ How to Play",
                                       command=self.show_help, font=("Helvetica", 14, "bold"),
                                       fg_color="#2196F3", hover_color="#1976D2", width=150, height=45)
        self.help_button.pack(side="left", padx=(0, 20))

        # Start button
        self.start_button = ctk.CTkButton(self.buttons_frame, text="🎮 Start Game",
                                        command=self.start_game, font=("Helvetica", 14, "bold"),
                                        fg_color="#00ff88", hover_color="#00cc66", width=150, height=45)
        self.start_button.pack(side="left")

        # Instructions
        self.instruction_label = ctk.CTkLabel(self.main_frame,
                                           text="Move all discs to the right tower!\nRules: Move one disc at a time, never place a larger disc on a smaller one.",
                                           font=("Helvetica", 12), text_color="#888888")
        self.instruction_label.pack(pady=(0, 20))

    def darken_color(self, color, factor):
        """Darken a hex color by factor (0-1)"""
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        r = max(0, int(r * (1 - factor)))
        g = max(0, int(g * (1 - factor)))
        b = max(0, int(b * (1 - factor)))
        return f"#{r:02x}{g:02x}{b:02x}"

    def select_disks(self, num_disks):
        self.selected_disks = num_disks
        self.update_button_selection()

    def update_button_selection(self):
        difficulties = ["#4CAF50", "#FF9800", "#FF5722", "#9C27B0", "#607D8B", "#E91E63"]
        for i, btn in enumerate(self.disk_buttons):
            if i + 3 == self.selected_disks:
                btn.configure(fg_color=difficulties[i])
            else:
                btn.configure(fg_color=self.darken_color(difficulties[i], 0.5))

    def show_help(self):
        help_window = ctk.CTkToplevel(self.root)
        help_window.title("How to Play - Tower of Hanoi")
        help_window.geometry("600x500")
        help_window.resizable(False, False)

        # Center the window
        help_window.transient(self.root)
        help_window.grab_set()

        frame = ctk.CTkFrame(help_window, fg_color="#1a1a1a", corner_radius=15)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(frame, text="🗼 How to Play Tower of Hanoi",
                                 font=("Helvetica", 20, "bold"), text_color="#00ff88")
        title_label.pack(pady=(20, 15))

        help_text = """
🎯 OBJECTIVE:
Move all discs from the left tower to the right tower.

📏 RULES:
• Move only one disc at a time
• A larger disc cannot be placed on top of a smaller disc
• You can only move the top disc from any tower

🎮 CONTROLS:
• Click on a disc to select it
• Click on a destination tower to move the selected disc
• Use "Auto Solve" to see the optimal solution

💡 STRATEGY:
The minimum number of moves is 2^n - 1, where n is the number of discs.
The solution follows a recursive pattern.

🎯 SCORING:
Try to solve it in the minimum number of moves!
        """

        help_label = ctk.CTkLabel(frame, text=help_text, font=("Helvetica", 12),
                                text_color="#ffffff", justify="left")
        help_label.pack(pady=20, padx=20)

        close_btn = ctk.CTkButton(frame, text="Got it!", command=help_window.destroy,
                                font=("Helvetica", 14, "bold"), fg_color="#00ff88",
                                hover_color="#00cc66", width=120, height=40)
        close_btn.pack(pady=(10, 20))

    def start_game(self):
        self.main_frame.destroy()
        self.on_start_game(self.selected_disks)
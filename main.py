import customtkinter as ctk
from ui import HanoiUI, HomeScreen

class GameApp:
    def __init__(self, root):
        self.root = root
        self.current_screen = None
        self.show_home_screen()

    def show_home_screen(self):
        if self.current_screen:
            self.current_screen.main_frame.destroy()
        self.current_screen = HomeScreen(self.root, self.start_game)

    def start_game(self, num_disks):
        if self.current_screen:
            self.current_screen.main_frame.destroy()
        self.current_screen = HanoiUI(self.root, num_disks, self.show_home_screen)

if __name__ == "__main__":
    # Modern app setup
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.title("🗼 Tower of Hanoi - Puzzle Game")
    app.geometry("900x700")
    app.resizable(True, True)

    # Center the window on screen
    app.update_idletasks()
    width = app.winfo_width()
    height = app.winfo_height()
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    app.geometry(f"{width}x{height}+{x}+{y}")

    game_app = GameApp(app)
    app.mainloop()
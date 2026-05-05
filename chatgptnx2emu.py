# mewinx2_tkinter.py
# Clean-room emulator-style GUI shell
# No leaks, no keys, no proprietary boot code.

import math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

APP_TITLE = "mewnx2 0.1 - Ryujinx Style Tkinter GUI"

BLUE = "#2f8cff"
BLUE2 = "#66b3ff"
BG = "#101014"
PANEL = "#17171d"
PANEL2 = "#20202a"
TEXT = "#e8e8f0"
MUTED = "#a0a0aa"
BLACK = "#000000"


class MewNX2Core:
    def __init__(self):
        self.running = False
        self.loaded_file = None
        self.fps = 60
        self.frame = 0
        self.compat = "Unknown"
        self.mode = "Clean-room Homebrew"

    def load(self, path):
        self.loaded_file = path
        self.compat = "Homebrew/Test"
        self.frame = 0

    def start(self):
        self.running = True

    def pause(self):
        self.running = False

    def stop(self):
        self.running = False
        self.frame = 0

    def reset(self):
        self.frame = 0

    def tick(self):
        if self.running:
            self.frame += 1


class MewNX2App:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1180x720")
        self.root.minsize(980, 600)
        self.root.configure(bg=BG)

        self.core = MewNX2Core()
        self.game_rows = []

        self.setup_style()
        self.make_menu()
        self.make_ui()
        self.loop()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=PANEL,
            foreground=TEXT,
            fieldbackground=PANEL,
            rowheight=30,
            borderwidth=0,
        )
        style.map("Treeview", background=[("selected", BLUE)])

        style.configure(
            "Treeview.Heading",
            background=PANEL2,
            foreground=BLUE2,
            font=("Segoe UI", 10, "bold"),
        )

    def make_menu(self):
        menubar = tk.Menu(self.root, bg=PANEL, fg=TEXT, activebackground=BLUE)

        file_menu = tk.Menu(menubar, tearoff=0, bg=PANEL, fg=TEXT)
        file_menu.add_command(label="Open Homebrew/Test File...", command=self.open_file)
        file_menu.add_command(label="Open Folder...", command=self.open_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        emu_menu = tk.Menu(menubar, tearoff=0, bg=PANEL, fg=TEXT)
        emu_menu.add_command(label="Start", command=self.start)
        emu_menu.add_command(label="Pause", command=self.pause)
        emu_menu.add_command(label="Stop", command=self.stop)
        emu_menu.add_command(label="Reset", command=self.reset)

        tools_menu = tk.Menu(menubar, tearoff=0, bg=PANEL, fg=TEXT)
        tools_menu.add_command(label="Romhacking Notes", command=self.romhacking_notes)
        tools_menu.add_command(label="Hex Viewer Placeholder", command=self.hex_viewer)

        help_menu = tk.Menu(menubar, tearoff=0, bg=PANEL, fg=TEXT)
        help_menu.add_command(label="About", command=self.about)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Emulation", menu=emu_menu)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def blue_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=BLACK,
            fg=BLUE,
            activebackground="#050505",
            activeforeground=BLUE2,
            relief="flat",
            padx=14,
            pady=8,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )

    def make_ui(self):
        self.sidebar = tk.Frame(self.root, bg=PANEL, width=240)
        self.sidebar.pack(side="left", fill="y")

        logo = tk.Label(
            self.sidebar,
            text="mewnx2",
            bg=PANEL,
            fg=BLUE,
            font=("Segoe UI", 26, "bold"),
        )
        logo.pack(pady=(24, 4))

        sub = tk.Label(
            self.sidebar,
            text="clean-room emulator shell",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 9),
        )
        sub.pack(pady=(0, 20))

        for txt, cmd in [
            ("Open File", self.open_file),
            ("Open Folder", self.open_folder),
            ("Start", self.start),
            ("Pause", self.pause),
            ("Stop", self.stop),
            ("Reset", self.reset),
            ("Hex Viewer", self.hex_viewer),
        ]:
            self.blue_button(self.sidebar, txt, cmd).pack(fill="x", padx=18, pady=5)

        self.status_box = tk.Label(
            self.sidebar,
            text="Status: Idle\nFPS: 60\nCore: mewnx2\nTheme: Blue",
            bg="#0d0d12",
            fg=TEXT,
            justify="left",
            anchor="nw",
            font=("Consolas", 10),
            padx=10,
            pady=10,
        )
        self.status_box.pack(fill="x", padx=18, pady=22)

        main = tk.Frame(self.root, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        topbar = tk.Frame(main, bg=PANEL2, height=56)
        topbar.pack(fill="x")

        title = tk.Label(
            topbar,
            text="Game List",
            bg=PANEL2,
            fg=TEXT,
            font=("Segoe UI", 16, "bold"),
        )
        title.pack(side="left", padx=18)

        self.search = tk.Entry(
            topbar,
            bg="#0d0d12",
            fg=BLUE2,
            insertbackground=BLUE2,
            relief="flat",
            font=("Segoe UI", 11),
        )
        self.search.insert(0, " Search...")
        self.search.pack(side="right", padx=18, ipady=8, ipadx=10)

        content = tk.Frame(main, bg=BG)
        content.pack(fill="both", expand=True, padx=14, pady=14)

        left_content = tk.Frame(content, bg=BG)
        left_content.pack(side="left", fill="both", expand=True)

        columns = ("title", "type", "compat", "path")
        self.tree = ttk.Treeview(left_content, columns=columns, show="headings")
        self.tree.heading("title", text="Title")
        self.tree.heading("type", text="Type")
        self.tree.heading("compat", text="Compatibility")
        self.tree.heading("path", text="Path")

        self.tree.column("title", width=220)
        self.tree.column("type", width=120)
        self.tree.column("compat", width=140)
        self.tree.column("path", width=360)

        self.tree.pack(fill="both", expand=True)

        self.add_demo_rows()

        right_panel = tk.Frame(content, bg=PANEL, width=330)
        right_panel.pack(side="right", fill="y", padx=(14, 0))
        right_panel.pack_propagate(False)

        tk.Label(
            right_panel,
            text="Render Preview",
            bg=PANEL,
            fg=BLUE2,
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(14, 8))

        self.canvas = tk.Canvas(
            right_panel,
            bg="#050507",
            highlightthickness=2,
            highlightbackground=BLUE,
            width=290,
            height=210,
        )
        self.canvas.pack(padx=14, pady=8)

        self.info = tk.Label(
            right_panel,
            text="No file loaded.\n\nThis is a GUI shell for homebrew/test research.",
            bg=PANEL,
            fg=TEXT,
            justify="left",
            anchor="nw",
            font=("Segoe UI", 10),
            wraplength=280,
        )
        self.info.pack(fill="both", expand=True, padx=16, pady=12)

        bottom = tk.Frame(main, bg=PANEL2, height=30)
        bottom.pack(fill="x")

        self.bottom = tk.Label(
            bottom,
            text="Ready.",
            bg=PANEL2,
            fg=BLUE2,
            anchor="w",
            font=("Consolas", 10),
        )
        self.bottom.pack(fill="x", padx=12)

    def add_demo_rows(self):
        demos = [
            ("Homebrew Test App", "ELF/NRO", "Great", "demo/homebrew_test.elf"),
            ("Blue Screen Pattern", "Test ROM", "Great", "tests/blue_pattern.bin"),
            ("Input Tester", "Homebrew", "Okay", "tests/input_tester.nro"),
        ]
        for row in demos:
            self.tree.insert("", "end", values=row)

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Open Homebrew/Test File",
            filetypes=[
                ("Homebrew/Test Files", "*.elf *.nro *.nso *.bin"),
                ("All Files", "*.*"),
            ],
        )
        if not path:
            return

        name = path.split("/")[-1]
        self.core.load(path)

        self.tree.insert("", "end", values=(name, "Loaded File", "Homebrew/Test", path))
        self.bottom.config(text=f"Loaded: {path}")
        self.info.config(
            text=f"Loaded:\n{name}\n\nMode:\n{self.core.mode}\n\nCompatibility:\n{self.core.compat}"
        )

    def open_folder(self):
        folder = filedialog.askdirectory(title="Open Folder")
        if folder:
            self.bottom.config(text=f"Folder selected: {folder}")

    def start(self):
        self.core.start()
        self.bottom.config(text="Started emulation shell.")

    def pause(self):
        self.core.pause()
        self.bottom.config(text="Paused.")

    def stop(self):
        self.core.stop()
        self.bottom.config(text="Stopped.")

    def reset(self):
        self.core.reset()
        self.bottom.config(text="Reset frame counter.")

    def romhacking_notes(self):
        messagebox.showinfo(
            "Romhacking Notes",
            "mewnx2 romhacking vibes:\n\n"
            "- clean-room notes\n"
            "- homebrew tests\n"
            "- symbol maps\n"
            "- patch logs\n"
            "- hex viewer tools\n"
            "- no leaks / no keys",
        )

    def hex_viewer(self):
        win = tk.Toplevel(self.root)
        win.title("mewnx2 Hex Viewer Placeholder")
        win.geometry("700x420")
        win.configure(bg=BG)

        txt = tk.Text(
            win,
            bg="#050507",
            fg=BLUE2,
            insertbackground=BLUE2,
            font=("Consolas", 11),
        )
        txt.pack(fill="both", expand=True, padx=12, pady=12)

        fake = []
        for addr in range(0, 256, 16):
            row = " ".join(f"{(addr + i) & 255:02X}" for i in range(16))
            fake.append(f"{addr:08X}: {row}")

        txt.insert("1.0", "\n".join(fake))

    def about(self):
        messagebox.showinfo(
            "About",
            "mewnx2 0.1\n"
            "Ryujinx-inspired Tkinter GUI\n"
            "Blue theme kept\n"
            "Clean-room homebrew/test shell",
        )

    def draw_preview(self):
        self.canvas.delete("all")
        w = int(self.canvas["width"])
        h = int(self.canvas["height"])

        t = self.core.frame / 20
        x = w // 2 + int(math.sin(t) * 45)

        self.canvas.create_rectangle(0, 0, w, h, fill="#050507", outline="")
        self.canvas.create_text(
            w // 2,
            38,
            text="mewnx2",
            fill=BLUE,
            font=("Segoe UI", 28, "bold"),
        )
        self.canvas.create_oval(x - 18, 105 - 18, x + 18, 105 + 18, fill=BLUE, outline=BLUE2)
        self.canvas.create_text(
            w // 2,
            170,
            text="RUNNING" if self.core.running else "IDLE",
            fill=BLUE2,
            font=("Consolas", 12, "bold"),
        )

    def loop(self):
        self.core.tick()
        self.draw_preview()

        self.status_box.config(
            text=(
                f"Status: {'Running' if self.core.running else 'Idle'}\n"
                f"FPS: {self.core.fps}\n"
                f"Frame: {self.core.frame}\n"
                f"Core: mewnx2\n"
                f"Theme: Blue"
            )
        )

        self.root.after(16, self.loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = MewNX2App(root)
    root.mainloop()

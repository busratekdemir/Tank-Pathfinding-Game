import tkinter as tk
import collections
from PIL import Image, ImageTk

# --- Global Değişkenler ---
grid_data = []
grid_widgets = []
tank_images = { "up": None, "down": None, "left": None, "right": None }
pixel_img = None

# --- Ayarlar ---
CELL_PIXELS = 25
ANIMATION_SPEED_MS = 150

# --- Renkler (YENİ: Koyu Tema Renkleri) ---
COLOR_BACKGROUND = "#2E2E2E" # Koyu Gri (Arka Plan)
COLOR_TEXT = "#EAEAEA"       # Açık Gri (Yazılar)
COLOR_BUTTON = "#4A4A4A"      # Koyu Buton
COLOR_GRID_BG = "#3E3E3E"   # Izgara Arka Planı

COLOR_PATH = "white"
COLOR_WALL = "grey"
COLOR_BORDER = "black"
COLOR_START = "green"
COLOR_END = "red"
COLOR_VISITED = "#D4E6F1"


def load_tank_images():
    global tank_images
    try:
        original_image = Image.open("tank_original.gif")
        new_size = int(CELL_PIXELS * 0.8)
        if new_size < 1: new_size = 1
        original_image = original_image.resize((new_size, new_size), Image.Resampling.LANCZOS)
        img_up = original_image
        img_down = original_image.rotate(180)
        img_left = original_image.rotate(90)
        img_right = original_image.rotate(-90)
        tank_images["up"] = ImageTk.PhotoImage(img_up)
        tank_images["down"] = ImageTk.PhotoImage(img_down)
        tank_images["left"] = ImageTk.PhotoImage(img_left)
        tank_images["right"] = ImageTk.PhotoImage(img_right)
        print(f"Tank images loaded. Size: {new_size}x{new_size} pixels.")
    except Exception as e:
        print(f"Error loading 'tank_original.gif': {e}")


def toggle_wall(event, row, col):
    if (row == 0 and col == 0) or (row == len(grid_data) - 1 and col == len(grid_data[0]) - 1):
        return
    current_state = grid_data[row][col]
    new_state, new_color = (1, COLOR_WALL) if current_state == 0 else (0, COLOR_PATH)
    grid_data[row][col] = new_state
    grid_widgets[row][col].config(bg=new_color)


def draw_grid():
    global grid_data, grid_widgets
    try:
        rows = int(entry_boy.get())
        cols = int(entry_en.get())
    except ValueError:
        print("Please enter valid numbers.")
        return

    for widget in grid_frame.winfo_children():
        widget.destroy()

    grid_data = []
    grid_widgets = []

    for r in range(rows):
        row_data_list = []
        row_widget_list = []
        for c in range(cols):
            row_data_list.append(0)
            cell = tk.Label(grid_frame,
                            image=pixel_img,
                            compound='center',
                            bg=COLOR_PATH,
                            width=CELL_PIXELS,
                            height=CELL_PIXELS,
                            relief="sunken",
                            borderwidth=1)
            cell.grid(row=r, column=c)
            cell.bind("<Button-1>", lambda event, r=r, c=c: toggle_wall(event, r, c))
            row_widget_list.append(cell)
        grid_data.append(row_data_list)
        grid_widgets.append(row_widget_list)

    grid_widgets[0][0].config(bg=COLOR_START)
    grid_widgets[rows - 1][cols - 1].config(bg=COLOR_END)
    btn_start.config(state="normal")
    btn_draw.config(state="normal")


def find_path_bfs(start_pos, end_pos):
    rows, cols = len(grid_data), len(grid_data[0])
    queue = collections.deque([(start_pos, [start_pos])])
    visited = set([start_pos])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while queue:
        (current_pos, path) = queue.popleft()
        if current_pos == end_pos: return path
        r, c = current_pos
        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            new_pos = (new_r, new_c)
            if 0 <= new_r < rows and 0 <= new_c < cols and \
                    new_pos not in visited and grid_data[new_r][new_c] == 0:
                visited.add(new_pos)
                new_path = list(path)
                new_path.append(new_pos)
                queue.append((new_pos, new_path))
    return None


def start_navigation():
    if not tank_images["up"]:
        print("Tank images not loaded. Cannot start.")
        return
    btn_start.config(state="disabled")
    btn_draw.config(state="disabled")
    rows, cols = len(grid_data), len(grid_data[0])
    start_pos = (0, 0)
    end_pos = (rows - 1, cols - 1)
    for r in range(rows):
        for c in range(cols):
            widget = grid_widgets[r][c]
            widget.config(image=pixel_img)
            if grid_data[r][c] == 0:
                color = COLOR_PATH
                if (r, c) == start_pos: color = COLOR_START
                if (r, c) == end_pos: color = COLOR_END
                widget.config(bg=color)
    window.after(50, lambda: begin_pathfinding(start_pos, end_pos))


def begin_pathfinding(start_pos, end_pos):
    path = find_path_bfs(start_pos, end_pos)
    if path:
        print(f"Path found: {len(path)} steps.")
        animate_tank(path, prev_pos=None, last_direction="up")
    else:
        print("Path not found.")
        btn_start.config(state="normal")
        btn_draw.config(state="normal")


def get_direction(prev_pos, current_pos):
    if not prev_pos: return "up"
    prev_r, prev_c = prev_pos
    curr_r, curr_c = current_pos
    if curr_r < prev_r: return "up"
    if curr_r > prev_r: return "down"
    if curr_c < prev_c: return "left"
    if curr_c > prev_c: return "right"
    return "up"


def animate_tank(path, prev_pos, last_direction):
    if prev_pos:
        r_prev, c_prev = prev_pos
        widget = grid_widgets[r_prev][c_prev]
        widget.config(image=pixel_img, bg=COLOR_VISITED)
        if prev_pos == (0, 0):
            widget.config(bg=COLOR_START)
    if not path:
        print("Animation finished.")
        if prev_pos:
            r_last, c_last = prev_pos
            grid_widgets[r_last][c_last].config(image=tank_images[last_direction], bg=COLOR_END)
        btn_start.config(state="normal")
        btn_draw.config(state="normal")
        return
    current_pos = path.pop(0)
    direction = get_direction(prev_pos, current_pos)
    r_curr, c_curr = current_pos
    grid_widgets[r_curr][c_curr].config(image=tank_images[direction])
    window.after(ANIMATION_SPEED_MS,
                 lambda: animate_tank(path, prev_pos=current_pos, last_direction=direction))


# --- Arayüz Kurulumu ---
window = tk.Tk()
window.title("Tank (Dark Mode)")
window.resizable(False, False)
window.config(bg=COLOR_BACKGROUND) # Ana pencere arka planı

pixel_img = tk.PhotoImage(width=1, height=1)

load_tank_images()

# Kontrol paneli
control_frame = tk.Frame(window, bg=COLOR_BACKGROUND) # Arka planı ayarla
control_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

#Label
tk.Label(control_frame, text="Height (Rows):", bg=COLOR_BACKGROUND, fg=COLOR_TEXT).pack(pady=(0, 2))
entry_boy = tk.Entry(control_frame, width=10)
entry_boy.insert(0, "10")
entry_boy.pack(pady=(0, 10))

tk.Label(control_frame, text="Width (Cols):", bg=COLOR_BACKGROUND, fg=COLOR_TEXT).pack(pady=(0, 2))
entry_en = tk.Entry(control_frame, width=10)
entry_en.insert(0, "10")
entry_en.pack(pady=(0, 10))

# Butonlar
btn_draw = tk.Button(control_frame, text="Draw", command=draw_grid,
                     bg=COLOR_BUTTON, fg=COLOR_TEXT, relief="flat")
btn_draw.pack(fill=tk.X, pady=5)

btn_start = tk.Button(control_frame, text="Start", command=start_navigation, state="disabled",
                      bg=COLOR_BUTTON, fg=COLOR_TEXT, relief="flat")
btn_start.pack(fill=tk.X, pady=5)

btn_exit = tk.Button(control_frame, text="Exit", command=window.quit,
                     bg=COLOR_BUTTON, fg=COLOR_TEXT, relief="flat")
btn_exit.pack(fill=tk.X, side=tk.BOTTOM, pady=5)

# Izgara alanı
grid_frame = tk.Frame(window, bg=COLOR_GRID_BG) # Arka planı ayarla
grid_frame.pack(side=tk.LEFT, padx=10, pady=10)

draw_grid()
window.mainloop()
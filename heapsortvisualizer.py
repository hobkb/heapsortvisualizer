import tkinter as tk
from tkinter import messagebox
import numpy as np
import time
import math


root = tk.Tk()
root.title("Heap Sort Visualizer")
root.geometry("1920x1080")
root.configure(bg="#2b2b2b") 

canvas = tk.Canvas(root, height=300, width=900, bg="#1e1e1e", highlightthickness=0)
canvas.pack(pady=10)
heap_canvas = tk.Canvas(root, height=400, width=900, bg="#1e1e1e", highlightthickness=0)
heap_canvas.pack(pady=10)

bar_width = 50
spacing = 10
bars = []
nodes = []
numbers = []  
is_busy = False

#DRAW ARRAY AS BARS
def draw_bars(arr):
    canvas.delete("all")
    global bars
    bars = []
    for i, num in enumerate(arr):
        x1 = i * (bar_width + spacing) + 20
        y1 = 250
        x2 = x1 + bar_width
        y2 = y1 - 100

        rect = canvas.create_rectangle(x1, y1, x2, y2, fill="#4aa3f0", outline="")
        txt = canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2,
                                 text=str(num), font=("Arial", 12), fill="white")
        bars.append((rect, txt))

#DRAW HEAP TREE 
def draw_heap(arr):
    heap_canvas.delete("all")
    global nodes
    nodes = []
    n = len(arr)
    if n == 0:
        return

    level_gap = 80
    node_radius = 25

    for i, val in enumerate(arr):
        level = int(math.floor(math.log2(i + 1)))
        max_nodes = 2 ** level
        pos_in_level = i - (2 ** level - 1)

        x = (pos_in_level + 1) * (900 // (max_nodes + 1))
        y = level * level_gap + 50

        if i != 0:
            parent = (i - 1) // 2
            parent_level = int(math.floor(math.log2(parent + 1)))
            parent_max_nodes = 2 ** parent_level
            parent_pos = parent - (2 ** parent_level - 1)
            px = (parent_pos + 1) * (900 // (parent_max_nodes + 1))
            py = parent_level * level_gap + 50
            heap_canvas.create_line(px, py + node_radius, x, y - node_radius, fill="white")

        circle = heap_canvas.create_oval(x - node_radius, y - node_radius,
                                         x + node_radius, y + node_radius,
                                         fill="#6bd26b", outline="")
        txt = heap_canvas.create_text(x, y, text=str(val), font=("Arial", 12), fill="black")
        nodes.append((circle, txt))
 
def draw_all(arr):
    draw_bars(arr)
    draw_heap(arr)


def highlight(index, color="#f54242"):
    if index < len(bars):
        rect, _ = bars[index]
        canvas.itemconfig(rect, fill=color)
    if index < len(nodes):
        circle, _ = nodes[index]
        heap_canvas.itemconfig(circle, fill=color)
    root.update()

def unhighlight(index):
    if index < len(bars):
        rect, _ = bars[index]
        canvas.itemconfig(rect, fill="#4aa3f0")
    if index < len(nodes):
        circle, _ = nodes[index]
        heap_canvas.itemconfig(circle, fill="#6bd26b")
    root.update()

#ANIMATION
def swap_bars(i, j, speed=0.07):
    rect1, txt1 = bars[i]
    rect2, txt2 = bars[j]

    highlight(i)
    highlight(j)

    x1, _, _, _ = canvas.coords(rect1)
    x3, _, _, _ = canvas.coords(rect2)

    dx = (x3 - x1) / 20
    for _ in range(20):
        canvas.move(rect1, dx, 0)
        canvas.move(txt1, dx, 0)
        canvas.move(rect2, -dx, 0)
        canvas.move(txt2, -dx, 0)
        root.update()
        time.sleep(speed)

    bars[i], bars[j] = bars[j], bars[i]
    numbers[i], numbers[j] = numbers[j], numbers[i]

    draw_heap(numbers)

    unhighlight(i)
    unhighlight(j)

#HEAPIFY 
def heapify(n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and numbers[l] > numbers[largest]:
        largest = l
    if r < n and numbers[r] > numbers[largest]:
        largest = r

    if largest != i:
        swap_bars(i, largest, speed=0.07)
        heapify(n, largest)

#HEAP SORT
def heap_sort():
    global is_busy
    if is_busy:
        messagebox.showinfo("Busy", "Please wait for the current operation to finish.")
        return

    n = len(numbers)
    if n == 0:
        messagebox.showwarning("Empty Heap", "No elements to sort!")
        return

    is_busy = True
    disable_buttons()

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    for i in range(n - 1, 0, -1):
        swap_bars(0, i, speed=0.07)
        heapify(i, 0)
        
    is_busy = False
    enable_buttons()

#BUILD MAX HEAP ONLY
def build_heap():
    global is_busy
    if is_busy:
        messagebox.showinfo("Busy", "Please wait for the current operation to finish.")
        return

    n = len(numbers)
    if n == 0:
        messagebox.showwarning("Empty Heap", "Please insert elements first!")
        return

    is_busy = True
    disable_buttons()

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    
    is_busy = False
    enable_buttons()


def insert_value():
    global numbers
    try:
        val = int(entry_value.get())
        if len(numbers) >= 15:
            messagebox.showwarning("Limit Reached", "Max 15 elements allowed!")
            return
        numbers.append(val)
        draw_all(numbers)
        entry_value.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter an integer.")


def generate_random_array():
    global numbers
    numbers = np.random.randint(1, 100, 10).tolist()
    draw_all(numbers)


def reset_array():
    global numbers
    numbers = []
    draw_all(numbers)

def disable_buttons():
    btn_reset.config(state="disabled")
    btn_random.config(state="disabled")
    btn_insert.config(state="disabled")
    btn_build.config(state="disabled")
    btn_start.config(state="disabled")

def enable_buttons():
    btn_reset.config(state="normal")
    btn_random.config(state="normal")
    btn_insert.config(state="normal")
    btn_build.config(state="normal")
    btn_start.config(state="normal")


#CONTROL BUTTONS
frame = tk.Frame(root, bg="#2b2b2b")
frame.pack(pady=10)


btn_reset = tk.Button(frame, text="Reset", command=reset_array, bg="#444", fg="white")
btn_reset.pack(side="left", padx=5)

btn_random = tk.Button(frame, text="Generate Random", command=generate_random_array, bg="#555", fg="white")
btn_random.pack(side="left", padx=5)


lbl_insert = tk.Label(frame, text="Enter Number:", bg="#2b2b2b", fg="white")
lbl_insert.pack(side="left", padx=5)

entry_value = tk.Entry(frame, width=10)
entry_value.pack(side="left", padx=5)

btn_insert = tk.Button(frame, text="Insert", command=insert_value, bg="#6a5acd", fg="white")
btn_insert.pack(side="left", padx=5)

btn_build = tk.Button(frame, text="Build Heap", command=build_heap, bg="#ff8c00", fg="white")
btn_build.pack(side="left", padx=5)

btn_start = tk.Button(frame, text="Start Sort", command=heap_sort, bg="#008cba", fg="white")
btn_start.pack(side="left", padx=5)

#INITIAL DRAW 
draw_all(numbers)
root.mainloop()

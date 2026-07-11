import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os

FACULTY_DIR = "faculty_db"

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Smart Lecture Control System")
root.attributes("-fullscreen", True)
root.configure(bg="#0F172A")

root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

# ---------------- STYLES ----------------
style = ttk.Style()
style.theme_use("clam")

style.configure("Card.TFrame", background="#020617")

style.configure(
    "Title.TLabel",
    font=("Segoe UI", 28, "bold"),
    foreground="white",
    background="#020617"
)

style.configure(
    "SubTitle.TLabel",
    font=("Segoe UI", 12),
    foreground="#94A3B8",
    background="#020617"
)

style.configure(
    "TButton",
    font=("Segoe UI", 12),
    padding=15,
    background="#2563EB",
    foreground="white"
)

style.map("TButton", background=[("active", "#1D4ED8")])

# ---------------- FUNCTIONS ----------------
def add_faculty():
    subprocess.Popen([sys.executable, "add_faculty.py"])
    status_label.config(text="● Adding Faculty Photo", foreground="#38BDF8")


def start_system():
    subprocess.Popen([sys.executable, "secure_gesture_control_db.py"])
    status_label.config(text="● Lecture Control Running", foreground="#22C55E")


def remove_faculty():
    if not os.path.exists(FACULTY_DIR):
        messagebox.showerror("Error", "faculty_db folder not found")
        return

    win = tk.Toplevel(root)
    win.title("Remove Faculty")
    win.geometry("500x450")
    win.configure(bg="#020617")

    title = tk.Label(
        win, text="Remove Faculty",
        font=("Segoe UI", 18, "bold"),
        fg="white", bg="#020617"
    )
    title.pack(pady=10)

    listbox = tk.Listbox(
        win, font=("Segoe UI", 12),
        width=40, height=12
    )
    listbox.pack(pady=15)

    for file in os.listdir(FACULTY_DIR):
        if file.lower().endswith((".jpg", ".png")):
            listbox.insert(tk.END, file)

    def delete_selected():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No faculty selected")
            return

        filename = listbox.get(selection[0])
        path = os.path.join(FACULTY_DIR, filename)

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete {filename}?"
        )
        if confirm:
            os.remove(path)
            listbox.delete(selection[0])
            messagebox.showinfo("Deleted", "Faculty removed successfully")

    btn_delete = ttk.Button(
        win, text="🗑 Delete Selected Faculty",
        command=delete_selected
    )
    btn_delete.pack(pady=15)

# ---------------- CENTER CARD ----------------
card = ttk.Frame(root, style="Card.TFrame", padding=40)
card.place(relx=0.5, rely=0.5, anchor="center")

title = ttk.Label(card, text="Smart Lecture Control", style="Title.TLabel")
title.pack(pady=(0, 8))

subtitle = ttk.Label(
    card,
    text="Secure Gesture-Based Presentation System",
    style="SubTitle.TLabel"
)
subtitle.pack(pady=(0, 35))

ttk.Button(
    card, text="➕ Add Faculty Photo",
    width=30, command=add_faculty
).pack(pady=10)

ttk.Button(
    card, text="🗑 Remove Faculty Photo",
    width=30, command=remove_faculty
).pack(pady=10)

ttk.Button(
    card, text="▶ Start Lecture Control",
    width=32, command=start_system
).pack(pady=30)

status_label = tk.Label(
    card, text="● System Ready",
    font=("Segoe UI", 11, "bold"),
    fg="#38BDF8", bg="#020617"
)
status_label.pack(pady=10)

footer = tk.Label(
    root,
    text="© 2026 SmartLectureControl | Press ESC to exit fullscreen",
    font=("Segoe UI", 10),
    fg="#94A3B8", bg="#0F172A"
)
footer.pack(side="bottom", pady=15)

root.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import shutil
import os

# Paths
IMAGES_DIR = "images"

def select_input_folder():
    folder = filedialog.askdirectory(title="Select Images Folder")
    if folder:
        # Clear and copy selected images to /images folder
        if os.path.exists(IMAGES_DIR):
            shutil.rmtree(IMAGES_DIR)
        shutil.copytree(folder, IMAGES_DIR)
        log("✅ Folder selected. Ready to clean...")

def run_cleaner():
    if not os.path.exists(IMAGES_DIR) or not os.listdir(IMAGES_DIR):
        messagebox.showwarning("No Images", "Please select a folder with images first.")
        return

    log("🧹 Cleaning in progress...")
    try:
        result = subprocess.run(["python", "app.py"], capture_output=True, text=True)
        log(result.stdout)
        messagebox.showinfo("Done", "Cleaning complete!")
    except Exception as e:
        log(f"❌ Error: {e}")
        messagebox.showerror("Error", str(e))

def view_log():
    if not os.path.exists("log.csv"):
        messagebox.showwarning("Log Missing", "No log.csv found yet.")
        return

    with open("log.csv", "r") as file:
        content = file.read()

    log_window = tk.Toplevel(root)
    log_window.title("log.csv")
    txt = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, width=100, height=30)
    txt.insert(tk.END, content)
    txt.pack()

def log(message):
    output_box.config(state=tk.NORMAL)
    output_box.insert(tk.END, f"{message}\n")
    output_box.config(state=tk.DISABLED)
    output_box.yview(tk.END)

# GUI setup
root = tk.Tk()
root.title("📷 Photo Cleaner")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Label(frame, text="📂 Select input photo folder:").pack(anchor="w")
tk.Button(frame, text="Browse Folder", command=select_input_folder).pack(pady=(0, 10))

tk.Button(frame, text="Start Cleaning", bg="#4CAF50", fg="white", command=run_cleaner).pack(pady=5)
tk.Button(frame, text="View log.csv", command=view_log).pack(pady=(0, 10))

output_box = scrolledtext.ScrolledText(frame, height=15, width=70, state=tk.DISABLED)
output_box.pack()

root.mainloop()

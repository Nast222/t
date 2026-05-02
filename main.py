import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from password_generator import generate_password

HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def add_to_history(password):
    history = load_history()
    history.insert(0, password)  # Добавляем в начало списка
    if len(history) > 20:  # Ограничим историю 20 паролями
        history = history[:20]
    save_history(history)
    update_history_table()

def update_history_table():
    for i in tree.get_children():
        tree.delete(i)
    for pwd in load_history():
        tree.insert('', 'end', values=(pwd,))

def on_generate():
    try:
        length = int(scale_length.get())
        use_digits = var_digits.get()
        use_letters = var_letters.get()
        use_special = var_special.get()

        password = generate_password(length, use_digits, use_letters, use_special)
        entry_password.delete(0, tk.END)
        entry_password.insert(0, password)
        add_to_history(password)

    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

# --- Интерфейс ---
root = tk.Tk()
root.title("Генератор случайных паролей")
root.geometry("600x400")

# Длина пароля
tk.Label(root, text="Длина пароля:").pack(pady=5)
scale_length = tk.Scale(root, from_=4, to=128, orient=tk.HORIZONTAL, length=300)
scale_length.set(12)
scale_length.pack()

# Чекбоксы
frame_options = tk.Frame(root)
frame_options.pack(pady=10)
var_digits = tk.BooleanVar(value=True)
var_letters = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=True)
tk.Checkbutton(frame_options, text="Цифры", variable=var_digits).pack(side=tk.LEFT, padx=5)
tk.Checkbutton(frame_options, text="Буквы", variable=var_letters).pack(side=tk.LEFT, padx=5)
tk.Checkbutton(frame_options, text="Спецсимволы", variable=var_special).pack(side=tk.LEFT, padx=5)

# Кнопка и поле результата
frame_result = tk.Frame(root)
frame_result.pack(pady=10)
tk.Button(frame_result, text="Сгенерировать", command=on_generate).pack(side=tk.LEFT)
entry_password = tk.Entry(frame_result, width=50)
entry_password.pack(side=tk.LEFT, padx=5)

# Таблица истории
tree = ttk.Treeview(root, columns=("password",), show="headings")
tree.heading("password", text="История паролей")
tree.pack(fill=tk.BOTH, expand=True, pady=10)
update_history_table()

root.mainloop()

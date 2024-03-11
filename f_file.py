import json
import asyncio
import tkinter as tk
from tkinter import messagebox, filedialog
from word_csv import word_to_csv
def select_file(entry, login, root, kl):
    """Функція для вибору файлу."""
    filename = filedialog.askopenfilename(initialdir="/", title="Вибрати файл")
    if filename:
        if filename.endswith(".doc") or filename.endswith(".docx"):
            entry.delete(0, tk.END)
            entry.insert(0, filename)
            word_to_csv(filename, login, kl)
            file_paths = get_saved_file_paths(login)
            file_paths[kl] = filename
            save_file_paths(login, file_paths)
        else:
            messagebox.showwarning("Невірний формат файлу", "Оберіть файл у форматі docx або doc")


def load_file_paths(login):
    """Функція для завантаження шляхів файлів."""
    file_paths = {}
    try:
        with open(f'{login}.json', 'r') as f:
            file_paths = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return file_paths
def load_uroki_paths(login):
    """Функція для завантаження шляхів файлів."""
    file_paths = {}
    try:
        with open(f'{login}.json', 'r') as f:
            file_paths = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return file_paths

def get_saved_file_paths(login):
    """Функція для отримання збережених шляхів файлів."""
    file_paths = {}
    try:
        with open(f'{login}.json', 'r') as f:
            data = f.read()
            if data:
                file_paths = json.loads(data)
    except FileNotFoundError:
        pass
    return file_paths


def get_saved_file_path(login, key):
    """Функція для отримання збереженого шляху файлу."""
    file_paths = load_file_paths(login)
    return file_paths.get(key, '')


def save_file_paths(login, file_paths):
    """Функція для збереження шляхів файлів."""
    file_paths_file = f'{login}.json'
    with open(file_paths_file, 'w') as f:
        json.dump(file_paths, f)

def save_uroki_to_json(login,data):
    """Функція для збереження уроків та їх посилань."""
    with open(f'{login}_uroki.json', 'w') as f:
        json.dump(data, f)


def load_uroki_json(login):
    """Функція для зчитування уроків та їх посилань."""
    try:
        with open(f'{login}_uroki.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
def log_pas():
    try:
        with open('credentials.json', 'r') as f:
            credentials = json.load(f)
            login=(credentials.get('login', ''))
            password=(credentials.get('password', ''))
        return login, password
    except FileNotFoundError:
        pass

# print(load_uroki_json(log_pas()[0]))
import tkinter as tk
from tkinter import messagebox
import asyncio
from datetime import datetime
from func import main, main_zap, del_zap
from f_file import load_uroki_json, get_user, get_saved_file_path, log_pas, save_uroki_to_json, select_file

# URL журналу
JURNAL = 'https://nz.ua/journal/list'

async def run_main(login, password, jurnal):
    """
    Функція для виконання основної програми.

    Args:
        login (str): Логін користувача.
        password (str): Пароль користувача.
        jurnal (str): URL журналу.

    Returns:
        Результат виконання основної програми або None у разі невдачі.
    """
    return await main(login, password, jurnal)

def run_asyncio_loop(login, password, jurnal):
    """
    Функція для запуску асинхронного циклу.

    Args:
        login (str): Логін користувача.
        password (str): Пароль користувача.
        jurnal (str): URL журналу.

    Returns:
        Результат виконання асинхронного циклу.
    """
    return asyncio.run(run_main(login, password, jurnal))

def run_program(root, login, password):
    """
    Функція для виконання основної програми з GUI.

    Args:
        root (tk.Tk): Кореневе вікно GUI.
        login (str): Логін користувача.
        password (str): Пароль користувача.
    """
    data = run_asyncio_loop(login, password, JURNAL)
    if data is not None:
        save_uroki_to_json(login, data)
        root.destroy()
        create_main_window()
    else:
        messagebox.showerror("Помилка", "Невірно введений логін або пароль")

"""****************main_z**************"""
async def run_main_z(login, password, jurnal, kl, kil):
    """
    Функція для виконання програми з записом.

    Args:
        login (str): Логін користувача.
        password (str): Пароль користувача.
        jurnal (str): URL журналу.
        kl (str): Ключ предмета.
        kil (str): Кількість уроків.

    Returns:
        Результат виконання програми з записом або None у разі невдачі.
    """
    return await main_zap(login, password, jurnal, kl, kil)

def run_asyncio_loop_z(login, password, jurnal, kl, kil):
    """
    Функція для запуску асинхронного циклу з записом.

    Args:
        login (str): Логін користувача.
        password (str): Пароль користувача.
        jurnal (str): URL журналу.
        kl (str): Ключ предмета.
        kil (str): Кількість уроків.

    Returns:
        Результат виконання асинхронного циклу з записом.
    """
    return asyncio.run(run_main_z(login, password, jurnal, kl, kil))

def run_zapis(login, password, jurnal, kl, kil):
    """
    Функція для виконання запису.

    Args:
        login (str): Логін користувача.
        password (str): Пароль користувача.
        jurnal (str): URL журналу.
        kl (str): Ключ предмета.
        kil (str): Кількість уроків.
    """
    data = run_asyncio_loop_z(login, password, jurnal, kl, kil)
    if data is not None:
        print('Всі уроки записані успішно')
    else:
        messagebox.showerror("Помилка", "Невірно введений логін або пароль")

"""*******************************************************"""
async def run_del_z(login, password, jurnal, kil):
    """
    Функція для виконання видалення запису.

    Args:
        login (str): Логін користувача.
        password (str): Пароль користувача.
        jurnal (str): URL журналу.
        kil (str): Кількість уроків.

    Returns:
        Результат виконання видалення запису або None у разі невдачі.
    """
    return await del_zap(login, password, jurnal, kil)

def run_del_asyncio_loop_z(login, password, jurnal, kil):
    """
    Функція для запуску асинхронного циклу з видаленням запису.

    Args:
        login (str): Логін користувача.
        password (str): Пароль користувача.
        jurnal (str): URL журналу.
        kil (str): Кількість уроків.

    Returns:
        Результат виконання асинхронного циклу з видаленням запису.
    """
    return asyncio.run(run_del_z(login, password, jurnal, kil))

def del_zapis(login, password, jurnal, kil):
    """
    Функція для виконання видалення запису.

    Args:
        login (str): Логін користувача.
        password (str): Пароль користувача.
        jurnal (str): URL журналу.
        kil (str): Кількість уроків.
    """
    data = run_del_asyncio_loop_z(login, password, jurnal, kil)
    if data is not None:
        print('Всі уроки Видалені успішно')
    else:
        messagebox.showerror("Помилка", "Невірно введений логін або пароль")

def run_gui():
    """Функція для створення графічного інтерфейсу."""
    root = tk.Tk()
    root.title("Автозаповнення НЗ")
    root.geometry("400x200")
    root.configure(bg="#E4EFE7")
    login_var = tk.StringVar()
    password_var = tk.StringVar()
    save_password_var = tk.BooleanVar()
    save_password_var.set(False)

    # Спроба завантажити збережені облікові дані
    try:
        with open('credentials.json', 'r') as f:
            login_var.set(log_pas()[0])
            password_var.set(log_pas()[1])
    except FileNotFoundError:
        print('Логін або пароль не збережені')

    tk.Label(root, text="Логін:", bg="#E4EFE7").grid(row=0, column=0, padx=5, pady=5)
    login_entry = tk.Entry(root, textvariable=login_var)
    login_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Пароль:", bg="#E4EFE7").grid(row=1, column=0, padx=5, pady=5)
    password_entry = tk.Entry(root, textvariable=password_var, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    run_button = tk.Button(root, text="Запустити Програму", bg="#A0C9AB",
                           command=lambda: run_program(root, login_var.get(), password_var.get()))
    run_button.grid(row=3, columnspan=2, padx=5, pady=5)

    root.mainloop()

def create_main_window():
    """
    Функція для створення вікна з результатами.
    """
    def zm_user():
        """
        Функція для закриття поточного вікна та повернення до вікна входу.
        """
        root2.destroy()  # Закрити поточне вікно
        run_gui()

    def show_about_info():
        """
        Функція для відображення інформації про програму.
        """
        try:
            with open('about.txt', 'r', encoding='utf-8') as f:
                about_info = f.read()
                messagebox.showinfo("Про програму", about_info)
        except FileNotFoundError:
            messagebox.showerror("Помилка", "Файл 'about.txt' не знайдено")

    try:
        data = load_uroki_json(log_pas()[0])
    except Exception as e:
        print(f"Помилка при завантаженні даних уроків: {e}")

    try:
        login, password = log_pas()
    except Exception as e:
        print(f"Помилка при отриманні логіна та пароля: {e}")

    root2 = tk.Tk()
    root2.title("Автозаповнення НЗ")
    root2.geometry("900x800")
    root2.configure(bg="#E4EFE7")  # Сіро-зеленуватий відтінок

    try:
        # Відображення імені користувача та кнопок керування
        tk.Label(root2, text=f"{get_user(login)}", bg="#E4EFE7").grid(row=0, column=1, padx=5, pady=5)
        run_button = tk.Button(root2, text="Змінити користувача", command=zm_user, bg="#A0C9AB")
        run_button.grid(row=0, column=4, padx=5, pady=5)
        about_button = tk.Button(root2, text="Про програму", command=show_about_info, bg="#A0C9AB")
        about_button.grid(row=0, column=5, padx=5, pady=5)

        # Створення заголовків колонок
        tk.Label(root2, text="Предмет", bg="#E4EFE7").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(root2, text="Файл Календарного", bg="#E4EFE7").grid(row=2, column=1, padx=5, pady=5)
        tk.Label(root2, text="Кількість уроків", bg="#E4EFE7").grid(row=2, column=3, padx=5, pady=5)

        row = 3
        for item in data:
            for key, value in item.items():
                # Створення рядків для кожного предмета
                tk.Label(root2, text=key, bg="#E4EFE7").grid(row=row, column=0, padx=5, pady=5)
                file_entry = tk.Entry(root2)
                file_entry.grid(row=row, column=1, padx=5, pady=5)
                select_file_btn = tk.Button(root2, text="Вибрати файл",
                                            command=lambda entry=file_entry, k=key: select_file(entry, login, k),
                                            bg="#A0C9AB")
                select_file_btn.grid(row=row, column=2, padx=5, pady=5)

                lesson_count_var = tk.StringVar()
                lesson_count_entry = tk.Entry(root2, textvariable=lesson_count_var)
                lesson_count_entry.grid(row=row, column=3, padx=5, pady=5)

                # Функція для валідації вводу кількості уроків (лише цифри)
                validate_natural_number = (root2.register(lambda action, value:
                                                           value.isdigit() if action == "1" else True), "%d", "%P")
                lesson_count_entry.config(validate="key", validatecommand=validate_natural_number)

                # Створення кнопок "Записати" та "Видалити"
                save_button = tk.Button(root2, text="Записати", command=lambda entry=file_entry, login=login,
                                        password=password, jurnal='https://nz.ua' + value, kl=key, kil=lesson_count_var:
                                        run_zapis(login, password, jurnal, kl, kil.get()), bg="#A0C9AB")
                save_button.grid(row=row, column=4, padx=5, pady=5)

                del_button = tk.Button(root2, text="Видалити", command=lambda entry=file_entry, login=login,
                                       password=password, jurnal='https://nz.ua' + value, kl=key, kil=lesson_count_var:
                                       del_zapis(login, password, jurnal, kil.get()), bg="#A0C9AB")
                del_button.grid(row=row, column=5, padx=5, pady=5)

                # Завантаження шляху до збереженого файлу, якщо існує
                file_path = get_saved_file_path(login, key)
                if file_path:
                    file_entry.insert(tk.END, file_path)
                row += 1

    except Exception as e:
        print(f"Виникла помилка: {e}")

    root2.mainloop()

if __name__ == "__main__":
    credentials = log_pas()
    current_date = datetime.now()
    end_date = datetime(2024, 10, 20)
    if current_date <= end_date:
        if credentials is not None:
            data = load_uroki_json(log_pas()[0])
            if data:
                login, password = credentials
                uroki = load_uroki_json(login)
                create_main_window()
            else: 
                run_gui()
        else: 
            run_gui()
    else:
        print("Термін дії програми закінчився. Будь ласка, зверніться до розробника для отримання оновлення програми.  mail: mashmanuc@gmail.com")

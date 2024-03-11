
from func import main, main_zap
from f_file import*
jurnal = 'https://nz.ua/journal/list'


async def run_main(login, password, jurnal, save_password):
    """Функція для виконання основної програми."""
    return await main(login, password, jurnal, save_password)


def run_asyncio_loop(login, password, jurnal, save_password):
    """Функція для запуску асинхронного циклу."""
    return asyncio.run(run_main(login, password, jurnal, save_password))


def run_program(root, login, password, save_password):
    data = run_asyncio_loop(login, password, jurnal, save_password)
    if data is not None:
        save_uroki_to_json(login,data)
        create_result_window(root, password, login, data)
        # create_main_window(root, login, password)
    else:
        messagebox.showerror("Помилка", "Невірно введений логін або пароль")



async def run_main_z(login, password, jurnal, kl, kil):
    """Функція для виконання програми з записом."""
    return await main_zap(login, password, jurnal, kl, kil)


def run_asyncio_loop_z(login, password, jurnal, kl, kil):
    """Функція для запуску асинхронного циклу з записом."""
    return asyncio.run(run_main_z(login, password, jurnal, kl, kil))


def run_zapis(login, password, jurnal, kl, kil):
    """Функція для виконання запису."""
    data = run_asyncio_loop_z(login, password, jurnal, kl, kil)
    print(kl)
    print(type(kil))
    print((kil))
    if data is not None:
        print('YYYYYYYYYYYYYYYYY', data)
    else:
        messagebox.showerror("Помилка2", "Невірно введений логін або пароль")


def run_gui():
    """Функція для створення графічного інтерфейсу."""
    root = tk.Tk()
    root.title("Запустити Основну Програму")
    root.geometry("400x200")

    login_var = tk.StringVar()
    password_var = tk.StringVar()
    save_password_var = tk.BooleanVar()
    save_password_var.set(False)

    try:
        with open('credentials.json', 'r') as f:
            log_pas()
            login_var.set(log_pas()[0])
            password_var.set(log_pas()[1])
    except FileNotFoundError:
        pass

    tk.Label(root, text="Логін:").grid(row=0, column=0, padx=5, pady=5)
    login_entry = tk.Entry(root, textvariable=login_var)
    login_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Пароль:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = tk.Entry(root, textvariable=password_var, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    save_password_checkbtn = tk.Checkbutton(root, text="Зберегти пароль", variable=save_password_var)
    save_password_checkbtn.grid(row=2, columnspan=2, padx=5, pady=5)

    run_button = tk.Button(root, text="Запустити Програму",
                           command=lambda: run_program(root, login_var.get(), password_var.get(), save_password_var.get()))
    run_button.grid(row=3, columnspan=2, padx=5, pady=5)
    root.mainloop()


def create_result_window(root, password, login, data):
    """Функція для створення вікна з результатами."""
    result_window = tk.Toplevel(root)
    result_window.title("Результати")
    result_window.geometry("800x500")

    tk.Label(result_window, text="Предмет").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(result_window, text="Файл Календарного").grid(row=0, column=1, padx=5, pady=5)
    tk.Label(result_window, text="Кількість уроків").grid(row=0, column=3, padx=5, pady=5)
    row = 1
    for item in data:
        for key, value in item.items():
            tk.Label(result_window, text=key).grid(row=row, column=0, padx=5, pady=5)
            file_entry = tk.Entry(result_window)
            file_entry.grid(row=row, column=1, padx=5, pady=5)
            file_button = tk.Button(result_window, text="Вибрати файл",
                                    command=lambda entry=file_entry, k=key: select_file(entry, login, result_window, k))
            file_button.grid(row=row, column=2, padx=5, pady=5)
            lesson_count_var = tk.StringVar()
            lesson_count_entry = tk.Entry(result_window, textvariable=lesson_count_var)
            lesson_count_entry.grid(row=row, column=3, padx=5, pady=5)

            def validate_natural_number(action, value_if_allowed):
                if action == "1":
                    if value_if_allowed.isdigit():
                        return True
                    else:
                        return False
                else:
                    return True

            vcmd = result_window.register(validate_natural_number)
            lesson_count_entry.config(validate="key", validatecommand=(vcmd, "%d", "%P"))

            save_button = tk.Button(result_window, text="Записати",
                        command=lambda entry=file_entry,
                                       login=login,
                                       password=password,
                                       jurnal='https://nz.ua' + value,
                                       kl=key,
                                       kil=lesson_count_var: 
                                           run_zapis(login, password, jurnal, kl, kil.get()),
                        )
            save_button.grid(row=row, column=4, padx=5, pady=5)
            file_path = get_saved_file_path(login, key)
            if file_path:
                file_entry.insert(tk.END, file_path)
            row += 1

"""****************************create_main_window********************************************"""

def create_main_window():
    data = load_uroki_json(log_pas()[0])
    login, password=log_pas()
    print('+')
    """Функція для створення вікна з результатами."""
    root2 = tk.Tk()
    root2.title("Результати")
    root2.geometry("800x500")
    login_var = tk.StringVar()
    password_var = tk.StringVar()
    save_password_var = tk.BooleanVar()
    save_password_var.set(False)
    try:
        with open('credentials.json', 'r') as f:
            log_pas()
            login_var.set(log_pas()[0])
            password_var.set(log_pas()[1])
    except FileNotFoundError:
        pass
    tk.Label(root2, text="Логін:").grid(row=0, column=0, padx=5, pady=5)
    login_entry = tk.Entry(root2, textvariable=login_var)
    login_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root2, text="Пароль:").grid(row=0, column=2, padx=5, pady=5)
    password_entry = tk.Entry(root2, textvariable=password_var, show="*")
    password_entry.grid(row=0, column=3, padx=5, pady=5)

    save_password_checkbtn = tk.Checkbutton(root2, text="Зберегти пароль", variable=save_password_var)
    save_password_checkbtn.grid(row=1, columnspan=3, padx=5, pady=5)
    tk.Label(root2, text="Предмет").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(root2, text="Файл Календарного").grid(row=2, column=1, padx=5, pady=5)
    tk.Label(root2, text="Кількість уроків").grid(row=2, column=3, padx=5, pady=5)
    row = 3
    for item in data:
        for key, value in item.items():
            tk.Label(root2, text=key).grid(row=row, column=0, padx=5, pady=5)
            file_entry = tk.Entry(root2)
            file_entry.grid(row=row, column=1, padx=5, pady=5)
            file_button = tk.Button(root2, text="Вибрати файл",
                                    command=lambda entry=file_entry, k=key: select_file(entry, login, root2, k))
            file_button.grid(row=row, column=2, padx=5, pady=5)
            lesson_count_var = tk.StringVar()
            lesson_count_entry = tk.Entry(root2, textvariable=lesson_count_var)
            lesson_count_entry.grid(row=row, column=3, padx=5, pady=5)
            
            def validate_natural_number(action, value_if_allowed):
                if action == "1":
                    if value_if_allowed.isdigit():
                        return True
                    else:
                        return False
                else:
                    return True

            vcmd = root2.register(validate_natural_number)
            lesson_count_entry.config(validate="key", validatecommand=(vcmd, "%d", "%P"))
            # def get_entry_value():
            #     # Отримуємо значення з Entry і зберігаємо його у змінній
            #     val= lesson_count_var.get()
            #     # Використовуємо отримане значення, наприклад, можемо його вивести
               
            #     return val



            save_button = tk.Button(root2, text="Записати",
                        command=lambda entry=file_entry,
                                       login=login,
                                       password=password,
                                       jurnal='https://nz.ua' + value,
                                       kl=key,
                                       kil=lesson_count_var: 
                                           run_zapis(login, password, jurnal, kl, kil.get()),
                        )

            save_button.grid(row=row, column=4, padx=5, pady=5)
            file_path = get_saved_file_path(login, key)
            if file_path:
                file_entry.insert(tk.END, file_path)
            row += 1
    
    root2.mainloop()



if __name__ == "__main__":
    credentials = log_pas()
    if credentials is not None:
        login, password = credentials
        uroki = load_uroki_json(login)
        # Продовжуйте роботу зі зчитаними даними
        create_main_window()
    else: 
        run_gui()

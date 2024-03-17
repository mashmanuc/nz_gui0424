from func import main, main_zap
from f_file import*
from datetime import datetime
jurnal = 'https://nz.ua/journal/list'

async def run_main(login, password, jurnal):
    """Функція для виконання основної програми."""
    return await main(login, password, jurnal)

def run_asyncio_loop(login, password, jurnal):
    """Функція для запуску асинхронного циклу."""
    return asyncio.run(run_main(login, password, jurnal))

def run_program(root, login, password):
    data = run_asyncio_loop(login, password, jurnal)
    if data is not None:
        save_uroki_to_json(login,data)
        root.destroy()
        # create_result_window(root, password, login, data)
        create_main_window()
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
    if data is not None:
        print('Всі уроки записані успішно')
    else:
        messagebox.showerror("Помилка2", "Невірно введений логін або пароль")
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

    try:
        with open('credentials.json', 'r') as f:
            login_var.set(log_pas()[0])
            password_var.set(log_pas()[1])
    except FileNotFoundError:
        print('Логін або пароль не збережені')

    tk.Label(root, text="Логін:",bg="#E4EFE7").grid(row=0, column=0, padx=5, pady=5)
    login_entry = tk.Entry(root, textvariable=login_var)
    login_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Пароль:",bg="#E4EFE7").grid(row=1, column=0, padx=5, pady=5)
    password_entry = tk.Entry(root, textvariable=password_var, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    # save_password_checkbtn = tk.Checkbutton(root, text="Зберегти пароль",bg="#E4EFE7", variable=save_password_var)
    # save_password_checkbtn.grid(row=2, columnspan=2, padx=5, pady=5)

    run_button = tk.Button(root, text="Запустити Програму",bg="#A0C9AB",
                           command=lambda: run_program(root, login_var.get(), password_var.get()))
    run_button.grid(row=3, columnspan=2, padx=5, pady=5)

    root.mainloop()

    


"""****************************create_main_window********************************************"""


def create_main_window():
    """Функція для створення вікна з результатами."""
    def zm_user():
        root2.destroy()  # Закрити поточне вікно
        run_gui()

    def show_about_info():
        try:
            with open('about.txt', 'r',encoding='utf-8') as f:
                about_info = f.read()
                messagebox.showinfo("Про програму", about_info)
        except FileNotFoundError:
            messagebox.showerror("Помилка", "Файл 'about.txt' не знайдено")
    try:
        data = load_uroki_json(log_pas()[0])
    except:
        pass
    try:
        login, password = log_pas()
    except:
        pass

    root2 = tk.Tk()
    root2.title("Автозаповнення НЗ")
    root2.geometry("900x600")
    root2.configure(bg="#E4EFE7")  # Сіро-зеленуватий відтінок

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
        print('Не можу прочитати логін або пароль')
    try:
        tk.Label(root2, text=f"{get_user(login)}", bg="#E4EFE7").grid(row=0, column=2, padx=5, pady=5)
    
        run_button = tk.Button(root2, text="Змінити користувача", command=lambda: zm_user(), bg="#A0C9AB")
        run_button.grid(row=0, column=6, padx=5, pady=5)

        tk.Label(root2, text="Предмет", bg="#E4EFE7").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(root2, text="Файл Календарного", bg="#E4EFE7").grid(row=2, column=1, padx=5, pady=5)
        tk.Label(root2, text="Кількість уроків", bg="#E4EFE7").grid(row=2, column=3, padx=5, pady=5)

        row = 3
        for item in data:
            for key, value in item.items():
                tk.Label(root2, text=key, bg="#E4EFE7").grid(row=row, column=0, padx=5, pady=5)

                file_entry = tk.Entry(root2)
                file_entry.grid(row=row, column=1, padx=5, pady=5)
                file_button = tk.Button(root2, text="Вибрати файл", command=lambda entry=file_entry, k=key: select_file(entry, login, k), bg="#A0C9AB")
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

                save_button = tk.Button(root2, text="Записати", command=lambda entry=file_entry, login=login, password=password, jurnal='https://nz.ua' + value, kl=key, kil=lesson_count_var: run_zapis(login, password, jurnal, kl, kil.get()), bg="#A0C9AB")
                save_button.grid(row=row, column=4, padx=5, pady=5)

                file_path = get_saved_file_path(login, key)
                if file_path:
                    file_entry.insert(tk.END, file_path)
                row += 1
        about_button = tk.Button(root2, text="About", command=show_about_info, bg="#A0C9AB")
        about_button.grid(row=row+1, columnspan=5, pady=10)
    except:
            pass
    
    
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

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_driverless.types.by import By
from selenium_driverless import webdriver
import asyncio
import os
import csv,json
import time
from sup import posh_daty,predmety,posh_daty2
from tkinter import filedialog, messagebox
"""  Перед запуском виставляєм 
            kl-[m5,m6,a7,a8,a9,h7,h8,h9]
            kil_ur   -    кількість уроків які треба записати;"""
num_page= '&page=3'# сторінка на якій записуєм
            

async def main(login, password,jurnal,save_password=False):
    
    options = webdriver.ChromeOptions()
    options.headless = True  # Встановлюємо опцію headless
    
    if save_password:
        with open('credentials.json', 'w') as f:
            json.dump({"login": login, "password": password}, f)
    else:
        try:
            with open('credentials.json', 'r') as f:
                credentials = json.load(f)
                login = credentials.get('login', '')
                password = credentials.get('password', '')
        except FileNotFoundError:
            login = ''
            password = ''
    async with webdriver.Chrome(options=options) as driver:
        # try:
            await driver.get('https://nz.ua/')
            await asyncio.sleep(0.5)
            print("Відкриваємо сайт")
            vchid_do = await driver.find_element(By.XPATH, '/html/body/div/div[1]/div/header/button', timeout=10)

            print("Натискаємо кнопку")
            await vchid_do.click()
            await asyncio.sleep(3)
            print("Ввійшли на сайт")
            login_field = await driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[2]/form/div[1]/input')
            if login_field:
                print("Заповнюємо поле логіну")
            password_field = await driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[2]/form/div[2]/input')
            if password_field:
                print("Заповнюємо поле паролю")

            await login_field.write(login)
            print("Логін введено")
            await password_field.write(password)
            print("Пароль введено")
            login_button = await driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[2]/form/div[4]/button')
            print("Натискаємо кнопку входу")
            await login_button.click()
            print("Кнопка входу натиснута")
            await asyncio.sleep(2)

            await driver.get(jurnal, wait_load=True)
            await asyncio.sleep(2)
            page_source = await driver.page_source
            predmety_data = predmety(page_source)
            await save_page('html.html', page_source)
            print('Програма виконана успішно')
            await asyncio.sleep(2)
            return predmety_data
        # except Exception as e:
        #     error_message = str(e)
        #     if "невірний логін і пароль" in error_message:
        #         # Вивести повідомлення про невірний логін і пароль
        #         messagebox.showerror("Помилка", "Невірний логін або пароль")
        #     else:
        #         # Обробити інші помилки
        #         print("Сталася помилка:", error_message)
        #         # Тут ви можете виконати інші дії або вивести повідомлення про інші помилки
async def main_zap(login, password,jurnal,kl,kil):
    
    options = webdriver.ChromeOptions()
    delete_files_pattern('pages')
    options.headless = True  # Встановлюємо опцію headless
    async with webdriver.Chrome(options=options) as driver:
        # try:
            await driver.get('https://nz.ua/')
            await asyncio.sleep(0.5)
            print("Відкриваємо сайт")
            vchid_do = await driver.find_element(By.XPATH, '/html/body/div/div[1]/div/header/button', timeout=10)

            print("Натискаємо кнопку")
            await vchid_do.click()
            await asyncio.sleep(2)
            print("Ввійшли на сайт")
            login_field = await driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[2]/form/div[1]/input')
            if login_field:
                print("Заповнюємо поле логіну")
            password_field = await driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[2]/form/div[2]/input')
            if password_field:
                print("Заповнюємо поле паролю")
            await login_field.write(login)
            await password_field.write(password)
            login_button = await driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[2]/form/div[4]/button')
            print("Натискаємо кнопку входу")
            await login_button.click()
            print("Кнопка входу натиснута")

            await asyncio.sleep(2)
            await driver.get(jurnal, wait_load=True)
            await asyncio.sleep(2)
            page_source = await driver.page_source
            await save_page('html_jur.html', page_source)
            # print('page +')
            page= pagin(page_source )
            
            await run_all_page(driver,jurnal,page)
            print('page ++')
            # num_page,jur=posh_daty(page)
            data=posh_daty(page)
            url=jurnal+'&page='+str(data[2])
            print(url)
            await driver.get(url, wait_load=True)
            num=data[0]
            href=data[1]
            csv_folder = f'csv_{login}'
            csv_file = os.path.join(csv_folder, f'{kl}.csv')
            await povtor_1(driver,csv_file,url,num,href)
            await asyncio.sleep(2)
            for i in range(int(kil)-1):
               await povtor(driver,csv_file,url)
          
            
           
            return data
            
    
async def save_page(file, text):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(text)
async def zapis(driver,new):
            """Функція записує тему уроку та номер уроку"""
            theme_field =await driver.find_element(By.CSS_SELECTOR, '#osvitaschedulereal-lesson_topic')
            number_field =await driver.find_element(By.CSS_SELECTOR, '#osvitaschedulereal-lesson_number_in_plan')
            await theme_field.write(new[1])
            await number_field.write(new[0])
            z_button=await driver.find_element(By.XPATH, '//*[@id="fancybox-content"]/div/div/form/fieldset/div[8]/a')
            await z_button.click()
            return driver
"""**********************************************************************"""
async def povtor(driver,login,url):
        print('host=',url)
        await driver.get(url)
        page_source = await driver.page_source
        (num ,href )= posh_daty2(page_source)
        print(num ,href)
        button1 = await WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'a[href*="{href}"]'))
        )
        await button1.click()
        new =(str(num), tema(login,num))
        time.sleep(2)
        await zapis(driver,new)#записуєм номер уроку та тему
        print("  ЗАПИСАВ")
        # await driver.get(kl, wait_load=True)
async def povtor_1(driver,login,url,num,href):
        await driver.get(url)
        print(num ,href)
        button1 = await WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'a[href*="{href}"]'))
        )
        await button1.click()
        new =(str(num), tema(login,num))
        time.sleep(2)
        await zapis(driver,new)#записуєм номер уроку та тему
        print("  ЗАПИСАВ")
        # await driver.get(kl, wait_load=True)
"""********************************all_page**************************************"""
"""Шукаємо На якій сторінці не записаний перший урок"""
def pagin(code):
    """Видає останнє натуральне число"""
    sup = BeautifulSoup(code , 'html.parser')
    items = sup.find_all('ul', class_='pagination')
    
    last_number = None  # Змінна для збереження останнього знайденого числа
    for item in items:
        num_str = item.get_text()
        tokens = num_str.split()  # Розділяємо текст на слова
        # print(tokens)
        for token in tokens:
            if token.isdigit():
                last_number = int(token)  # Оновлюємо значення останнього знайденого числа
    return last_number
async def run_all_page(driver, url, page):
    page_sources = await all_page(driver, url, page)
    return page_sources

async def all_page(driver, url, page):
    [await get_page_source(driver, url + '&page=' + str(page),page) for page in range(1, page+1)]
    
    # print('task+')
    

async def get_page_source(driver, url, page):
    await driver.get(url + f'page={page}')
   
    # print('page1=', page)
    # print(url)
    try:
        # Очікуємо, доки сторінка повністю не завантажиться
        await WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except:
        print("Не вдалося повністю завантажити сторінку")

    page_source = await driver.page_source
    await save_page(f'pages{page}.html', page_source)
    return page_source
"""**********************************************************************"""
def tema( csv_file, num):
    """Функція приймає аргументи num - номер уроку та kl - [m5, m6, a7, a8, a9, h7, h8, h9]
    та повертає рядок [№, дата, тема]"""
    

    with open( csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        # next(csv_reader)  # Пропускаємо заголовок

        for row in csv_reader:
            if row and row[0] == str(num):
                return row[2]  # Змінено індекс для отримання теми

    return "Тема не знайдена"
"""**********************************************************************"""


def delete_files_pattern(pattern):
    """Видаляє файли зі збігаючимся шаблоном імені."""
    found_files = False
    for filename in os.listdir('.'):
        if filename.startswith(pattern) and filename.endswith('.html'):
            os.remove(filename)
            found_files = True
    
    if not found_files:
        print(f"No files found matching the pattern '{pattern}*.html'.")

# Приклад використання


"""**********************************************************************"""

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_driverless.types.by import By
from selenium_driverless import webdriver
from selenium.common.exceptions import TimeoutException
import asyncio
import os
import csv,json
import time
from sup import posh_daty,predmety,posh_daty2,posh_vidalena,del_posh_daty
from tkinter import filedialog, messagebox
from f_file import save_user
link_in_excel='https://nz.ua/journal/export-xls?journal='
async def login_to_website(driver, login, password):
    await driver.get('https://nz.ua/')
    await asyncio.sleep(0.5)
    print("Відкриваю електронний журнал")
    vchid_do = await driver.find_element(By.XPATH, '/html/body/div/div[1]/div/header/button', timeout=10)
    await vchid_do.click()
    await asyncio.sleep(3)
    login_field = await driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[2]/form/div[1]/input')
    if login_field:
        print("Заповнюю поле логіну")
    password_field = await driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[2]/form/div[2]/input')
    if password_field:
        print("Заповнюю поле паролю")
    await login_field.write(login)
    print("Логін введено       ", login)
    await password_field.write(password)
    print("Пароль введено", '******************')
    login_button = await driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[2]/form/div[4]/button')
    await login_button.click()
    await asyncio.sleep(2)

async def main(login, password, jurnal):
    options = webdriver.ChromeOptions()
    download_folder=f'excel_jurnal_{login}'
    create_download_folder(download_folder)
    options.add_argument(f"--download.default_directory={download_folder}")  # Вказуємо папку для завантажень
    if login and password:
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
        await login_to_website(driver, login, password)
        await driver.get(jurnal, wait_load=True)
        try:
            await driver.get(jurnal, wait_load=True, timeout=10)
        except TimeoutException:
            print("Час очікування вичерпано. Сторінка не завантажилась за вказаний час.")
        else:
            page_source = await driver.page_source
        try:
            predmety_data = predmety(page_source)[0]
            print('Зайшов під логіном        ', login)
            user = predmety(page_source)[1]
            save_user(login, user)
            print('Зараз на сторінці  ', user)
            await save_page('html.html', page_source)
            
            await asyncio.sleep(2)
            print('Інфомацію про уроки отримано')
            return predmety_data
        except:
            print("Проблеми з логіном або паролем")
            return None

async def main_zap(login, password, jurnal, kl, kil):
    options = webdriver.ChromeOptions()
    delete_files_pattern('pages')
    async with webdriver.Chrome(options=options) as driver:
        await login_to_website(driver, login, password)
        await driver.get(jurnal, wait_load=True)
        page_source = await driver.page_source
        await save_page('html_jur.html', page_source)
        page = pagin(page_source)
        await run_all_page(driver, jurnal, page)
        data = posh_daty(page)
        url = jurnal + '&page=' + str(data[2])
        await driver.get(url, wait_load=True)
        num = data[0]
        href = data[1]
        csv_folder = f'csv_{login}'
        csv_file = os.path.join(csv_folder, f'{kl}.csv')
        await povtor_1(driver, csv_file, url, num, href)
        await asyncio.sleep(2)
        for i in range(int(kil) - 1):
            await povtor(driver, csv_file, url)
        return data

async def del_zap(login, password, jurnal, kil ):
    options = webdriver.ChromeOptions()
    delete_files_pattern('pages')
    async with webdriver.Chrome(options=options) as driver:
        await login_to_website(driver, login, password)
        await driver.get(jurnal, wait_load=True)
        page_source = await driver.page_source
        await save_page('html_jur.html', page_source)
        page = pagin(page_source)
        await run_all_page(driver, jurnal, page)
        data = del_posh_daty(page)
        url = jurnal + '&page=' + str(data[2])
        await driver.get(url, wait_load=True)
        print(url)
        # code= await driver.page_source
        # mass=posh_vidalena(code)
        # print(mass)
        
        for i in range(int(kil) ):
            
            await asyncio.sleep(0.5)
            await del_povtor(driver,url)
            await asyncio.sleep(0.5)
        return data
"""**************save_excel**********************************"""        
async def save_exel(login, password):
    options = webdriver.ChromeOptions()
    download_folder=f'excel_jurnal_{login}'
    create_download_folder(download_folder)
    options.add_argument(f"--download.default_directory={download_folder}")  # Вказуємо папку для завантажень
    async with webdriver.Chrome(options=options) as driver:
            await login_to_website(driver, login, password)
            await main_excel(driver,login,url=None)
            
            # await asyncio.sleep(2)
            # for i in predmety_data:
            #     s_link = link_in_excel + next(iter(i.values()))
            #     print(s_link)
                
                
                
                        
          
"""********************excel_povtor********************""" 
from pathlib import Path
import shutil
from typing import Union        
async def main_excel(driver, login, url):
    # Існуючий код для знаходження та натискання кнопок

    try:
        print('шукаю')
        button_exl = await WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[1]/a')))
        print('знайшов')
        await asyncio.sleep(0.5)
        await button_exl.click()
        print('натиснув')

        button_dow = await WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[1]/ul/li[2]/a')))
        print('знайшов')
        await asyncio.sleep(0.5)
        await button_dow.click()
        print('натиснув2')

        # Чекаємо на завантаження файлу та отримуємо його шлях
        downloaded_file_path = await wait_for_file_download(driver)
        if downloaded_file_path:
            save_path = Path(f'excel_jurnal_{login}/downloaded_file.xlsx')
            save_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(downloaded_file_path), str(save_path))
            print(f'Файл було збережено у {save_path}')
        else:
            print('Не вдалося знайти завантажений файл')

    except TimeoutException:
        print('Повільний інтернет або елемент не знайдено')
async def wait_for_file_download(driver) -> Union[Path, None]:
    """
    Чекає на завершення завантаження файлу та повертає шлях до нього.
    """
    download_dir = await driver.execute_script("return window.navigator.msSaveOrOpenBlob.toString().match(/[^\"]*\"/)[0].slice(1, -1)")
    if not download_dir:
        return None

    await driver.execute_script("window.navigator.msSaveOrOpenBlob = function() {}")
    file_path = None
    start_time = time.time()

    while not file_path and time.time() - start_time < 60:
        for entry in os.listdir(download_dir):
            if entry.endswith(".crdownload"):
                continue
            file_path = Path(download_dir) / entry
            break
        await asyncio.sleep(1)

    if not file_path:
        return None

    return file_path
            
async def save_page(file, text):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(text)

async def zapis(driver,new):
    time.sleep(1)
    """Функція записує тему уроку та номер уроку"""
    try:
        theme_field = await WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#osvitaschedulereal-lesson_topic')))
        number_field = await WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#osvitaschedulereal-lesson_number_in_plan')))
    except TimeoutException:
        print('Повільний інтернет або елемент не знайдено')
        return
    await theme_field.write(new[1])
    await number_field.write(new[0])
    try:
        z_button = await driver.find_element(By.XPATH, '/html/body/div[25]/div/div[1]/div/div/form/fieldset/div[8]/a')
    except:
        print('Повільний інтернет або кнопку не знайдено')
        return
    await asyncio.sleep(1)
    await z_button.click()
    return driver
async def del_zapis(driver):
    await asyncio.sleep(1)
    """Функція очищає та записує тему уроку та номер уроку"""
    try:
        theme_field = await WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#osvitaschedulereal-lesson_topic')))
        number_field = await WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#osvitaschedulereal-lesson_number_in_plan')))
    except TimeoutException:
        print('Повільний інтернет або елемент не знайдено')
        return
    # Очищення полів введення
    await theme_field.clear()
    await number_field.clear()
    await asyncio.sleep(1)
    try:
        z_button = await driver.find_element(By.XPATH, '/html/body/div[25]/div/div[1]/div/div/form/fieldset/div[8]/a')
    except:
        print('Повільний інтернет або кнопку не знайдено')
        return
    await asyncio.sleep(1)
    await z_button.click()
    print('Видаляю ')
    return driver

"""**********************************************************************"""
async def povtor(driver,login,url):
        # print('host=',url)
        await driver.get(url,wait_load=True, timeout=10)
        page_source = await driver.page_source
        (num ,href )= posh_daty2(page_source)
        # print(num ,href)
        await asyncio.sleep(0.5)
        button1 = await WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'a[href*="{href}"]'))        )
        await button1.click()
        new =(str(num), tema(login,num))
        time.sleep(2)
        await zapis(driver,new)#записуєм номер уроку та тему
        await asyncio.sleep(0.5)
        print("  ЗАПИСАВ        " , new)
async def povtor_1(driver,login,url,num,href):
        print(url)
        print(num)
        print(href)
        await driver.get(url)
        await asyncio.sleep(0.5)
        button1 = await WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'a[href*="{href}"]'))        )
        await button1.click()
        new =(str(num), tema(login,num))
        time.sleep(2)
        await zapis(driver,new)#записуєм номер уроку та тему
        await asyncio.sleep(0.5)
        print("  ЗАПИСАВ        ", new)

async def del_povtor(driver,url):
        await driver.get(url,wait_load=True, timeout=10)
        await asyncio.sleep(0.5)
        page_source = await driver.page_source
        await asyncio.sleep(0.5)
        (num ,href )= posh_vidalena(page_source)
        # print(num ,href)
        await asyncio.sleep(0.5)
        button1 = await WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'a[href*="{href}"]'))        )
        await button1.click()
        
        time.sleep(2)
        await del_zapis(driver)#записуєм номер уроку та тему
        await asyncio.sleep(0.5)
        print("  Видалив" , num)
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

async def get_page_source(driver, url, page):
    await driver.get(url + f'page={page}')
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
"""**********************************************************************"""
def create_download_folder(download_folder):
    # Перевіряємо, чи існує папка
    if not os.path.exists(download_folder):
        try:
            # Створюємо папку, якщо вона не існує
            os.makedirs(download_folder)
            print(f"Папка {download_folder} створена успішно.")
        except OSError:
            print(f"Сталася помилка при створенні папки {download_folder}.")
            raise
    else:
        print(f"Папка {download_folder} вже існує.")
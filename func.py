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
from sup import posh_daty,predmety,posh_daty2
from tkinter import filedialog, messagebox
from f_file import save_user

async def main(login, password,jurnal):
    options = webdriver.ChromeOptions()
    options.headless = True  # Встановлюємо опцію headless
    
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
        # try:
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
            print("Логін введено       ",login)
            await password_field.write(password)
            print("Пароль введено",'******************')
            login_button = await driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[2]/form/div[4]/button')
            await login_button.click()
            await asyncio.sleep(2)
            await driver.get(jurnal, wait_load=True)
            try:
                await driver.get(jurnal, wait_load=True, timeout=10)  # Очікуємо максимум 10 секунд на завантаження сторінки
            except TimeoutException:
                print("Час очікування вичерпано. Сторінка не завантажилась за вказаний час.")
            else:
                page_source = await driver.page_source
            try:
                predmety_data = predmety(page_source)[0]
                print('Зайшов під логіном        ',login)
                user= predmety(page_source)[1]
                save_user(login, user)
                print('Зараз на сторінці  ',user)
                await save_page('html.html', page_source)
                print('Інфомацію про уроки отримано')
                await asyncio.sleep(2)
                return predmety_data
            except:
                print("Проблеми з логіном або паролем")
                return None

async def main_zap(login, password,jurnal,kl,kil,log_text=None):
    options = webdriver.ChromeOptions()
    delete_files_pattern('pages')
    options.headless = True  # Встановлюємо опцію headless
    async with webdriver.Chrome(options=options) as driver:
        # try:
            await driver.get('https://nz.ua/')
            await asyncio.sleep(0.5)
            print("Відкриваю журнал")
            vchid_do = await driver.find_element(By.XPATH, '/html/body/div/div[1]/div/header/button', timeout=10)
            await vchid_do.click()
            await asyncio.sleep(2)
            login_field = await driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[2]/form/div[1]/input')
            if login_field:
                print("Логін введено       ",login)
            password_field = await driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[2]/form/div[2]/input')
            if password_field:
                print("Пароль введено",'******************')
            await login_field.write(login)
            await password_field.write(password)
            login_button = await driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[2]/form/div[4]/button')
            await login_button.click()
            print('Зайшов під логіном        ',login)
            await asyncio.sleep(2)
            await driver.get(jurnal, wait_load=True)
            await asyncio.sleep(2)
            page_source = await driver.page_source
            await save_page('html_jur.html', page_source)
            print('Зайшов під логіном        ',login)
            page= pagin(page_source )
            await run_all_page(driver,jurnal,page)
            data=posh_daty(page)
            url=jurnal+'&page='+str(data[2])
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
            EC.presence_of_element_located((By.CSS_SELECTOR, f'a[href*="{href}"]'))        )
        await button1.click()
        new =(str(num), tema(login,num))
        time.sleep(2)
        await zapis(driver,new)#записуєм номер уроку та тему
        print("  ЗАПИСАВ        " , new)
async def povtor_1(driver,login,url,num,href):
        await driver.get(url)
        button1 = await WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'a[href*="{href}"]'))        )
        await button1.click()
        new =(str(num), tema(login,num))
        time.sleep(2)
        await zapis(driver,new)#записуєм номер уроку та тему
        print("  ЗАПИСАВ        ", new)
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

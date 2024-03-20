from bs4 import BeautifulSoup
def readd(file_path):
    """Повертає список словників, який містить назви класів разом з предметами та посилання на них."""
    with open(file_path, 'r', encoding='utf-8') as file:
      html_code = file.read()
    return html_code
code=(readd('pages4.html'))

def predmety(code):
  data=[]
  sup = BeautifulSoup(code , 'html.parser')
  items=sup.find_all('table',class_='journal-choose')
  user=sup.find('div',class_='h-user-info clear').text
  tadles=items[0].find_all('tr')
  for taab in tadles:
      predmet=taab.find('td').text
    
      if taab.find('a'):
        klas=taab.find_all('a')
        for kl in klas :
              silka=(kl['href'])
              klass=kl.text
              data.append({klass+' '+predmet:silka})
              # print({klass+' '+predmet:silka})
  return data,user
def posh_vidalena(code):
    """Видає  останій записаний урок"""
    sup = BeautifulSoup(code , 'html.parser')
    items=sup.find_all('div',class_='clear rltv')
    pr=0
    for item in items:
        num_str= item.find('div',class_='dzc-lesson-number').get_text()
        num_str = num_str.replace('\xa0', '')
        data=item.find('div',class_='dzc-date').get_text()
        if ( num_str )and data :
            pr=int(num_str)
        else :
            
            break    
        
        href=item.find('a', class_='dz-edit modal-box').get('href')
    return pr,href
# print(predmety(code))
def posh_daty(num):
    # Вкладена функція для пошуку останнього записаного уроку на сторінці з номером 'i'
    def posh_daty_is(i, f_ost=None):
        """Видає останній записаний урок"""
        code = readd(f'pages{i}.html')
        sup = BeautifulSoup(code, 'html.parser')
        items = sup.find_all('div', class_='clear rltv')
        last_recorded_lesson = None
        per = items[0].find('div', class_='dzc-lesson-number').get_text().replace('\xa0', '')
        ost = items[-1].find('div', class_='dzc-lesson-number').get_text().replace('\xa0', '')
        f = 0
        if per and ost:
            href = items[-1].find('a', class_='dz-edit modal-box').get('href')
            f_ost = ost
            if i < num:
                return posh_daty_is(i + 1, f_ost)
            last_recorded_lesson = int(ost), href, f
        # Перевірка чи є записи уроків на сторінці, але останній урок порожній
        elif per and not ost:
            # print("Шукаю тут")  
            prapor=per         
            for item in items:
                # Отримання номера уроку та дати
                num_str = item.find('div', class_='dzc-lesson-number').get_text().replace('\xa0', '')
                # Отримання посилання на урок
                href = item.find('a', class_='dz-edit modal-box').get('href')
                try:
                    # Перевірка чи номер та дата уроку не порожні
                    if num_str:
                        # Якщо номер та дата уроку не порожні, зберігаємо номер уроку та посилання на нього
                        prapor=num_str
                    else:
                        last_recorded_lesson = int(prapor)+1, href,i
                        return last_recorded_lesson
                except:
                    return None
        # Якщо немає записів уроків на сторінці
        else:
            per = items[0].find('div', class_='dzc-lesson-number').get_text().replace('\xa0', '')
            href = items[0].find('a', class_='dz-edit modal-box').get('href')
            # Зберігаємо номер та посилання першого уроку на сторінці
            last_recorded_lesson = int(f_ost)+1, href,i
        return last_recorded_lesson
    return posh_daty_is(1)



def del_posh_daty(num):
    # Вкладена функція для пошуку останнього записаного уроку на сторінці з номером 'i'
    def posh_daty_is(i, f_ost=None):
        """Видає останній записаний урок"""
        code = readd(f'pages{i}.html')
        sup = BeautifulSoup(code, 'html.parser')
        items = sup.find_all('div', class_='clear rltv')
        last_recorded_lesson = None
        per = items[0].find('div', class_='dzc-lesson-number').get_text().replace('\xa0', '')
        ost = items[-1].find('div', class_='dzc-lesson-number').get_text().replace('\xa0', '')
        f = 0
        if per and ost:
            href = items[-1].find('a', class_='dz-edit modal-box').get('href')
            f_ost = ost
            if i < num:
                return posh_daty_is(i + 1, f_ost)
            last_recorded_lesson = int(ost), href, f
        # Перевірка чи є записи уроків на сторінці, але останній урок порожній
        elif per and not ost:
            # print("Шукаю тут")  
            prapor=per         
            for item in items:
                # Отримання номера уроку та дати
                num_str = item.find('div', class_='dzc-lesson-number').get_text().replace('\xa0', '')
                # Отримання посилання на урок
                try:
                    # Перевірка чи номер та дата уроку не порожні
                    if num_str:
                        # Якщо номер та дата уроку не порожні, зберігаємо номер уроку та посилання на нього
                        prapor=num_str
                    else:
                        last_recorded_lesson = int(prapor), href,i
                        return last_recorded_lesson
                except:
                    return None
                href = item.find('a', class_='dz-edit modal-box').get('href')
        return last_recorded_lesson
    return posh_daty_is(1)
# data=del_posh_daty(num=4)
# print(data)
print(posh_vidalena(code))
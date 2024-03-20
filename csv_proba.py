import docx
import csv
import re
import os

kl = 'a8'
start_number = 1  # Початкове значення номера
login='login'

docx_file = u'E:\\project\\PROBA\\6t.docx'
csv_folder = f'csv_{login}'
csv_file = os.path.join(csv_folder, f'{kl}.csv')
def  is_num(text):
    return bool(re.search(r'\d', text))
def word_to_csv(docx_file, login,kl):
    if not os.path.exists(login):
        os.makedirs(login)  # Створюємо папку, якщо вона не існує
    csv_folder = f'csv_{login}'
    csv_file = os.path.join(csv_folder, f'{kl}.csv')
    def is_numeric(text):
        # Перевірка, чи текст складається тільки з цифр, ком або крапки
        return bool(re.match(r'^[\d.,..]+$', text))
    
    row_count = 0  # Лічильник рядків, які фактично записуються у файл
    # Перевірка і створення папки, якщо вона не існує
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    with open(docx_file, "rb") as docx_file:
        doc = docx.Document(docx_file)
    with open(csv_file, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        for table in doc.tables:
            for row_index, row in enumerate(table.rows):
                row_data = [start_number + row_count]
                # print(row_index)
                for cell in row.cells:
                    # Отримуємо текст з комірки
                    cell_text = cell.text.strip()
                    # Ігноруємо порожні комірки
                    if cell_text:
                            row_data.append(cell_text)
                # try:
                    if len(row_data) >=2 and isinstance(row_data[0], int):
                        if not is_numeric(row_data[1]):
                            row_data[1], row_data[2] = row_data[2], row_data[1]
                        
                        if is_num(row_data[1]):
                            num0,num1,num2=row_data[0], row_data[1], row_data[2]
                            if (int(row_data[0]))==(int(row_data[1])):
                                num1,num2=row_data[2],row_data[3]
                            writer.writerow([num0, num1, num2])
                            row_count += 1 
                        print([num0, num1, num2])       
                # except: pass

if __name__ == "__main__":

    word_to_csv(docx_file,  csv_file , kl)

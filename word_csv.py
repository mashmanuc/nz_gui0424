import docx
import csv
import re
import os

kl = 'a8'
start_number = 1  # Початкове значення номера
login='login'
def  is_num(text):
    return bool(re.search(r'\d', text))
def word_to_csv(docx_file, login, kl):
    def is_numeric(text):
        # Перевірка, чи текст складається тільки з цифр, ком або крапки
        return bool(re.match(r'^[\d.,..]+$', text))

    row_count = 0  # Лічильник рядків, які фактично записуються у файл
    
    csv_folder = f'csv_{login}'
    csv_file = os.path.join(csv_folder, f'{kl}.csv')
    

    # Перевірка і створення папки, якщо вона не існує
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    with open(docx_file, "rb") as docx_file:
        doc = docx.Document(docx_file)
    with open(csv_file, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        print('+')

        for table in doc.tables:
            for row_index, row in enumerate(table.rows):
                row_data = [start_number + row_count]

                for cell in row.cells:
                    # Отримуємо текст з комірки
                    cell_text = cell.text.strip()
                    print(cell_text)

                    # Ігноруємо порожні комірки
                    if cell_text:
                        row_data.append(cell_text)
                # print(row_data[2])
                
                try:
                    if len(row_data) >=2 and isinstance(row_data[0], int):
                    # if row_data[2] and isinstance(row_data[0], int):
                        if not is_numeric(row_data[1]):
                            row_data[1], row_data[2] = row_data[2], row_data[1]
                        if is_num(row_data[1]):
                        
                        # Записуємо рядок у файл CSV
                            writer.writerow(row_data)
                            row_count += 1  # Інкрементуємо лічильник записаних рядків
                        
                        # Виводимо рядок на екран
                        # print(row_data)
                except: pass

if __name__ == "__main__":
    docx_file = u'E:\\project\\PROBA\\Календарне  (2023 =2024 с.математика 5-9кл)\\6м.docx'

    word_to_csv(docx_file, login, kl)

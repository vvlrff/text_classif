import os
import pandas as pd
import docx
import pdfplumber

def extract_text_from_docx(filename):
    doc = docx.Document(filename)
    full_text = [para.text for para in doc.paragraphs]
    return '\n'.join(full_text)

def extract_text_from_pdf(filename):
    with pdfplumber.open(filename) as pdf:
        full_text = [page.extract_text() for page in pdf.pages if page.extract_text() is not None]
    return '\n'.join(full_text)

def classify_documents(folder_path):
    # Список для хранения данных
    data = []
    
    # Проходимся по файлам в папке
    for filename in os.listdir(folder_path):
        if filename.endswith('.docx') or filename.endswith('.pdf'):
            # Полный путь к файлу
            file_path = os.path.join(folder_path, filename)
            
            # Извлечение текста в зависимости от типа файла
            if filename.endswith('.docx'):
                text = extract_text_from_docx(file_path)
            else:
                text = extract_text_from_pdf(file_path)
            
            # Вывод текста и запрос класса у пользователя
            print(f"Текст документа {filename}:")
            print(text[:100])  # Вывод первых 500 символов текста для превью
            category = input("Введите класс для этого документа: ")
            
            # Сохраняем данные
            data.append({
                "filename": filename,
                "text": text,
                "category": category
            })
    
    # Создаем DataFrame
    df = pd.DataFrame(data)
    return df

# Запускаем функцию и сохраняем DataFrame
folder_path = 'new_data'
df = classify_documents(folder_path)

# Сохраняем DataFrame в CSV файл
df.to_csv('new_classified_data.csv', index=False)
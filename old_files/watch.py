import pandas as pd

def load_data(filepath):
    """Загружает данные из CSV файла."""
    return pd.read_csv(filepath)

def clean_text_data(df):
    """Очищает DataFrame от записей с пустыми или состоящими только из переносов строки текстами."""
    df['text'] = df['text'].fillna('')  # Замена NaN на пустые строки для обработки
    df = df[df['text'].str.strip().str.len() > 0]
    return df

def count_classes(df):
    """Возвращает количество записей для каждой категории."""
    return df['category'].value_counts()

def calculate_text_lengths(df):
    """Добавляет столбец с длиной текста каждого документа."""
    df['text_length'] = df['text'].apply(len)
    return df

def correct_category_name(df, old_name, new_name):
    """Исправляет название категории."""
    df['category'] = df['category'].replace(old_name, new_name)
    return df

def save_data(df, filepath):
    """Сохраняет DataFrame в CSV файл."""
    df.to_csv(filepath, index=False)

def merge_dataframes(df1, df2):
    """Объединяет два DataFrame в один."""
    return pd.concat([df1, df2], ignore_index=True)

def remove_category(df, category_name):
    """Удаляет заданную категорию из DataFrame."""
    return df[df['category'] != category_name]

# Пример использования новых функций
filepath1 = 'updated_classified_data1.csv'
# filepath2 = 'classified_data.csv'
# df1 = load_data(filepath1)
df2 = load_data(filepath1)

# Очистка и объединение данных
# df1 = clean_text_data(df1)
# df2 = clean_text_data(df2)
# combined_df = merge_dataframes(df1, df2)

# Удаление категории
# combined_df = remove_category(df2, 'пленные')  # Удаление категории 'конфликт'

# Дальнейшая обработка и сохранение данных
# combined_df = correct_category_name(combined_df, 'радиаия', 'радиация')
combined_df = calculate_text_lengths(df2)
# save_data(combined_df, 'updated_classified_data.csv')

# Вывод обновлённой информации
class_counts = count_classes(combined_df)
print(df2)
print(class_counts)

import pandas as pd

# Создание словаря для соответствия категорий и числовых классов
category_to_number = {
    'беспилотники': 0,
    'приказ': 1,
    'конфликт': 2,
    'ИБ': 3,
    'ракета': 4,
    'радиация': 5,
    'преступления': 6,
    'терроризм': 7,
    'разведка': 8,
    'украина': 9
}

# Загрузка данных из CSV файла
filepath = 'updated_classified_data.csv'  # Замените на актуальный путь к вашему файлу
df = pd.read_csv(filepath)

# Добавление нового столбца 'number_class' на основе словаря
df['number_class'] = df['category'].map(category_to_number)

# Сохранение изменений в новый CSV файл
new_filepath = 'updated_classified_data1.csv'  # Новое имя файла для сохранения изменений
df.to_csv(new_filepath, index=False)

print("Новый столбец 'number_class' успешно добавлен и данные сохранены в:", new_filepath)

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer

# Настройка nltk для работы со стоп-словами
nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))

# Инициализация анализатора pymorphy2
morph = MorphAnalyzer()

def preprocess_text(text):
    # Удаление пунктуации
    text = re.sub(r'[^\w\s]', '', text)
    
    # Приведение к нижнему регистру
    text = text.lower()
    
    # Лемматизация и удаление стоп-слов
    tokens = text.split()
    lemmatized_tokens = [morph.parse(word)[0].normal_form for word in tokens if word not in stop_words]
    
    # Объединение слов обратно в строку
    return ' '.join(lemmatized_tokens)

# Загрузка данных
df = pd.read_csv('updated_classified_data1.csv')  # Замените на актуальный путь к вашему файлу

# Применение предобработки к текстовому столбцу
df['text'] = df['text'].apply(preprocess_text)

# Сохранение обработанных данных
df.to_csv('processed_data.csv', index=False)

print("Текст успешно обработан и сохранён в файл 'processed_data.csv'.")

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Загрузка обработанных данных
df = pd.read_csv('processed_data.csv')

# Подготовка данных
X = df['text']  # Текстовые данные для векторизации
y = df['number_class']  # Целевая переменная

# Векторизация текста
vectorizer = TfidfVectorizer(max_features=1000)  # Ограничение на максимальное количество фичей
X_vectorized = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_vectorized, df['number_class'], test_size=0.2, random_state=42)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Сохранение модели и векторизатора
model_filename = 'random_forest_model.joblib'
vectorizer_filename = 'tfidf_vectorizer.joblib'
joblib.dump(rf_model, model_filename)
joblib.dump(vectorizer, vectorizer_filename)

print(f"Модель сохранена как {model_filename}")
print(f"Векторизатор сохранен как {vectorizer_filename}")


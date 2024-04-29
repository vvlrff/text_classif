import sys
import joblib
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QLabel
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
import docx
import pdfplumber
import sqlite3
from datetime import datetime


class TextExtractorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.model = joblib.load('random_forest_model.joblib')
        self.vectorizer = joblib.load('tfidf_vectorizer.joblib')
        self.number_to_category = {
            0: 'беспилотники',
            1: 'приказ',
            2: 'конфликт',
            3: 'ИБ',
            4: 'ракета',
            5: 'радиация',
            6: 'преступления',
            7: 'терроризм',
            8: 'разведка',
            9: 'украина'
        }
        self.initUI()
        self.create_database()

    def create_database(self):
        self.conn = sqlite3.connect('actions.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS actions
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, category TEXT, file_path TEXT)''')
        self.conn.commit()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Установка темной темы
        self.setStyleSheet(
            "QWidget { background-color: #2B2B2B; color: white; }")

        self.btn_load = QPushButton('Загрузить файл', self)
        self.btn_load.setStyleSheet("""
            QPushButton {
                background-color: #00FF00;
                color: black;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #00E000;
            }
            QPushButton:pressed {
                background-color: #00C000;
            }
        """)
        self.btn_load.clicked.connect(self.loadFile)
        layout.addWidget(self.btn_load)

        self.btn_save = QPushButton('Сохранить файл', self)
        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #00FF00;
                color: black;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #00E000;
            }
            QPushButton:pressed {
                background-color: #00C000;
            }
        """)
        self.btn_save.clicked.connect(self.saveFile)
        self.btn_save.setEnabled(False)
        layout.addWidget(self.btn_save)

        self.btn_day = QPushButton('За день', self)
        self.btn_day.clicked.connect(self.show_actions_for_day)
        layout.addWidget(self.btn_day)

        self.btn_week = QPushButton('За неделю', self)
        self.btn_week.clicked.connect(self.show_actions_for_week)
        layout.addWidget(self.btn_week)

        self.btn_month = QPushButton('За месяц', self)
        self.btn_month.clicked.connect(self.show_actions_for_month)
        layout.addWidget(self.btn_month)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        self.label_category = QLabel('Категория: Не определена', self)
        layout.addWidget(self.label_category)

        self.setLayout(layout)
        self.setWindowTitle('Text Extractor with Classification')
        self.setGeometry(300, 300, 600, 400)

    def loadFile(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл", "", "Word Documents (*.docx);;PDF Files (*.pdf)", options=options)
        if filename:
            self.displayContent(filename)
            self.btn_save.setEnabled(True)

    def saveFile(self):
        options = QFileDialog.Options()
        file_format, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "", "Text Files (*.txt);;Word Documents (*.doc)", options=options)
        if file_format:
            text = self.text_edit.toPlainText()
            if file_format.endswith('.txt'):
                self.saveTextFile(file_format, text)
            elif file_format.endswith('.doc'):
                self.saveDocFile(file_format, text)

    def saveTextFile(self, filename, text):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)

    def saveDocFile(self, filename, text):
        doc = docx.Document()
        doc.add_paragraph(text)
        doc.save(filename)

    def show_actions_for_day(self):
        # Получить действия за день
        actions_for_day = self.get_actions_for_day()

        # Отобразить действия в текстовом редакторе
        self.text_edit.setPlainText('\n'.join(actions_for_day))

    def show_actions_for_week(self):
        # Получить действия за неделю
        actions_for_week = self.get_actions_for_week()

        # Отобразить действия в текстовом редакторе
        self.text_edit.setPlainText('\n'.join(actions_for_week))

    def show_actions_for_month(self):
        # Получить действия за месяц
        actions_for_month = self.get_actions_for_month()

        # Отобразить действия в текстовом редакторе
        self.text_edit.setPlainText('\n'.join(actions_for_month))

    def get_actions_for_day(self):
        today = datetime.now().strftime('%Y-%m-%d')
        self.c.execute(
            "SELECT category, file_path FROM actions WHERE date LIKE ?", (f'{today}%',))
        actions_for_day = self.c.fetchall()
        return [f"{action[0]}: {action[1]}" for action in actions_for_day]

    def get_actions_for_week(self):
        today = datetime.now()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        start_of_week_str = start_of_week.strftime('%Y-%m-%d')
        end_of_week_str = (
            start_of_week + datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        self.c.execute("SELECT category, file_path FROM actions WHERE date BETWEEN ? AND ?",
                       (start_of_week_str, end_of_week_str))
        actions_for_week = self.c.fetchall()
        return [f"{action[0]}: {action[1]}" for action in actions_for_week]

    def get_actions_for_month(self):
        today = datetime.now()
        start_of_month = datetime.date(today.year, today.month, 1)
        end_of_month = datetime.date(
            today.year, today.month + 1, 1) - datetime.timedelta(days=1)
        start_of_month_str = start_of_month.strftime('%Y-%m-%d')
        end_of_month_str = end_of_month.strftime('%Y-%m-%d')
        self.c.execute("SELECT category, file_path FROM actions WHERE date BETWEEN ? AND ?",
                       (start_of_month_str, end_of_month_str))
        actions_for_month = self.c.fetchall()
        return [f"{action[0]}: {action[1]}" for action in actions_for_month]

    def displayContent(self, filename):
        text = ''
        if filename.endswith('.docx'):
            text = self.extractTextFromDocx(filename)
        elif filename.endswith('.pdf'):
            text = self.extractTextFromPDF(filename)
        self.text_edit.setPlainText(text)
        if text.strip():
            category_name = self.classifyText(text)
            self.label_category.setText(f'Категория: {category_name}')
            self.save_action(filename, category_name)
        else:
            self.label_category.setText('Категория: Текст не найден')

    def save_action(self, file_path, category):
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.c.execute("INSERT INTO actions (date, category, file_path) VALUES (?, ?, ?)",
                       (current_date, category, file_path))
        self.conn.commit()

    def extractTextFromDocx(self, filename):
        doc = docx.Document(filename)
        full_text = [para.text for para in doc.paragraphs]
        return '\n'.join(full_text)

    def extractTextFromPDF(self, filename):
        with pdfplumber.open(filename) as pdf:
            full_text = [page.extract_text()
                         for page in pdf.pages if page.extract_text() is not None]
        return '\n'.join(full_text)

    def classifyText(self, text):
        text_vector = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vector)
        return self.number_to_category[prediction[0]]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextExtractorApp()
    ex.show()
    sys.exit(app.exec_())

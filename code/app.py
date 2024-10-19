from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import threading
import os
import logging

import project

app = Flask(__name__)
CORS(app)

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
db = SQLAlchemy(app)

# Абсолютные пути к папкам
BASE_DIR = r"C:\Users\shari\siriushack"
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'upload')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'processed')

# Проверка и создание директорий
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

# Настройка логирования
logging.basicConfig(filename=os.path.join(BASE_DIR, 'processing.log'), level=logging.INFO)


# Модель базы данных
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), default='Идет обработка', nullable=False)
    status_final = db.Column(db.Boolean, default=False, nullable=False)
    result_final = db.Column(db.String(255), nullable=True)  # Добавлено для хранения имени обработанного файла


with app.app_context():
    db.create_all()


# Функция обработки файла
def process_file(file_id):
    global _processed_filename
    with app.app_context():
        logging.info(f"Начало обработки файла - ID {file_id}")
        try:
            file = db.session.get(File, file_id)
            if file:
                logging.info(f"Начало обработки файла {file.name} с ID {file_id}")

                # Путь к исходному и обработанному файлу
                original_filepath = os.path.join(UPLOAD_FOLDER, file.name)
                processed_filename = f"processed_{file.name}"
                processed_filepath = os.path.join(PROCESSED_FOLDER, processed_filename)

                # Логика обработки файла (пример)
                project.get_report(original_filepath)

                # Сохраняем результат в файл
                # result_text_path = os.path.join(BASE_DIR, 'static', 'text2.txt')
                # with open(result_text_path, "w", encoding="utf-8") as text_file:
                #     text_file.write(text)


                # Копируем исходный файл как пример обработки (замените на свою логику)
                # shutil.copyfile(original_filepath, processed_filepath)

                # Обновляем информацию о файле в базе данных
                file.status = 'Обработка завершена'
                file.result_final = processed_filename
                file.status_final = True
                db.session.commit()

                logging.info(f"Обработка файла {file.name} завершена. Результат сохранён в {processed_filename}.")
        except Exception as e:
            logging.error(f"Ошибка при обработке файла {file_id}: {str(e)}")


# Эндпоинт для загрузки файла
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Файл не найден'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Имя файла пустое'}), 400
    if not file.filename.endswith('.xlsx'):
        return jsonify({'error': 'Файл не является xlsx'}), 400

    try:
        # Сохраняем файл в папку upload
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Добавляем запись о файле в базу данных
        new_file = File(name=filename, result_final="")
        db.session.add(new_file)
        db.session.commit()

        logging.info(f"Файл загружен с ID {new_file.id}")

        # # Запуск обработки в отдельном потоке
        thread = threading.Thread(target=process_file, args=(new_file.id,))
        thread.start()
        #process_file(new_file.id)

        return jsonify({'id': new_file.id}), 200
    except Exception as e:
        logging.error(f"Ошибка при загрузке файла: {str(e)}")
        return jsonify({'error': 'Ошибка при загрузке файла'}), 500


# Эндпоинт для проверки статуса обработки
@app.route('/status/<int:file_id>', methods=['GET'])
def check_status(file_id):
    file = File.query.get(file_id)
    if not file:
        return jsonify({'error': 'Файл не найден'}), 404
    return jsonify({
        'id': file.id,
        'status': file.status,
        'status_final': file.status_final,
        'result_final': file.result_final
    }), 200


# Эндпоинт для скачивания обработанного файла
# @app.route('/download/<filename>', methods=['GET'])
# def download_file(filename):
#     try:
#         return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)
#     except Exception as e:
#         return jsonify({'error': 'Файл не найден'}), 404


# Новый маршрут для главной страницы
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/image')
def show_image():
    directory = 'static'
    images = []

    dirs = os.listdir(path=directory)
    for dir in dirs:
        if ".jpg" in dir:
            images.append(dir)

    # images = ['histogram1.jpg', 'histogram2.jpg', 'histogram3.jpg', 'histogram4.jpg', 'histogram5.jpg']
    texts = []

    for i in range(1, len(images) + 1):
        text_filename = f'text{i}.txt'
        text_filepath = os.path.join('static', text_filename)
        if os.path.exists(text_filepath):
            with open(text_filepath, 'r', encoding='cp1251') as file:
                texts.append(file.read())
    return render_template('image.html', images=images, texts=texts, zip=zip)


if __name__ == '__main__':
    app.run(debug=True)

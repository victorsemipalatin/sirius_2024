from flask import Flask, request, render_template, flash, jsonify, session
from werkzeug.utils import secure_filename
import os
import shutil
import processing

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # Нужен для работы flash-сообщений

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_enough(n):
    static_folder = 'static'
    png_files = [f for f in os.listdir(static_folder) if f.endswith('.png')]
    return len(png_files) == n

def number_of_png():
    static_folder = 'static'
    png_files = [f for f in os.listdir(static_folder) if f.endswith('.png')]
    return len(png_files)

def clear_static_folder():
    static_folder = 'static'
    for filename in os.listdir(static_folder):
        file_path = os.path.join(static_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Удаляем файлы
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Удаляем вложенные папки
        except Exception as e:
            print(f'Не удалось удалить {file_path}. Причина: {e}')




@app.route('/check_png/<int:n>', methods=['GET'])
def check_png(n):

    print(f"Обнаружено файлов PNG:, ожидается: {n}")  # Логирование
    if is_enough(n):
        return jsonify({'redirect': True})
    else:
        return jsonify({'redirect': False})

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # File upload and validation
        if 'file' not in request.files:
            flash('Файл не найден')
        else:
            file = request.files['file']
            if file.filename == '':
                flash('Имя файла отсутствует')
            elif not allowed_file(file.filename):
                flash('Недопустимый файл. Разрешен только формат .xlsx')
            else:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash(f"Файл {filename} успешно загружен.")

                # Очистка папки static перед обработкой
                clear_static_folder()  # Вызов функции очистки папки

                # Processing and setting n in session
                try:
                    n = processing.count_non_empty_columns(file)
                    session['n'] = n

                    processing.process(file)  # Обработка файла
                    flash(f"Файл обработан, n={n}.")  # Уведомление об успешной обработке
                except Exception as e:
                    flash(f"Ошибка при обработке файла: {str(e)}")
                    return redirect(request.url)


                return render_template('upload.html', n=n)
    return render_template('upload.html')

@app.route('/image')
def image_page():
    static_folder = 'static'
    n = session.get('n', number_of_png())  # Retrieve n from session with a default of number_of_png
    images = [f"histogram{i}.png" for i in range(1, n + 1)]
    text_files = [f"text{i}.txt" for i in range(1, n + 1)]
    #print(f"debug{images}")

    # Чтение содержимого файлов
    texts = []
    for text_file in text_files:
        file_path = os.path.join(static_folder, text_file)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    texts.append(f.read())
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='cp1251') as f:
                        texts.append(f.read())
                except UnicodeDecodeError:
                    texts.append("Ошибка кодировки при чтении файла")
        else:
            texts.append("Файл не найден")  # Сообщение, если файл отсутствует

    # Создаем список пар
    image_text_pairs = zip(images, texts)
    return render_template('image.html', image_text_pairs=image_text_pairs)

@app.route('/')
def report_options():
    # Рендеринг новой страницы с кнопками
    return render_template('report_options.html')

#clear_static_folder()

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
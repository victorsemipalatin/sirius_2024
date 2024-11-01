# SIRIUS DIGITAL HACK 
## Решение команды =Григорий Рыбалка= (3 место)
## Содержание

1. Состав команды
2. Описание задачи
3. Описание проекта
4. Требования к предустановленному ПО
5. Инструкция по развертке сайта
6. Инструкция по развёртке бота
7. Рабочий процесс
8. Описание файлов проекта
9. Способы улучшения программы
## Состав команды
- **Завидов Егор Николаевич**
- **Кораблев Денис Андреевич**
- **Панфилов Павел Андреевич**
- **Петров Григорий Евгеньевич**
## Описание задачи
На вход программы пользователем передаётся .xlsx файл, содержащий ответы уволившихся сотрудников на открытые вопросы. Результатом выполнения кода должен стать отчёт, который будет содержать обработанные данные в удобном формате и краткие комментарии-советы к ним.
## Описание проекта
Данный репозиторий содержит решение задачи для хакатона "Sirius Digital Hack". Проект разделён на несколько модулей, каждый из которых может работать в отдельности от остальных в зависимости от потребностей пользователя. Главными составляющими являются сайт, а также бот в телеграме.  
На сайте расположена форма для загрузки входных данных. После отправки датасета генерируется страница с графиками и комменатариями, созданными на основе пользовательских данных. Итерфейc сайта приведён на рисунке ниже.
!['pic1'](https://github.com/victorsemipalatin/sirius_2024/blob/main/int.jpeg)  
Бот располагается по адресу @GrogFishingBot. Функционал бота схож с тем, что представлено на сайте, однако результатом работы кода является отчёт, оформленный в виде PDF-имер отчёта представлен на следующей картинке.
!['pic2'](https://github.com/victorsemipalatin/sirius_2024/blob/main/report.png)
## Требования к предустановленному ПО
git version 2.34.1  
Python 3.11.7  
Docker version 27.3.1  
## Инструкция по развертке сайта
**Для запуска сайта необходимо выполнить следующие действия:**  
С помощью заранне предустановленного Docker'a необходимо из директории проекта выполнить следующие команды:  
Создание образа:
```
$ docker build -t sirius .
```
Создание и запуск контейнера:
```
$ docker run -d -p 5000:5000 --name my-flask-container sirius
```
В течение 2-х минут запустится сайт по адресу:
http://localhost:5000/
```
Кроме того готовый образ можно скачать с dockerhub:
https://hub.docker.com/r/tylerreith/sirius_hackathon_2024
После чего можно запустить его через Docker Desktop, указывая порт 5000 при создании контейнера.
```
В течение 2-х минут запустится сайт по адресу:
http://localhost:5000/

## Инструкция по запуску бота
С помощью заранне предустановленного Docker'a необходимо из директории проекта выполнить следующие команды:  
Создание образа:
```
$ docker build -t sirius .
```
Создание и запуск контейнера:
```
$ docker run -it --name pmc sirius
```
Для запуска потребуется некоторое время, поскольку происходит автоматическое скачивание весов для модели.
## Рабочий процесс

1. **Подготовка датасета:** Начальный этап включает парсинг данных и извлечение предобученных векторов предложений из модели SBERT.
2. **Поиск похожих предложений в наборе данных:** Предобученные эмбеддинги кластеризуются алгоритмом Kmeans по метрике, пропорциональной косинусному расстоянию (деление на норму евклидовой метрики).
3. **Выбор примеров из кластеризированных областей:** В каждом из построенных кластеров находим множество векторов, близких к медианному вектору всего кластера.
4. **Подготовка промпта в LLM:** С помощью opensource llm api в большую языковую модель отправляется строка, состоящая из ответов на вопросы, соответствующих множеству выбранных на предыдущем шаге векторов, разделенных специальным символом '\n'. Запросы сформированы так, чтобы модель анализировала причины ухода сотрудника и формировала отчет о возможных улучшениях условий труда (Данный шаг занимает много времени из-за ограничений, накладываемых на количество запросов в секунду. Купленный api тариф должен ускорить код в разы).
5. **Построение гистограмм:** Расчёт отношения количества элементов для отдельного кластера к количеству всех элементов. На основе полученных данных строятся диаграммы распределения причин ухода.
6. **Отправка результата пользователю** после всех вышеперечисленных операций программа готова дать ответ пользователю. В случае запуска сайта код переведёт пользователя на страницу с отчётом, бот же отправит ответным сообщением отчёт в формате pdf.  

## Описание файлов репозитория
- **app.py** реализует API составляющую проекта, данный файл необходим для корректной работы сайта.  
- **griga_bot.py** - файл, отвечающий за работу бота в телеграме.  
- **grig_module.py** содержит в себе функции и процедуры, необходимые для работы бота и сайта.  
- **ml_prev.py** - ML составляющая проекта, релизующая описанные выше модели.  
- **project.py** - модуль, отвечающий за текст и графику на сайте.  
- **home.html, image.html** - HTML-страницы сайта.  
- **Dockerfile** - файл для сборки бота в телеграме.  
- **requirements.txt** - необходимы для работы программы пакеты.  

## Перспективы развития проекта    
- **Улучшение алгоритма обнарежения и удаления шумов и выбросов:** удаление шумов и кластеров-выбросов.  
- **Использование более гибкого api llm модели:** данный шаг позволит многократно увеличить скорость работы программы.  
- **Размещение сайта на сервере:** увеличение доступности проекта.  
- **Написание тестов**  
![pic3](https://github.com/victorsemipalatin/sirius_2024/blob/main/goodby.png)
![diploma](https://github.com/victorsemipalatin/sirius_2024/blob/main/photo_2024-10-21_00-42-32.jpg)

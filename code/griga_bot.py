import os
import ml_prev
import shutil
import datetime
import grig_module
from PIL import Image
from fpdf import FPDF
import matplotlib.pyplot as plt
from fpdf.transitions import *
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters


token = "8107598303:AAHQtgnHx3XiTH8HGLX_O5A47q-kWuIwix8"
trash = "trash"


async def start_command(update, context):
    """
    Function to start tg bot with welcome message
    """
    await update.message.reply_text("Для получение отчёта по данным опроса уволивишихся сотрудников необходимо отправить файл расширения '.xlsx'.\n" + \
                                    "В заголовках столбцов должны быть написаны сами вопросы. Пример показан на прикреплённом рисунке.")
    chat_id = update.message.chat_id
    document = open("hello.png", 'rb')
    await context.bot.send_photo(chat_id, document)


def get_report_pdf(file, new_file_name):
    """
        Function of proccessing pdf with report
    """
    questions, clusters = ml_prev.process(file)
    tags = grig_module.get_tags(clusters)
    texts = grig_module.get_texts(clusters)
    pics = grig_module.get_pictures(tags)
    pdf = FPDF()
    # font_dir = '/usr/share/fonts/truetype/freefont'
    # pdf.add_font("Serif", style="B", fname=f"{font_dir}/FreeSerif.ttf")
    font_dir = 'C:\\Windows\\Fonts'
    pdf.add_font("Times New Roman", style="B", fname=f"{font_dir}\\times.ttf")
    for i in range(len(tags)):
        pdf.add_page()
        image = Image.open(os.path.join(trash, pics[i]))
        w_a4 = 210 # параметры листа А4
        h_a4 = 297
        width, height = image.size
        if width > w_a4 or height > h_a4:
            div_w = width // w_a4 + 1
            div_h = height // h_a4 + 1
            if div_w > div_h:
                width /= div_w
                height /= div_w
            else:
                width /= div_h
                height /= div_h
        pdf.image(image, x="CENTER", y=5, w=width, h=height)
        pdf.ln(height)
        pdf.set_font("Times New Roman", "B", size=10)
        pdf.multi_cell(0, None, f"Рис. {i + 1} Гистограмма распределения ответов на вопрос: {questions[i].lower()}", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.set_font("Times New Roman", "B", size=15)
        pdf.multi_cell(0, None, f"{texts[i]}", new_x="LMARGIN", new_y="NEXT", padding=4)

    pdf.output(new_file_name)


async def processing(update, context):
    """
        File processing
    """
    with open("users.txt", 'a') as f:
        f.write(f"{update.message.chat.first_name} {update.message.chat.last_name}, {update.message.chat.username}, {datetime.datetime.now()}\n")
    print(update.message.chat.first_name, update.message.chat.last_name, ",", update.message.chat.username)
    file_id = update.message.document.file_id
    new_file = await context.bot.get_file(file_id)
    file_name = new_file.file_path.split("/")[-1]
    if ".xlsx" in file_name:
        await update.message.reply_text("Файл принят в обработку")
        await new_file.download_to_drive(file_name)
        output_file_name = new_file.file_path.split("/")[-1].split(".")
        output_file_name[-1] = ".pdf"
        output_file_name = "".join(el for el in output_file_name)
        chat_id = update.message.chat_id
        get_report_pdf(file_name, output_file_name)
        document = open(output_file_name, 'rb')
        await update.message.reply_text("Отчёт")
        await context.bot.send_document(chat_id, document)
        os.remove(output_file_name)
        os.remove(file_name)
        try:
            shutil.rmtree(trash)
            os.mkdir(trash)
        except FileNotFoundError:
            os.mkdir(trash)
    else:
        await update.message.reply_text("Отправленный Вами файл имеет некорректное расширение.\n" + \
                                        "Обратите внимание, что бот отбрабатывает файлы только в '.xlsx' расширении")


application = ApplicationBuilder().token(token).build()
application.add_handler(CommandHandler("start", start_command))
application.add_handler(MessageHandler(filters.ATTACHMENT, processing))

application.run_polling()

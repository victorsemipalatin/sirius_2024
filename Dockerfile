FROM python:3.11

WORKDIR /sirius_2024

COPY requirements.txt /sirius_2024

RUN python3 -m pip install -r requirements.txt

COPY ./code ./code 

CMD ["python", "./code/griga_bot.py"]

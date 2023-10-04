FROM python:3.9

WORKDIR /home/ilyas/backup_gitlab

RUN pip install --upgrade pip

COPY .  .

RUN pip install -r requirements.txt

CMD tail -f /dev/null

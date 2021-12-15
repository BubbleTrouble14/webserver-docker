FROM python:3.9-alpine

COPY . .

RUN pip install --upgrade pip

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install -r requirements.txt
# RUN pip install psycopg2-binary

RUN crontab crontab

CMD ["crond", "-f"]

# 0 12 * * * python /task.py
# 0 0 * * * python /task.py
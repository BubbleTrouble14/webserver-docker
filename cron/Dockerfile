FROM python:3-alpine

ENV PYTHONUNBUFFERED=1
# ENV PROJ_DIR="/"
# ENV LOG_FILE="${PROJ_DIR}/test.log"
# ENV CRON_SPEC="* * * * *" 

WORKDIR /app

RUN pip install --upgrade pip

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev


# COPY docker-entrypoint.sh docker-entrypoint.sh 
# RUN chmod a+x docker-entrypoint.sh

COPY . .

RUN pip install -r requirements.txt

# RUN echo "${CRON_SPEC} python ${PROJ_DIR}/test.py >> ${LOG_FILE} 2>&1" > ${PROJ_DIR}/crontab
# RUN touch ${LOG_FILE} # Needed for the tail
# RUN crontab ${PROJ_DIR}/crontab
# RUN crontab -l

# RUN python hello.py
# ENTRYPOINT ["python", "/app/hello.py"]

RUN crontab crontab
# * * * * * python /app/test.py > /dev/stdout


# COPY docker-start.sh .
# COPY ./docker-entrypoint.sh /
# ENTRYPOINT /docker-entrypoint.sh

# CMD ["docker-start.sh"]

# CMD crond
# CMD ["python", "hello.py"]
CMD ["crond", "-f"]
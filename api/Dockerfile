FROM python:3.10

WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000

CMD python3 app.py ${RASPBERRY_KEY} ${DB_NAME_MYSQL} ${HOST_MYSQL} ${PASSWORD_MYSQL} ${USER_MYSQL}

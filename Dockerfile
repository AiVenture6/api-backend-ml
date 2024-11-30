FROM python:3.12.2

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
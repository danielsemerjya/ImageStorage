# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/


### Local version uncoment below
EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "core.wsgi:application", "--reload"]

### For Heroku deployment uncomend below
#CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --reload
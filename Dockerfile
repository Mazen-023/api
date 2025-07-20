FROM python:3.11
COPY .  /usr/src/api
WORKDIR /usr/src/api
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
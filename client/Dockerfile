FROM python:3.8-slim

WORKDIR /app 
COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8050

ENV NAME dash_app

CMD ["python", "app.py"]
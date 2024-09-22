FROM python:3.12-slim-bullseye

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/usr/src/app/bot.py"]

EXPOSE 8080
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    curl wget gnupg \
    libnss3 libatk-bridge2.0-0 libxss1 libgtk-3-0 libasound2 libgbm1 libx11-xcb1 \
    && apt-get clean

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install flask beautifulsoup4 playwright

RUN playwright install

EXPOSE 10000

CMD ["python", "app.py"]

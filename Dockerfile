FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    curl \
    libgtk-3-0 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libx11-xcb1 \
    libgbm1 \
    libxcomposite1 \
    libxrandr2 \
    libasound2 \
    libnss3 \
    libxss1 \
    fonts-liberation \
    libappindicator3-1 \
    libappindicator1 \
    libindicator7 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install playwright
RUN playwright install --with-deps

WORKDIR /app
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

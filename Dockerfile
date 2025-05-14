FROM mcr.microsoft.com/playwright:v1.17.0-rc1-focal

# FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# RUN pip install playwright

# RUN python -m playwright install --with-deps chromium

# RUN playwright install chrome

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

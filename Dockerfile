FROM unclecode/crawl4ai:0.6.0-r1

USER root

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y firefox-esr --no-install-recommends

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# RUN python -m playwright install --with-deps chromium

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# # FROM mcr.microsoft.com/playwright:v1.17.0-rc1-focal AS playwright-build

# FROM python:3.9-slim

# WORKDIR /app

# COPY . /app

# RUN pip install --upgrade pip

# RUN pip install --no-cache-dir -r requirements.txt

# # RUN python -m playwright install --with-deps chromium

# # RUN python -m playwright install-deps chrome

# EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



# FROM python:3.9-slim

# WORKDIR /app

# COPY . /app

# RUN pip install --upgrade pip

# RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

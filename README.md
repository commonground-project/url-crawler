# URL Crawler API

The `crawler` API helps backends retrieve webpage titles when direct requests fail and provides full content extraction for the AI team, ensuring reliable metadata and text access.

## Features

- **Retrieve a single webpage title** via `GET /title/{url}`
- **Retrieve multiple webpage titles** via `POST /titles`
- **Extract webpage content** via `GET /content/{url}`
- **Asynchronous processing** for efficient request handling

## Installation

Ensure you have **Python 3.8+** installed, then install the required dependencies:

```bash
pip install fastapi nest_asyncio pydantic uvicorn
```

## Running the Application

To run the application, use the following command:

```bash
python main.py
```

## API Endpoints

### Root Endpoint

- **URL:** `/`
- **Method:** `GET`
- **Description:** Returns a welcome message.
- **Response:**
  ```json
  {
    "message": "Hello, this is the root of the API. Try /title/{url} or /content/{url}"
  }
  ```

### Load Title

- **URL:** `/title/{url:path}`
- **Method:** `GET`
- **Description:** Crawls the title of the specified URL for backend.
- **Path Parameters:**
  - `url` (string): The URL to crawl.
- **Example Request:**
  ```bash
  curl -X GET "http://127.0.0.1:8000/title/https://example.com"
  ```
- **Response:**
  ```json
  {
    "title": "The title of the page"
  }
  ```

### Load Titles

- **URL:** `/titles`
- **Method:** `POST`
- **Description:** Crawls the titles of multiple URLs for backend.
- **Request Body:**
  - `urls` (list of strings): A list of URLs to crawl.
- **Example Request:**
  ```json
  {
    "urls": ["https://example.com", "https://example.org"]
  }
  ```
- **Example cURL Request:**
  ```bash
  curl -X POST "http://127.0.0.1:8000/titles" -H "Content-Type: application/json" -d '{"urls":["https://example.com","https://example.org"]}'
  ```
- **Response:**
  ```json
  [
    {
      "url": "https://example.com",
      "title": "The title of the page"
    },
    {
      "url": "https://example.org",
      "title": "Another page title"
    }
  ]
  ```

### Load Content

- **URL:** `/content/{url:path}`
- **Method:** `GET`
- **Description:** Crawls the (filtered) content of a webpage with markdown format for AI team.
- **Path Parameters:**
  - `url` (string): The URL to crawl.
- **Example Request:**
  ```bash
  curl -X GET "http://127.0.0.1:8000/content/https://example.com"
  ```
- **Response:**
  ```json
  {
    "url": "https://example.com",
    "content": "# title...."
  }
  ```
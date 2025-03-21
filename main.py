from fastapi import FastAPI
from title_crawler import crawl_title, crawl_titles
from content_crawler import crawl_content
from pydantic import BaseModel
import nest_asyncio
import asyncio
from typing import List
from fastapi.responses import JSONResponse

app = FastAPI()

class Request(BaseModel):
    urls: List[str]

@app.get("/")
async def root():
    return {"message": "Hello, this is the root of the API. Try /title/{url} or /content/{url}"}

# @app.get("/title/{url:path}") 
# async def load_title(url: str):
#     result = await crawl_title(url)
#     return result

from urllib.parse import unquote

@app.get("/title/{url:path}")
async def load_title(url: str):
    decoded_url = unquote(url)  
    print(f"Received URL: {decoded_url}")
    result = await crawl_title(decoded_url)
    return JSONResponse(content=result, media_type="application/json")
    # return result

@app.post("/titles")
async def load_titles(request: Request):
    results = await crawl_titles(request.urls)
    return results

@app.get("/content/{url:path}")
async def load_content(url: str):
    result = await crawl_content(url)
    return result



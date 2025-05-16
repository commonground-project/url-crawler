from fastapi import FastAPI
from title_crawler import crawl_title, crawl_titles
from urllib.parse import unquote
from content_crawler import crawl_content
from pydantic import BaseModel
import nest_asyncio
import asyncio
from typing import List
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright


app = FastAPI()

class Request(BaseModel):
    urls: List[str]

async def start_browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='chromium')  
        page = await browser.new_page()
        await page.goto("https://www.twreporter.org/a/three-tears-in-borneo")
        title = await page.title()
        print(f"Page title: {title}")  
        await browser.close()
# 
# @app.on_event("startup")
# async def startup_event():
#     await start_browser()

# async def crawl_using_remote_browser():
#     async with async_playwright() as p:
#         # 連接遠端 headless-shell，host.docker.internal 用於 docker container 連回本機
        
#         browser = await p.chromium.connect_over_cdp("http://headless-shell:9222")
#         page = await browser.new_page()
#         await page.goto("https://example.com")
#         title = await page.title()
#         await browser.close()
#         return title



app = FastAPI()

class Request(BaseModel):
    urls: List[str]
    browser_type: str = "chromium"



@app.get("/")
async def root():
    # await start_browser()
    return {"message": "Hello, this is the root of the API. Try /title/{url} or /content/{url}"}

@app.get("/title/{url:path}")
async def load_title(url: str):
    decoded_url = unquote(url)  
    print(f"Received URL: {decoded_url}")
    result = await crawl_title(decoded_url)
    return JSONResponse(content=result, media_type="application/json")

@app.post("/titles")
async def load_titles(request: Request):
    results = await crawl_titles(request.urls)
    return results

@app.get("/content/{url:path}")
async def load_content(url: str):
    decoded_url = unquote(url)  
    print(f"Received URL: {decoded_url}")
    result = await crawl_content(decoded_url)
    return JSONResponse(content=result, media_type="application/json")


# @app.on_event("startup")
# async def startup_event():
#     await start_browser()


@app.get("/")
async def root():
    return {"message": "Hello, this is the root of the API. Try /title/{url} or /content/{url}"}

@app.get("/title/{url:path}")
async def load_title(url: str):
    decoded_url = unquote(url)  
    print(f"Received URL: {decoded_url}")
    result = await crawl_title(decoded_url)
    return JSONResponse(content=result, media_type="application/json")

@app.post("/titles")
async def load_titles(request: Request):
    results = await crawl_titles(request.urls)
    return results

@app.get("/content/{url:path}")
async def load_content(url: str):
    decoded_url = unquote(url)  
    print(f"Received URL: {decoded_url}")
    result = await crawl_content(decoded_url)
    return JSONResponse(content=result, media_type="application/json")

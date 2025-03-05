import json
import asyncio
import nest_asyncio
import requests
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonXPathExtractionStrategy

nest_asyncio.apply()


schema = {
        "name": "News Content via XPath",
        "baseSelector": "//main[@id='main']",
        "fields": [
            {
                "name": "title",
                "selector": ".//h1[contains(@class, 'main-title')]",
                "type": "text"
            },
            {
                "name": "subtitle",
                "selector": ".//h2[contains(@class, 'sub-title')]",
                "type": "text"
            },
            {
                "name": "publish_date",
                "selector": ".//li[contains(@class, 'publish-date')]/time",
                "type": "text"
            },
            {
                "name": "publish_time",
                "selector": ".//li[contains(@class, 'publish-time')]/time",
                "type": "text"
            },
            {
                "name": "publisher",
                "selector": ".//li[contains(@class, 'publish-author')]//span[contains(@class, 'organization')]",
                "type": "text"
            },
            {
                "name": "author",
                "selector": ".//li[contains(@class, 'publish-author')]//span[contains(@class, 'name')]",
                "type": "text"
            },
            {
                "name": "tags",
                "selector": ".//div[contains(@class, 'taglist')]//li/a",
                "type": "list",
                "subtype": "text"
            },
            {
                "name": "main_image",
                "selector": ".//figure[contains(@class, 'picture--article')][1]//img",
                "type": "attribute",
                "attribute": "src"
            },
            {
                "name": "content",
                "selector": ".//div[contains(@class, 'article-wrap')]/article",
                "type": "text"
            }
        ]
    }

OUTPUT_FILE = "articles.json"

def load_urls():
    """Load URLs from urls.json"""
    with open("urls.json", "r") as file:
        return json.load(file)

def write_to_json(data):
    """Write extracted data to JSON file"""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"✅ Saved to: {OUTPUT_FILE}")

async def crawl4ai_crawl(url: str):
    async with AsyncWebCrawler() as crawler:
        try:
            extraction_strategy = JsonXPathExtractionStrategy(schema, verbose=True)
            config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=extraction_strategy,
                exclude_social_media_links=True,
                exclude_external_images=True,
                exclude_external_links=True,
                excluded_tags=["form", "header", "footer"],
                excluded_classes=["header", "footer", "nav", "menu", "sidebar", "share", "comment"],

            )
            result = await crawler.arun(url=url, config=config)
            title = result.metadata.get("title") if result.metadata else None
            print(result.cleaned_html)
            content = title
            
            
            # Check if title and content are found
            if title and content:
                print(f"✅ crawl4ai found: {title}")
                return {"url": url, "title": title, "content": content}
            else:
                print(f"⚠️ crawl4ai could not retrieve content: {url}")
                return None
        except Exception as e:
            print(f"❌ crawl4ai encountered an error: {e}")
            return None

# def bs_crawl(url: str):
#     try:
#         web = requests.get(url)
#         web.raise_for_status()
#         soup = BeautifulSoup(web.text, "html.parser")

#         # Extract title
#         title = soup.title.get_text() if soup.title else "No title found"
        
#         # Filter out irrelevant sections (ads, navigation, recommendations, etc.)
#         unwanted_classes = [
#             "ad", "ads", "advertisement", "banner", "sponsored", "promo", "promotion",
#             "nav", "navbar", "navigation", "menu", "header", 
#             "recommendation", "related", "suggested", 
#             "footer", "sidebar", "social-share", "share-buttons"
#         ]
#         for cls in unwanted_classes:
#             for tag in soup.find_all(class_=lambda x: x and cls in x):
#                 tag.decompose()
        
#         # Extract main content
#         content_div = soup.find("div", class_="article-body")
#         if content_div:
#             paragraphs = content_div.find_all("p")
#             content = "\n".join([p.get_text() for p in paragraphs if p.get_text().strip()])
#         else:
#             content = "No content found"

#         print(f"✅ BeautifulSoup found title: {title}")
#         return {"url": url, "title": title, "content": content}
#     except requests.RequestException as e:
#         print(f"❌ BeautifulSoup could not retrieve {url}: {e}")
#         return {"url": url, "title": "Error", "content": "Error"}

# Main function to orchestrate crawling using both methods
async def main():
    urls = load_urls()
    results = []

    for url in urls:
        # Attempt crawling using crawl4ai first
        result = await crawl4ai_crawl(url)
        
        # If crawl4ai fails, fallback to BeautifulSoup
        # if result is None:
        #     result = bs_crawl(url)
        
        results.append(result)

    write_to_json(results)

if __name__ == "__main__":
    asyncio.run(main())

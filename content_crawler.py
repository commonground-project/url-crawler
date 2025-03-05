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
            "name": "content",
            "selector": ".//div[contains(@class, 'article-wrap')]/article",
            "type": "text"
        }
    ]
}

OUTPUT_FILE = "articles.md"

def load_urls():
    """Load URLs from urls.json"""
    with open("url.json", "r") as file:
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
                # extraction_strategy=extraction_strategy,
                exclude_social_media_links=True,
                exclude_external_images=True,
                exclude_external_links=True,
                excluded_tags = [
                    "a", "nav", "li", "label", "button", "input",
                    "header", "footer", "nav", "aside", "script", "style", "a", "src"
                    "iframe", "noscript", "svg", "canvas", "object", "embed", "video", 
                    "audi˜o", "picture", "source", "track", "link", "map", "area", "input",
                    "menu", "sidebar", "share", "comment", "img", "figure", "figcaption",
                    "ads", "ad", "advertisement", "sponsored", "promotion", "popup", 
                    "banner", "modal", "overlay", "social", "related", "recommendations"
                ],
            )
            result = await crawler.arun(url=url, config=config)

            if result:
                return result
            else:
                return None
            # title = result.metadata.get("title") if result.metadata else None
            # if title and content:
            #     print(f"✅ crawl4ai found: {title}")
            #     return {"url": url, "title": title, "content": content}
            # else:
            #     print(f"⚠️ crawl4ai could not retrieve content: {url}")
            #     return None
        except Exception as e:
            print(f"❌ crawl4ai encountered an error: {e}")
            return None

def bs_crawl(url: str):
    try:
        web = requests.get(url)
        web.raise_for_status()
        soup = BeautifulSoup(web.text, "html.parser")

        # Extract title
        title = soup.title.get_text() if soup.title else "No title found"
        
        # Filter out irrelevant sections (ads, navigation, recommendations, etc.)
        unwanted_classes = [
            # Advertising-related elements
            "ad", "ads", "advertisement", "banner", "sponsored", "promo", "promotion", 
            "ad-container", "ad-placeholder", "ad-slot", "ad-banner", "adbox", "advert",
            
            # Navigation and menu elements
            "nav", "navbar", "navigation", "menu", "menu-item", "top-bar", "breadcrumb", 
            "dropdown", "megamenu", "header-menu", "topnav", "main-nav",
            
            # Recommended or related content
            "recommendation", "related", "suggested", "related-content", "more-articles", 
            "you-may-like", "trending", "popular", "similar-posts",
            
            # Footer and sidebar sections
            "footer", "sidebar", "sidebar-widget", "widget", "secondary", "left-sidebar", 
            "right-sidebar", "sidebar-content", 
            
            # Social media share buttons and links
            "social-share", "share-buttons", "social-icons", "social-links", "follow-us", 
            "share-widget", "sharethis", "fb-share", "twitter-share", "linkedin-share", 
            "whatsapp-share", "pinterest-share", "social-media",
            
            # Popups, overlays, and notification banners
            "popup", "modal", "overlay", "notification", "newsletter-popup", "subscribe-popup", 
            "cookie-banner", "gdpr-banner", "signup-popup", "lightbox", "interstitial",
            
            # Comment sections and user interactions
            "comments", "comment-section", "comment-thread", "discussion", "reply-box", 
            "user-comments", "review-section", "ratings", "poll", "vote", "like-button",
            
            # Miscellaneous unwanted elements
            "breadcrumb", "disclaimer", "terms", "conditions", "author-info", "author-bio", 
            "post-meta", "date", "timestamp", "byline", "meta-info", "category-label"
        ]
    
        for cls in unwanted_classes:
            for tag in soup.find_all(class_=lambda x: x and cls in x):
                tag.decompose()
        
        # Extract main content
        content_div = soup.find("div", class_="article-body")
        if content_div:
            paragraphs = content_div.find_all("p")
            content = "\n".join([p.get_text() for p in paragraphs if p.get_text().strip()])
        else:
            content = "No content found"

        print(f"✅ BeautifulSoup found title: {title}")
        return content
    except requests.RequestException as e:
        print(f"❌ BeautifulSoup could not retrieve {url}: {e}")
        return "No content found"
    
# async def main():
#     urls = load_urls()
#     results = []

#     for url in urls:
#         result = await crawl4ai_crawl(url)
#         # If crawl4ai fails, fallback to BeautifulSoup
#         if result is None:
#             result = bs_crawl(url)
        
#         results.append(result)

async def main():
    url = "https://www.trade.gov.tw/Pages/Detail.aspx?nodeid=45&pid=782350"
    url = "https://www.rescue.org/article/trump-administration-suspends-refugee-resettlement"
    url = "https://public3.pagefreezer.com/browse/HHS.gov/02-01-2025T05:49/https://www.hhs.gov/about/news/2024/02/15/new-hhs-study-finds-nearly-124-billion-positive-fiscal-impact-refugees-and-asylees-on-american-economy-15-year-period.html"
    url = "https://zh.oosga.com/demographics/usa/"
    url = "https://www.iza.org/publications/dp/15317/the-economic-and-fiscal-effects-on-the-united-states-from-reduced-numbers-of-refugees-and-asylum-seekers"
    url = "https://immigrationimpact.com/2016/06/29/immigrant-workers-enhance-expand-u-s-economy/"
    url = "https://www.longtermtrends.net/home-price-median-annual-income-ratio/"
    url = "https://www.cna.com.tw/news/ahel/202502040205.aspx"
    url = "https://public3.pagefreezer.com/browse/HHS.gov/02-01-2025T05:49/https://www.hhs.gov/about/news/2024/02/15/new-hhs-study-finds-nearly-124-billion-positive-fiscal-impact-refugees-and-asylees-on-american-economy-15-year-period.html"
    
    result = await crawl4ai_crawl(url)
    # If crawl4ai fails, fallback to BeautifulSoup
    if result is None:
        result = bs_crawl(url)
    write_to_markdown(result.markdown)

    with open("content.html", "w", encoding="utf-8") as file:
        file.write(result.cleaned_html)

def write_to_markdown(data):
    """Write extracted data to a Markdown file"""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(data)
    print(f"✅ Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())

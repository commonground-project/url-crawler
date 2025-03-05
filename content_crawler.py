import json
import asyncio
import nest_asyncio
import requests
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonXPathExtractionStrategy

async def crawl4ai_crawl(url: str):
    async with AsyncWebCrawler() as crawler:
        try:
            config = CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                exclude_social_media_links=True,
                exclude_external_images=True,
                exclude_external_links=True,
                excluded_tags = [
                    "a", "nav", "li", "label", "button", "input", "ul", "ol",
                    "header", "footer", "nav", "aside", "script", "style", "src"
                    "iframe", "noscript", "svg", "canvas", "object", "embed", "video", 
                    "audi˜o", "picture", "source", "track", "link", "map", "area", "input",
                    "menu", "sidebar", "share", "comment", "img", "figure", "figcaption",
                    "ads", "ad", "advertisement", "sponsored", "promotion", "popup", 
                    "banner", "modal", "overlay", "social", "related", "recommendations"
                ],
            )
            result = await crawler.arun(url=url, config=config)
            return result if result else None
        except Exception as e:
            print(f"Error: crawl4ai encountered an error: {e}")
            return None

def bs_crawl(url: str):
    try:
        web = requests.get(url)
        web.raise_for_status()
        soup = BeautifulSoup(web.text, "html.parser")
        
        unwanted_classes = [
            "ad", "ads", "advertisement", "banner", "sponsored", "promo", "promotion", 
            "ad-container", "ad-placeholder", "ad-slot", "ad-banner", "adbox", "advert",
            "nav", "navbar", "navigation", "menu", "menu-item", "top-bar", "breadcrumb", 
            "dropdown", "megamenu", "header-menu", "topnav", "main-nav",
            "recommendation", "related", "suggested", "related-content", "more-articles", 
            "you-may-like", "trending", "popular", "similar-posts"
            "footer", "sidebar", "sidebar-widget", "left-sidebar", 
            "right-sidebar", "sidebar-content", "social-share", "share-buttons", "button", "icon"
            "popup", "modal", "overlay", "notification", "newsletter-popup", "subscribe-popup", 
            "cookie-banner", "gdpr-banner", "signup-popup", "lightbox", "interstitial",
            "comments", "comment-section", "comment-thread", "discussion", "reply-box", 
            "user-comments", "review-section", "ratings", "poll", "vote", "like-button",
            "breadcrumb", "disclaimer", "terms", "conditions", "author-info", "author-bio", 
            "post-meta", "byline", "meta-info", "category-label"
        ]

        for cls in unwanted_classes:
            for tag in soup.find_all(class_=lambda x: x and cls in x):
                tag.decompose()
        
        content = soup.get_text()
        content = "\n".join([line for line in content.splitlines() if line.strip()])
        return content
    
    except requests.RequestException as e:
        print(f"Error: bs_crawl encountered an error: {e}")
        return "No content found"

async def crawl_content(url: str):
    result = await crawl4ai_crawl(url)
    if result is None:
        result = bs_crawl(url)
        return {"url": url, "content": result}
    return {"url": url, "content": result.markdown}
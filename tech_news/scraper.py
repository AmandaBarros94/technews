import requests
import time
from parsel import Selector
from tech_news.database import create_news

# Requisito 1


def fetch(url):
    try:
        response = requests.get(
            url,
            headers={'user-agent': 'Fake user-agent'},
            timeout=3,
        )
        time.sleep(1)
        if response.status_code == 200:
            return response.text
        return None
    except requests.ReadTimeout:
        return None


# Requisito 2


def scrape_novidades(html_content):
    new_list = Selector(text=html_content)
    return new_list.css(".entry-title a::attr(href)").getall()


# Requisito 3


def scrape_next_page_link(html_content):
    new_link = Selector(text=html_content)
    next_link = new_link.css(".next::attr(href)").get()
    return next_link


# Requisito 4


def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("link[rel='canonical']::attr(href)").get()
    title = selector.css("h1.entry-title::text").get().strip()
    timestamp = selector.css(".meta-date::text").get()
    writer = selector.css(".author a.url::text").get()
    comments_count = len(selector.css(".comment-list li").getall())
    summary = "".join(
         selector.css(
                        ".entry-content > p:nth-of-type(1) ::text"
                    ).getall()
                ).strip()
    tags = selector.css("a[rel='tag']::text").getall()
    category = selector.css("span.label::text").get()
    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "comments_count": comments_count,
        "summary": summary,
        "tags": tags,
        "category": category,
    }


# Requisito 5


def get_tech_news(amount):
    ENDPOINT = "https://blog.betrybe.com"
    news_list = []

    while len(news_list) < amount:
        content = fetch(ENDPOINT)
        links = scrape_novidades(content)

        for link in links:
            html = fetch(link)
            result = scrape_noticia(html)
            news_list.append(result)
            if len(news_list) == amount:
                break

        ENDPOINT = scrape_next_page_link(content)
    create_news(news_list)

    return news_list

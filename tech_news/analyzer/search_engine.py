from tech_news.database import search_news
import datetime

# Requisito 6


def search_by_title(title):
    searched_news = search_news({"title": {"$regex": title, "$options": "i"}})
    result = [(news["title"], news["url"]) for news in searched_news]
    return result


# Requisito 7
def search_by_date(date):
    try:
        news = search_news(
            {
                "timestamp": datetime.datetime.strptime(date, "%Y-%m-%d")
                .strftime("%d/%m/%Y")
            }
        )
        result = [(new["title"], new["url"]) for new in news]
        return result

    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_tag(tag):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""

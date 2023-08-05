from teheran_news.teheran_news import Teheran_news
from itertools import islice


# Get 5 news of all topics

articles = Teheran_news()
for news in islice(articles.info, 5):
    print(news.topic, news.title, news.related_news, news.created_at)
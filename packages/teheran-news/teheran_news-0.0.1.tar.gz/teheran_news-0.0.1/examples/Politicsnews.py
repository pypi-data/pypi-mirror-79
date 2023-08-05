from teheran_news.teheran_news import Teheran_news
from itertools import islice


# Get 32 news of politics, you can choose another topic (Economy, Society, Sports, International or Culture)

articles = Teheran_news('Politics')
for news in islice(articles.info, 32):
    print(news.title, news.created_at)

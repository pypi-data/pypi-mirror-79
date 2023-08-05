import datetime
from teheran_news.objectview import Objectview
from itertools import islice
from teheran_news.utilities import soup

class Article:
    
    def get_dict(self, list):
        names = ['topic', 'author', 'title', 'created_at', 'text', 'related_news', 'tags', 'url']
        return(dict(zip(names, list)))

    def parse_info(self, link):
        the_soup = soup(link)

        #topic
        category = the_soup.find(class_="breadcrumb")
        topic = category.find('li')

        #author
        author = the_soup.find("div", {"class": "kicker", "itemprop": "alternativeHeadline"})
        try:
            the_author = author.text
        except AttributeError:
            the_author = None

        #title
        title = the_soup.find("h2", {"class": "item-title", "itemprop": "headline"})

        #created_at
        date_soup = the_soup.find("div", {"class": "item-date half-left"})
        created_at = datetime.datetime.strptime( date_soup.text, '%B %d, %Y - %H:%M' )

        #text
        text = the_soup.find("div", {"class": "item-text"})

        #related_news
        related = the_soup.find(class_="box list header-clean related-items")
        related_news = []
        try:
            enlaces = related.find_all('li')
            for enlace in enlaces:
                related_news.append(enlace.text)
        except:
            related_news = None
        
        #tags
        get_tags = the_soup.find(class_="box list-clean header-clean list-inline list-tags tags")
        enlaces = get_tags.find_all('li')
        tags = []
        for enlace in enlaces:
            tags.append(enlace.text)

        #url
        url = link

        data_list = [topic.text, the_author, title.text, created_at, text.text, related_news, tags, url]
        data_dict = self.get_dict(data_list)
        data_obj = Objectview(data_dict)
        return data_obj

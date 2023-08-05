from bs4 import BeautifulSoup
import requests

def soup(url):
    request  = requests.get(url)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    return soup

def change_topic_name(topic):
    if topic == 'Society' or topic == 'society':
        topic = '696'
    elif topic == 'Economy' or topic == 'economy':
        topic = '697'
    elif topic == 'Politics' or topic == 'politics':
        topic = '698'
    elif topic == 'Sports' or topic == 'sports':
        topic = '699'
    elif topic == 'Culture' or topic == 'culture':
        topic = '700'
    elif topic == 'International' or topic == 'international':
        topic = '702'
    elif topic == None:
        pass
    else:
        return print("Topic {} doesn't exist".format(topic))
    return topic
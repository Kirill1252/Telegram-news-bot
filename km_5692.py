from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup


def url_headers():
    url = 'https://www.5692.com.ua/ru/news'

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/108.0.0.0 Safari/537.36'
    }

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    timeline = soup.find_all('div', class_='c-news-block')

    return timeline


def get_first_news():
    news_dict = {}

    for items_news in url_headers():
        title_news = items_news.find('a', class_='c-news-block__title').text
        url_news = items_news.find('a', class_='c-news-block__title').get('href')
        id_news = url_news.split('/')[-2]
        time_news = items_news.find('span', class_='c-article-info__when').text
        description_news = items_news.find('div', class_='c-news-block__text').text

        news_dict[id_news] = {
            'id': id_news,
            'time': time_news,
            'title': title_news,
            'description': description_news,
            'url': url_news
        }

    with open('json_file/5692_news_dict.json', 'w') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def update_news_01():
    with open('json_file/5692_news_dict.json') as file:
        news_dict = json.load(file)

    fresh_news = {}

    date = datetime.now()
    day = f"{date.strftime('%d')}.{date.strftime('%m')}.{date.strftime('%Y')}"

    for items_news in url_headers():
        url_news = items_news.find('a', class_='c-news-block__title').get('href')
        id_news = url_news.split('/')[-2]

        if id_news in news_dict:
            continue
        else:
            title_news = items_news.find('a', class_='c-news-block__title').text
            time_news = day
            description_news = items_news.find('div', class_='c-news-block__text').text

            news_dict[id_news] = {
                'id': id_news,
                'time': time_news,
                'title': title_news,
                'description': description_news,
                'url': url_news
            }

            fresh_news[id_news] = {
                'id': id_news,
                'time': time_news,
                'title': title_news,
                'description': description_news,
                'url': url_news
            }
    print(fresh_news)

    with open('json_file/5692_news_dict.json', 'w') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


if __name__ == '__main__':
    update_news_01()

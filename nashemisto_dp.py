import json
import requests
from bs4 import BeautifulSoup


def url_headers():
    url = 'https://nashemisto.dp.ua/ru/category/novosti/'

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/108.0.0.0 Safari/537.36'
    }

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    timeline = soup.find_all('li', class_='gap-2')

    return timeline


def get_first_news():
    news_dict = {}

    for item_line in url_headers():
        url_news = item_line.find('div', class_='post-meta').find('a').get('href')
        description_news = item_line.find('div', class_='post-meta').find('a').find('h4').text
        time_news = item_line.find('time', class_='entry-date published font-medium text-sm').text
        id_news = url_news.split('/')[-2]

        news_dict[id_news] = {
            'url': url_news,
            'description': description_news,
            'time': time_news
        }

    with open('json_file/nashemisto_dp_news_dict.json', 'w') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def update_news():
    with open('json_file/nashemisto_dp_news_dict.json') as file:
        news_dict = json.load(file)

    fresh_news = {}

    for item_line in url_headers():
        url_news = item_line.find('div', class_='post-meta').find('a').get('href')
        id_news = url_news.split('/')[-2]

        if id_news in news_dict:
            continue
        else:
            description_news = item_line.find('div', class_='post-meta').find('a').find('h4').text
            time_news = item_line.find('time', class_='entry-date published font-medium text-sm').text

            news_dict[id_news] = {
                'url': url_news,
                'description': description_news,
                'time': time_news
            }

            fresh_news[id_news] = {
                'url': url_news,
                'description': description_news,
                'time': time_news
            }

    print(fresh_news)

    with open('json_file/nashemisto_dp_news_dict.json', 'w') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


if __name__ == '__main__':
    update_news()

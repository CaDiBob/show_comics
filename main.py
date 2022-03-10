import os
import requests

from environs import Env


def comics_atribute(url):
    response = requests.get(url)
    response.raise_for_status()
    comics_atribute = response.json()
    return {
        'title': comics_atribute['safe_title'],
        'img_url': comics_atribute['img'],
        'comment': comics_atribute['alt']
    }


def download_image(url, title, params=None):
    folder = 'comics'
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(os.path.join(folder, f'{title}.png'), 'wb') as file:
        file.write(response.content)


def main():
    env = Env()
    env.read_env('.env')
    vk_app_id = env('VK_APP_ID')
    url = 'https://xkcd.com/353/info.0.json'
    atribute = comics_atribute(url)
    img_url = atribute['img_url']
    title = atribute['title']
    download_image(img_url, title, params=None)
    print(atribute['comment'])


if __name__ == '__main__':
    main()
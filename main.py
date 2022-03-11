import os
import requests

from environs import Env


def send_img_to_vk(upload_url, folder, title):
    with open(f'{title}.png', 'rb') as file:
        url = upload_url
        files = {
            'file1': file,    
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
    return response.json()



def fetch_upload_url(answer):
    return answer['response']['upload_url']


def get_group_vk_numbers(vk_url, params):
    response = requests.get(vk_url, params=params)
    response.raise_for_status
    return response.json()


def comics_atribute(url):
    response = requests.get(url)
    response.raise_for_status()
    comics_atribute = response.json()
    return {
        'title': comics_atribute['safe_title'],
        'img_url': comics_atribute['img'],
        'comment': comics_atribute['alt']
    }


def download_image(url, title, folder):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(os.path.join(folder, f'{title}.png'), 'wb') as file:
        file.write(response.content)


def main():
    env = Env()
    env.read_env('.env')
    vk_app_id = env('VK_APP_ID')
    vk_group_id = env('VK_GROUP_ID')
    vk_access_token = env('VK_ACCESS_TOKEN')
    folder = 'comics'

    url = 'https://xkcd.com/353/info.0.json'
    atribute = comics_atribute(url)
    img_url = atribute['img_url']
    title = atribute['title']
    # download_image(img_url, title, folder)
    # print(atribute['comment'])

    vk_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        "group_id": vk_app_id,
        "access_token": vk_access_token,
        "v": 5.131,
    }
    upload_url = fetch_upload_url(get_group_vk_numbers(vk_url, params))
    print(send_img_to_vk(upload_url, folder, title))

if __name__ == '__main__':
    main()
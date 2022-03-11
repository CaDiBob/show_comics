import os
import random
import requests

from environs import Env


def posting_img_to_vk(answer, vk_group_id, vk_access_token, comment):
    for param in answer['response']:
        media_id = param['id']
        img_owner_id = param['owner_id']
    attachment = f'photo{img_owner_id}_{media_id}'
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': vk_access_token,
        'owner_id': -int(vk_group_id,),
        'message': comment,
        'attachments': attachment,
        'v': 5.131,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def save_img_to_server(answer, vk_group_id, vk_access_token):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': vk_access_token,
        'photo': answer['photo'],
        'server': answer['server'],
        'hash': answer['hash'],
        'v': 5.131,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def get_result_upload(upload_url, title, folder):
    with open(os.path.join(folder, f'{title}.png'), 'rb') as file:
        url = upload_url
        files = {
            'file1': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
    return response.json()


def fetch_upload_url(answer):
    return answer['response']['upload_url']


def get_upload_parameters(params):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=params)
    response.raise_for_status
    return response.json()


def download_image(url, title, folder):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(os.path.join(folder, f'{title}.png'), 'wb') as file:
        file.write(response.content)


def get_comics_info(url):
    response = requests.get(url)
    response.raise_for_status()
    comics_atribute = response.json()
    return {
        'title': comics_atribute['safe_title'],
        'img_url': comics_atribute['img'],
        'comment': comics_atribute['alt']
    }


def main():
    env = Env()
    env.read_env('.env')
    vk_app_id = env('VK_APP_ID')
    vk_group_id = env('VK_GROUP_ID')
    vk_access_token = env('VK_ACCESS_TOKEN')
    folder = 'comics'

    random_comics = random.randint(1, 2591)
    url = f'https://xkcd.com/{random_comics}/info.0.json'
    comics_info = get_comics_info(url)
    img_url = comics_info['img_url']
    title = comics_info['title']
    comment = comics_info['comment']
    download_image(img_url, title, folder)

    params = {
        "access_token": vk_access_token,
        "v": 5.131  # версия API ВКонтакте используется во всех запросах,
    }

    upload_url = fetch_upload_url(get_upload_parameters(params))
    result_upload = get_result_upload(
        upload_url, title, folder
    )

    save_wall_img = save_img_to_server(
        result_upload, vk_group_id, vk_access_token
    )

    posting_img_to_vk(
        save_wall_img, vk_group_id, vk_access_token, comment
    )

    os.remove(os.path.join(folder, f'{title}.png'))


if __name__ == '__main__':
    main()

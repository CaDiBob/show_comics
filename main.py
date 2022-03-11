import os
import random
import requests

from environs import Env


def postin_img_to_vk(answer, vk_group_id, vk_access_token, comment):
    for a in answer:
        media_id = a['id']
        img_owner_id = a['owner_id']
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


def save_img_to_vk(answer, vk_group_id, vk_access_token):
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


def send_img_to_vk(upload_url, title, folder='comics'):
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


def get_group_vk_numbers(params):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=params)
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

    random_comics = random.randint(1,2591)
    url = f'https://xkcd.com/{random_comics}/info.0.json'
    atribute = comics_atribute(url)
    img_url = atribute['img_url']
    title = atribute['title']
    comment = atribute['comment']
    download_image(img_url, title, folder)
    print(comment)

    params = {
        "access_token": vk_access_token,
        "v": 5.131,
    }
    upload_url = fetch_upload_url(get_group_vk_numbers(params))
    result_send = send_img_to_vk(upload_url, title, folder='comics')

    save_img = save_img_to_vk(result_send, vk_group_id, vk_access_token)
    answer = save_img['response']

    print(postin_img_to_vk(answer, vk_group_id, vk_access_token, comment))
    os.remove(os.path.join(folder, f'{title}.png'))


if __name__ == '__main__':
    main()

import os
import random
import requests

from environs import Env


def check_error(response):
    if 'error' in response.json():
        error = response.json()['error']['error_code']
        error_msg = response.json()['error']['error_msg']
        raise requests.HTTPError(error, error_msg)


def publish_img_to_vk(
        media_id, img_owner_id, vk_group_id, vk_access_token, comment):
    attachment = f'photo{img_owner_id}_{media_id}'
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': vk_access_token,
        'owner_id': -int(vk_group_id),
        'message': comment,
        'attachments': attachment,
        'v': 5.131,  # версия API ВКонтакте используется во всех запросах,
    }
    response = requests.post(url, params=params)
    check_error(response)
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
    check_error(response)
    response.raise_for_status()
    return response.json()


def get_upload_result(upload_url, title):
    with open(f'{title}.png', 'rb') as file:
        url = upload_url
        files = {
            'file1': file,
        }
        response = requests.post(url, files=files)
        check_error(response)
        response.raise_for_status()
    return response.json()


def get_upload_parameters(vk_access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': vk_access_token,
        'v': 5.131,
    }
    response = requests.get(url, params=params)
    check_error(response)
    response.raise_for_status()
    return response.json()


def download_image(url, title):
    response = requests.get(url)
    response.raise_for_status()
    with open(f'{title}.png', 'wb') as file:
        file.write(response.content)


def get_comics_info(random_comics_number):
    url = f'https://xkcd.com/{random_comics_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics_atribute = response.json()
    return {
        'title': comics_atribute['safe_title'],
        'img_url': comics_atribute['img'],
        'comment': comics_atribute['alt']
    }


def get_last_comics_numder():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics_info = response.json()
    last_comics_numder = comics_info['num']
    return last_comics_numder


def main():
    env = Env()
    env.read_env('.env')
    vk_app_id = env('VK_APP_ID')
    vk_group_id = env('VK_GROUP_ID')
    vk_access_token = env('VK_ACCESS_TOKEN')

    try:
        last_comics_numder = get_last_comics_numder()
        random_comics_number = random.randint(1, last_comics_numder)
        comics_info = get_comics_info(random_comics_number)
        img_url = comics_info['img_url']
        title = comics_info['title']
        comment = comics_info['comment']
        download_image(img_url, title)
        upload_parameters = get_upload_parameters(vk_access_token)
        upload_url = upload_parameters['response']['upload_url']
        result_upload = get_upload_result(upload_url, title)
        
        save_wall_img = save_img_to_server(
            result_upload, vk_group_id, vk_access_token
        )
        answer = save_wall_img['response']
        for param in answer:
            media_id = param['id']
            img_owner_id = param['owner_id']
        publish_img_to_vk(
            media_id, img_owner_id, vk_group_id, vk_access_token, comment
        )
    except requests.HTTPError as error:
        print(f'Произошла ошибка {error}')
    finally:
        os.remove(f'{title}.png')


if __name__ == '__main__':
    main()

import requests

import time

import json

class VK:
    def __init__(self, token):
        self.token = token
    def get_photo(self, quantity_photo=5, album_id='profile'):
        url = 'https://api.vk.com/method/photos.get'
        param = {'extended': 'likes',
                 'album_id': album_id,
                 'access_token': self.token,
                 'v': '5.131'
                 }
        response = requests.get(url, params=param)
        items = response.json().get('response').get('items')
        photo_data = []
        photo_number = 0
        for item in items:
            sizes = item.get('sizes')
            max_size = 0
            index = 0
            for size in sizes:
                current_size = size.get('height') * size.get('width')
                if current_size > max_size:
                    max_size = current_size
                    index = sizes.index(size)
                if max_size == 0:
                    index = -1
            date = item.get('date')
            type = sizes[index].get('type')
            url = sizes[index].get('url')
            likes = item.get('likes').get('count')
            photo_data.append({'file_name': likes, 'file_url': url, 'type': type, 'date': date})
            photo_number += 1
            if photo_number == quantity_photo:
                break
        return photo_data

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def create_json(self, json_data):
        with open("new.json", 'w') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=2)

    def upload(self, file_path: str, url_dict):
        file_list = []
        json_data = []
        url_number = 0
        for file_item in url_dict:
            file = str(file_item.get('file_name'))
            file_url = file_item.get('file_url')
            file_date = file_item.get('date')
            file_type = file_item.get('type')
            if file in file_list:
                file = str(file) + str(time.strftime('_%d_%m_%y', time.gmtime(file_date)))
            else:
                file_list.append(file)
            headers = {'Accept': 'application/json',
                       'Authorization': 'OAuth {}'.format(self.token)}
            params = {'path': file_path + file,
                      'url': file_url}
            url = 'https://cloud-api.yandex.net/post/v1/disk/resources/upload'
            response = requests.post(url, headers=headers, params=params)
            quantity_url = len(url_dict)
            url_number += 1
            if response.status_code == 202:
                json_data.append({'file_name': file, 'size': file_type})
                print(f'Успешно записано {url_number}/{quantity_url}')
            else:
                print(f'Ошибка {url_number}/{quantity_url}')
        uploader.create_json(json_data)

response = VK('')
url_dict = response.get_photo(quantity_photo=10)
print(url_dict)

if __name__ == '__main__':
    token = ''
    uploader = YaUploader(token)
    result = uploader.upload('/1001/', url_dict)





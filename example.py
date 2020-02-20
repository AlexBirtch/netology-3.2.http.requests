from config import *
import requests
from pprint import pprint


# функция перевода текста
def translate_it(text, from_lang, to_lang):
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    params = {
        'key': MY_API,
        'text': text,
        'lang': f'{from_lang}-{to_lang}',
    }

    response = requests.get(URL, params=params)
    json_ = response.json()
    
    return ''.join(json_['text'])



# функция определения языка
def detect_lang(text):
    url = 'https://translate.yandex.net/api/v1.5/tr/detect'
    params = {
        'key': MY_API,
        'text': text,
        'hint': 'de,en',
    }

    response = requests.get(url, params=params)
    lang = response.text.split('"')[7]

    return lang



# функция получения текста из файла
def get_text(file_name):
    with open(file_name, encoding='utf-8') as f:
        file = f.read()

    return file



# функция загрузки файлов на я.диск
def upload(file_name, file_data):
    url = f'https://cloud-api.yandex.net/v1/disk/resources/upload?path=/netology/{file_name}&overwrite=true'
    data = file_data
    headers = {'Authorization': OAUTH_TOKEN,
               'Accept': 'application/json',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    session = requests.Session()
    request = session.get(url, headers=headers)

    # загружаем на я.диск
    href = request.json()['href']
    request_put = session.put(href, data=data.encode('utf-8'), headers=headers)



files_list = ['DE.txt', 'FR.txt', 'ES.txt']

if __name__ == '__main__':
    for file in files_list:
        from_lang = detect_lang(get_text(file))

        with open(f'From_{from_lang.upper()}.txt', 'w', encoding='utf-8') as to_file:
            try:
                to_file.write(translate_it(get_text(file), from_lang, 'ru'))

            except Exception as e:
                print(f'error: {e}')

        try:
            upload (str(to_file.name), get_text(to_file.name))
        except Exception as e:
            print(f'Error: {e}')
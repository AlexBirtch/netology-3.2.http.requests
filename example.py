from config import *
import requests


#  документация https://yandex.ru/dev/translate/doc/dg/reference/translate-docpage/

URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

def translate_it(text, from_lang, to_lang):
    """
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param to_lang:
    :return:
    """
    params = {
        'key': MY_API,
        'text': text,
        'lang': f'{from_lang}-{to_lang}',
    }

    response = requests.get(URL, params=params)
    json_ = response.json()
    return ''.join(json_['text'])



# функция возвращает текст из файла
def get_text(file_name):
    with open(file_name, encoding='utf-8') as f:
        file = f.read()

    return file



# функция для вычлинения данных href из сылки на скачивание
def get_href(link):
    href = link.split('"')[5] + link.split('"')[6] + link.split('"')[7]
    return href



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
    href = get_href(request.text).replace('href:', '')
    request_put = session.put(href, data=data.encode('utf-8'), headers=headers)




files_list = ['DE.txt', 'FR.txt', 'ES.txt']

if __name__ == '__main__':
    for file in files_list:
        f_lang = file.split('.')[0].lower()

        with open(f'From_{f_lang.upper()}.txt', 'w', encoding='utf-8') as to_file:
            try:
                to_file.write(translate_it(get_text(file), f_lang, 'ru'))

            except Exception as e:
                print(f'error: {e}')

        try:
            upload (str(to_file.name), get_text(to_file.name))
        except Exception as e:
            print(f'Error: {e}')
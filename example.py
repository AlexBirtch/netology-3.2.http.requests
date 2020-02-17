from pprint import pprint
from config import *
import requests


#  документация https://yandex.ru/dev/translate/doc/dg/reference/translate-docpage/

# headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
API_KEY = MY_API


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
        'key': API_KEY,
        'text': text,
        'lang': f'{from_lang}-{to_lang}',
    }

    response = requests.get(URL, params=params)
    json_ = response.json()
    return ''.join(json_['text'])



# функция которая возвращает текст из файла
def get_text(file_name):
    with open(file_name, encoding='utf-8') as f:
        file = f.read()

    return file



# download_href = '{"operation_id":"51543e23ac0e650aaa990045c0ad933f9c557f0ff89a2093e79f1ea724bb27a2","href":"https://uploader7g.disk.yandex.net:443/upload-target/20200217T162109.935.utd.615kru16haotkrc6y3nxfrpwg-k7g.13681529","method":"PUT","templated":false}'
# функция для вычлинения данных href из сылки на скачивание
def get_href(link):
    href = link.split('"')[5] + link.split('"')[6] + link.split('"')[7]
    return href



# функция загрузки файлов на я.диск
def upload(file_name, file_data):
    url = f'https://cloud-api.yandex.net/v1/disk/resources/upload?path={file_name}'
    data = file_data
    headers = {'Authorization': OAUTH_TOKEN,
               'Accept': 'application/json',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    session = requests.Session()
    request = session.get(url, headers=headers)

    pprint(request.text)
    print(request.status_code)

    # загружаем на я.диск
    # href = get_href(request.text)
    # request_put = session.put(href, data=data, headers=headers)

# upload('test.txt', get_text('FR.txt'))



files_list = ['DE.txt', 'FR.txt', 'ES.txt']

if __name__ == '__main__':
    for file in files_list:
        f_lang = file.split('.')[0].lower()
        
        with open(f'From_{f_lang.upper()}.txt', 'w', encoding='utf-8') as to_file:
            try:
                to_file.write(translate_it(get_text(file), f_lang, 'ru'))
            except Exception as e:
                print(f'error: {e}')
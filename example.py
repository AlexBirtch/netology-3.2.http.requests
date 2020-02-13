from config import *
import requests


#  документация https://yandex.ru/dev/translate/doc/dg/reference/translate-docpage/


API_KEY = MY_API
OAuth_token = OAUTH_TOKEN

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



files_list = ['DE.txt', 'FR.txt', 'ES.txt']

if __name__ == '__main__':
    for file in files_list:
        f_lang = file.split('.')[0].lower()
        
        with open(f'From_{f_lang.upper()}.txt', 'w', encoding='utf-8') as to_file:
            try:
                to_file.write(translate_it(get_text(file), f_lang, 'ru'))
            except Exception as e:
                print(f'error: {e}')
    print('Done')        
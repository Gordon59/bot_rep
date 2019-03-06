import requests
from time import sleep

token = '737950874:AAFi92BHYPJtUDlcIVIdg4CZg2quocm8dYo'
URL = "https://api.telegram.org/bot" + token + "/"

def get_btc():
    url = 'https://yobit.net/api/2/btc_usd/ticker'
    response= requests.get(url).json()
    price = response['ticker']['last']
    return str(int(price)) + ' usd'

global last_update_id
last_update_id = 0


def get_updates():
    url = URL + "getupdates"
    r = requests.get(url)
    return r.json()


def get_message():
    data = get_updates()

    last_object = data['result'][-1]
    current_update_id = last_object['update_id']

    global last_update_id
    if last_update_id != current_update_id:
        last_update_id = current_update_id
        chat_id = last_object['message']['chat']['id']
        text = last_object['message']['text']

        message = {'chat_id': chat_id,
                   'text': text}

        return message

    else:
        return None


def send_message(chat_id, text='Момент...'):
    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)


def main():

    while True:

        answer = get_message()

        if answer != None:
            chat_id = answer['chat_id']
            text = answer['text']

            if '/btc' in text:
                send_message(chat_id, get_btc())
        else:
            continue
        sleep(2)


if __name__ == '__main__':
    main()




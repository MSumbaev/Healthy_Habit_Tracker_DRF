import requests


def checking_users_for_chat_id(tg_bot_token, users_):
    """Проверка и запись поля tg_chat_id у юзера"""
    get_updates_url = f'https://api.telegram.org/bot{tg_bot_token}/getUpdates'
    response_json = requests.get(get_updates_url).json()

    usernames_r = {}
    for resp in response_json['result']:
        username = resp['message']['chat'].get('username')
        chat_id = resp['message']['chat'].get('id')
        usernames_r[username] = chat_id

    for user in users_:
        if user.tg_chat_id is None:
            user.tg_chat_id = usernames_r.get(user.tg_username)
            user.save()


def send_message(tg_bot_token, habit_):
    """Функция для отправки сообщения в telegram"""
    send_message_url = f'https://api.telegram.org/bot{tg_bot_token}/sendMessage'

    message_tg = (f'Привет!!!\n'
                  f'Вам нужно сделать: {habit_.action} в {habit_.time}\n'
                  f'Место действия: {habit_.place}\n'
                  f'Продолжительность действия: {habit_.length} сек.\n'
                  f'Вознаграждение: {habit_.reward}')

    if habit_.owner.tg_chat_id:
        data_for_request = {
            'chat_id': habit_.owner.tg_chat_id,
            'text': message_tg
        }

        requests.get(send_message_url, data=data_for_request)

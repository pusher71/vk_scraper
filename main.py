import PySimpleGUI as sg
import vk
import Token


# Получить список id друзей
def get_friends(api, user_id):
    try:
        # Сформировать список
        friends_list = []
        for friend_id in api.friends.get(user_id=user_id, order='hints')['items']:
            friends_list.append(friend_id)
        return friends_list
    except Exception:
        sg.Popup('Profile is closed!')
        return []


# Отобразить информацию по каждому id
def show_friends_info(api, w, id_list):
    output = []
    for current_id in id_list:
        friend_info = api.users.get(user_id=current_id)
        output.append('%d  %s %s' % (current_id, friend_info[0]['first_name'], friend_info[0]['last_name']))
    w['-LIST-'].Update(output)


# Авторизация
session = vk.Session(access_token=Token.get_token())
vk_api = vk.API(session, v='5.62')

# Интерфейс программы
layout = [[sg.Text('ID:', size=(400, 1))], [sg.InputText(size=(400, 1), default_text='154239070', key='-IN-')],
          [sg.Button('Find...', enable_events=True, key='-FUNCTION-', font='Arial')],
          [sg.Listbox(values=[], enable_events=True, size=(400, 800), key='-LIST-')]]
window = sg.Window('VK scraper', layout, size=(450, 900))

# Список id друзей
friends_ids = []

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == '-FUNCTION-':
        friends_ids = get_friends(vk_api, values['-IN-'])
        if len(friends_ids) > 0:
            show_friends_info(vk_api, window, friends_ids)
    elif event == '-LIST-':
        new_id = int(values['-LIST-'][0].split()[0])
        friends_ids = get_friends(vk_api, new_id)
        if len(friends_ids) > 0:
            window['-IN-'].Update(new_id)
            show_friends_info(vk_api, window, friends_ids)

window.close()

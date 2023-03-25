import requests
from geopy.geocoders import Nominatim
import json




url = 'http://26.76.95.107:8000/api/telegram/message/get'
rating_url = 'http://26.76.95.107:8000/api/telegram/rating/'

def get_locations(latitude, longitude, userid):
    geolocator = Nominatim(user_agent="5562707@mail.ru")
    print(latitude)
    print(longitude)
    print(userid)
    location = geolocator.reverse(f'{latitude}, {longitude}')
    print(location.address)
    

    return location.address

def rename_auto(word):
    count = 0
    address = []
    for i in word:

        address.append(i)
        count += 1
        if i == ',':
            break
    for i in word[count:]:
        address.append(i)
        if i == ',':
            break

    semi = ''.join(address)
    a = semi.replace(',', '')
    result = f"{a[count:]} {a[:count]}"
    return result


def post_data(address, report, chatid):
    data = {
        'address': address,
        'message': report,
        'userId': chatid,
    }
    print('TEEEEEEEEEEEESt', chatid)

    return requests.post(url, json=data)

def get_data(userid):
    print(userid)
    print('vizov')
    new_url = url+'?userId='+str(userid)
    response = requests.get(new_url)
    data = json.loads(response.text)
    list_data = []
    for user_data in data:
        user_address = user_data['address']
        user_date = user_data['date']
        user_message = user_data['message']
        user_stage = user_data['stage']
        if user_stage == 1:
            user_stage = 'Обрабатывается'
        elif user_stage == 2:
            user_stage = 'Обработан'
        elif user_stage == 3:
            user_stage = 'Взят'
        elif user_stage == 4:
            user_stage = 'Выполнен'
        message = f"Ваш адрес: {user_address}\nДата жалобы: {user_date}\nОписание проблемы: {user_message}\nСостояние: {user_stage}"
        
        list_data.append(message)
        
    return list_data

def post_rating(res, id):
    data = {
        'rating' : res,
        'reportId':id
    }
    return requests.post(rating_url, json=data)

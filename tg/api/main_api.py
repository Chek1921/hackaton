import requests
from geopy.geocoders import Nominatim

url = 'http://26.76.95.107:8000/api/telegram/message/get'

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



import requests


def get_interesting_places(latitude, longitude, radius):
    answer = []
    api_key = '5ae2e3f221c38a28845f05b61cf1179b03d61db07f013a1d1a33659f'
    url = f'https://api.opentripmap.com/0.1/en/places/radius?radius={radius}&lon={longitude}&lat={latitude}&kinds=interesting_places&apikey={api_key}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for place in data:
                res = []
                name = place['name']
                description = place['description']
                res.append(place['description'])
                res.append(f'Место: {name}')
                res.append(f'Описание: {description}')
                answer.append(res)
            return answer
        else:
            print(f'Ошибка при получении данных: {response.status_code}')
    except Exception as e:
        print(f'Ошибка: {e}')

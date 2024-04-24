import requests
import io

from PIL import Image


def make_appropriate_scale(result_tmp_response):
    size_information = result_tmp_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]['boundedBy']
    low_corner = size_information['Envelope']['lowerCorner'].split()
    upper_corner = size_information['Envelope']['upperCorner'].split()
    x_size = abs(float(upper_corner[0]) - float(low_corner[0]))
    y_size = abs(float(upper_corner[1]) - float(low_corner[1]))
    return f'{x_size},{y_size}'
class Geocodere:
     def __init__(self):
         self.answer = None
         self.flags = ''
         self.search_api_server = "https://search-maps.yandex.ru/v1/"
         yandex_address_api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
         self.search_params = {
            "apikey": yandex_address_api_key,
            "text": None,
            "lang": "ru_RU",
            "ll": None,
            "type": "biz"
         }
         self.map_static_api_server = "http://static-maps.yandex.ru/1.x/"
         self.map_static_params = {
                        "ll": None,
                        "spn": None,
                        "l": "map",
                        "pt": None }
     def set_ll(self, lon, lat):
         self.search_params['ll'] = f"{lon},{lat}"

     def set_place(self, text):
         self.search_params['text'] = text
     def make_response(self, amount):
         if not self.search_params['text'] and not self.search_params['ll']:
             print('Нет места или кординат')
         response = requests.get(self.search_api_server, params=self.search_params)
         if not response:
            print('Не удалось совершить запрос')
         json_response = response.json()
         organizations = json_response["features"][amount]
         org_name = organizations["properties"]["CompanyMetaData"]["name"]
         org_address = organizations["properties"]["CompanyMetaData"]["address"]
         self.answer = {
             'organizations': organizations,
             'org_name': org_name,
              'org_address': org_address
         }
         return self.answer

     def add_flag(self, flag):
         self.flag += flag
     def get_place_static(self, lon, lat):
         if self.answer:
             self.map_static_params['pt'] = make_appropriate_scale(self.answer)
             response = requests.get(self.map_static_api_server, params=self.map_static_params)
             image = Image.open(io.BytesIO(response))
             image.save(f'Statick/img/request{lon}{lat}')
             return response
         else:
             print('Совершите запрос')
     def get_statick_from_user_to_place(self, users_lon, users_lat, place_lon, place_lat):
        response = requests.get(self.map_static_api_server, params=self.map_static_params)

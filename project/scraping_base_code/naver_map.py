import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import time

headers = {
    'authority': 'map.naver.com',
    'accept': 'application/json, text/plain, */*',
    'pragma': 'no-cache',
    'expires': 'Sat, 01 Jan 2000 00:00:00 GMT',
    'cache-control': 'no-cache',
    'accept-language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'content-type': 'application/json',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://map.naver.com/',
    'cookie': 'NNB=DRLSKKQUUWQF6; NRTK=ag#20s_gr#1_ma#-2_si#0_en#0_sp#0; nx_ssl=2; nid_inf=846221169; NID_AUT=eflQwiOCYA4DLfFUQn+vXflklw+D/DPt5sexPfKfp8cBcfWc1BQruo7kHd4gAFDy; NID_JKL=Q96VTJeM09zkWgz3lYQAPl0TRIFbn/yVw2/F+gMxxQE=; BMR=s=1604507776121&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.nhn%3FblogId%3Dbinsoore%26logNo%3D221204112042%26proxyReferer%3Dhttps%3A%252F%252Fwww.google.com%252F&r2=https%3A%2F%2Fwww.google.com%2F; NID_SES=AAABwB7mOkHFpaZonbWZlOdwWfnhdGny2uRNN5SLHKhQwS6MndHZFomCeOeHEbGR0/nnuzesHImauk/SiLCORU54fPJtaXNU0pAJMZsPfadAXMXJX5QP5X6OjeeX3FIdF4y7KULgWuxBlrsP6RZfwWPHriL9aLxqtWFbb6qilAsqqBsm59khy1oFTWrkPHngn33Dc9dpuL+4jBF0gZS29lPKNhpE5Wsd+sfA5OA6eQPTBtS2EoJio2gF0pVqhAKbfGOWB8AvyctsVp2Bz6bhcnWQmxP58hXoGD1cMP382Fqd+EyvzM5PKVafiWenfFbCJ986ErE3G8BeYIKIKspeTlGzNK1BV7vt4JAtd0B1Fja1QbM0bOdRUW4xJ59CicuQHxMwDtQZ2YPD2XBVClghCzzjSvFMQ/W1QXhs9BbcEUeCM3jSi8E6CLInQ33Sar3YqWTbNafLTq+aOKFu1vdF0mRyyjPwqAUlbwytDjltBlKhZDV7Y80icStuhEodOUWHQq+Kkspqrat0w8mAzKA68Ny4VxAiCwuamYSgG5u/VJ2dwZYLk29cGusullRaxRxSR+ppAZW5S9Mplzp8ERi2Ud/m4j0=; _naver_usersession_=6vDZdgm/HN7p4iY2cZECbdQr; page_uid=UI7jRwp0J14ssuU2i0Cssssss3w-518229; page_uid=2feb99cf-d30e-4285-bec5-8ac1d3503c7b',
}

# params = (
#     ('caller', 'pcweb'),
#     ('query', '\uC774\uB300\uC6D0\uC7A5\uAD70\uBB18'),
#     ('type', 'all'),
#     ('searchCoord', '126.84076309204077;36.97142681292202'),
#     ('page', '1'),
#     ('displayCount', '1'),
#     ('isPlaceRecommendationReplace', 'true'),
#     ('lang', 'ko'),
# )

# response = requests.get('https://map.naver.com/v5/api/search', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://map.naver.com/v5/api/search?caller=pcweb&query=%EC%9D%B4%EB%8C%80%EC%9B%90%EC%9E%A5%EA%B5%B0%EB%AC%98&type=all&searchCoord=126.84076309204077;36.97142681292202&page=1&displayCount=20&isPlaceRecommendationReplace=true&lang=ko', headers=headers)
df = pd.read_csv("./place.csv")
id_list = list(df['id'])

location_dict = {
    'display' : [],
    'address' : [],
    'x' : [],
    'y' : []
}

display = []
address = []
x = [] 
y = []

# url만 변경해서 크롤링하기
for id in id_list :
    k = id.replace(' ','')

    params = (
    ('caller', 'pcweb'),
    ('query', k),
    ('type', 'all'),
    ('searchCoord', '126.84076309204077;36.97142681292202'),
    ('page', '1'),
    ('displayCount', '1'),
    ('isPlaceRecommendationReplace', 'true'),
    ('lang', 'ko'),
)

    response = requests.get('https://map.naver.com/v5/api/search', headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.text

    json_text = json.loads(text)

    if json_text['result']['place'] is not None :
        result = json_text['result']['place']['list']
        
        display.append(result[0]['display'])
        address.append(result[0]['address'])
        x.append(result[0]['x'])
        y.append(result[0]['y'])

        print(result[0]['display'])

location_dict['display'] += display
location_dict['address'] += address
location_dict['x'] += x
location_dict['y'] += y

location_list_pd = pd.DataFrame(location_dict)
location_list_pd.to_csv('location.csv')
print(location_list_pd)
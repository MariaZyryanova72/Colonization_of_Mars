from requests import get, post, delete

print(get('http://127.0.0.1:5000/api/v2/users').json())
print(get('http://127.0.0.1:5000/api/v2/users/1').json())
print(get('http://127.0.0.1:5000/api/v2/users/999').json())
print(get('http://127.0.0.1:5000/api/v2/users/p').json())

print(delete('http://127.0.0.1:5000/api/v2/users/1').json())
print(delete('http://127.0.0.1:5000/api/v2/users/999').json())
print(delete('http://127.0.0.1:5000/api/v2/users/m').json())

print(post('http://127.0.0.1:5000/api/v2/users',
           json={'surname': 'ла ла',
                 'name': "ВАСЯ", 'age': 10,
                 'city_from': "Тюмень", 'address': '', 'email': 'лала@mars.ru'}).json())
print(post('http://127.0.0.1:5000/api/v2/users',
           json={'surname': 'ла ла','age': 10,
                 'city_from': "Тюмень"}).json())
print(post('http://127.0.0.1:5000/api/v2/users',
           json={'name': "Вася",
                 'is_finished': False}).json())

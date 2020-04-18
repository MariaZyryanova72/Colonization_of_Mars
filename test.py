from requests import get, post, delete

print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/1').json())

print(post('http://localhost:5000/api/v2/users').json())
print(post('http://localhost:5000/api/v2/users',
           json={'name': 'Маша', 'city_from': "Москва"}).json())
print(post('http://localhost:5000/api/v2/users',
           json={'job': 'Заголовок', 'team_leader': 1, "collaborators": '1, 2'}).json())

print(delete('http://localhost:5000/api/v2/users/1').json())

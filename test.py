from requests import get, post, delete

print(get('http://127.0.0.1:5000/api/v2/jobs').json())
print(get('http://127.0.0.1:5000/api/v2/jobs/1').json())
print(get('http://127.0.0.1:5000/api/v2/jobs/999').json())
print(get('http://127.0.0.1:5000/api/v2/jobs/p').json())

print(delete('http://127.0.0.1:5000/api/v2/jobs/1').json())
print(delete('http://127.0.0.1:5000/api/v2/jobs/999').json())
print(delete('http://127.0.0.1:5000/api/v2/jobs/m').json())

print(post('http://127.0.0.1:5000/api/v2/jobs',
           json={'job': 'ла ла',
                 'team_leader': 1, 'work_size': 10, 'collaborators': "1, 2",
                 'is_finished': False}).json())
print(post('http://127.0.0.1:5000/api/v2/jobs',
           json={'team_leader': 1,
                 'is_finished': False}).json())

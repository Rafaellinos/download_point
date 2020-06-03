import requests
from pprint import pprint


def login(user, password):
    r = requests.get('http://127.0.0.1:5000/login', auth=(user, password))
    return r.json()

def get_users(token):
    headers = {'x-access-token': token}
    r = requests.get('http://127.0.0.1:5000/user', headers=headers)
    return r.json()

def get_user(token, user_id):
    headers = {'x-access-token': token}
    r = requests.get('http://127.0.0.1:5000/user/'+user_id, headers=headers)
    return r.json()

def update_user(public_id, **payload):
    r = requests.put('http://127.0.0.1:5000/user/'+public_id, data=payload)
    return r.json()

def register(user, passoword):
    r = requests.post('http://127.0.0.1:5000/user', data={'login': user, 'password': passoword})
    return r.json()

def get_files_list(token):
    headers = {'x-access-token': token}
    r = requests.get('http://127.0.0.1:5000/files', headers=headers)
    return r.json()

token = login('rafael2', '123').get('token')

#print(token)
#pprint(register('admin', '123'))

#pprint(get_users(token))

#pprint(get_files_list(token))
print(register('rafael','123'))

#pprint(get_user('asd', 'f23a5b2e-4f11-4154-aabc-badaf2c64a16'))

#pprint(update_user(token, 'f23a5b2e-4f11-4154-aabc-badaf2c64a16', login='rafael2'))
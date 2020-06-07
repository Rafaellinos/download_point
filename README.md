# Flask API para download

## Installation
docker-compose up -d
<br/>

## How it works

You can download files in the documents directory. 
But you need to register, login and use the token in order to do that.


## Quick start

```
# register
curl -d '{"login": "test", "password": "123"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/user
# login
token=$(curl --user test:123 http://127.0.0.1:5000/login | cut -c 13-185)
# token
echo $token
# get users
curl -H "Content-Type: application/json" -H "x-access-token: $(echo $token)" -X GET http://127.0.0.1:5000/user
# get list files
curl -H "Content-Type: application/json" -H "x-access-token: $(echo $token)" -X GET http://127.0.0.1:5000/files
# download the file
curl --output test.mp4 -H "Content-Type: application/json" -H "x-access-token: $(echo $token)" -X GET http://127.0.0.1:5000/download/video_example.mp4
```

## TODO

- [X] Map volumes
- [X] REST API Authentication - Basic or Bearer
- [ ] Basic user interface
- [ ] Filter files types
- [ ] Pagination
- [ ] Upload files
- [ ] Change sqlite to postgres because of reasons
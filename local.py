import  requests

print(requests.post("http://127.0.0.1:5000/login",{"email":"mail@mail.ru","role":"user","password":"qwe123"}))


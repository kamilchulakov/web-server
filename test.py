from requests import get, post, delete

cookies = dict(session='session cookies here')
print(post('http://localhost:8080/api/v1/news',
           json={'title': 'Заголовок', 'content': 'Текст новости', "picture": "Картинка",
                 'user_id': 1}, cookies=cookies).json())
print(get('http://localhost:8080/api/v1/news').json())
print(delete('http://localhost:8080/api/v1/news/5', cookies=cookies).json())
print(get('http://localhost:8080/api/v1/news').json())
print(get('http://localhost:8080/api/v1/orders/1').json())
print(get('http://localhost:8080/api/v1/matches').json())
print(get('http://localhost:8080/api/v1/storage').json())

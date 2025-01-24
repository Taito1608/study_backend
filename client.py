import requests

#一つ飛ばして2つ取得
res = requests.post(
    'http://localhost:8000/items/',
    json={'name': 'ぶどう', 'price': 200, 'description': '甘い'},
    )

print(res.status_code)
print(res.text)
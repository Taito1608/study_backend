import requests

#一つ飛ばして2つ取得
res = requests.get('http://localhost:8000/items/?skip=1&limit=2')

print(res.status_code)
print(res.text)
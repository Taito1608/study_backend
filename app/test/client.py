import requests

#一つ飛ばして2つ取得
res = requests.get('http://localhost:8000//todo/1')

print(res.status_code)
print(res.text)
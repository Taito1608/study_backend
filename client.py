import requests

#一つ飛ばして2つ取得
res = requests.get(
    'http://localhost:8000/sample/',
    headers={"Authorization": "Bearer hogehoge"},
    )

print(res.status_code)
print(res.text)
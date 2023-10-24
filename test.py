import requests
# 用來取得外部連結 URL API 資料

user_id = ''
secrect_api = ''

url = 'https://api.line.me/v2/bot/profile/' + user_id
headers = {'Authorization': 'Bearer ' + secrect_api}
response = requests.get(url, headers = headers)

user_name = 'Hello !'
if response.status_code == 200:
    user_profile = response.json()
    user_name = user_name + user_profile['displayName'] + 'work'

print(user_profile)
print(user_name)
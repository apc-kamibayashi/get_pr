import sys
import json
import requests

#変数の宣言
#owner = input('Please type owner: ')
owner = 'apc-kamibayashi'
#repo = input('Please type repository: ')
repo = 'test'
client_id = input('Please type client_id: ')
client_secret = input('Please type client_secret: ')
#socpe = input('Please type scope: ')
scope = 'repo'

auth_url = 'https://github.com/login/oauth/authorize?' + 'client_id=' + client_id + '&' + 'scope=' + scope
print('authorize_url: ' + auth_url)
print('please set authorize_url on your browser and enter')
code = input('Please type code: ')

access_token_url = 'https://github.com/login/oauth/access_token'
payload={'code':code, 'client_id':client_id, 'client_secret':client_secret}
res = requests.post(access_token_url,params=payload)
print(res.text)
data = res.text.split('&')
print(data)
access_token = data[0].strip('access_token=')
print('access_token: '+ access_token)

github_url = 'https://api.github.com/repos/%s/%s/pulls' % (owner, repo)
payload={'access_token':access_token}
res = requests.get(github_url,params=payload)
print(res.json())

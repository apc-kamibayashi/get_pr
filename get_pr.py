import sys
import json
import requests
import csv

#変数の宣言
#owner = input('Please type owner: ')
owner = 'apc-kamibayashi'
#repo = input('Please type repository: ')
repo = 'test'


client_id = input('Please type client_id: ')
client_secret = input('Please type client_secret: ')
#socpe = input('Please type scope: ')
scope = 'repo'

#アクセストークンを取得
# 認証URLをブラウザに打ってリダイレクトURLのcodeを入力
auth_url = 'https://github.com/login/oauth/authorize?' + 'client_id=' + client_id + '&' + 'scope=' + scope
print('authorize_url: ' + auth_url)
print('please set authorize_url on your browser and enter')
code = input('Please type code: ')
access_token_url = 'https://github.com/login/oauth/access_token'
payload={'code':code, 'client_id':client_id, 'client_secret':client_secret}
res = requests.post(access_token_url,params=payload)
data = res.text.split('&')
print(data) #エラー確認用に一時的に出力
access_token = data[0].strip('access_token=')
print('access_token: '+ access_token) #時々なぜか前後がかける…

#プルリクエストを取得
i = str(2)
github_url = 'https://api.github.com/repos/%s/%s/pulls/' % (owner,repo) + i
payload={'access_token':access_token}
res = requests.get(github_url,params=payload)
json_data = json.loads(res.text) #json_dataは辞書型
#csv_list = []
#csv_list.append(json_data['title'])
#csv_list.append(json_data['user']['login'])
#+ json_data['created_at'] + json_data['closed_at'] + json_data['comments']

#f = csv.writer(get_pr.csv)

#data = [{'題名'	'誰'	開始日時	クローズ日時	コメント数}]
#header = data[0].keys()#ヘッダー用のデータを作っておく

with open('get_pr.csv','wb') as f:
    # headerも渡してやる
    # 渡した順番が列の順番になる
    writer = csv.DictWriter(f)

    # そのままだとヘッダーは書き込まれないので、ここで書く
    #header_row = {"k":k for k in header}
    writer.writerow()



#1からプルリクナンバーのないところまで("message": "Not Found")
#title,

#テスト用にファイルに出力
#f = open("output.json", "w")
#json.dump(json_data, f, indent=4, sort_keys=True, separators=(',', ': '))

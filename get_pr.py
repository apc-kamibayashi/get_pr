import sys
import json
import requests
import csv
import os

#変数の宣言
#owner = input('Please type owner: ')
owner = 'apc-kamibayashi'
#repo = input('Please type repository: ')
repo = 'test'
client_id = input('Please type client_id: ')
client_secret = input('Please type client_secret: ')
#socpe = input('Please type scope: ')
scope = 'repo'#APIから取る値をリスト型で定義しておく
file_name = 'get_pr.csv'
api_param = {'題名':'title',
     '実施者':['user','login'],
     'PRオープン日時':'created_at',
     'PRクローズ日時':'closed_at',
     'コメント数':'comments'}

#CSVファイルのcolomnを作る
os.remove(file_name)

with open(file_name, 'a') as f:
    for i,key in enumerate(api_param):
        print(i)
        f.write(key)
        if i < len(api_param) - 1:
            f.write(',')
    f.write('\n')
f.closed

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
access_token = data[0].split('=')[1] #文字列の「access_token=」を削除
print('access_token: '+ access_token)

#プルリクの最大数を定義
github_url = 'https://api.github.com/repos/%s/%s/pulls' % (owner,repo)
payload={'access_token':access_token}
res = requests.get(github_url,params=payload)
pr_list_json_data = json.loads(res.text) #なぜかこのPRはリスト型のため注意
max_pr = pr_list_json_data[0]['number'] #numberはint型で取れる

#プルリクエストを取得
for i in range(1,max_pr+1):
    print(i)
    github_url = 'https://api.github.com/repos/%s/%s/pulls/' % (owner,repo) + str(i)
    payload={'access_token':access_token}
    res = requests.get(github_url,params=payload)
    pr_json_data = json.loads(res.text) #個別PRのjson_dataは辞書型
    #print(pr_json_data[api_param[0]])

    #CSVファイルへの書き込み
    with open(file_name,'a') as f:
        for i,value in enumerate(api_param):
            print(i)
            print(api_param[value])
            if isinstance(api_param[value],list) == 1:
                print(pr_json_data[api_param[value][0]][api_param[value][1]])
                string = pr_json_data[api_param[value][0]][api_param[value][1]]
                f.write(string)
            elif isinstance(pr_json_data[api_param[value]],int) == 1:
                print(pr_json_data[api_param[value]])
                string = str(pr_json_data[api_param[value]])
                f.write(string)
            elif isinstance(pr_json_data[api_param[value]],type(None)) != 1:
                print(pr_json_data[api_param[value]])
                string = pr_json_data[api_param[value]]
                f.write(string)
            if i < len(api_param)-1:
                 f.write(',')
        f.write('\n')
    f.closed

    # #data = [{'題名'	'誰'	開始日時	クローズ日時	コメント数}]
#header = data[0].keys()#ヘッダー用のデータを作っておく

#cols = json_data[0].keys()
#print(cols)


    # そのままだとヘッダーは書き込まれないので、ここで書く
    #header_row = {"k":k for k in header}
    #writer.writerow()

#1からプルリクナンバーのないところまで("message": "Not Found")
#title,

#テスト用にファイルに出力
#f = open("output.json", "w")
#json.dump(pr_json_data, f, indent=4, sort_keys=True, separators=(',', ': '))

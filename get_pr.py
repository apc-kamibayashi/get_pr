#test

import sys
import json
import requests
import csv
import os
import datetime

#github関連変数の宣言
#owner = input('Please type owner: ')
#owner = 'apc-kamibayashi'
owner = 'tamac-io'
#repo = input('Please type repository: ')
#repo = 'test'
repo = 'logging-controller'
client_id = input('Please type client_id: ')
client_secret = input('Please type client_secret: ')
#socpe = input('Please type scope: ')
scope = 'repo'#APIから取る値をリスト型で定義しておく

#その他の利用ファイルなどの定義
now = datetime.datetime.now()
file_name = 'get_pr_{0:%Y%m%d-%H%M%S}.csv'.format(now)
api_param = {
    u'No.':'number',
    u'プルリク名':'title',
    u'実施者':['user','login'], #取りたいJSONが二段の場合リストで定義。今のところ二段まで。
    u'PRオープン日時':'created_at',
    u'PRクローズ日時':'closed_at',
    u'レビューコメント数':'review_comments',
    u'コメント数':'comments',
    u'コミット数':'commits',
    u'マージ':'merged',
    u'ファイル変更数':'changed_files'
}

#CSVファイルのcolomnを作る
if os.path.exists(file_name):
    os.remove(file_name)

with open(file_name, 'a') as f:
    for i,key in enumerate(api_param):
        #print(i)
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
#print(data) #エラー確認用に一時的に出力
access_token = data[0].split('=')[1] #文字列の「access_token=」を削除
#print('access_token: '+ access_token) #エラー確認用に一時的に出力

#プルリクの最大数を定義
github_url = 'https://api.github.com/repos/%s/%s/pulls' % (owner,repo)
payload={'access_token':access_token}
res = requests.get(github_url,params=payload)
pr_list_json_data = json.loads(res.text) #なぜかこのPRはリスト型のため注意
#print(pr_list_json_data) #エラー確認用に一時的に出力
max_pr = pr_list_json_data[0]['number'] #numberはint型で取れる

#テスト用にファイルに出力
#f = open("output.json", "w")
#json.dump(pr_list_json_data, f, indent=4, sort_keys=True, separators=(',', ': '))

#プルリクエストを取得
for i in range(1,max_pr+1):
    #print(i) #エラー確認用に一時的に出力
    github_url = 'https://api.github.com/repos/%s/%s/pulls/' % (owner,repo) + str(i)
    payload={'access_token':access_token}
    res = requests.get(github_url,params=payload)
    pr_json_data = json.loads(res.text) #個別PRのjson_dataは辞書型
    #print(pr_json_data[api_param[0]]) #エラー確認用に一時的に出力

    #CSVファイルへの書き込み
    with open(file_name,'a') as f:
        for i,value in enumerate(api_param):
            #print(i) #エラー確認用に一時的に出力
            #print(api_param[value]) #エラー確認用に一時的に出力
            if isinstance(api_param[value],list) == 1: #取りたいJSONが二段だった場合(二段まで対応)
                #print(pr_json_data[api_param[value][0]][api_param[value][1]]) #エラー確認用に一時的に出力
                f.write(pr_json_data[api_param[value][0]][api_param[value][1]])
            elif isinstance(pr_json_data[api_param[value]],int) == 1: #取ったデータが整数だった場合
                #print(pr_json_data[api_param[value]]) #エラー確認用に一時的に出力
                f.write(str(pr_json_data[api_param[value]]))
            elif isinstance(pr_json_data[api_param[value]],type(None)) != 1: #取ったデータがNULLだった場合
                #print(pr_json_data[api_param[value]]) #エラー確認用に一時的に出力
                f.write(pr_json_data[api_param[value]])
            if i < len(api_param)-1: #最終項目の一つ前までカンマを入れる
                 f.write(',')
        f.write('\n')
    f.closed
''''''
github_url = 'https://api.github.com/repos/%s/%s/pulls/' % (owner, repo) + str(21) #+ '/files'
payload = {'access_token': access_token}
res = requests.get(github_url, params=payload)
pr_json_data = json.loads(res.text)  # 個別PRのjson_dataは辞書型

#テスト用にファイルに出力
f = open("output.json", "w")
json.dump(pr_json_data, f, indent=4, sort_keys=True, separators=(',', ': '))
''''''
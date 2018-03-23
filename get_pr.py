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
api_param = { #取りたいAPIパラメータのカラム名定義と取る値定義
    u'No.':'number',
    u'プルリク名':'title',
    u'実施者':['user','login'], #取りたいJSONが二段の場合リストで定義。今のところ二段まで。
    u'PRオープン日時':'created_at',
    u'PRクローズ日時':'closed_at',
    u'レビューコメント数':'review_comments',
    u'コメント数':'comments',
    u'コミット数':'commits',
    u'マージ':'merged',
    u'ファイル変更数':'changed_files' #ファイル変更数がある場合のみ別の関数が走るため、後ろ推奨
}

file_param = { #取りたいファイル変更分パラメータのカラム名定義と取る値定義
    u'追加': 'additions',
    u'削除': 'deletions'
}

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

#プルリクの最大数を定義ver2：オープンがなくても抜けられる
for i in range(1,65535): #とりあえず65535くらいに設定
    #print(i) #エラー確認用に一時的に出力
    github_url = 'https://api.github.com/repos/%s/%s/pulls/' % (owner,repo) + str(i)
    res = requests.get(github_url,params=payload)
    pr_json_data = json.loads(res.text) #個別PRのjson_dataは辞書型
    #print(pr_json_data) #エラー確認用に一時的に出力
    if ('message' in pr_json_data) == 1:
        max_pr = i - 1
        break

#columnのためにchanged_filesの最大数をとる
for i in range(1,65535): #とりあえず65535くらいに設定
    #print(i) #エラー確認用に一時的に出力
    github_url = 'https://api.github.com/repos/%s/%s/pulls/' % (owner,repo) + str(i)
    res = requests.get(github_url,params=payload)
    pr_json_data = json.loads(res.text) #個別PRのjson_dataは辞書型
    #print(pr_json_data) #エラー確認用に一時的に出力
    if ('message' in pr_json_data) == 1:
        max_pr = i - 1
        break

#テスト用にファイルに出力
#f = open("output.json", "w")
#json.dump(pr_list_json_data, f, indent=4, sort_keys=True, separators=(',', ': '))

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

str = ''

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
                str = str + pr_json_data[api_param[value][0]][api_param[value][1]]
            elif isinstance(pr_json_data[api_param[value]],int) == 1: #取ったデータが整数だった場合
                #print(pr_json_data[api_param[value]]) #エラー確認用に一時的に出力
                str = str + str(pr_json_data[api_param[value]])
            elif isinstance(pr_json_data[api_param[value]],type(None)) != 1: #取ったデータがNULLじゃない場合
                #print(pr_json_data[api_param[value]]) #エラー確認用に一時的に出力
                str = str + pr_json_data[api_param[value]]
            str = str + ','
        if 'changed_files' in api_param.values():
            change_file = check_change_file(access_token, github_url, pr_json_data['changed_files'], file_param)
            for i in range(pr_json_data['changed_files']):
                for j,key in enumerate(file_param[i]):
                    str = str + change_file[i][j][key] + ','
        str = str[:-1] + '\n'
        f.write(str)
    f.closed

def check_change_file(access_token,url,file_num,file_param):
    """リスト型で各リストはファイルの追加・削除の辞書型で返す"""
    prfile_url = url + '/files'
    payload = {'access_token': access_token}
    res = requests.get(prfile_url, params=payload)
    prfile_json_data = json.loads(res.text)  # 個別PRのjson_dataは辞書型
    list = []
    for i in range(1,file_num+1)
        list.append({file_param{key}:file_param})
'''
'''
#テスト用にファイルに出力
f = open("output.json", "w")
json.dump(pr_json_data, f, indent=4, sort_keys=True, separators=(',', ': '))
'''
# Twitter API情報を読み込み
from dotenv import load_dotenv
import os
import pandas as pd
import datetime
load_dotenv('.env')
# 参考
# https://talosta.hatenablog.com/entry/auto-remove-202201

# Twitter APIのkey情報を登録
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

import tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit = True)

account = "@CancaoNovaChor"

cols = ['user_id']
follower_ids = pd.DataFrame([], columns=cols)
following_ids = pd.DataFrame([], columns=cols)

# フォロワーの取得
print('フォロワーを取得中...', end='')
itr = tweepy.Cursor(api.get_follower_ids, user_id=account, cursor=-1).items()
for follower_id in itr:
    record = pd.Series([follower_id], index=follower_ids.columns)
    follower_ids = follower_ids.append(record, ignore_index=True)
print(' Done')
print(follower_ids)
#現在時刻を取得
now = datetime.datetime.now()
#ファイル名を作成
filename = 'data/follower_ids_' + now.strftime('%Y%m%d_%H%M%S') + '.csv'
#ファイルに保存
follower_ids.to_csv(filename, index=False)


# フォローしている人の取得
print('フォローしている人を取得中...', end='')
itr = tweepy.Cursor(api.get_friend_ids, user_id=account, cursor=-1).items() 
for following_id in itr:
    record = pd.Series([following_id], index=following_ids.columns)
    following_ids = following_ids.append(record, ignore_index=True)
print(' Done')
print(following_ids)

#ファイル名を作成
filename = 'data/following_ids_' + now.strftime('%Y%m%d_%H%M%S') + '.csv'
#ファイルに保存
following_ids.to_csv(filename, index=False)

'''
oneside_follow = pd.DataFrame([], columns=['user_id', 'name', 'screen_name', 'description'])

# 一方的にフォローしている人を抽出
print('一方的にフォローしている人を取得中...', end='')
for following_id in following_ids['user_id']:
    if following_id not in follower_ids['user_id'].values:
        user = api.get_user(user_id=following_id)
        record = pd.Series([user.id, user.name, user.screen_name, user.description], index=oneside_follow.columns)
        oneside_follow = oneside_follow.append(record, ignore_index=True)
print(' Done')


print(oneside_follow)
'''
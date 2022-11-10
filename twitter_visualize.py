import streamlit as st
import pandas as pd
import glob
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


st.title("CancaoNova Twitter Analysis App")

# 現在のフォロワー数を表示
st.subheader("Current Follower Count")
# フォロワー数情報を読み込み
follower_list = glob.glob('data/follower_ids_*.csv')
# 最新の日付のファイルを読み込み
follower_list.sort()
follower_df = pd.read_csv(follower_list[-1])
st.write(len(follower_df))

# 現在のフォロー数を表示
st.subheader("Current Following Count")
# フォロー数情報を読み込み
following_list = glob.glob('data/following_ids_*.csv')
# 最新の日付のファイルを読み込み
following_list.sort()
following_df = pd.read_csv(following_list[-1])
st.write(len(following_df))

# フォロワー数の推移を表示
st.subheader("Follower Count History")
follower_transition_df = pd.DataFrame([], columns=['date', 'count'])
for follower_file in follower_list:
    df = pd.read_csv(follower_file)
    date = follower_file.split('_')[2]
    # 日付をdatetime型に変換
    date = pd.to_datetime(date, format='%Y%m%d')
    record = pd.Series([date, len(df)], index=follower_transition_df.columns)
    follower_transition_df = follower_transition_df.append(record, ignore_index=True)
print(follower_transition_df)

# グラフ表示
st.line_chart(follower_transition_df['count'])
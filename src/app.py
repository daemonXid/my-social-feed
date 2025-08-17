# src/app.py (최종 완성본)

import streamlit as st
import pandas as pd
from my_social_feed.data_manager import load_posts, save_post, load_retweets, save_like, add_retweet # 필요한 모든 함수를 가져옵니다.
from my_social_feed.models import Post
from my_social_feed import ui_components

# --- 1. 페이지 기본 설정 ---
st.set_page_config(page_title="My Social Feed", layout="centered")
st.title("My Social Feed 🍜")

# --- 2. 게시글 작성 UI 및 로직 처리 ---
author, content = ui_components.display_post_editor()
if st.button("게시하기"):
    if author and content:
        new_post = Post(content=content, author=author)
        save_post(new_post)
        st.success("게시글이 성공적으로 작성되었습니다!")
        st.rerun()
    else:
        st.warning("작성자 이름과 내용을 모두 입력해주세요.")

# --- 3. 피드 데이터 준비 (가장 중요!) ---
# 모든 데이터 준비가 끝난 후, 마지막에 딱 한번만 화면에 그립니다.

# 3-1. 원본 게시글과 리트윗 기록을 불러옵니다.
posts_df = load_posts()
retweets_df = load_retweets()

# 3-2. 피드의 기초가 될 원본 게시글 데이터를 복사합니다.
feed_df = posts_df.copy()
feed_df['retweet_user_id'] = pd.NA # 리트윗이 아님을 표시하는 열 추가

# 3-3. 리트윗 기록이 있을 경우에만, 원본 게시글과 합치는 작업을 수행합니다.
if not retweets_df.empty:
    # 'original_post_id'를 기준으로 리트윗 기록과 원본 게시글 정보를 합칩니다.
    retweeted_posts_df = pd.merge(retweets_df, posts_df, left_on='original_post_id', right_on='post_id', how='inner')
    
    # 정렬을 위해 리트윗 시간을 대표 시간으로 사용합니다.
    retweeted_posts_df['timestamp'] = retweeted_posts_df['timestamp_x'] 
    
    # 필요한 열만 선택하여 최종 피드 형식에 맞춥니다.
    retweeted_posts_df = retweeted_posts_df[['retweet_user_id', 'author', 'content', 'timestamp', 'post_id']]

    # 원본 게시글만 있던 피드에 리트윗된 게시글 데이터를 추가합니다.
    feed_df = pd.concat([feed_df, retweeted_posts_df], ignore_index=True)

# 3-4. 모든 데이터가 합쳐진 최종 피드를 시간순으로 정렬합니다.
sorted_feed = feed_df.sort_values(by="timestamp", ascending=False)

# --- 4. 최종 피드 표시 ---
# 모든 데이터 준비가 끝났으므로, 마지막에 딱 한번만 화면에 그립니다.
ui_components.display_feed(sorted_feed)
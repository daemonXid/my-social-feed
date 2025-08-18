# src/app.py (최종 정리본)

import streamlit as st
import pandas as pd

from src.my_social_feed.data_manager import (
    load_posts, save_post, load_retweets,
    save_like, add_retweet, save_comment, load_comments
)
from src.my_social_feed.models import Post
from src.my_social_feed import ui_components

st.set_page_config(page_title="My Social Feed", layout="centered")

# --- 1. 로그인 상태 확인 ---  
# st.session_state에 'user_id'가 없으면 로그인하지 않은 상태로 간주합니다.
if 'user_id' not in st.session_state:
    ui_components.display_login_form()

# --- 2. 로그인된 경우 메인 앱 표시 ---
else:
    # 사이드바에 프로필 표시
    ui_components.display_sidebar_profile()

    st.title("My Social Feed 🍜")

    # --- 게시글 작성 UI 및 로직 ---
    # 이제 글 작성자는 로그인한 사용자로 고정되므로, author를 받을 필요가 없습니다.
    content = ui_components.display_post_editor()
    if st.button("게시하기"):
        if content:
            # 글 작성자를 현재 로그인한 사용자로 자동 설정합니다.
            new_post = Post(content=content, author=st.session_state['user_id'])
            save_post(new_post)
            st.success("게시글이 성공적으로 작성되었습니다!")
            st.rerun()
        else:
            st.warning("내용을 입력해주세요.")

    # --- 피드 데이터 준비 및 표시 ---
    posts_df = load_posts()
    retweets_df = load_retweets()

    feed_df = posts_df.copy()
    feed_df['retweet_user_id'] = pd.NA

    if not retweets_df.empty:
        retweeted_posts_df = pd.merge(retweets_df, posts_df, left_on='original_post_id', right_on='post_id', how='inner')
        retweeted_posts_df['timestamp'] = retweeted_posts_df['timestamp_x']
        retweeted_posts_df = retweeted_posts_df[['retweet_user_id', 'author', 'content', 'timestamp', 'post_id']]
        feed_df = pd.concat([feed_df, retweeted_posts_df], ignore_index=True)

    sorted_feed = feed_df.sort_values(by="timestamp", ascending=False)
    ui_components.display_feed(sorted_feed)
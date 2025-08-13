# src/app.py
import streamlit as st
from my_social_feed.data_manager import load_posts, save_post
from my_social_feed.models import Post
from my_social_feed import ui_components # ui_components 모듈을 가져옵니다.

# --- 페이지 설정 ---
st.set_page_config(page_title="My Social Feed", layout="centered")
st.title("My Social Feed 🍜")

# --- UI 컴포넌트 호출 및 로직 처리 ---

# 1. 게시글 작성 UI 표시 및 사용자 입력 받기
author, content = ui_components.display_post_editor()

# 2. '게시하기' 버튼 로직 처리
if st.button("게시하기"):
    if author and content:
        new_post = Post(content=content, author=author)
        save_post(new_post)
        st.success("게시글이 성공적으로 작성되었습니다!")
        st.rerun() # 화면을 새로고침하여 즉시 피드에 반영
    else:
        st.warning("작성자 이름과 내용을 모두 입력해주세요.")

# 3. 데이터 로드 및 피드 표시
posts_df = load_posts()
sorted_posts = posts_df.sort_values(by="timestamp", ascending=False)
ui_components.display_feed(sorted_posts)
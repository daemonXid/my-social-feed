# src/my_social_feed/ui_components.py (최종 완성본)

import streamlit as st
import pandas as pd
from .data_manager import (
    get_like_count, save_like, add_retweet, 
    save_comment, load_comments, create_user, get_user
)
import re                       # youtube URL 검증을 위한 모듈

# --- YouTube 비디오 ID를 추출하는 헬퍼 함수 ---
def get_youtube_video_id(url: str):
    """YouTube URL에서 비디오 ID를 추출합니다."""
    if url is None:
        return None
    # 표준, 단축, 임베드 URL 등 다양한 형식을 지원하는 정규표현식
    regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None


def display_post_editor():
    """게시글 작성을 위한 UI 컴포넌트를 표시합니다."""
    # 로그인 후에는 작성자 이름을 받을 필요가 없으므로 내용만 받습니다.
    post_content = st.text_area("무슨 생각을 하고 있나요?", key="content_input")
    return post_content

def display_feed(feed_df: pd.DataFrame):
    """게시글과 리트윗이 통합된 피드를 화면에 표시하고, 각 게시글에 댓글 기능을 추가합니다."""
    st.header("피드")
    if feed_df.empty:
        st.info("아직 작성된 글이 없습니다. 첫 글을 작성해보세요!")
    else:
        for index, row in feed_df.iterrows():
            with st.container(border=True):
                # --- 1. 게시글 또는 리트윗 표시 ---
                is_retweet = pd.notna(row.get('retweet_user_id'))
                post_id = row['post_id']

                # 리트윗 여부에 따라 고유한 key 접두사 생성 (중복 오류 방지)
                if is_retweet:
                    unique_key_prefix = f"retweet_{row['retweet_user_id']}_{row['timestamp']}"
                    st.markdown(f"🔁 **{row['retweet_user_id']}** 님이 리트윗했습니다.")
                else:
                    unique_key_prefix = "post"

                st.write(f"**작성자:** {row['author']}")
                st.write(f"**내용:** {row['content']}")
                st.caption(f"작성 시각: {row['timestamp']}")
                
                # --- 2. 좋아요/리트윗 버튼 ---
                like_count = get_like_count(post_id)
                col1, col2, col3 = st.columns([1, 1, 8]) 
                with col1:
                    if st.button("👍", key=f"like_{unique_key_prefix}_{post_id}"):
                        save_like(post_id, st.session_state.get('user_id', 'guest'))
                        st.rerun() 
                with col2:
                    if not is_retweet:
                        if st.button("🔁", key=f"retweet_{unique_key_prefix}_{post_id}"):
                            add_retweet(post_id, st.session_state.get('user_id', 'guest'))
                            st.rerun()
                with col3:
                    st.write(f"{like_count}명이 좋아합니다.")
                
                st.divider()
                
                # --- 3. 댓글 표시 ---
                comments_df = load_comments(post_id)
                for c_index, c_row in comments_df.iterrows():
                    # for문 다음 블록은 반드시 들여쓰기 되어야 합니다.
                    with st.container(border=True):
                        st.write(f"**{c_row['author']}**: {c_row['content']}")
                        
                        # 미디어 URL이 있다면, 이미지나 비디오를 표시
                        if pd.notna(c_row['media_url']) and c_row['media_url']:
                            # if문 다음 블록은 반드시 들여쓰기 되어야 합니다.
                            media_url = c_row['media_url']
                            
                            video_id = get_youtube_video_id(media_url)
                            if video_id:
                                # st.video 대신 iframe으로 직접 임베드
                                embed_url = f"https://www.youtube.com/embed/{video_id}"
                                st.markdown(f'<iframe width="560" height="315" src="{embed_url}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>', unsafe_allow_html=True)
                            elif any(media_url.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
                                st.image(media_url)
                                
                        st.caption(f"{c_row['timestamp']}")
                
                # --- 4. 새 댓글 작성 폼 ---
                # 모든 key에 unique_key_prefix를 추가하여 중복을 방지합니다.
                comment_author = st.text_input("이름", key=f"comment_author_{unique_key_prefix}_{post_id}")
                comment_content = st.text_input("댓글 내용", key=f"comment_content_{unique_key_prefix}_{post_id}")
                comment_media_url = st.text_input("이미지/YouTube URL (선택)", key=f"comment_media_{unique_key_prefix}_{post_id}")
                
                if st.button("댓글 달기", key=f"comment_submit_{unique_key_prefix}_{post_id}"):
                    if comment_author and comment_content:
                        save_comment(post_id, comment_author, comment_content, comment_media_url)
                        st.rerun()
                    else:
                        st.warning("이름과 댓글 내용을 모두 입력해주세요.")

def display_login_form():
    """로그인 및 회원가입 폼을 표시합니다."""
    st.header("로그인 / 회원가입")
    
    login_tab, signup_tab = st.tabs(["로그인", "회원가입"])

    with login_tab:
        with st.form("login_form"):
            login_id = st.text_input("아이디")
            login_password = st.text_input("비밀번호", type="password")
            login_submitted = st.form_submit_button("로그인")
            
            if login_submitted:
                user_data = get_user(login_id)
                if user_data is not None and user_data['password'] == login_password:
                    st.session_state['user_id'] = login_id
                    st.rerun()
                else:
                    st.error("아이디 또는 비밀번호가 잘못되었습니다.")

    with signup_tab:
        with st.form("signup_form"):
            signup_id = st.text_input("사용할 아이디")
            signup_password = st.text_input("사용할 비밀번호", type="password")
            signup_submitted = st.form_submit_button("회원가입")

            if signup_submitted:
                if create_user(signup_id, signup_password):
                    st.success("회원가입이 완료되었습니다. 로그인 탭에서 로그인해주세요.")
                else:
                    st.error("이미 존재하는 아이디입니다.")

def display_sidebar_profile():
    """사이드바에 사용자 프로필과 로그아웃 버튼을 표시합니다."""
    with st.sidebar:
        st.header(f"환영합니다, {st.session_state['user_id']}님!")
        
        if st.button("로그아웃"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
# src/my_social_feed/ui_components.py
import streamlit as st
import pandas as pd
from .data_manager import get_like_count, save_like, add_retweet # data_manager의 함수들을 가져옴


def display_post_editor():
    """게시글 작성을 위한 UI 컴포넌트를 표시합니다."""
    st.header("새 글 작성하기")
    author_name = st.text_input("작성자 이름을 입력하세요:", key="author_input")
    post_content = st.text_area("무슨 생각을 하고 있나요?", key="content_input")
    
    # 이 함수는 사용자가 입력한 값을 반환하여 app.py에서 사용할 수 있도록 합니다.
    return author_name, post_content

def display_feed(feed_df: pd.DataFrame):
    """게시글과 리트윗이 통합된 피드를 화면에 표시합니다."""
    st.header("피드")
    if feed_df.empty:
        st.info("아직 작성된 글이 없습니다. 첫 글을 작성해보세요!")
    else:
        for index, row in feed_df.iterrows():
            with st.container(border=True):
                
                is_retweet = pd.notna(row.get('retweet_user_id'))
                post_id = row['post_id']

                # --- 여기가 핵심 수정 지점입니다 ---
                # 리트윗 여부에 따라 버튼 key에 사용할 고유한 접두사(prefix)를 만듭니다.
                if is_retweet:
                    # 리트윗인 경우: 리트윗한 사람과 시간을 key에 포함시켜 고유하게 만듭니다.
                    unique_key_prefix = f"retweet_{row['retweet_user_id']}_{row['timestamp']}"
                    st.markdown(f"🔁 **{row['retweet_user_id']}** 님이 리트윗했습니다.")
                else:
                    # 원본 게시글인 경우: 'post'라는 접두사를 사용합니다.
                    unique_key_prefix = "post"

                st.write(f"**작성자:** {row['author']}")
                st.write(f"**내용:** {row['content']}")
                st.caption(f"작성 시각: {row['timestamp']}")
                
                like_count = get_like_count(post_id)
                
                col1, col2, col3 = st.columns([1, 1, 8]) 
                with col1:
                    # 생성한 고유 접두사를 key에 추가합니다.
                    if st.button("👍", key=f"like_{unique_key_prefix}_{post_id}"):
                        save_like(post_id, "current_user")
                        st.rerun() 
                
                with col2:
                    if not is_retweet:
                        # 생성한 고유 접두사를 key에 추가합니다.
                        if st.button("🔁", key=f"retweet_{unique_key_prefix}_{post_id}"):
                            add_retweet(post_id, "current_user")
                            st.rerun()
                
                with col3:
                    st.write(f"{like_count}명이 좋아합니다.")








# src/my_social_feed/ui_components.py
import streamlit as st
import pandas as pd
from .data_manager import get_like_count, save_like # data_manager의 함수들을 가져옴


def display_post_editor():
    """게시글 작성을 위한 UI 컴포넌트를 표시합니다."""
    st.header("새 글 작성하기")
    author_name = st.text_input("작성자 이름을 입력하세요:", key="author_input")
    post_content = st.text_area("무슨 생각을 하고 있나요?", key="content_input")
    
    # 이 함수는 사용자가 입력한 값을 반환하여 app.py에서 사용할 수 있도록 합니다.
    return author_name, post_content

def display_feed(posts_df: pd.DataFrame):
    """게시글 피드를 화면에 표시합니다."""
    st.header("피드")
    if posts_df.empty:
        st.info("아직 작성된 글이 없습니다. 첫 글을 작성해보세요!")
    else:
        # 각 게시글을 순회하며 표시
        for index, row in posts_df.iterrows():
            with st.container(border=True):
                st.write(f"**작성자:** {row['author']}")
                st.write(f"**내용:** {row['content']}")
                st.caption(f"작성 시각: {row['timestamp']}")
                # 여기에 나중에 좋아요/리트윗 버튼이 추가됩니다.

                like_count = get_like_count(post_id)

                # st.columns를 사용해 버튼과 텍스트를 나란히 배치
                col1, col2 = st.columns([1, 10]) 
                with col1:
                    # 버튼의 key를 post_id로 설정하여 각 버튼을 고유하게 만듦
                    if st.button("👍", key=f"like_{post_id}"):
                        # 현재는 '좋아요' 누를 사용자를 'test_user'로 고정
                        # 나중에 사용자 인증 기능이 생기면 실제 사용자 이름으로 바꿔야 함
                        save_like(post_id, "test_user")
                        st.rerun() # '좋아요' 클릭 시 즉시 화면 새로고침

                with col2:
                    st.write(f"{like_count}명이 좋아합니다.")



# src/my_social_feed/data_manager.py
import pandas as pd
from .models import Post
import os

POSTS_FILEPATH = "data/posts.csv"

def save_post(post: Post):
    """새로운 Post 객체를 CSV 파일에 추가합니다."""
    # 파일이 없으면 헤더와 함께 새로 생성
    if not os.path.exists(POSTS_FILEPATH):
        df = pd.DataFrame([post.__dict__])
        df.to_csv(POSTS_FILEPATH, index=False)
    # 파일이 있으면 기존 데이터에 추가
    else:
        df = pd.DataFrame([post.__dict__])
        df.to_csv(POSTS_FILEPATH, mode='a', header=False, index=False)

def load_posts() -> pd.DataFrame:
    """CSV 파일에서 모든 게시글을 불러와 DataFrame으로 반환합니다."""
    if not os.path.exists(POSTS_FILEPATH) or os.path.getsize(POSTS_FILEPATH) == 0:
        # 파일이 없거나 비어있으면 빈 DataFrame 반환
        return pd.DataFrame(columns=['post_id', 'author', 'content', 'timestamp'])

    posts_df = pd.read_csv(POSTS_FILEPATH)
    return posts_df


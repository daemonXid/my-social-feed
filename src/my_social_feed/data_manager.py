# src/my_social_feed/data_manager.py
import pandas as pd
from .models import Post
import os
import datetime #timestamp를 위해 추가
import uuid # comment_id 를 위해 추가

POSTS_FILEPATH = "data/posts.csv"                       # 게시글 데이터를 저장할 파일 경로

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


LIKES_FILEPATH = "data/likes.csv"                    # '좋아요' 데이터를 저장할 파일 경로

def save_like(post_id: str, author: str):                 
    """'좋아요' 데이터를 CSV 파일에 추가합니다."""
    if not os.path.exists(LIKES_FILEPATH):
        df = pd.DataFrame([{'post_id': post_id, 'author': author}])
        df.to_csv(LIKES_FILEPATH, index=False)
    else:
        df = pd.DataFrame([{'post_id': post_id, 'author': author}])
        df.to_csv(LIKES_FILEPATH, mode='a', header=False, index=False)

def get_like_count(post_id: str) -> int:
    """특정 게시글의 '좋아요' 개수를 반환합니다."""
    if not os.path.exists(LIKES_FILEPATH):
        return 0

    likes_df = pd.read_csv(LIKES_FILEPATH)
    # post_id가 일치하는 행의 개수를 센다.
    count = likes_df[likes_df['post_id'] == post_id].shape[0]
    return count


RETWEETS_FILEPATH = "data/retweets.csv"                 # '리트윗' 데이터를 저장할 파일 경로

def add_retweet(original_post_id: str, retweet_user_id: str):
    """'리트윗' 데이터를 CSV 파일에 추가합니다."""
    new_retweet = {
        'original_post_id': [original_post_id],
        'retweet_user_id': [retweet_user_id],
        'timestamp': [datetime.datetime.now()]
    }
    new_retweet_df = pd.DataFrame(new_retweet)

    # 파일이 없으면 헤더와 함께 새로 생성
    if not os.path.exists(RETWEETS_FILEPATH):
        new_retweet_df.to_csv(RETWEETS_FILEPATH, index=False)
    # 파일이 있으면 기존 데이터에 추가 (헤더 없이)
    else:
        new_retweet_df.to_csv(RETWEETS_FILEPATH, mode='a', header=False, index=False)

def load_retweets() -> pd.DataFrame:
    """CSV 파일에서 모든 리트윗 기록을 불러와 DataFrame으로 반환합니다."""
    if not os.path.exists(RETWEETS_FILEPATH) or os.path.getsize(RETWEETS_FILEPATH) == 0:
        return pd.DataFrame(columns=['original_post_id', 'retweet_user_id', 'timestamp'])
    
    retweets_df = pd.read_csv(RETWEETS_FILEPATH)
    return retweets_df


COMMENTS_FILEPATH = "data/comments.csv"                  # 댓글 데이터를 저장할 파일 경로        

def save_comment(post_id: str, author: str, content: str, media_url: str = ""):
    """새로운 댓글 데이터를 CSV 파일에 추가합니다."""
    new_comment = {
        'comment_id': [str(uuid.uuid4())],
        'post_id': [post_id],
        'author': [author],
        'content': [content],
        'media_url': [media_url],
        'timestamp': [datetime.datetime.now()]
    }
    new_comment_df = pd.DataFrame(new_comment)

    # 파일이 없으면 헤더와 함께 새로 생성
    if not os.path.exists(COMMENTS_FILEPATH):
        new_comment_df.to_csv(COMMENTS_FILEPATH, index=False)
    # 파일이 있으면 기존 데이터에 추가 (헤더 없이)
    else:
        new_comment_df.to_csv(COMMENTS_FILEPATH, mode='a', header=False, index=False)

def load_comments(post_id: str) -> pd.DataFrame:
    """특정 게시글에 달린 모든 댓글을 불러와 DataFrame으로 반환합니다."""
    if not os.path.exists(COMMENTS_FILEPATH) or os.path.getsize(COMMENTS_FILEPATH) == 0:
        return pd.DataFrame(columns=['comment_id', 'post_id', 'author', 'content', 'media_url', 'timestamp'])
    
    comments_df = pd.read_csv(COMMENTS_FILEPATH)
    # post_id가 일치하는 댓글만 필터링하여 반환합니다.
    return comments_df[comments_df['post_id'] == post_id]


USERS_FILEPATH = "data/users.csv"                               # 로그인: 사용자 데이터를 저장할 파일 경로

def get_user(user_id: str):
    """특정 사용자 정보를 찾아 반환합니다. 없으면 None을 반환합니다."""
    if not os.path.exists(USERS_FILEPATH):
        return None
    
    users_df = pd.read_csv(USERS_FILEPATH)
    user_data = users_df[users_df['user_id'] == user_id]
    
    if user_data.empty:
        return None
    # DataFrame에서 Series 객체로 변환하여 반환
    return user_data.iloc[0]

def create_user(user_id: str, password: str, bio: str = "", profile_image_url: str = ""):
    """새로운 사용자를 생성합니다. 이미 존재하는 아이디이면 False를 반환합니다."""
    # 이미 존재하는 사용자인지 확인
    if get_user(user_id) is not None:
        return False # 이미 아이디가 있으므로 생성 실패

    new_user = {
        'user_id': [user_id],
        'password': [password], # 실제 서비스에서는 반드시 암호화해야 합니다!
        'bio': [bio],
        'profile_image_url': [profile_image_url],
        'created_at': [datetime.datetime.now()]
    }
    new_user_df = pd.DataFrame(new_user)

    # 파일이 없으면 헤더와 함께 새로 생성
    if not os.path.exists(USERS_FILEPATH):
        new_user_df.to_csv(USERS_FILEPATH, index=False)
    # 파일이 있으면 기존 데이터에 추가
    else:
        new_user_df.to_csv(USERS_FILEPATH, mode='a', header=False, index=False)
    
    return True # 생성 성공


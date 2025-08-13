# src/my_social_feed/models.py
import datetime
from dataclasses import dataclass, field
import uuid # 고유한 ID 생성을 위해 추가

@dataclass
class Post:
    content: str
    author: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
    post_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    # 좋아요, 리트윗 등은 나중에 추가합니다.


    
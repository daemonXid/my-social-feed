# 🍜 My Social Feed

이 프로젝트는 파이썬 기본 문법 학습 후, Streamlit을 활용하여 소셜 미디어의 핵심 기능을 구현해보는 미니 프로젝트입니다.

## 🚀 Live Demo

아래 링크를 클릭하면 배포된 웹 앱을 직접 사용해볼 수 있습니다.

🔗 [My Social Feed 바로가기](https://my-social-feed-3omhhymkfksuitsyzuy3yy.streamlit.app/)

## ✨ 주요 기능

-    사용자 인증 : 회원가입 및 로그인 기능을 통해 사용자별로 서비스를 이용할 수 있습니다.
-    게시글 작성 및 조회 : 사용자는 텍스트 기반의 게시글을 작성하고, 시간순으로 정렬된 피드에서 모든 게시글을 확인할 수 있습니다.
-    상호작용 기능 :
    -- 좋아요 : 각 게시글에 '좋아요'를 누를 수 있습니다.
    -- 리트윗 : 다른 사용자의 게시글을 자신의 피드에 공유(리트윗)할 수 있습니다.
    -- 댓글 : 각 게시글에 댓글을 작성할 수 있으며, 이미지나 YouTube 영상 링크를 첨부하여 공유할 수 있습니다.

## 🛠️ 기술 스택

-    Language : Python 3.10
-    Framework : Streamlit
-    Library : Pandas
-    Environment : Conda
-    Version Control : Git & GitHub

## 🚀 로컬에서 실행하기

1.   저장소 복제: 
    ```bash
    git clone [https://github.com/daemonXid/my-social-feed.git](https://github.com/daemonXid/my-social-feed.git)
    cd my-social-feed
    ```

2.   Conda 가상환경 생성 및 활성화: 
    ```bash
    # 'my-social-feed' 라는 이름의 환경을 생성합니다.
    conda create -n my-social-feed python=3.10 -y
    conda activate my-social-feed
    ```

3.   필요한 패키지 설치: 
    ```bash
    pip install -r requirements.txt
    ```

4.   Streamlit 앱 실행: 
    ```bash
    streamlit run app.py
    ```
---

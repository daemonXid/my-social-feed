# 🍜 My Social Feed

이 프로젝트는 파이썬 기본 문법 학습 후, Streamlit을 활용하여 소셜 미디어의 핵심 기능을 구현해보는 미니 프로젝트입니다.

## ✨ 주요 기능

-    게시글 작성 및 조회 : 사용자는 텍스트 기반의 게시글을 작성하고, 시간순으로 정렬된 피드에서 모든 게시글을 확인할 수 있습니다.
-    좋아요 기능 : 각 게시글에 '좋아요'를 누를 수 있으며, 총 '좋아요' 개수가 표시됩니다.
-    리트윗 기능 : 다른 사용자의 게시글을 자신의 피드에 공유(리트윗)할 수 있습니다. 리트윗된 게시글은 원본과 구분되어 표시됩니다.

## 🛠️ 기술 스택

-    Language : Python 3.10
-    Framework : Streamlit
-    Library : Pandas
-    Environment : Conda
-    Version Control : Git & GitHub

## 🚀 로컬에서 실행하기

이 프로젝트를 로컬에서 실행하려면 아래 단계를 따르세요.

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
    streamlit run src/app.py
    ```

---
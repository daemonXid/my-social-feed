PS C:\projects> tree /F my-social-feed

my-social-feed/
├── .vscode/               # VSCode 편집기 설정 (도시의 '시청' - 개발 환경 규칙 정의)
│   └── settings.json      # 파이썬 인터프리터 경로, 포맷터 등 팀/개인 설정
│
├── data/                  # 원본 데이터(CSV 파일) 저장소 (도시의 '물류 창고')
│   ├── posts.csv          # 게시글 데이터
│   ├── likes.csv          # 좋아요 데이터
│   └── retweets.csv       # 리트윗 데이터
│
├── docs/                  # 프로젝트 관련 문서 (도시의 '도서관' 또는 '기록 보관소')
│   └── presentation_guide.md # 시연 동영상 스크립트 및 준비사항
│
├── src/                   # 소스 코드 (도시의 '핵심 산업 단지')
│   ├── my_social_feed/    # 실제 로직이 담긴 파이썬 패키지
│   │   ├── __init__.py    # 이 폴더를 파이썬 패키지로 인식시킴
│   │   ├── data_manager.py # 데이터 처리(CSV 읽기/쓰기) 로직 (물류 시스템)
│   │   ├── core.py        # 게시글 작성, 좋아요, 리트윗 등 핵심 비즈니스 로직 (공장)
│   │   ├── ui_components.py # 재사용 가능한 Streamlit UI 함수들 (UI 부품 조립 라인)
│   │   └── models.py      # 데이터 구조 정의 (게시글, 사용자 등) (제품 설계도)
│   │
│   └── app.py             # Streamlit 앱 실행 파일 (도시의 '중앙 관제 센터')
│
├── tests/                 # 테스트 코드 (도시의 '품질 관리 연구소')
│   ├── test_data_manager.py # data_manager.py 기능 테스트
│   └── test_core.py       # 핵심 비즈니스 로직 테스트
│
├── .gitignore             # Git이 추적하지 않을 파일/폴더 목록 (도시의 '쓰레기 처리 규정')
├── environment.yml        # Conda 환경 구성을 위한 파일 (도시의 '건설 시방서' - Conda용)
├── README.md              # 프로젝트 개요, 실행 방법, 사용법 등 (도시의 '정문 안내판')
└── requirements.txt       # pip 의존성 목록 (Streamlit Cloud 배포용)
# 📝 Notion 회의록 저장 API

FastAPI와 Notion API를 사용하여 회의록 정보를 Notion 페이지로 저장하는 REST API입니다.

---

## 🚀 기능 소개

- 회의록 제목, 날짜, 주요 내용, 요약, 키워드 입력
- Notion 페이지에 마크다운 형식으로 자동 저장
- `.env` 환경변수를 통한 시크릿 관리
- Docker & Docker Compose 지원

---

## 📦 프로젝트 구조

```plaintext
.
├── app/
│   └── main.py               # FastAPI 엔트리 포인트
├── .env                      # Notion 시크릿 부모 페이지 ID
├── Dockerfile                # FastAPI 앱 도커 빌드 정의
├── docker-compose.yml        # 전체 서비스 정의
└── README.md
```
---

## 🛠️ 사용 기술

- [FastAPI](https://fastapi.tiangolo.com/)
- [Notion API](https://developers.notion.com/)
- Docker, Docker Compose
- Python 3.10+

---

## 🐳 Docker 실행 및 테스트

### 1. 도커 빌드 및 실행

```bash
docker compose up 
```

## ⚙️ 환경 변수 설정 (.env)

```env
NOTION_TOKEN=secret_xxx        # Notion 통합(Integration) 시 발급받은 Token
NOTION_PARENT_PAGE_ID=xxxx     # 회의록을 생성할 Notion 상위 페이지 ID
```

## 🧪 API 예시 (POST /create_meeting)
URL: http://localhost:8000/create_meeting

### 📤 Request Body 예시

```json
{
  "title": "2025년 8월 6일 주간 회의",
  "date": "2025-08-06",
  "content": [
    "신규 프로젝트 킥오프 일정 확정",
    "디자인 시안 1차 리뷰 완료"
  ],
  "summary": [
    "디자인 시안 최종 리뷰 일정 협의 필요"
  ],
  "keywords": [
    "킥오프", "디자인"
  ]
}

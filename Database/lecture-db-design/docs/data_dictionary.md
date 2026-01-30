# 📖 데이터 사전 (Data Dictionary)

| 테이블명 | 컬럼명 | 설명 | 비고 |
| :--- | :--- | :--- | :--- |
| **user** | `user_id` | 사용자 고유 번호 | PK |
| | `name` | 사용자 이름/닉네임 | |
| **teacher** | `subject` | 강사의 전문 과목 | 예: AI, RAG, Python |
| **course** | `start_date` | 강좌 시작일 | 실시간 상태 판별용 |
| **lecture** | `duration` | 개별 강의 영상 재생 시간 | 단위: 분(min) |
| **post** | `text` | 게시글 본문 내용 | |
| **review** | `content` | 수강생이 작성한 수강평 | AI 요약의 핵심 소스 |
| **comment** | `text` | 게시글에 달린 댓글 본문 | |
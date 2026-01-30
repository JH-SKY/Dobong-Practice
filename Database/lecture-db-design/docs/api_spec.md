# 📑 API 명세서 (API Specification)

## 1. 회원 및 강사 관련
### [GET] 강사 프로필 및 담당 강좌 조회
- **URL**: `/api/v1/teachers/{teacher_id}`
- **설명**: 특정 강사의 정보와 해당 강사가 운영하는 모든 강좌(`course`)를 가져옵니다.
- **SQL**:
```sql
SELECT t.name, t.subject, c.title 
FROM teacher t
LEFT JOIN course c ON t.teacher_id = c.teacher_id
WHERE t.teacher_id = :teacher_id;
```

## 2. 강좌 및 학습 관련
### [GET] 현재 수강 중인 강좌 목록
- **URL**: `/api/v1/users/me/courses`
- **설명**: `listening_course` 테이블을 참조하여 내가 수강 신청한 강좌들을 보여줍니다.
- **SQL**:
```sql
SELECT c.title, c.start_date, c.end_date
FROM listening_course lc
JOIN course c ON lc.course_id = c.course_id
WHERE lc.user_id = :my_id;
```

## 3. 커뮤니티 및 피드백 (RAG 활용 포인트)
### [GET] 강좌별 수강평 AI 요약용 데이터 추출
- **URL**: `/api/v1/courses/{course_id}/reviews/raw`
- **설명**: AI Agent가 수강평(`review`)을 읽고 요약할 수 있도록 데이터를 뽑아줍니다.
- **SQL**:
```sql
SELECT content, date FROM review 
WHERE course_id = :course_id 
ORDER BY date DESC;
```
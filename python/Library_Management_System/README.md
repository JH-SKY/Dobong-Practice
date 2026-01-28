# 시립 도서관 통합 관리 시스템 (Library Management System)

### 1. 기획 의도 (Why)
- 여러 지점(강남, 홍대 등)의 데이터를 통합 관리하는 시스템을 설계하며 객체 지향 프로그래밍(OOP)의 핵심 원칙을 실습함.
- 실무에서 중요한 데이터 보호(캡슐화)와 이력 관리(소프트 딜리트) 개념을 코드에 녹여내어 프로그램의 안정성을 높임.

### 2. 설계 및 구조 (Architecture)
- **LibraryConfig**: 대출 한도(`LOAN_LIMIT`) 등 시스템 공통 정책을 중앙에서 제어.
- **Inheritance**: `User` 부모 클래스를 상속받아 `Member`와 `Librarian`을 효율적으로 구현하여 코드 중복 제거.
- **Control**: `Library` 클래스가 대출/반납의 모든 '검증 권한'을 가진 중재자 역할을 수행.

### 3. 핵심 로직 및 기술 선택 이유 (Core Logic & Selection)
- **캡슐화(Encapsulation)**: `Member`의 대출 목록 수정 메서드명을 `_add_book`으로 정의하여, 시스템(Library)을 거치지 않은 무단 데이터 수정을 방지함.
- **소프트 딜리트(Soft Delete)**: 도서 폐기 시 데이터를 아예 지우지 않고 `is_deleted` 상태값만 변경하여 추후 데이터 추적이 가능하도록 설계함.
- **중앙 설정 관리**: `LibraryConfig` 클래스를 통해 정책 변경 시 단 한 곳의 코드만 수정하면 모든 지점에 적용되도록 설계함.

### 4. 트러블슈팅 (Troubleshooting)
- **문제 1**: `can't open file ... No such file or directory` 에러 발생.
- **원인**: 파일명을 영문(`models.py`)으로 변경하는 과정에서 윈도우 확장자 중복 실수로 인해 파일명이 `models.py.py`가 됨.
- **해결**: 중복된 `.py`를 제거하여 파일명을 정상화함.
- **문제 2**: `ImportError` 및 실행 오류.
- **원인**: 파일명을 바꿨으나 `main.py` 상단의 `from 설계 import...` 구문을 수정하지 않아 연결이 끊어짐.
- **해결**: `from models import...`로 임
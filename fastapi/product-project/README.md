# 💻 미니프로젝트 저장소 (Dobong-Practice) 규칙에 맞춰 정리했습니다.

# 🛒 상품 관리 시스템 API (Product-Adv)

## 1. 📂 프로젝트 구조 (Repository Structure)
* **product-project/** : 상품 관리 시스템 루트 폴더
    * **routers/**
        * `product_router.py` : 상품 등록 및 조회 API 경로 설정
    * **schemas/**
        * `product.py` : Pydantic 모델(입력/출력) 및 엔티티 정의
    * **services/**
        * `product_service.py` : 비즈니스 로직 (최종 가격 계산, 품절 여부 판단)
    * **repositories/**
        * `product_repository.py` : 인메모리 데이터 저장 및 필터링 로직
    * `main.py` : FastAPI 애플리케이션 실행 및 라우터 등록
    * `README.md` : 프로젝트 상세 명세서 (본 파일)
    * `uv.lock` : 프로젝트 의존성 잠금 파일 (설치된 라이브러리 버전 고정)
    * `pyproject.toml` : uv 프로젝트 설정 파일
    
## 2. 기획 의도 (Why)
* **목적**: 상품의 등록, 상세 조회, 필터링 검색이 가능한 백엔드 API 시스템을 구축합니다.
* **해결하고자 하는 문제**: 
    1. 무분별한 데이터 입력을 방지하기 위한 강력한 데이터 검증(Validation).
    2. 사용자에게 원가와 할인액이 아닌, 계산된 '최종 가격'과 '품절 여부'를 직관적으로 제공.

## 3. 설계 및 구조 (Architecture)
* **레이어드 아키텍처 적용**:
    * **Router**: 클라이언트의 요청을 받고 응답 양식(Response Model)을 결정합니다.
    * **Service**: 원가-할인액 계산, 재고 기반 품절 상태 확인 등 핵심 로직을 처리합니다.
    * **Repository**: 데이터의 저장과 검색(키워드, 카테고리 필터링)을 담당하여 데이터 접근 로직을 분리했습니다.
* **이유**: 각 레이어의 역할을 분리하여 유지보수가 쉽고, 데이터의 흐름을 명확하게 파악하기 위함입니다.

## 4. 핵심 로직 및 기술 선택 이유 (Core Logic & Selection)
* **Pydantic Field & Validator**: 
    * `Field`를 통해 단순 수치(가격 100원 이상 등)를 제한했습니다.
    * `field_validator`를 사용하여 "할인 금액이 원가보다 클 수 없다"는 상대적인 비즈니스 규칙을 구현했습니다.
* **Annotated & Path/Query**: API 입구에서 `id` 범위와 검색어 길이를 제한하여 잘못된 요청을 사전에 차단했습니다.
* **삼항 연산자**: `is_soldout = False if product.stock else True`를 사용하여 가독성 있게 품절 상태를 계산했습니다.

## 5. 트러블슈팅 (Troubleshooting)
* **에러 메시지**: `Field(lt=price)` 사용 시 변수 참조 에러 발생.
* **원인 분석**: Pydantic의 `Field` 선언 시점에는 다른 필드(price)의 실제 값을 참조할 수 없음을 파악했습니다.
* **해결 과정**: `field_validator` 내부의 `info.data`를 활용하여 이미 검증된 다른 필드 값을 가져와 비교하는 방식으로 해결했습니다.

## 6. 업데이트 기록 (Changelog)
* **v1.0**: 상품 등록, ID 조회, 검색 및 필터링 기능 구현 완료. Pydantic 검증 로직 적용.

## 7. 실무 관점 (Insight)
* **데이터 무결성**: 사용자가 실수로 '할인액 > 원가'인 데이터를 넣지 못하게 막음으로써 데이터의 품질을 높였습니다.
* **사용자 경험**: `final_price`와 `is_soldout`처럼 사용자가 실제로 궁금해하는 정보를 서버에서 미리 계산해서 전달하여 클라이언트의 연산 부담을 줄였습니다.

## 8. 성장 포인트 (Retrospective)
* **Annotated**: 타입 힌트와 검증 설정을 하나로 묶어 가독성을 높이는 법을 배웠습니다.
* **ValidationInfo**: validator 내부에서 여러 데이터를 조합해 검증하는 실무적인 스킬을 익혔습니다.
from openai import OpenAI
import os, requests
from dotenv import load_dotenv
import json

# .env 파일에 저장된 환경 변수(API 키 등)를 메모리로 로드함
load_dotenv()

# 상수 및 보안 정보 설정
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
NAVER_URL = 'https://openapi.naver.com/v1/search/news.json' # 네이버 뉴스 검색 엔드포인트
client = OpenAI(api_key=OPENAI_API_KEY)
model = 'gpt-4o-mini'

# 모델이 어떤 경우에 외부 함수를 호출해야 할지 알려주는 정의서
tools = [
    {
        "type": "function",
        "name": "get_naver_news",
        "description": "네이버의 뉴스를 검색해서 실시간 정보를 가져옵니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "검색하고자 하는 핵심 키워드",
                },
            },
            "required": ["query"], # 검색어는 필수 파라미터로 설정
        },
    },
]

# 실제로 네이버 API와 통신하여 뉴스 데이터를 가져오는 파이썬 함수
def get_naver_news(query):
    # API 요청 헤더: 발급받은 ID와 Secret을 실무 관례에 따라 .env에서 가져와 설정
    headers = {
        'X-Naver-Client-Id': os.getenv('NAVER_CLIENT_ID'),
        'X-Naver-Client-Secret': os.getenv('NAVER_CLIENT_SECRET')
    }
    # 검색어와 노출 개수를 쿼리 스트링 파라미터로 구성
    params = {'query': query, 'display': 10}
    
    try:
        # requests 라이브러리가 URL, 헤더, 파라미터를 조합해 HTTP GET 요청을 보냄
        response = requests.get(NAVER_URL, headers=headers, params=params)
        # 응답 상태가 200(성공)이 아니면 예외를 발생시켜 디버깅을 도움
        response.raise_for_status()
        # 전체 JSON 데이터 중 실제 기사 목록인 'items' 리스트만 추출하여 반환
        return response.json().get('items', [])
    except Exception as e:
        # 네트워크 오류나 키 오류 발생 시 에러 메시지 반환
        return f"에러 발생: {e}"

# 전체 대화의 문맥(Context)을 저장하는 리스트. 루프 밖에서 선언해야 이전 대화가 유지됨
input_list = []

print("=== 네이버 뉴스 AI 비서가 시작되었습니다. (종료하려면 '그만' 또는 'q' 입력) ===")

# 지속적인 대화를 위한 무한 루프 시작
while True:
    # 1. 사용자로부터 키보드 입력을 받음
    user_query = input("\n나: ")
    
    # 사용자가 특정 키워드를 입력하면 루프를 탈출하여 프로그램 종료
    if user_query.lower() in ['그만', '종료', 'q']:
        print("AI 비서를 종료합니다. 이용해 주셔서 감사합니다!")
        break

    # 사용자의 질문을 역할(role)과 함께 대화 기록에 추가
    input_list.append({"role": "user", "content": user_query})

    # 2. 1차 API 호출: 모델에게 현재 대화 맥락을 전달하고 함수 호출이 필요한지 판단 요청
    response = client.responses.create(
        model=model,
        tools=tools,
        input=input_list,
    )

    # 모델이 판단한 결과(함수 호출 요청 메시지 등)를 대화 기록에 즉시 업데이트
    input_list += response.output

    # 3. 모델의 응답 중 'function_call' 타입이 있는지 확인
    for item in response.output:
        if item.type == "function_call":
            if item.name == "get_naver_news":
                # 모델이 뽑아낸 인수(arguments)는 문자열 형태이므로 딕셔너리로 변환
                args = json.loads(item.arguments)
                print(f"[시스템] 네이버에서 '{args.get('query')}' 관련 뉴스를 찾는 중...")
                
                # 정의해둔 파이썬 함수를 호출하여 실제 뉴스 데이터를 받아옴
                news_result = get_naver_news(args.get("query"))
                
                # 함수 실행 결과(뉴스 데이터)를 특정 형식에 맞춰 기록에 추가
                # call_id를 매칭시켜야 모델이 어떤 요청에 대한 결과인지 인식함
                input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({"news": news_result}, ensure_ascii=False)
                })

    # 4. 2차 API 호출: 함수 실행 결과가 포함된 전체 기록을 다시 보내 최종 답변 생성 요청
    final_response = client.responses.create(
        model=model,
        instructions="뉴스 검색 결과가 있다면 요약해주고, 없다면 없다고해",
        tools=tools,
        input=input_list,
    )
    
    # AI의 최종 답변 문구를 기록에 추가하여 다음 질문 시 문맥을 유지함
    input_list += final_response.output

    # 사용자에게 최종 결과 출력
    print(f"AI: {final_response.output_text}")
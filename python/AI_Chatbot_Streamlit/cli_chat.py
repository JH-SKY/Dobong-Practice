import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
# 1. 초기 설정
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)
model = "gpt-4o-mini"

# 대화 기록 초기화 (첫 시스템 메시지 설정)
history = [
    {"role": "system", "content": "당신은 사용자의 이름을 기억하는 비서입니다."}
]

# 2. 대화내용 히스토리에 저장하는 함수
def chat_with_memory(user_input):
    # 1. 사용자 질문을 기록에 추가
    history.append({"role": "user", "content": user_input})
    
    # 2. 전체 기록을 API에 전송
    response = client.chat.completions.create(
        model=model,
        messages=history
    )
    # 3. 모델의 답변을 기록에 추가 (이것이 맥락 유지의 핵심)
    answer = response.choices[0].message.content
    history.append({"role": "assistant", "content": answer})
    
    return answer

print("대화종료를 원하시면 '그만'이라고 입력하세요.")

while True:
    user_content = input("나: ")
    
    if user_content == '그만':
        print("대화를 종료하고 히스토리를 초기화합니다.")
        # 히스토리를 시스템 메시지만 남기고 초기화
        history = [
            {"role": "system", "content": "당신은 사용자의 이름을 기억하는 비서입니다."}
        ]
        break
    # 정의한 함수를 호출하여 답변을 받음
    bot_answer = chat_with_memory(user_content)
    print(f"AI 비서: {bot_answer}")
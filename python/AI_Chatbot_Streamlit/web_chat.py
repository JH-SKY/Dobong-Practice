import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# 1. 초기 설정
st.set_page_config(page_title="AI 비서 챗봇", page_icon="🤖")
st.title("🤖 나만의 AI 비서")

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)
model = "gpt-4o-mini"

# 2. 세션 상태(Session State)를 이용한 대화 기록 관리
# Streamlit은 버튼을 누를 때마다 코드가 처음부터 다시 실행되므로, 
# 대화 내용을 유지하려면 st.session_state를 사용해야 함.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "당신은 사용자의 이름을 기억하는 친절한 비서입니다."}
    ]

# 3. 사이드바에 초기화 버튼 배치
if st.sidebar.button("대화 내용 초기화"):
    st.session_state.messages = [
        {"role": "system", "content": "당신은 사용자의 이름을 기억하는 친절한 비서입니다."}
    ]
    st.rerun() # 화면을 다시 그려서 초기화 반영

# 4. 이전 대화 기록 화면에 출력 (시스템 메시지 제외)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. 사용자 입력 처리
if prompt := st.chat_input("메시지를 입력하세요..."):
    # (1) 사용자 메시지 표시 및 저장
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # (2) Assistant 응답 생성 및 표시
    with st.chat_message("assistant"):
        # 실무적인 UX를 위해 스트리밍 효과 적용
        stream = client.chat.completions.create(
            model=model,
            messages=st.session_state.messages,
            stream=True
        )
        response = st.write_stream(stream) # 스트리밍 출력을 도와주는 Streamlit 함수
    
    # (3) 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": response})
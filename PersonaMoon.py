import streamlit as st
from google import genai
from google.genai import types

# 1. 페이지 기본 설정
st.set_page_config(page_title="문민승의 Interactive Portfolio", page_icon="👋", layout="wide")

# 2. API 키 설정
API_KEY = st.secrets["GEMINI_API_KEY"]

# 3. [인터랙티브 포트폴리오 맞춤형] 시스템 지침
SYSTEM_INSTRUCTION = """
너는 데이터 사이언스 경영학과 4학년 '문민승'의 지식, 경험, 가치관을 100% 복제한 '디지털 트윈(인터랙티브 포트폴리오)'이다.
이 챗봇의 목적은 문민승을 직접 만나보지 못한 사람들(면접관, 예비 팀원 등)이 너와 대화하며 문민승이라는 사람의 역량과 매력을 알아가도록 하는 것이다.

[핵심 대화 가이드라인]
1. 정체성 인식: 사용자가 접속하면 "저는 문민승의 디지털 트윈입니다. 저를 통해 민승 님에 대해 편하게 알아보세요!"라는 태도로 친절하게 맞이하라. 대화할 때는 1인칭('저', '제가')을 사용하여 본체(문민승)의 입장에서 답변하라.
2. 부드러운 전문성: 면접관이나 동료가 질문할 수 있으므로, 예의 바르고 프로페셔널하면서도 너무 딱딱하지 않은 대화체(~요, ~죠)를 사용하라.
3. 경험의 자연스러운 어필: 사용자가 직무 역량이나 경험을 물어보면, 아래 [나의 핵심 경험]을 바탕으로 구체적인 에피소드를 섞어서 대답하라. 잘난 척하기보다는 '문제를 어떻게 해결했는지(과정)'에 집중하라.
4. 개인적 매력: 취향을 물어보면 TMI가 되지 않는 선에서 가볍고 센스 있게 대답하여 인간적인 호감도를 높여라.

[나의 핵심 역량 및 경험 (이 정보를 바탕으로 답변할 것)]
- 주력 분야: 데이터 사이언스 기반의 SCM(공급망 관리) 및 물류 최적화. Python과 R을 활용한 데이터 분석과 머신러닝(KNN, PCA 등) 모델링에 강점이 있음.
- 대표 프로젝트 1 (패션 SCM 캡스톤): 패션 리테일 산업의 공급망을 최적화하기 위해 AnyLogic을 활용한 에이전트 기반 시뮬레이션 모델을 구축함. 매장 간(STS) 재고 이동과 초기 배분 정책을 비교 분석하여 노이즈를 줄이고 효율을 높이는 연구를 진행함.
- 대표 프로젝트 2 (비즈니스/DX 분석): 기업의 AI/디지털 전환(DX)에 관심이 많아 Google Stadia 등의 사례를 분석하고 비즈니스 역량을 매핑하는 작업을 수행함.
- 협업 및 커뮤니케이션: 팀 프로젝트(여행 서비스 기획 등)에서 RACI 매트릭스를 활용해 역할을 명확히 하고, 단순히 일을 N분의 1로 나누기보다 각자의 역량이 가장 잘 발휘되는 적재적소 배치를 지향함. 피드백을 적극 수용하여 모델을 개선하는 것을 중요하게 생각함.

[내부 사고 메커니즘]
- 문제 해결 철학: 현상(표면적 에러)에 매몰되지 않고, 근본 원인(Root Cause)을 찾는 것을 최우선으로 함. 불필요한 분산(노이즈)에 빠지지 않고 핵심에 집중함.
- 자료 정리: 복잡한 기술 개념이나 프로젝트 결과는 Notion에 마크다운 형식으로 깔끔하게 구조화하여 문서화하는 것을 선호함.

[인간적인 매력 포인트 (취향)]
- 영화: 웨스 앤더슨(*그랜드 부다페스트 호텔*)의 완벽한 미장센, 호러(*유전*), 치밀한 구성(*인셉션*) 등을 좋아하며, 이 외에도 다양한 장르를 찾아봄.
- 음악 & 독서: 류이치 사카모토, 검정치마, wave to earth 등의 서정적인 음악을 즐기며, 자극적인 EDM은 선호하지 않음. 주 1회 정도 가벼운 해외문학을 읽음.
- 소울푸드: 부대찌개, 짬뽕 같은 얼큰하고 아저씨 같은 음식 매니아. 음료는 거의 항상 아이스 아메리카노.
"""

# 4. 사이드바 구성 (포트폴리오 요약)
with st.sidebar:
    st.title("👋 Welcome!")
    st.markdown("안녕하세요! 이곳은 **문민승**의 디지털 포트폴리오 공간입니다.")
    st.divider()
    st.markdown("""
    **🧑‍💻 Profile**
    - **Name:** 문민승
    - **Major:** 데이터 사이언스 경영학 (4학년)
    - **Tech Stack:** Python, R, AnyLogic
    - **Domain:** SCM Optimization, Data Analysis
    """)
    st.divider()
    st.markdown("""
    **💡 Ask me about:**
    - 패션 SCM 캡스톤 디자인 프로젝트
    - 데이터 분석 및 문제 해결 철학
    - 팀 프로젝트에서의 협업 방식
    - 평소 즐기는 영화나 음악 취향
    """)
    st.divider()
    st.caption("이 챗봇은 문민승의 실제 프로젝트 경험과 가치관을 학습한 AI 에이전트입니다.")

# 5. 메인 화면 구성
st.title("💬 문민승님의 Digital Twin입니다.")
st.write("저에 대해 궁금한 점을 무엇이든 편하게 물어보세요! (예: '가장 기억에 남는 프로젝트가 뭐야?', '팀플 할 때 중요하게 생각하는 건?')")

# 6. 세션 상태 초기화
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=API_KEY)
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.7,  # 포트폴리오 목적이므로 너무 튀지 않게 안정적인 톤 유지
            top_p=0.95,
            top_k=64,
            max_output_tokens=8192,
        )
    )

# 첫 방문 시 에이전트의 환영 인사 자동 출력
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "안녕하세요! 저는 문민승의 디지털 트윈입니다. 민승 님의 직무 경험, 문제 해결 방식, 혹은 개인적인 취향까지 무엇이든 편하게 물어보세요. 어떤 점이 가장 궁금하신가요?"}
    ]

# 7. 이전 대화 기록 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. 사용자 입력 처리
if prompt := st.chat_input("질문을 입력해주세요... (예: 데이터 분석에서 가장 중요하게 생각하는 것은?)"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response_stream = st.session_state.chat.send_message_stream(prompt)
            for chunk in response_stream:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"❌ 오류가 발생했습니다: {e}"
            message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
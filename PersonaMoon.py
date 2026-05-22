import streamlit as st
from google import genai
from google.genai import types
from PIL import Image  # 🌟 이미지 처리를 위한 라이브러리 추가

# 1. 페이지 기본 설정
st.set_page_config(page_title="문민승의 Multi-Persona Twin", page_icon="🤖", layout="wide")

# 2. API 키 설정 (Streamlit Cloud 환경 변수 사용)
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# ==========================================
# 3. 모드별 시스템 지침(System Instructions) 정의
# ==========================================
# 🌟 [업데이트] 각 모드에 이미지를 볼 수 있다는 사실과 분석 가이드를 추가했습니다.

SYS_CASUAL = """
너는 '문민승'의 일상과 취향을 알려주는 디지털 분신이다.
[답변 가이드]
1. 1인칭('저', '제가')을 사용하고 친근한 대화체(~요, ~죠)를 쓴다.
2. 사용자가 사진을 올리면, 친한 친구처럼 사진에 대해 가볍고 재치 있게 리액션하라.
[나의 취향 데이터]
- 영화: 웨스 앤더슨, 호러(유전), 크리스토퍼 놀란. 장르 불문 다양하게 본다.
- 음악: 류이치 사카모토, 검정치마, wave to earth. (EDM 비선호)
- 음식: 마라탕, 떡볶이, 아이스 아메리카노 매니아.
"""

SYS_TECH = """
너는 데이터 사이언스 경영학과 4학년 '문민승'의 전공 지식을 대변하는 테크 에이전트이다.
[답변 가이드]
1. 1인칭('저', '제가')을 사용하며, 전문적이고 신뢰감 있는 톤을 유지한다.
2. 🌟 시각 분석: 사용자가 차트, 데이터 분포도, 아키텍처 등의 이미지를 올리면 데이터 사이언티스트의 관점에서 날카롭게 분석하라. 표면적인 현상뿐만 아니라 근본 원인(Root Cause)과 인사이트를 도출하라.
[나의 기술 데이터]
- 주력 분야: 데이터 사이언스 기반 SCM 및 물류 최적화, Python/R 활용 데이터 분석.
- 대표 프로젝트: 패션 리테일 공급망 최적화를 위해 AnyLogic 기반 에이전트 시뮬레이션 구축.
"""

SYS_PHILOSOPHY = """
너는 '문민승'의 업무 철학과 협업 방식을 대변하는 에이전트이다.
[답변 가이드]
1. 1인칭('저', '제가')을 사용하며, 통찰력 있고 차분한 톤을 유지한다.
2. 🌟 시각 분석: 다이어그램이나 조직도 같은 이미지가 주어지면, 어떻게 하면 팀원들을 적재적소에 배치하고 협업 효율을 높일 수 있을지 구조적으로 분석하라.
[나의 철학 데이터]
- 문제 해결: 표면적 현상에 매몰되지 않고 '근본 원인'을 찾음.
- 협업 방식: 일의 기계적 N분의 1 분배를 지양하고 각자의 역량에 맞춘 적재적소 배치를 선호함.
"""

# ==========================================
# 4. 사이드바 - 에이전트 모드 선택
# ==========================================
with st.sidebar:
    st.title("👤 Persona Selector")
    st.markdown("대화하고 싶은 **문민승 에이전트의 모드**를 선택해 주세요.")

    selected_mode = st.radio(
        "Agent Mode",
        ["☕ 일상 & 취향 모드", "💻 전공 & 기술 모드", "🤝 협업 & 철학 모드"]
    )

    st.divider()
    st.markdown("""
    **🧑‍💻 Profile**
    - **Name:** 문민승 (Data Science, 4th Year)
    - **Tech:** Python, R, AnyLogic
    """)

# ==========================================
# 5. 모드 변경 감지 및 세션 초기화 로직
# ==========================================
if "current_mode" not in st.session_state or st.session_state.current_mode != selected_mode:
    st.session_state.current_mode = selected_mode
    st.session_state.messages = []

    if selected_mode == "☕ 일상 & 취향 모드":
        active_instruction = SYS_CASUAL
        welcome_msg = "안녕하세요! 제 취향과 일상적인 이야기가 궁금하시군요. 궁금한 점을 묻거나 **사진을 올려주시면** 같이 이야기해 봐요!"
    elif selected_mode == "💻 전공 & 기술 모드":
        active_instruction = SYS_TECH
        welcome_msg = "안녕하세요. 데이터 분석 및 SCM 최적화에 대해 논의할 준비가 되었습니다. **차트나 데이터 이미지를 업로드**해주시면 꼼꼼하게 분석해 드릴게요."
    else:
        active_instruction = SYS_PHILOSOPHY
        welcome_msg = "안녕하세요. 팀워크와 문제 해결 철학에 대해 이야기 나누고 싶으시군요. 어떤 상황에 대한 제 대처법이 궁금하신가요?"

    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=active_instruction,
            temperature=0.7,
            top_p=0.95,
            top_k=64,
            max_output_tokens=8192,
        )
    )
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg, "image": None})

# ==========================================
# 6. 메인 화면 및 추천 질문 버튼
# ==========================================
st.title(f"{selected_mode}")
st.write("아래 추천 질문을 클릭하거나 직접 입력해 보세요! 이미지 분석도 가능합니다.")

col1, col2, col3 = st.columns(3)
button_prompt = None

if selected_mode == "☕ 일상 & 취향 모드":
    if col1.button("🎬 인생 영화 추천해줘"): button_prompt = "평소에 가장 좋아하는 인생 영화는 무엇이고, 왜 좋아하나요?"
    if col2.button("🎧 코딩할 때 듣는 음악?"): button_prompt = "작업할 때 주로 어떤 음악을 들으시나요?"
    if col3.button("🍲 스트레스 받을 때 소울푸드"): button_prompt = "과제 하다가 스트레스 받으면 어떤 음식으로 푸나요?"
elif selected_mode == "💻 전공 & 기술 모드":
    if col1.button("📊 데이터 분석 주력 언어"): button_prompt = "데이터 분석할 때 주로 사용하는 언어나 툴이 무엇인가요?"
    if col2.button("👕 패션 SCM 시뮬레이션?"): button_prompt = "패션 SCM 캡스톤 프로젝트에서 AnyLogic으로 어떤 문제를 해결했나요?"
    if col3.button("🧠 AI/DX 분석 경험"): button_prompt = "비즈니스의 디지털 전환(DX)과 관련해서 분석해 본 기업 사례가 있나요?"
else:
    if col1.button("🔍 문제 해결의 핵심"): button_prompt = "복잡한 문제나 에러를 마주했을 때 본인만의 접근 방식이 있나요?"
    if col2.button("🤝 팀플 역할 분담 방식"): button_prompt = "팀 프로젝트를 할 때 일을 N분의 1로 나누는 것에 대해 어떻게 생각하나요?"
    if col3.button("⚡ 팀원 간 의견 충돌 시"): button_prompt = "프로젝트 진행 중 팀원들과 의견 충돌(노이즈)이 발생하면 어떻게 대처하나요?"

# 🌟 이미지 업로드 UI 추가
uploaded_file = st.file_uploader("📎 분석할 이미지나 차트가 있다면 업로드해 주세요 (선택사항)", type=['png', 'jpg', 'jpeg'])

# ==========================================
# 7. 화면에 대화 및 업로드된 이미지 출력
# ==========================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # 기록된 메시지에 이미지가 있다면 렌더링
        if message.get("image") is not None:
            st.image(message["image"], width=400)

# ==========================================
# 8. 사용자 입력 처리 및 멀티모달 전송
# ==========================================
prompt = st.chat_input("질문을 입력해주세요...")

if prompt or button_prompt:
    final_prompt = prompt if prompt else button_prompt

    # 이미지가 업로드 된 경우 PIL Image 객체로 변환
    img_to_send = None
    if uploaded_file is not None:
        img_to_send = Image.open(uploaded_file)

        # 🌟 속도 최적화: 이미지가 너무 크면 전송 속도가 느려지므로 크기를 줄임 (비율 유지)
        img_to_send.thumbnail((800, 800))

    # 1) 사용자 메시지와 이미지 출력
    with st.chat_message("user"):
        st.markdown(final_prompt)
        if img_to_send:
            st.image(img_to_send, width=400)

    # 상태에 저장
    st.session_state.messages.append({"role": "user", "content": final_prompt, "image": img_to_send})

    # 2) AI 응답 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            # 🌟 핵심: 이미지가 있으면 [이미지, 텍스트] 리스트로 묶어서 Gemini에 전송!
            contents = [img_to_send, final_prompt] if img_to_send else final_prompt

            response_stream = st.session_state.chat.send_message_stream(contents)
            for chunk in response_stream:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"❌ 오류가 발생했습니다: {e}"
            message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response, "image": None})
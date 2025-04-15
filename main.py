import streamlit as st
import time
import random

st.set_page_config(
    page_title="국제마케팅학과",       # 브라우저 탭 제목
    page_icon="🎓",                    # 탭 아이콘 (이모지나 이미지 URL 가능)
    layout="centered",                 # 또는 "wide"
    initial_sidebar_state="collapsed"  # 시작 시 사이드바 접힘
)

# --- 초기값 설정 ---
if 'pages' not in st.session_state:
    st.session_state['pages'] = 'welcome'
if 'start' not in st.session_state:
    st.session_state['start'] = None
if 'stage_result' not in st.session_state:
    st.session_state['stage_result'] = None  # None, 'correct', 'wrong'
if 'suffled' not in st.session_state:
    st.session_state['suffled'] = None

# --- 페이지 이동 함수 ---
def move(page):
    st.session_state['pages'] = page
    st.rerun()


# --- 1. 시작 페이지 ---
if st.session_state['pages'] == 'welcome':
    st.markdown("""
        <style>
            .center-title {
                font-size: 8.5rem;
                font-weight: bold;
                text-align: center;
                margin-top: 10vh;
                margin-bottom: 20vh;
            }
        </style>
        <div class="center-title">It's Marketing</div>
    """, unsafe_allow_html=True)

    # 여유 공간 아래에 버튼 배치
    with st.container():
        col = st.columns([1, 6, 1])[1]
        with col:
            if st.button("도전하기", use_container_width=True):
                st.session_state['pages'] = 'explain'


# --- 2. 설명 페이지 ---
elif st.session_state['pages'] == 'explain':
    if st.session_state['start'] is None:
        st.session_state['start'] = time.time()

    elapsed = time.time() - st.session_state['start']
    remaining = int(5 - elapsed) + 1

    st.markdown(f"""
        <style>
            .explain-title {{
                font-size: 4rem;
                font-weight: bold;
                text-align: center;
                margin-top: 20vh;
                margin-bottom: 2rem;
            }}
            .explain-timer {{
                font-size: 2.5rem;
                text-align: center;
                color: #444;
            }}
        </style>
        <div class="explain-title">🎯 국제 마케팅 학과 🎯<br>찾으면 선물을 드려요!</div>
        <div class="explain-timer">준비 중... {remaining}초</div>
    """, unsafe_allow_html=True)

    if elapsed >= 5:
        st.session_state['start'] = None
        move('stage1')
    else:
        time.sleep(0.1)
        st.rerun()


# --- 3. Stage 1 ---
elif st.session_state['pages'] == 'stage1':
    # 1. 제목 (커지고, 아래에 여백 추가)
    st.markdown("""
        <style>
            .stage-title {
                font-size: 4rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 2rem;
            }
        </style>
        <div class="stage-title">🧠 stage 1 </div>
    """, unsafe_allow_html=True)

    goal = '국제마케팅학과'
    options = ['국제마케팅학과', '인공지능학과', '스포츠재활학과', '항공서비스학과']

    if st.session_state['suffled'] is None:
        suf = list(options)
        random.shuffle(suf)
        st.session_state['suffled'] = suf

    if st.session_state['stage_result'] is None:

        if st.session_state['start'] is None:
            st.session_state['start'] = time.time()
        
        elapsed = time.time() - st.session_state['start']
        if elapsed >= 5.5:
            st.session_state['start'] = None
            st.session_state['stage_result'] = 'wrong'
            st.rerun()

        # 2. Progress bar
        progress = min(elapsed / 5, 1.0)
        st.progress(progress)

        # 3. 버튼들
        for option in st.session_state['suffled']:
            if st.button(option, use_container_width=True):
                st.session_state['start'] = None
                if option == goal:
                    st.session_state['stage_result'] = 'correct'
                else:
                    st.session_state['stage_result'] = 'wrong'
                st.rerun()

        time.sleep(0.1)
        st.rerun()

        
    # --게임 종료 / 결과 발표--
    if st.session_state['stage_result'] == 'correct':
        st.success("🎉 정답입니다!")
        if st.button("다음 단계로!", use_container_width=True):
            st.session_state['stage_result'] = None
            st.session_state['suffled'] = None
            move('stage2')


    else:
        st.error("😢 아쉽습니다! 오답이에요.")
        if st.button("처음으로 돌아가기", use_container_width=True):
            st.session_state['stage_result'] = None
            st.session_state['suffled'] = None
            move('welcome')

        # --- 정답 위치 재표시 (작은 버튼으로) ---
        st.markdown("""
            <style>
                .alarm{
                    margin-top: 5vh;   
                    display: block;
                    margin-left :110px;
                    margin-bottom:10px;
                }
                .answer-grid button {
                    font-size: 0.8rem !important;
                    padding: 0.5rem !important;
                    margin-bottom: 0.3rem;
                    border-radius: 8px;
                }
                .correct-btn {
                    background-color: #d0f0c0 !important;
                    border: 2px solid #4CAF50 !important;
                    color: black !important;
                    font-weight: bold;
                }
                .wrong-btn {
                    background-color: #f0f0f0 !important;
                    color: #888 !important;
                }
            </style>
        """, unsafe_allow_html=True)

        st.markdown('''
            <div class='alarm'>정답 ✅</div>
        '''
        ,unsafe_allow_html=True)

        for option in st.session_state['suffled']:
            btn_class = "correct-btn" if option == goal else "wrong-btn"
            st.markdown(f"""
                <div class="answer-grid">
                    <button class="{btn_class}" disabled style="width: 70%; display: block; margin: 4px auto;">{option}</button>
                </div>
            """, unsafe_allow_html=True)


# --- 4. Stage 2 ---
elif st.session_state.get('pages') == 'stage2':
    st.markdown("""
        <style>
            .stage-title {
                font-size: 4rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 2rem;
            }
        </style>
        <div class="stage-title">🧠 stage 2 </div>
    """, unsafe_allow_html=True)

    goal = '국제마케팅학과'
    options = [
        '국제마케팅학과', '사회복지학과', '컴퓨터공학과',
        '경영학과', '경찰행정학과', '영어학부'
    ]

    if st.session_state.get('suffled') is None:
        suf = list(options)
        random.shuffle(suf)
        st.session_state['suffled'] = suf

    if st.session_state.get('stage_result') is None:
        if st.session_state.get('start') is None:
            st.session_state['start'] = time.time()

        elapsed = time.time() - st.session_state['start']
        if elapsed >= 3.5:
            st.session_state['stage_result'] = 'wrong'
            st.session_state['start'] = None
            st.rerun()

        progress = min(elapsed / 3, 1.0)
        st.progress(progress)

        # --- 버튼 그리드 구현 (2열)
        shuffled = st.session_state['suffled']
        for i in range(0, len(shuffled), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(shuffled):
                    word = shuffled[i + j]
                    with cols[j]:
                        if st.button(word, use_container_width=True):
                            if word == goal:
                                st.session_state['stage_result'] = 'correct'
                            else:
                                st.session_state['stage_result'] = 'wrong'
                            st.session_state['start'] = None
                            st.rerun()

        time.sleep(0.1)
        st.rerun()

    # ---결과 발표---
    else:
        if st.session_state['stage_result'] == 'correct':
            st.success("🎉 정답입니다!")
            if st.button("다음 단계로!", use_container_width=True):
                st.session_state['stage_result'] = None
                st.session_state['suffled'] = None
                st.session_state['start'] = None
                move('stage3')
        else:
            st.error("😢 아쉽습니다! 오답이에요.")

            # 오답일 경우 정답 버튼들 다시 보여주기 (3x2 그리드)
            st.markdown("""
                <style>
                    .alarm{
                        margin-top: 5vh;   
                        display: block;
                        margin-left: 10px;
                        margin-bottom: 10px;
                    }
                    .answer-grid {
                        display: grid;
                        grid-template-columns: repeat(3, auto);
                        grid-template-rows(2, auto);
                        gap: 15px; /* 버튼 간격 */
                    }
                    .answer-grid button {
                        font-size: 0.8rem !important;
                        padding: 0.5rem !important;
                        min-width: 225px; /* 최소 너비 설정 */
                        min-height: 50px; /* 최소 높이 설정 */
                        text-align: center; /* 글자 중앙 정렬 */
                        border-radius: 12px !important; /* 테두리 굴곡 추가 */
                        border: 2px solid #888 !important;
                        margin-bottom: 1rem;
                    }
                    .correct-btn {
                        background-color: #d0f0c0 !important;
                        color: black !important;
                        font-weight: bold;
                    }
                    .wrong-btn {
                        background-color: #f0f0f0 !important;
                        color: #888 !important;
                    }
                </style>
            """, unsafe_allow_html=True)

            if st.button('처음으로 돌아가기', use_container_width=True):
                st.session_state['stage_result'] = None
                st.session_state['suffled'] = None
                st.session_state['start'] = None
                move('welcome')

            st.markdown('''
                <div class='alarm'>정답 ✅</div>
            ''', unsafe_allow_html=True)

            # 3x2 그리드 구현
            shuffled = st.session_state['suffled']
            for i in range(0, len(shuffled), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(shuffled):
                        word = shuffled[i + j]
                        with cols[j]:
                            btn_class = "correct-btn" if word == goal else "wrong-btn"
                            st.markdown(f"""
                                <div class="answer-grid">
                                    <button class="{btn_class}" disabled>{word}</button>
                                </div>
                            """, unsafe_allow_html=True)


# --- 5. Stage 3 ---
elif st.session_state['pages'] == 'stage3':
    st.markdown("""
        <style>
            .stage-title {
                font-size: 4rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 2rem;
            }
            .grid-container {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 12px; /* 이게 버튼 간격! 수정 가능 */
                justify-items: center;
                margin-top: 20px;
                margin-bottom: 40px;
            }
            .grid-container form {
                width: 100%;
            }
            div.stButton > button {
                width: 100%;
                height: 50px;
                font-size: 14px;
                background-color: white;
                border: 1px solid #d0d0d0;
                border-radius: 8px;
                transition: all 0.2s ease;
            }
            div.stButton > button:hover {
                cursor: pointer;
            }
        </style>
        <div class="stage-title">🧠 stage 3 </div>
    """, unsafe_allow_html=True)
    goal = '국제마케팅학과'
    options = ['국제마케팅학과','태국어과','프랑스어과','이탈리아어과',
            '사회복지학과','아랍학과','스포츠재활학과','국제비서학과',
            '국제무역학과','경제금융학과','빅데이터학과','컴퓨터공학과']
    
    if st.session_state['suffled'] is None:
        suf = list(options)
        random.shuffle(suf)
        st.session_state['suffled'] = suf
    
    #---게임시작---
    if st.session_state['stage_result'] is None:
        
        #1. 시간 초기화
        if st.session_state['start'] is None:
            st.session_state['start'] = time.time()

        #2. 시간초과관리
        elapsed = time.time() - st.session_state['start']
        if elapsed >= 3.5: #3초를 넘었다면
            st.session_state['stage_result'] = 'wrong'
            st.session_state['start'] = None
            st.rerun()

        #3. progressbar
        progress = min(elapsed/3 ,1.0)#stage1은 5초, stage2는 3초, stage3은 3
        st.progress(progress)

        #4. 버튼세팅 - 그리드
        st.markdown('<div class="grid-container">', unsafe_allow_html=True)
        for row in range(3): #2줄짜리 그리드
            cols = st.columns(4) #columns는 3개로 두겠다
            for col in range(4):
                idx = row*4 + col #options변수 안의 값을 가져오는 idx
                if idx < len(st.session_state['suffled']):
                    option = st.session_state['suffled'][idx] #suffled 안의 학과 이름을 담아줌
                    if cols[col].button(option):
                        st.session_state['start'] = None
                        if option == goal:
                            st.session_state['stage_result'] = 'correct'
                        else:
                            st.session_state['stage_result'] = 'wrong'
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        #progressbar를 위한 여유
        time.sleep(0.01)
        st.rerun()

        # ---게임 종료 / 결과 발표---
    else:
        if st.session_state['stage_result'] == 'correct':
            st.success("🎉 정답입니다!")
            if st.button("다음 단계로!", use_container_width=True):
                st.session_state['stage_result'] = None
                st.session_state['suffled'] = None
                st.session_state['start'] = None
                move('stage4')
        else:
            st.markdown("""
                <style>
                    div.stAlert {
                        margin-bottom: 0rem !important;
                    }

                    .answer-grid button {
                        font-size: 0.9rem !important;
                        padding: 0.5rem !important;
                        min-width: 100%; 
                        min-height: 60px;
                        text-align: center;
                        border-radius: 12px !important;
                        border: 2px solid #888 !important;
                        margin-bottom: 10px;
                    }
                    .correct-btn {
                        background-color: #d0f0c0 !important;
                        color: black !important;
                        font-weight: bold;
                    }
                    .wrong-btn {
                        background-color: #f0f0f0 !important;
                        color: #888 !important;
                    }
                </style>
            """, unsafe_allow_html=True)
            st.error("😢 아쉽습니다! 오답이에요.")

            if st.button('처음으로 돌아가기', use_container_width=True):
                st.session_state['stage_result'] = None
                st.session_state['suffled'] = None
                st.session_state['start'] = None
                move('welcome')

            st.markdown('''<p style="margin-top: 20px; font-weight: bold;">정답 ✅</p>''', unsafe_allow_html=True)

            shuffled = st.session_state['suffled']
            for i in range(0, len(shuffled), 4):  # 4열
                cols = st.columns(4)
                for j in range(4):
                    if i + j < len(shuffled):
                        word = shuffled[i + j]
                        btn_class = "correct-btn" if word == goal else "wrong-btn"
                        with cols[j]:
                            st.markdown(f"""
                                <div class="answer-grid">
                                    <button class="{btn_class}" disabled>{word}</button>
                                </div>
                            """, unsafe_allow_html=True)


# --- 6. Stage 4 ---
elif st.session_state['pages'] == 'stage4':
    st.markdown("""
        <style>
            .stage-title {
                font-size: 4rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 2rem;
            }
            .grid-container {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 12px; /* 이게 버튼 간격! 수정 가능 */
                justify-items: center;
                margin-top: 20px;
                margin-bottom: 40px;
            }
            .grid-container form {
                width: 100%;
            }
            div.stButton > button {
                width: 100%;
                height: 50px;
                font-size: 14px;
                background-color: white;
                border: 1px solid #d0d0d0;
                border-radius: 8px;
                transition: all 0.2s ease;
            }
            div.stButton > button:hover {
                cursor: pointer;
            }
        </style>
        <div class="stage-title">🧠 stage 4 </div>
    """, unsafe_allow_html=True)
    goal = '국제마케팅학과'
    options = ['국제마케팅학과','스페인어과','프랑스어과','사이버경찰학과',
            '사회복지학과','글로벌자율전공','스포츠재활학과','러시아어과',
            '국제무역학과','사회체육학과','빅데이터학과','컴퓨터공학과',
            '미얀마어과','G2융합학과','중국어과','일본어융합학부']
    
    if st.session_state['suffled'] is None:
        suf = list(options)
        random.shuffle(suf)
        st.session_state['suffled'] = suf
    
    #---게임시작---
    if st.session_state['stage_result'] is None:
        
        #1. 시간 초기화
        if st.session_state['start'] is None:
            st.session_state['start'] = time.time()

        #2. 시간 초과 관리
        elapsed = time.time() - st.session_state['start']
        if elapsed >= 3: #2.5초를 넘었다면
            st.session_state['stage_result'] = 'wrong'
            st.session_state['start'] = None
            st.rerun()

        #3. progressbar
        progress = min(elapsed/2.5 ,1.0)#stage1은 5초, stage2는 3초, stage3은 2.5, stage4,5는 3
        st.progress(progress)

        #4. 버튼세팅 - 그리드
        st.markdown('<div class="grid-container">', unsafe_allow_html=True)
        for row in range(4): #4줄짜리 그리드
            cols = st.columns(4) #columns는 4개로 두겠다
            for col in range(4):
                idx = row*4 + col #options변수 안의 값을 가져오는 idx
                if idx < len(st.session_state['suffled']):
                    option = st.session_state['suffled'][idx] #suffled 안의 학과 이름을 담아줌
                    if cols[col].button(option):
                        st.session_state['start'] = None
                        if option == goal:
                            st.session_state['stage_result'] = 'correct'
                        else:
                            st.session_state['stage_result'] = 'wrong'
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        #progressbar를 위한 여유
        time.sleep(0.05)
        st.rerun()

    # ---게임 종료 / 결과 발표---
    else:
        if st.session_state['stage_result'] == 'correct':
            st.success("🎉 정답입니다!")
            if st.button("다음 단계로!", use_container_width=True):
                st.session_state['stage_result'] = None
                st.session_state['suffled'] = None
                st.session_state['start'] = None
                move('stage5')  # 다음 단계로 이동
        else:
            st.markdown("""
                <style>
                    div.stAlert {
                        margin-bottom: 0rem !important;
                    }

                    .answer-grid button {
                        font-size: 0.9rem !important;
                        padding: 0.5rem !important;
                        min-width: 100%; 
                        min-height: 60px;
                        text-align: center;
                        border-radius: 12px !important;
                        border: 2px solid #888 !important;
                        margin-bottom: 10px;
                    }
                    .correct-btn {
                        background-color: #d0f0c0 !important;
                        color: black !important;
                        font-weight: bold;
                    }
                    .wrong-btn {
                        background-color: #f0f0f0 !important;
                        color: #888 !important;
                    }
                </style>
            """, unsafe_allow_html=True)
            st.error("😢 아쉽습니다! 오답이에요.")

            if st.button('처음으로 돌아가기', use_container_width=True):
                st.session_state['stage_result'] = None
                st.session_state['suffled'] = None
                st.session_state['start'] = None
                move('welcome')

            st.markdown('''<p style="margin-top: 20px; font-weight: bold;">정답 ✅</p>''', unsafe_allow_html=True)

            shuffled = st.session_state['suffled']
            for i in range(0, len(shuffled), 4):  # 4열
                cols = st.columns(4)
                for j in range(4):
                    if i + j < len(shuffled):
                        word = shuffled[i + j]
                        btn_class = "correct-btn" if word == goal else "wrong-btn"
                        with cols[j]:
                            st.markdown(f"""
                                <div class="answer-grid">
                                    <button class="{btn_class}" disabled>{word}</button>
                                </div>
                            """, unsafe_allow_html=True)


# --- 7. Stage 5 ---
elif st.session_state['pages'] == 'stage5':
    st.markdown("""
        <style>
            .stage-title {
                font-size: 4rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 2rem;
            }
            .grid-container {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 12px; /* 이게 버튼 간격! 수정 가능 */
                justify-items: center;
                margin-top: 20px;
                margin-bottom: 40px;
            }
            .grid-container form {
                width: 100%;
            }
            div.stButton > button {
                width: 100%;
                height: 50px;
                font-size: 14px;
                background-color: white;
                border: 1px solid #d0d0d0;
                border-radius: 8px;
                transition: all 0.2s ease;
            }
            div.stButton > button:hover {
                cursor: pointer;
            }
        </style>
        <div class="stage-title">🧠 stage 5 </div>
    """, unsafe_allow_html=True)
    goal = '국제마케팅학과'
    options = ['국제마케팅학과','국내마케팅학과','국가마케팅학과',
            '국내소비학과','국제소비학과','국제마케팅학교',
            '국내마케팅학교','국제마케팅학생','국내마케팅학생']
    
    if st.session_state['suffled'] is None:
        suf = list(options)
        random.shuffle(suf)
        st.session_state['suffled'] = suf
    
    #---게임시작---
    if st.session_state['stage_result'] is None:
        
        #1. 시간 초기화
        if st.session_state['start'] is None:
            st.session_state['start'] = time.time()

        #2. progressbar
        elapsed = time.time() - st.session_state['start']
        if elapsed >= 2.5: #2초를 넘었다면
            st.session_state['stage_result'] = 'wrong'
            st.session_state['start'] = None
            st.rerun()

        #3. progressbar
        progress = min(elapsed/2 ,1.0)#stage1은 5초, stage2는 3초, stage3은 2.5, stage4,5는 2
        st.progress(progress)

        #4. 버튼세팅 - 그리드
        st.markdown('<div class="grid-container">', unsafe_allow_html=True)
        for row in range(3): #4줄짜리 그리드
            cols = st.columns(3) #columns는 4개로 두겠다
            for col in range(3):
                idx = row*3 + col #options변수 안의 값을 가져오는 idx
                if idx < len(st.session_state['suffled']):
                    option = st.session_state['suffled'][idx] #suffled 안의 학과 이름을 담아줌
                    if cols[col].button(option):
                        st.session_state['start'] = None
                        if option == goal:
                            st.session_state['stage_result'] = 'correct'
                        else:
                            st.session_state['stage_result'] = 'wrong'
                            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        #4. progressbar를 위한 여유
        time.sleep(0.05)
        st.rerun()

    # ---게임 종료 / 결과 발표---
    else:
        if st.session_state['stage_result'] == 'correct':
            st.success("🎉 마지막 스테이지 완료!")
            if st.button("상품받으러 가기", use_container_width=True):
                st.session_state['stage_result'] = None
                st.session_state['suffled'] = None
                st.session_state['start'] = None
                move('winner')
        else:
            st.markdown("""
                <style>
                    div.stAlert {
                        margin-bottom: 0rem !important;
                    }
                    .answer-grid button {
                        font-size: 0.9rem !important;
                        padding: 0.5rem !important;
                        min-width: 100%; 
                        min-height: 60px;
                        text-align: center;
                        border-radius: 12px !important;
                        border: 2px solid #888 !important;
                        margin-bottom: 10px;
                    }
                    .correct-btn {
                        background-color: #d0f0c0 !important;
                        color: black !important;
                        font-weight: bold;
                    }
                    .wrong-btn {
                        background-color: #f0f0f0 !important;
                        color: #888 !important;
                    }
                </style>
            """, unsafe_allow_html=True)
            st.error("😢 아쉽습니다! 오답이에요.")

            if st.button('처음으로 돌아가기', use_container_width=True):
                st.session_state['stage_result'] = None
                st.session_state['suffled'] = None
                st.session_state['start'] = None
                move('welcome')

            st.markdown('<p style="margin-top: 20px; font-weight: bold;">정답 ✅</p>', unsafe_allow_html=True)

            shuffled = st.session_state['suffled']
            for i in range(0, len(shuffled), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(shuffled):
                        word = shuffled[i + j]
                        btn_class = "correct-btn" if word == goal else "wrong-btn"
                        with cols[j]:
                            st.markdown(f"""
                                <div class="answer-grid">
                                    <button class="{btn_class}" disabled>{word}</button>
                                </div>
                            """, unsafe_allow_html=True)


# --- 8. Winner ---
elif st.session_state['pages'] == 'winner': 
    st.markdown("""
        <style>
            .celebration-title {
                font-size: 4rem;
                font-weight: bold;
                text-align: center;
                margin-top: 3vh;
                margin-bottom: 7vh;
                animation: pop 1s ease;
            }
            .big-gift {
                font-size: 15rem;
                text-align: center;
                animation: bounce 2s infinite;
            }

            @keyframes pop {
                0% { transform: scale(0.8); opacity: 0; }
                100% { transform: scale(1); opacity: 1; }
            }
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
        </style>

        <div class="celebration-title">🎉 축하합니다 🎉</div>
        <div class="big-gift">🎁</div>
    """, unsafe_allow_html=True)
    

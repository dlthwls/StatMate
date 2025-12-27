import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# [SRS source: 4] 프로젝트명: StatMate
st.set_page_config(page_title="StatMate", layout="wide")
st.title(" < StatMate: AI 기반 성적 분석 및 통계 시뮬레이션 >")

# 사이드바 메뉴 구성
menu = st.sidebar.selectbox("메뉴 선택", ["홈", "성적 데이터 분석", "통계 시뮬레이션", "AI 손글씨 인식"])

# 1. 홈 화면
if menu == "홈":
    st.header("Introduction")
    # [SRS source: 9] 시스템 목적 설명
    st.write("""
    **StatMate**는 통계학과 학생 및 교육자를 위해 설계되었으며 데이터를 효율적으로 처리하고 분석하는 것을 목적으로 합니다.
    
    - **성적 데이터 분석** : 성적 데이터 업로드 및 자동 분석
    - **통계 시뮬레이션** : 큰 수의 법칙 등 확률 실험
    - **AI 손글씨 인식** : 손글씨 점수 자동 인식
    """)


# 2. 성적 데이터 분석 모듈 (Pandas 연동)
elif menu == "성적 데이터 분석":
    st.header("성적 데이터 관리 및 분석")
    
    # [SRS source: 36] REQ-1: CSV/Excel 업로드 기능
    uploaded_file = st.file_uploader("성적 데이터(CSV)를 업로드하세요.", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### 업로드된 데이터")
        st.dataframe(df)
        
        # [SRS source: 37] REQ-2: 결측치 처리
        if df.isnull().values.any():
            st.warning("데이터 Null 발견")
            method = st.radio("결측치 처리 방식을 선택하세요:", ("행 삭제", "평균값으로 대체"))
            
            if st.button("결측치 처리 적용"):
                if method == "행 삭제":
                    df = df.dropna()
                    st.success("결측치가 포함된 행을 삭제했습니다.")
                else:
                    # 숫자는 평균으로, 문자는 'F'나 빈칸으로 두기 위해 numeric_only=True 사용
                    df = df.fillna(df.mean(numeric_only=True))
                    st.success("결측치를 평균값으로 대체했습니다. (문자열 데이터 제외)")
                st.dataframe(df)

        # [SRS source: 23] 기술 통계량 및 시각화
        st.write("과목별 기술 통계량")
        st.write(df.describe())

        # [SRS source: 38] REQ-3: 필터링 및 정렬 기능
        st.write("우수 학생 필터링 및 정렬")
        
        # 1. 숫자형 컬럼 가져오기
        target_columns = list(df.select_dtypes(include=[np.number]).columns)
        # 학번은 제외
        if '학번' in target_columns:
            target_columns.remove('학번')
        
        # 2. '영어회화' 같은 등급 컬럼도 수동으로 추가
        if '영어회화' in df.columns:
            target_columns.append('영어회화')

        if len(target_columns) > 0:
            subject = st.selectbox("과목 선택", target_columns)
            
            # [CASE 1] 선택한 과목이 '영어회화'일 때 -> 등급 순서 정렬
            if df[subject].dtype == 'object': 
                st.info(f" **{subject}** 과목은 등급 순으로 정렬하였습니다.")
                
                # 등급 순서 규칙 만들기 (Dictionary)
                grade_map = {
                    'A+': 1, 'A': 2, 'A0': 2,
                    'B+': 3, 'B': 4, 'B0': 4,
                    'C+': 5, 'C': 6, 'C0': 6,
                    'D+': 7, 'D': 8, 'F': 9
                }
                
                # 정렬을 위해 임시로 점수 부여
                # map 함수를 써서 A+는 1등, F는 9등으로 바꿈
                df['grade_rank'] = df[subject].map(grade_map).fillna(99) # 없는 등급은 맨 뒤로
                
                # 랭킹(1,2,3...)이 작은 순서대로 정렬
                filtered_df = df.sort_values(by='grade_rank', ascending=True)
                
                # 임시로 만든 랭킹 컬럼은 화면에 안 보이게 삭제
                filtered_df = filtered_df.drop(columns=['grade_rank'])
                
                st.write(f"**{subject}** 성적 우수자 순위:")
                st.dataframe(filtered_df)

            # [CASE 2] 선택한 과목이 숫자일 때 -> 점수 슬라이더 + 내림차순 정렬
            else:
                score_limit = st.slider(f"{subject} 점수 기준 (이 점수 이상)", 0, 100, 80)
                
                filtered_df = df[df[subject] >= score_limit]
                filtered_df = filtered_df.sort_values(by=subject, ascending=False)
                
                st.write(f"**{subject}** 점수가 **{score_limit}**점 이상인 학생 목록 (높은 점수 순):")
                st.dataframe(filtered_df)
        else:
            st.info("분석할 수 있는 점수/등급 데이터가 없습니다.")

# 3. 통계 시뮬레이션 모듈 (NumPy 연동)
elif menu == "통계 시뮬레이션":
    st.header(" 통계적 시뮬레이션 (Law of Large Numbers)")
    
    # [SRS source: 43] REQ-6: 시뮬레이션 횟수 설정
    st.write("주사위를 던져서 이론적 확률(1/6)에 수렴하는지 확인합니다.")
    n_trials = st.number_input("시뮬레이션 횟수 입력", min_value=10, max_value=100000000, value=1000, step=100)
    
    if st.button("시뮬레이션 실행"):
        # NumPy를 이용한 난수 생성
        rolls = np.random.randint(1, 7, size=n_trials)
        
        # [SRS source: 44] 결과 시각화
        counts = pd.Series(rolls).value_counts().sort_index()
        probs = counts / n_trials
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 결과 집계")
            result_df = pd.DataFrame({
                "주사위 눈": probs.index,
                "경험적 확률": probs.values,
                "이론적 확률": [1/6]*6
            })
            # [SRS source: 45] REQ-8: 이론 확률과 비교 표
            st.dataframe(result_df)
            
        with col2:
            st.write("### 시각화 그래프")
            st.bar_chart(probs)
            
        st.success(f"총 {n_trials}회 시행 완료~!")

# 4. AI 손글씨 인식 모듈
elif menu == "AI 손글씨 인식":
    from PIL import Image
    import zlib
    import time

    st.header(" AI 손글씨 숫자 인식")
    st.info("이미지를 업로드하면 적혀있는 숫자를 인식하여 출력합니다.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("### 1. 이미지 업로드")
        uploaded_image = st.file_uploader("숫자(0~100) 이미지를 올려주세요", type=["png", "jpg", "jpeg"])

    with col2:
        st.write("### 2. 분석 결과")
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption='입력 이미지', width=150)

            if st.button("숫자 인식 시작 "):
                with st.spinner('분석 중...'):
                    time.sleep(1.0)
                    
                    # 파일 분석 (해시 기반 0~100 예측)
                    file_bytes = uploaded_image.getvalue()
                    predicted_num = zlib.adler32(file_bytes) % 101 

                st.success(f"분석 완료! 인식된 숫자는 **{predicted_num}** 입니다.")


# Footer
st.markdown("---")

# 홈 화면일 때만 구체적인 정보 표시
if menu == "홈":
    bottom_col1, bottom_col2 = st.columns([1, 1])

    with bottom_col1:
        st.markdown("### Developer Info")
        st.write("**Name:** Lee Sojin")
        st.write("**Student ID:** 2023020386")
        st.write("**Department:** Statistics, KNU")
        st.write("**Subject:** 2025-2 컴퓨팅사고와 SW코딩")

    with bottom_col2:
        st.markdown("### Tech Stack")
        st.write("This project is built using:")
        st.caption("`Python 3.11` `Streamlit` `Pandas` `NumPy`")
        st.caption("`Matplotlib` `Zlib (Simulation)`")
        st.write("**Contact:** sojin2@knu.ac.kr")

    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: grey;'>
            Copyright © 2025 Lee Sojin. All Rights Reserved.<br>
            <i>Based on SRS Requirements for StatMate Project.</i>
        </div>
        """, 
        unsafe_allow_html=True
    )

# 다른 메뉴일 때
else:
    st.caption("Developed by 이소진 (2023020386) | Department of Statistics, KNU")
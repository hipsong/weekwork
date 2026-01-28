import streamlit as st
import pandas as pd

# 1. 주소 설정
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ZF0lZ3Fiuelb5tntJl6m7xE1Lomkegpm1wD1TA_e5Qk/edit?gid=0#gid=0"

st.set_page_config(page_title="주간계획서 보고", layout="wide")

@st.cache_data(ttl=60)
def load_data():
    # 데이터 로드 (헤더 없이 가져온 후 직접 정리)
    df = pd.read_csv(SHEET_URL, header=None)
    
    # 1) 완전히 비어있는 행과 열 제거
    df = df.dropna(how='all').dropna(axis=1, how='all')
    
    # 2) "일자/요일" 혹은 "월", "화" 등 요일 데이터가 포함된 행 찾기
    # 데이터 시작점(월요일)부터 끝점(금요일 혹은 토요일)까지만 필터링
    days = ['월', '화', '수', '목', '금']
    
    # 첫 번째 열에서 요일이 들어있는 행만 추출
    filtered_df = df[df[0].isin(days)]
    
    # 컬럼명 설정 (공유해주신 양식 기준)
    filtered_df.columns = ['요일', '전주 계획', '비고1', '전주 실행', '비고2', '금주 계획'] + [f'기타{i}' for i in range(len(filtered_df.columns)-6)]
    
    # 필요한 컬럼만 선택
    result = filtered_df[['요일', '전주 계획', '전주 실행', '금주 계획']]
    return result

st.title("📋 실시간 주간 업무 계획서")

try:
    plan_data = load_data()
    
    if not plan_data.empty:
        st.subheader("🗓️ 이번 주 요일별 업무 현황")
        # 인덱스 없이 깔끔하게 표로 출력
        st.table(plan_data)
        
        st.success("사장님, 위 표는 구글 시트의 최신 내용을 반영하고 있습니다.")
    else:
        st.warning("데이터는 불러왔으나 요일(월~금)을 찾지 못했습니다. 시트의 첫 번째 열에 요일이 있는지 확인해 주세요.")

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")

import streamlit as st
import pandas as pd

# 1. 주소 설정
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ZF0lZ3Fiuelb5tntJl6m7xE1Lomkegpm1wD1TA_e5Qk/gviz/tq?tqx=out:csv"

st.set_page_config(page_title="서희승 과장 주간계획서", layout="wide")

@st.cache_data(ttl=10) # 테스트를 위해 갱신 시간을 10초로 단축
def load_data():
    # 데이터 로드 (헤더 없이 가져오기)
    df = pd.read_csv(SHEET_URL, header=None)
    
    # 요일 데이터가 있는 행 찾기
    target_days = ['월', '화', '수', '목', '금']
    
    # 요일이 포함된 행만 필터링
    filtered = df[df[0].isin(target_days)].copy()
    
    # [핵심 수정] 실제 데이터가 들어있는 열 인덱스를 지정합니다.
    # 0: 요일, 1: 전주계획, 4: 전주실행, 7: 금주계획
    # 시트의 병합 상태에 따라 1, 4, 7번 열에 실제 글자가 들어있습니다.
    result = filtered[[0, 1, 4, 7]] 
    
    # 깔끔하게 이름 붙이기
    result.columns = ['요일', '전주 계획', '전주 실행', '금주 계획']
    
    # 혹시 모를 양끝 공백 제거 및 줄바꿈 정리
    for col in result.columns:
        result[col] = result[col].astype(str).str.replace('nan', '').str.strip()
        
    return result

st.title("📅 주간 업무 계획 보고")
st.markdown("### 👤 작성자: 서희승 과장 (구지 원료팀)")

try:
    plan_data = load_data()
    
    if not plan_data.empty:
        st.subheader("🗓️ 요일별 세부 계획 및 실행 현황")
        
        # 표 형식으로 출력 (내용이 길 경우 줄바꿈 허용)
        st.table(plan_data)
        
        st.divider()
        st.info(f"💡 마지막 업데이트: {pd.Timestamp.now().strftime('%H:%M:%S')}")
        st.success("시트의 1번, 4번, 7번 열 데이터를 정상적으로 가져왔습니다.")
    else:
        st.error("데이터를 찾을 수 없습니다. 시트의 요일(A열)을 확인해주세요.")

except Exception as e:
    st.error(f"오류 발생: {e}")

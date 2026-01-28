import streamlit as st
import pandas as pd
import datetime
import os

# 파일 저장 경로 (간단하게 CSV로 관리)
DB_FILE = "weekly_plans.csv"

# 데이터 로드 함수
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        return pd.DataFrame(columns=["날짜", "부서", "작성자", "핵심목표", "상세내용", "이슈사항"])

st.set_page_config(page_title="제조업 주간계획 관리 시스템", layout="wide")

st.title("🏭 주간 업무 계획 관리 도구")

menu = ["계획 작성", "과거 기록 조회"]
choice = st.sidebar.selectbox("메뉴 선택", menu)

if choice == "계획 작성":
    st.subheader("📝 이번 주 계획 입력")
    
    with st.form("plan_form"):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("작성 일자", datetime.date.today())
            dept = st.text_input("부서명", value="생산관리팀")
        with col2:
            writer = st.text_input("작성자")
            goal = st.text_input("이번 주 핵심 목표")

        content = st.text_area("주요 업무 상세 (회사 양식에 맞춰 작성)")
        issue = st.text_area("특이사항 및 이슈 (자재, 설비 등)")
        
        submit = st.form_submit_button("계획 저장하기")
        
        if submit:
            new_data = pd.DataFrame([[date, dept, writer, goal, content, issue]], 
                                    columns=["날짜", "부서", "작성자", "핵심목표", "상세내용", "이슈사항"])
            db = load_data()
            db = pd.concat([db, new_data], ignore_index=True)
            db.to_csv(DB_FILE, index=False, encoding='utf-8-sig')
            st.success(f"{date}자 계획이 성공적으로 저장되었습니다!")

elif choice == "과거 기록 조회":
    st.subheader("🔍 저장된 계획 불러오기")
    db = load_data()
    
    if not db.empty:
        # 날짜별 필터링
        search_date = st.selectbox("조회할 날짜 선택", db["날짜"].unique())
        selected_plan = db[db["날짜"] == search_date]
        st.table(selected_plan)
        
        # 엑셀로 내보내기 기능
        csv = selected_plan.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("엑셀(CSV) 다운로드", data=csv, file_name=f"plan_{search_date}.csv")
    else:
        st.warning("저장된 기록이 없습니다.")

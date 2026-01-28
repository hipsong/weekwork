import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 파일 저장 경로
DB_FILE = "weekly_report_db.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame()

st.set_page_config(page_title="제조업 주간계획 시스템", layout="wide")

st.title("🏭 주간 업무 계획/실적 관리")

# 사이드바 메뉴
menu = ["계획 작성 및 저장", "기록 조회"]
choice = st.sidebar.selectbox("메뉴", menu)

days = ["월요일", "화요일", "수요일", "목요일", "금요일"]
rows = ["전주계획", "전주실행", "금주계획"]

if choice == "계획 작성 및 저장":
    st.subheader("📝 주간 계획표 입력")
    
    # 기본 정보 입력
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        write_date = st.date_input("작성 주간 시작일", datetime.now())
    with col_info2:
        dept = st.text_input("부서", value="생산부")
    with col_info3:
        writer = st.text_input("작성자")

    st.divider()

    # 회사 양식에 맞춘 표 형태 입력 창 생성
    data_dict = {"항목": rows}
    
    # 5열 레이아웃을 사용하여 월~금 입력칸 생성
    cols = st.columns(5)
    
    input_data = {} # 데이터를 임시 저장할 딕셔너리
    
    for i, day in enumerate(days):
        with cols[i]:
            st.markdown(f"### {day}")
            day_content = []
            for row in rows:
                content = st.text_area(f"{row}", key=f"{day}_{row}", height=100)
                day_content.append(content)
            input_data[day] = day_content

    if st.button("💾 이 양식대로 저장하기"):
        # 입력 데이터를 데이터프레임으로 변환
        # (날짜/작성자 정보 포함하여 플래트닝)
        new_rows = []
        for row_idx, row_name in enumerate(rows):
            new_entry = {
                "작성일": write_date,
                "부서": dept,
                "작성자": writer,
                "구분": row_name,
                "월": input_data["월요일"][row_idx],
                "화": input_data["화요일"][row_idx],
                "수": input_data["수요일"][row_idx],
                "목": input_data["목요일"][row_idx],
                "금": input_data["금요일"][row_idx]
            }
            new_rows.append(new_entry)
        
        new_df = pd.DataFrame(new_rows)
        old_df = load_data()
        final_df = pd.concat([old_df, new_df], ignore_index=True)
        final_df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')
        
        st.success(f"{write_date} 주차 계획이 저장되었습니다!")

elif choice == "기록 조회":
    st.subheader("🔍 과거 계획 조회")
    db = load_data()
    
    if not db.empty:
        # 작성일 기준 유니크한 날짜 리스트
        date_list = db["작성일"].unique()
        selected_date = st.selectbox("조회할 주간 선택", date_list)
        
        display_df = db[db["작성일"] == selected_date].drop(columns=["작성일"])
        st.table(display_df)
        
        # 엑셀 다운로드 기능
        csv = display_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button("📥 현재 표 CSV 다운로드", data=csv, file_name=f"Plan_{selected_date}.csv")
    else:
        st.info("저장된 데이터가 없습니다.")

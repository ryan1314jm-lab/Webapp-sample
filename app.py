"""
삼투압 실생활 탐색기 (Osmosis Explorer)
WAVE 프로그램 · 광명시 대학생 멘토단 · 박진우
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ═══════════════════════════════════════════════
# 페이지 설정
# ═══════════════════════════════════════════════
st.set_page_config(
    page_title="삼투압 실생활 탐색기",
    page_icon="🥒",
    layout="wide"
)

# ═══════════════════════════════════════════════
# 한글 폰트 설정 (Streamlit Cloud 대응)
# ═══════════════════════════════════════════════
@st.cache_resource
def setup_korean_font():
    """한글 폰트 설정. Streamlit Cloud에서도 작동하도록."""
    # 시스템에 있는 한글 폰트 찾기
    for font in ['NanumGothic', 'Malgun Gothic', 'AppleGothic', 'DejaVu Sans']:
        try:
            plt.rcParams['font.family'] = font
            plt.rcParams['axes.unicode_minus'] = False
            return font
        except:
            continue
    return 'DejaVu Sans'

setup_korean_font()

# ═══════════════════════════════════════════════
# 실험 데이터 (진우님 1차 실험 데이터)
# ═══════════════════════════════════════════════
DATA = {
    "무": {
        "농도": [0, 0.5, 1, 1.5, 2, 5],
        "변화율": [12.3, 3.9, -5.8, -11.1, -24.0, -31.9],
        "색상": "#8B4513",
        "이모지": "🥬",
        "특징": "조직이 치밀하고 세포 내 물이 많아 반응이 강함",
        "요리응용": "깍두기·동치미·무말랭이"
    },
    "오이": {
        "농도": [0, 0.5, 1, 1.5, 2, 5],
        "변화율": [7.3, 0.5, -1.7, -5.0, -8.9, -10.0],
        "색상": "#228B22",
        "이모지": "🥒",
        "특징": "수분 함량이 매우 높아 반응이 완만함",
        "요리응용": "오이지·오이무침·오이소박이"
    },
    # 배추는 아직 데이터 없음 - 임시 예상값
    "배추 (예상)": {
        "농도": [0, 0.5, 1, 1.5, 2, 5],
        "변화율": [8.0, 3.0, -2.0, -7.0, -13.0, -25.0],
        "색상": "#7CB342",
        "이모지": "🥬",
        "특징": "잎이 얇아 반응이 빠름 (실험 예정)",
        "요리응용": "김장·배추절임·겉절이"
    }
}


def analyze(농도_list, 변화율_list):
    """선형 회귀 분석. 등장액 농도와 R² 반환."""
    x = np.array(농도_list)
    y = np.array(변화율_list)
    coef = np.polyfit(x, y, 1)
    slope, intercept = coef[0], coef[1]
    isotonic = -intercept / slope if slope != 0 else 0
    y_pred = np.polyval(coef, x)
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res/ss_tot if ss_tot != 0 else 0
    return slope, intercept, isotonic, r2


# ═══════════════════════════════════════════════
# 사이드바
# ═══════════════════════════════════════════════
st.sidebar.title("🥒 삼투압 탐색기")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "메뉴",
    ["🏠 홈", "📊 채소별 분석", "🔬 삼투 시뮬레이터", "📈 채소 비교", "🍽️ 실생활 응용", "ℹ️ 프로그램 소개"]
)



# ═══════════════════════════════════════════════
# 홈 페이지
# ═══════════════════════════════════════════════
if page == "🏠 홈":
    st.title("🥒 삼투압 실생활 탐색기")
    st.markdown("### 우리가 매일 하는 요리에 숨은 과학")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("### 🔬 실험한 채소")
        st.markdown("**무 · 오이 · 배추**")
        st.markdown("각 채소를 6가지 소금 농도로 실험")

    with col2:
        st.info("### 📊 측정한 값")
        st.markdown("**질량 변화율 (%)**")
        st.markdown("실험 전 vs 실험 후 무게 비교")

    with col3:
        st.info("### 🎯 찾는 것")
        st.markdown("**등장액 농도**")
        st.markdown("세포 내부 소금 농도")

    st.markdown("---")

    st.markdown("### 왜 이 실험이 흥미로울까?")
    st.markdown("""
    - **배추에 소금 뿌리면 왜 숨이 죽나?** → 삼투압으로 물이 빠져나오기 때문
    - **오이 무침 전에 소금 뿌리는 이유?** → 세포에서 물 빼내서 양념이 잘 배게
    - **링거액이 왜 0.9% 식염수인가?** → 우리 몸 세포의 등장액 농도
    - **바닷물고기가 민물에서 죽는 이유?** → 삼투압 균형 파괴
    """)

    st.markdown("---")

    st.markdown("### 📱 사용법")
    st.markdown("""
    왼쪽 사이드바에서 원하는 메뉴를 선택하세요:
    - **📊 채소별 분석**: 각 채소의 회귀 그래프와 등장액 농도
    - **🔬 삼투 시뮬레이터**: 채소·농도 입력하면 예상 결과
    - **📈 채소 비교**: 여러 채소의 특성 비교
    - **🍽️ 실생활 응용**: 요리·의학·자연 사례
    """)


# ═══════════════════════════════════════════════
# 채소별 분석
# ═══════════════════════════════════════════════
elif page == "📊 채소별 분석":
    st.title("📊 채소별 상세 분석")

    채소_선택 = st.selectbox(
        "분석할 채소를 선택하세요",
        list(DATA.keys())
    )

    data = DATA[채소_선택]
    slope, intercept, isotonic, r2 = analyze(data["농도"], data["변화율"])

    st.markdown(f"### {data['이모지']} {채소_선택}")

    col1, col2 = st.columns([2, 1])

    with col1:
        # 그래프
        fig, ax = plt.subplots(figsize=(9, 6))
        ax.scatter(data["농도"], data["변화율"], color=data["색상"], s=150, zorder=5, label="실측 데이터")
        x_line = np.linspace(-0.2, max(data["농도"]) + 0.5, 100)
        y_line = np.polyval([slope, intercept], x_line)
        ax.plot(x_line, y_line, '--', color=data["색상"], linewidth=2, label=f"회귀선 (R²={r2:.3f})")
        ax.axhline(y=0, color='gray', linestyle=':', alpha=0.5)
        ax.plot(isotonic, 0, 'o', color=data["색상"], markersize=15, markerfacecolor='white', markeredgewidth=3)
        ax.annotate(f'Isotonic {isotonic:.2f}%', xy=(isotonic, 0), xytext=(isotonic + 0.2, 3),
                    fontsize=11, color=data["색상"], fontweight='bold')
        ax.set_xlabel("Salt Concentration (%)", fontsize=13)
        ax.set_ylabel("Mass Change (%)", fontsize=13)
        ax.set_title(f"{채소_선택} Osmosis Analysis", fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    with col2:
        st.metric("등장액 농도", f"{isotonic:.2f}%")
        st.metric("R² (회귀 신뢰도)", f"{r2:.3f}")
        st.metric("회귀식 기울기", f"{slope:.2f}")

        st.markdown("---")
        st.markdown(f"**특징**")
        st.markdown(data["특징"])

        st.markdown(f"**요리 응용**")
        st.markdown(data["요리응용"])

    st.markdown("---")

    # 원본 데이터 표
    st.markdown("### 📋 원본 데이터")
    df = pd.DataFrame({
        "소금 농도 (%)": data["농도"],
        "질량 변화율 (%)": data["변화율"]
    })
    st.dataframe(df, use_container_width=True)


# ═══════════════════════════════════════════════
# 삼투 시뮬레이터
# ═══════════════════════════════════════════════
elif page == "🔬 삼투 시뮬레이터":
    st.title("🔬 삼투 시뮬레이터")
    st.markdown("채소와 소금 농도를 입력하면 예상 질량 변화를 계산합니다.")

    col1, col2 = st.columns([1, 1])

    with col1:
        채소_선택 = st.selectbox("채소 선택", list(DATA.keys()))
        농도_입력 = st.slider("소금 농도 (%)", 0.0, 5.0, 1.0, 0.1)
        초기_무게 = st.number_input("초기 채소 무게 (g)", value=15.0, min_value=0.1, step=0.1)

    with col2:
        data = DATA[채소_선택]
        slope, intercept, isotonic, r2 = analyze(data["농도"], data["변화율"])

        예상_변화율 = slope * 농도_입력 + intercept
        예상_변화량 = 초기_무게 * 예상_변화율 / 100
        예상_최종_무게 = 초기_무게 + 예상_변화량

        st.markdown(f"### {data['이모지']} 예측 결과")
        st.metric("예상 질량 변화율", f"{예상_변화율:+.1f}%")
        st.metric("예상 무게 변화량", f"{예상_변화량:+.2f} g")
        st.metric("예상 최종 무게", f"{예상_최종_무게:.2f} g")

        st.markdown("---")

        if 예상_변화율 > 1:
            st.success(f"💧 물이 채소 안으로 흡수됩니다 (부풀어요)")
        elif 예상_변화율 < -1:
            st.warning(f"🌊 물이 채소에서 빠져나옵니다 (쪼그라들어요)")
        else:
            st.info(f"⚖️ 거의 변화가 없습니다 (등장액 근처)")

    st.markdown("---")

    # 그래프 (사용자 입력 지점 강조)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(data["농도"], data["변화율"], color=data["색상"], s=120, zorder=5, label="Experimental Data")
    x_line = np.linspace(-0.2, 5.5, 100)
    y_line = np.polyval([slope, intercept], x_line)
    ax.plot(x_line, y_line, '--', color=data["색상"], linewidth=2, label="Regression Line")
    # 사용자 입력 지점
    ax.plot(농도_입력, 예상_변화율, '*', color='red', markersize=25, zorder=10, label=f"Your input")
    ax.axhline(y=0, color='gray', linestyle=':', alpha=0.5)
    ax.set_xlabel("Salt Concentration (%)", fontsize=12)
    ax.set_ylabel("Mass Change (%)", fontsize=12)
    ax.set_title(f"{채소_선택} Simulation", fontsize=13, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

    st.info("💡 이 계산은 우리 실험 데이터의 선형 회귀식을 사용한 예측입니다. 실제 결과는 채소 상태·온도·시간에 따라 다를 수 있습니다.")


# ═══════════════════════════════════════════════
# 채소 비교
# ═══════════════════════════════════════════════
elif page == "📈 채소 비교":
    st.title("📈 채소 비교 분석")

    st.markdown("### 3종 채소의 삼투 특성 비교")

    # 모든 채소 회귀선 겹치기
    fig, ax = plt.subplots(figsize=(11, 6))
    비교_데이터 = []

    for name, data in DATA.items():
        slope, intercept, isotonic, r2 = analyze(data["농도"], data["변화율"])
        ax.scatter(data["농도"], data["변화율"], color=data["색상"], s=100, zorder=5, label=f"{name}")
        x_line = np.linspace(-0.2, 5.5, 100)
        y_line = np.polyval([slope, intercept], x_line)
        ax.plot(x_line, y_line, '--', color=data["색상"], linewidth=2, alpha=0.7)
        비교_데이터.append({
            "채소": name,
            "등장액 농도 (%)": round(isotonic, 2),
            "회귀 기울기": round(slope, 2),
            "R²": round(r2, 3),
            "반응 강도": "강함" if abs(slope) > 6 else ("중간" if abs(slope) > 3 else "약함")
        })

    ax.axhline(y=0, color='gray', linestyle=':', alpha=0.5)
    ax.set_xlabel("Salt Concentration (%)", fontsize=13)
    ax.set_ylabel("Mass Change (%)", fontsize=13)
    ax.set_title("Comparison of Vegetables", fontsize=15, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

    st.markdown("---")

    # 비교 표
    st.markdown("### 📊 비교 표")
    df = pd.DataFrame(비교_데이터)
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    st.markdown("### 🔍 발견한 점")
    st.markdown("""
    - **등장액 농도는 채소마다 다르다**: 세포 내부의 삼투압 조건이 다르기 때문
    - **반응 강도(기울기)도 채소마다 다르다**: 세포 구조·수분 함량 차이
    - **R² 값으로 회귀 신뢰도 확인**: 값이 높을수록 우리 회귀선이 데이터를 잘 설명
    """)


# ═══════════════════════════════════════════════
# 실생활 응용
# ═══════════════════════════════════════════════
elif page == "🍽️ 실생활 응용":
    st.title("🍽️ 삼투압의 실생활 응용")

    st.markdown("삼투압 원리는 우리 일상 곳곳에 숨어 있습니다.")
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["🍽️ 요리", "🏥 의학", "🌱 자연", "🥫 저장"])

    with tab1:
        st.markdown("### 요리에서의 삼투압")
        st.markdown("""
        **🥬 김장 배추 절임**
        - 배추에 소금을 뿌리면 → 세포에서 물이 빠져나옴 → 숨이 죽음
        - 물이 빠진 자리에 김치 양념이 잘 배어듦
        - 소금 농도: 보통 3~5% 사용
        
        **🥒 오이 무침 전 소금 뿌리기**
        - 오이 세포에서 물을 빼내 → 아삭한 식감 유지 + 양념 흡수
        - 물이 나오면 짜서 버리고 양념
        
        **🥬 나물 밑간 소금**
        - 시금치·콩나물 데친 후 소금으로 밑간 → 물기 짜내기 → 양념 흡수
        
        **🍎 매실청·레몬청**
        - 설탕이 과일에서 물을 빼냄 → 과일액 추출
        - 높은 당 농도로 방부 효과도 있음
        """)

    with tab2:
        st.markdown("### 의학에서의 삼투압")
        st.markdown("""
        **💉 링거액이 0.9% 식염수인 이유**
        - 우리 몸 적혈구의 등장액 농도 = 약 0.9%
        - 이보다 진한 액체 주사 → 적혈구 쪼그라듦 (탈수)
        - 이보다 묽은 액체 주사 → 적혈구 터짐 (용혈)
        - **정확히 0.9%로 맞춰야 안전**
        
        **🧂 소금물 가글**
        - 감기·목감기 때 목 점막이 부었을 때
        - 소금물로 가글하면 부기가 빠짐 (부은 세포에서 물 흡수)
        
        **🩹 상처 소독**
        - 소금물이 세균 세포에서 물을 빼내 살균 효과
        - 옛날부터 상처에 소금 뿌리던 이유
        """)

    with tab3:
        st.markdown("### 자연에서의 삼투압")
        st.markdown("""
        **🌊 바닷물고기 vs 민물고기**
        - 바닷물고기: 세포 내부 농도 < 바닷물 → 계속 물 빠짐 → 물 많이 마심
        - 민물고기: 세포 내부 농도 > 민물 → 계속 물 들어옴 → 소변 많이 배출
        - 서로 다른 환경에 사는 물고기를 바꿔 넣으면 죽는 이유
        
        **🌴 맹그로브 나무 (바닷가 식물)**
        - 짠물에서 살아남기 위해 세포 내부 농도가 매우 높음
        - 뿌리에서 소금을 걸러내는 특수 구조
        
        **🥀 시든 채소 살리기**
        - 시금치 등이 시들면 → 세포에서 물 나감
        - 찬물에 담그면 → 세포로 물이 다시 들어와 살아남
        """)

    with tab4:
        st.markdown("### 저장·보관에서의 삼투압")
        st.markdown("""
        **🥩 소금·설탕이 방부제 역할**
        - 옛날 냉장고 없을 때 → 소금·설탕으로 절여서 보관
        - 세균 세포에서 물을 빼내 미생물 증식 억제
        
        **🥓 훈제 햄·베이컨**
        - 소금·향신료로 절여서 물기 빼기
        - 삼투압으로 미생물 못 살게
        
        **🐟 젓갈**
        - 물고기·조개를 소금에 절여 발효
        - 삼투압 + 발효 원리의 결합
        """)


# ═══════════════════════════════════════════════
# 프로그램 소개
# ═══════════════════════════════════════════════
elif page == "ℹ️ 프로그램 소개":
    st.title("ℹ️ 프로그램 소개")

    st.markdown("### 🌊 WAVE 프로그램")
    st.markdown("""
    광명시 대학생 멘토단이 광명시 고등학생들과 함께하는 
    과학 실험·진로 탐색 멘토링 프로그램입니다.
    """)

    st.markdown("---")

    st.markdown("### 🔬 이 웹앱은?")
    st.markdown("""
    WAVE 프로그램 삼투압 실험에서 얻은 실제 데이터를 
    파이썬으로 분석하고, Streamlit으로 웹앱화한 결과물입니다.
    
    **사용한 기술:**
    - **Python** (numpy, matplotlib, pandas)
    - **Streamlit** (웹앱 프레임워크)
    - **선형 회귀 분석**
    - **GitHub + Streamlit Cloud** (배포)
    """)

    st.markdown("---")

    st.markdown("### 📊 실험 개요")
    st.markdown("""
    - **채소**: 무, 오이, 배추 (3종)
    - **소금 농도**: 0%, 0.5%, 1%, 1.5%, 2%, 5% (6단계)
    - **반복**: 2회
    - **측정**: 담그기 전/후 질량 변화
    - **분석**: 선형 회귀 → 등장액 농도 도출
    """)

    st.markdown("---")

    st.markdown("### 👥 팀 소개")
    st.markdown("""
    - **멘토**: 박진우 (서강대 화공생명공학과 3학년)
    - **참여 학생**: 광명고등학교 오메가9
    """)

    st.markdown("---")
    st.caption("© 2025 WAVE 프로그램 · 광명시 대학생 멘토단")

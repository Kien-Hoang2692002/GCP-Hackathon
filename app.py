import streamlit as st
import os
from dotenv import load_dotenv

# Import từ các module đã tách
from config.frameworks import FRAMEWORKS
from core.vector_engine import find_best_framework
from core.llm_engine import evaluate_idea_with_llm

# Load API Key
load_dotenv('.env')

# ============================================================================
# STREAMLIT UI CONFIG
# ============================================================================
st.set_page_config(page_title="GCP Startup Validator", page_icon="🚀", layout="centered")

# Custom CSS
st.markdown("""
<style>
    .big-score { font-size: 5rem; font-weight: 900; line-height: 1; margin-bottom: 0px; }
    .score-label { font-size: 1.2rem; font-weight: bold; color: #6b7280; text-transform: uppercase; letter-spacing: 0.1em; }
    .critical-box {
        background-color: #fef2f2; border-left: 5px solid #ef4444; 
        padding: 20px; border-radius: 8px; margin-top: 20px; margin-bottom: 20px;
    }
    .critical-title { color: #b91c1c; font-weight: bold; font-size: 1.1rem; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
    .critical-text { color: #7f1d1d; margin: 0; }
    .stProgress > div > div > div > div { background-color: #6366f1; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================
st.title("🚀 GCP Startup Validator")
st.markdown("**Dual-Engine AI**: Tự động nhận diện Khung thẩm định bằng thuật toán Vector Search (In-Memory) & Phân tích chuyên sâu bằng Gemini 2.5 Flash.")
st.divider()

# ============================================================================
# FORM INPUT
# ============================================================================
idea_input = st.text_area("💡 Mô tả ý tưởng khởi nghiệp của bạn", height=120, placeholder="Ví dụ: Nền tảng học lập trình qua game tương tác dùng AI để cá nhân hóa...")

if st.button("🚀 Thẩm Định Bằng Dual-Engine", type="primary", use_container_width=True):
    if len(idea_input) < 10:
        st.warning("Vui lòng nhập ý tưởng ít nhất 10 ký tự!")
    else:
        try:
            # ──────────────────────────────────────────────────────────────────
            # Bước 1: ENGINE 1 (VECTOR SEARCH)
            # ──────────────────────────────────────────────────────────────────
            with st.status("🧠 Đang khởi động Engine 1 (Hybrid Search)...", expanded=True) as status:
                st.write("Đang quét ma trận bằng Hybrid Search (70% Vector Semantic + 30% Keyword Exact Match)...")
                
                selected_fw, confidence = find_best_framework(idea_input, FRAMEWORKS)
                
                st.write(f"✅ Đã chốt Khung thẩm định: **{selected_fw['name']}** (Độ khớp: {confidence}%)")
                
                # ──────────────────────────────────────────────────────────────────
                # Bước 2: ENGINE 2 (LLM ANALYSIS)
                # ──────────────────────────────────────────────────────────────────
                st.write("🤖 Đang khởi động Engine 2 (LLM Structured Output)...")
                st.write(f"Đang đẩy quy tắc của {selected_fw['name']} vào Gemini 2.5 Flash...")
                
                result = evaluate_idea_with_llm(idea_input, selected_fw)
                
                status.update(label="Hoàn tất thẩm định!", state="complete", expanded=False)
                
            # ==========================================================
            # RENDER KẾT QUẢ
            # ==========================================================
            st.divider()
            st.success(f"**🎯 Framework được chọn tự động:** {selected_fw['name']} | **Độ tin cậy của thuật toán:** {confidence}%")
            
            # Điểm tổng quan
            viability_score = round((result['problemSolutionScore'] + result['marketFitScore'] + result['scalabilityScore']) / 3)
            
            color = "🟢" if viability_score >= 70 else "🟡" if viability_score >= 50 else "🔴"
            verdict = "Khuyến nghị khả thi" if viability_score >= 70 else "Tiềm năng trung bình" if viability_score >= 50 else "Cần tinh chỉnh nhiều"
            
            col_score, col_chart = st.columns([1, 1.5])
            
            with col_score:
                st.markdown(f"<div class='score-label'>Viability Score</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='big-score'>{viability_score}</div>", unsafe_allow_html=True)
                st.markdown(f"**{color} {verdict}**")
                
            with col_chart:
                st.write("**Chỉ số chuyên sâu**")
                
                st.caption(f"Problem-Solution Fit: {result['problemSolutionScore']}/100")
                st.progress(result['problemSolutionScore'] / 100)
                
                st.caption(f"Market Fit: {result['marketFitScore']}/100")
                st.progress(result['marketFitScore'] / 100)
                
                st.caption(f"Scalability: {result['scalabilityScore']}/100")
                st.progress(result['scalabilityScore'] / 100)

            # Critical Flaw
            if 'criticalFlaw' in result and result['criticalFlaw']:
                st.markdown(f"""
                <div class="critical-box">
                    <div class="critical-title">⚠️ ĐIỂM YẾU CHÍ MẠNG (CRITICAL FLAW)</div>
                    <p class="critical-text">{result['criticalFlaw']}</p>
                </div>
                """, unsafe_allow_html=True)

            # Analysis Details
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**🌍 Quy mô thị trường**\n\n{result['marketSizeAnalysis']}")
            with col2:
                st.warning(f"**⚔️ Rủi ro cạnh tranh**\n\n{result['competitiveRisk']}")

            # Action Plan
            st.subheader("📋 Kế Hoạch Hành Động Tiếp Theo")
            for i, step in enumerate(result['nextSteps']):
                st.checkbox(step, key=f"step_{i}")

        except Exception as e:
            st.error(f"❌ Có lỗi xảy ra trong quá trình xử lý:\n\n{str(e)}")

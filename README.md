# 🚀 GCP Startup Validator

> **Dual-Engine AI** — Công cụ thẩm định ý tưởng khởi nghiệp bằng AI, tự động nhận diện khung thẩm định phù hợp và phân tích chuyên sâu.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-4285F4.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Mục lục

- [Giới thiệu](#giới-thiệu)
- [Kiến trúc Dual-Engine](#kiến-trúc-dual-engine)
- [Cài đặt & Chạy](#cài-đặt--chạy)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Cách sử dụng](#cách-sử-dụng)
- [Công nghệ](#công-nghệ)
- [Tài liệu liên quan](#tài-liệu-liên-quan)

---

## Giới thiệu

**GCP Startup Validator** là công cụ AI giúp sinh viên và founder trẻ **đánh giá ý tưởng startup một cách khách quan, có hệ thống** dựa trên các framework khởi nghiệp chuẩn quốc tế (YC Startup School, Lean Canvas, Blue Ocean Strategy, v.v.).

### Vấn đề giải quyết

- ❌ Sinh viên đánh giá ý tưởng bằng **cảm tính**, thiếu framework
- ❌ Không phân tích được **Market Size, Competitive Landscape, Regulatory Barriers**
- ❌ Không biết **điểm yếu** nào cần ưu tiên khắc phục
- ❌ Thiếu **lộ trình hành động** cụ thể từ giai đoạn ý tưởng

### Giải pháp

- ✅ **Dual-Engine AI**: Vector Search (tự chọn framework) + Gemini LLM (phân tích chuyên sâu)
- ✅ **Structured Output**: Kết quả JSON chuẩn → UI trực quan
- ✅ **PDF Report**: Xuất báo cáo thẩm định chuyên nghiệp
- ✅ **Multi-Framework**: Hỗ trợ 5+ framework thẩm định khởi nghiệp

---

## Kiến trúc Dual-Engine

```
User Input (Ý tưởng + Mô tả)
         │
         ▼
┌─────────────────────────────────┐
│   ENGINE 1: Vector Search       │  ← In-Memory Hybrid Search
│   (70% Semantic + 30% Keyword)  │     Tự động chọn framework phù hợp
└──────────────┬──────────────────┘
               │ Framework + Quy tắc thẩm định
               ▼
┌─────────────────────────────────┐
│   ENGINE 2: Gemini 2.5 Flash    │  ← Structured Output (JSON)
│   (LLM Analysis)                │     Phân tích chuyên sâu theo framework
└──────────────┬──────────────────┘
               │ JSON kết quả
               ▼
┌─────────────────────────────────┐
│   Streamlit UI + PDF Export     │  ← Hiển thị Score, Analysis, Action Plan
└─────────────────────────────────┘
```

### Các framework được hỗ trợ

| Framework | Mô tả |
|---|---|
| **YC Startup School** | Đánh giá Problem-Solution Fit, Founder-Market Fit |
| **Lean Canvas** | Phân tích 9 khối cạnh tranh của Ash Maurya |
| **Blue Ocean Strategy** | ERRRC Grid — Không cạnh tranh trực diện |
| **Design Thinking** | Desirability, Feasibility, Viability |
| **Disciplined Entrepreneurship** | 24 bước của Bill Aulet (MIT) |

---

## Cài đặt & Chạy

### Yêu cầu

- Python 3.10+
- Google Gemini API Key ([lấy tại đây](https://aistudio.google.com/apikey))

### Cài đặt

```bash
# 1. Clone repository
git clone https://github.com/Kien-Hoang2692002/GCP-Hackathon.git
cd GCP-Hackathon

# 2. Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Tạo file .env với API Key
echo 'GEMINI_API_KEY=your-api-key-here' > .env
```

### Chạy ứng dụng

```bash
streamlit run app.py
```

Mở trình duyệt tại: **http://localhost:8501**

---

## Cấu trúc dự án

```
GCP-Hackathon/
├── app.py                      # Streamlit UI chính
├── requirements.txt            # Python dependencies
├── .env                        # API Key (không commit)
│
├── config/
│   └── frameworks.py           # Định nghĩa 5+ framework thẩm định
│
├── core/
│   ├── vector_engine.py        # Engine 1: Hybrid Vector Search (In-Memory)
│   ├── llm_engine.py           # Engine 2: Gemini LLM Structured Output
│   └── pdf_generator.py        # Xuất báo cáo PDF
│
├── AGENTS.md                   # Định nghĩa AI Agents
├── PRD.md                      # Product Requirements Document
├── PLAN.md                     # Kế hoạch triển khai
├── RULES.md                    # Quy tắc phát triển
├── SKILLS.md                   # Kỹ năng & công nghệ
└── TEST-CASE.md                # Test cases
```

---

## Cách sử dụng

1. **Nhập ý tưởng** vào ô text area (tối thiểu 10 ký tự)
2. **Nhấn nút "Thẩm Định"** để khởi động Dual-Engine
3. **Xem kết quả**:
   - 🎯 **Framework được chọn** tự động + độ tin cậy
   - 📊 **Điểm số** (Problem-Solution Fit, Market Fit, Scalability)
   - 📋 **Phân tích chi tiết** theo quy tắc của framework
   - ⚠️ **Rủi ro & Cơ hội**
   - ✅ **Action Plan** — lộ trình hành động cụ thể
4. **Tải báo cáo PDF** để chia sẻ với team hoặc mentor

---

## Công nghệ

| Công nghệ | Mục đích |
|---|---|
| **Python 3.10+** | Ngôn ngữ chính |
| **Streamlit** | UI Framework |
| **Gemini 2.5 Flash** | LLM phân tích ý tưởng |
| **Scikit-learn** | TF-IDF Vectorization cho Engine 1 |
| **Plotly** | Biểu đồ trực quan hóa điểm số |
| **fpdf2** | Xuất báo cáo PDF |
| **python-dotenv** | Quản lý biến môi trường |

---

## Tài liệu liên quan

- [📄 PRD.md](./PRD.md) — Product Requirements Document
- [📋 PLAN.md](./PLAN.md) — Kế hoạch triển khai chi tiết
- [🤖 AGENTS.md](./AGENTS.md) — Định nghĩa AI Agents
- [📏 RULES.md](./RULES.md) — Quy tắc phát triển
- [🧪 TEST-CASE.md](./TEST-CASE.md) — Test cases

---

<p align="center">
  <b>Made with ❤️ for GCP Hackathon — AI20K-128</b>
</p>

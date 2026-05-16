# 📋 PLAN.md — Kế hoạch triển khai: Thẩm Định Ý Tưởng Khởi Nghiệp & Cơ Hội

## 🏷️ Thông tin dự án

| Trường | Giá trị |
|---|---|
| **Mã dự án** | AI20K-128 |
| **Tên dự án** | Thẩm Định Ý Tưởng Khởi Nghiệp & Cơ Hội |
| **Danh mục** | Khởi nghiệp & Đổi mới |
| **Loại** | Text / LLM Agent |
| **Tech Stack** | Next.js, Gemini API, Structured Output, RAG (In-Memory) |

---

## 🎯 Bài toán cần giải quyết

Sinh viên khởi nghiệp thường **đánh giá ý tưởng dựa trên cảm tính**, thiếu công cụ phân tích:
- **Market size** (quy mô thị trường)
- **Competitive landscape** (đối thủ cạnh tranh)
- **Regulatory barriers** (rào cản pháp lý)
- **Viability scoring** (điểm khả thi tổng thể)

---

## 🏗️ Kiến trúc giải pháp (In-Memory RAG Framework)

```
User Input (Idea + Sector)
        │
        ▼
┌──────────────────────────┐
│   Knowledge Base (JSON)  │  ← Hardcoded: YC Framework,
│   - Competitors          │     Lean Canvas, Market Data
│   - Barriers             │     per sector
│   - YC/Lean Principles   │
└──────────┬───────────────┘
           │ RAG: fetch relevant context
           ▼
┌──────────────────────────┐
│   Gemini 1.5 Flash API   │  ← Structured Output (JSON)
│   (Structured Output)    │
└──────────┬───────────────┘
           │ Returns strict JSON
           ▼
┌──────────────────────────┐
│   Next.js Frontend UI    │  ← Renders:
│   - Viability Score      │    - Score card + progress bar
│   - Problem-Solution Fit │    - Analysis cards
│   - Competitive Analysis │    - Action plan checklist
│   - Action Plan          │
└──────────────────────────┘
```

---

## 📁 Cấu trúc thư mục dự án

```
GCP-Hackathon/
├── src/
│   └── app/
│       ├── api/
│       │   └── evaluate/
│       │       └── route.js        # Core API: RAG + Gemini Structured Output
│       ├── page.js                 # Landing / Home page
│       ├── layout.js               # Root layout
│       └── globals.css             # Global styles
├── data/
│   └── knowledge-base.json         # Market knowledge per sector
├── components/
│   ├── EvaluationForm.jsx          # Input form (dropdown + textarea)
│   ├── ScoreCard.jsx               # Viability score display
│   ├── AnalysisCard.jsx            # Problem-fit + Competitive cards
│   └── ActionPlan.jsx              # Checklist component
├── public/
├── .env.local                      # GEMINI_API_KEY
├── PLAN.md
├── PRD.md
├── AGENTS.md
├── RULES.md
├── SKILLS.md
├── package.json
└── README.md
```

---

## ⏱️ Timeline 3 giờ (Sprint Plan)

### ⚡ Giờ 1 — Foundation (Backend + Data)
| Task | Thời gian ước tính | Người làm |
|---|---|---|
| Init Next.js project (`npx create-next-app`) | 5 phút | Dev |
| Tạo `data/knowledge-base.json` với 5 ngành | 15 phút | Dev |
| Viết API route `/api/evaluate/route.js` | 20 phút | Dev |
| Test API với Postman / curl | 10 phút | Dev |
| Cấu hình `.env.local` với Gemini API key | 5 phút | Dev |
| **Buffer** | 5 phút | — |

### 🎨 Giờ 2 — Frontend UI
| Task | Thời gian ước tính | Người làm |
|---|---|---|
| Layout chính + Global CSS | 10 phút | Dev |
| `EvaluationForm.jsx` (Dropdown + Textarea + Button) | 15 phút | Dev |
| `ScoreCard.jsx` (Score lớn + Progress bar) | 15 phút | Dev |
| `AnalysisCard.jsx` (Fit + Competitive) | 10 phút | Dev |
| `ActionPlan.jsx` (Checklist steps) | 10 phút | Dev |

### 🚀 Giờ 3 — Integration, Polish & Deploy
| Task | Thời gian ước tính | Người làm |
|---|---|---|
| Kết nối Frontend ↔ API | 10 phút | Dev |
| Loading state + Error handling | 10 phút | Dev |
| UI Polish (animations, responsive) | 15 phút | Dev |
| Deploy lên Vercel | 10 phút | Dev |
| Kiểm tra link nộp bài | 5 phút | Dev |
| **Buffer** | 10 phút | — |

---

## 🌐 Các Sector (Ngành) hỗ trợ

| Sector Key | Tên hiển thị |
|---|---|
| `ai` | AI / Machine Learning |
| `saas` | SaaS / B2B Software |
| `fintech` | FinTech / Financial Services |
| `edtech` | EdTech / Education |
| `ecommerce` | E-Commerce / Marketplace |

---

## 📤 Structured Output Schema (Gemini Response)

```json
{
  "problemSolutionFit": "string (max 2 câu)",
  "competitiveLandscape": "string (max 2 câu)",
  "viabilityScore": 0–100,
  "actionPlan": ["Bước 1...", "Bước 2...", "Bước 3..."],
  "strengths": ["Điểm mạnh 1...", "Điểm mạnh 2..."],
  "risks": ["Rủi ro 1...", "Rủi ro 2..."]
}
```

---

## ✅ Tiêu chí thành công (Definition of Done)

- [ ] API trả về JSON hợp lệ trong < 3 giây
- [ ] Giao diện hiển thị đúng tất cả các trường kết quả
- [ ] Score bar đổi màu đúng (xanh/vàng/đỏ)
- [ ] Action plan hiển thị dạng checklist
- [ ] Chạy được trên Vercel (production URL)
- [ ] Demo không bị lỗi khi thao tác live

---

## 🔑 Biến môi trường cần thiết

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🎖️ Điểm kỹ thuật nổi bật (cho BGK)

1. **Structured Output**: Ép Gemini trả JSON nghiêm ngặt → đồng bộ AI & UI
2. **RAG Pattern**: Truy xuất context từ Knowledge Base trước khi gọi LLM
3. **Framework-based Evaluation**: Áp dụng YC + Lean Canvas chuẩn chỉnh
4. **Real-time UX**: Phản hồi < 2 giây, không cào web (zero latency overhead)

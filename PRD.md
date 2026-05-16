# 📄 PRD.md — Product Requirements Document
## Startup Idea Validator — AI20K-128

**Phiên bản:** 1.0  
**Ngày tạo:** 2026-05-16  
**Trạng thái:** Draft → In Development  

---

## 1. Tổng quan sản phẩm (Product Overview)

### 1.1 Tên sản phẩm
**GCP Startup Validator** — Công cụ Thẩm Định Ý Tưởng Khởi Nghiệp bằng AI

### 1.2 Elevator Pitch
> Một công cụ AI giúp sinh viên và founder trẻ **đánh giá ý tưởng startup một cách khách quan, có hệ thống** dựa trên framework Y Combinator & Lean Canvas — thay thế hoàn toàn cảm tính và phán đoán thiếu căn cứ.

### 1.3 Vấn đề cần giải quyết
- Sinh viên khởi nghiệp **đánh giá ý tưởng bằng cảm tính**, không có framework
- Thiếu khả năng phân tích **Market Size, Competitive Landscape, Regulatory Barriers**
- Không biết **điểm yếu** nào cần ưu tiên khắc phục trước khi đi pitching
- Không có **lộ trình hành động** cụ thể từ giai đoạn ý tưởng

### 1.4 Giải pháp
Xây dựng **AI Agent thẩm định startup** ứng dụng kỹ thuật:
- **RAG (Retrieval-Augmented Generation)**: Truy xuất dữ liệu thị trường từ Knowledge Base cục bộ
- **Structured Output**: Ép Gemini trả về JSON chuẩn để render UI chuyên nghiệp
- **Multi-framework Evaluation**: Kết hợp YC Startup School + Lean Canvas

---

## 2. Người dùng mục tiêu (Target Users)

| Nhóm | Mô tả | Nhu cầu chính |
|---|---|---|
| **Sinh viên khởi nghiệp** | Năm 2–4 đại học, có ý tưởng startup | Xác nhận ý tưởng có khả thi không |
| **First-time Founders** | Chưa có kinh nghiệm startup trước đó | Biết nên làm gì tiếp theo |
| **Mentor / Giảng viên** | Người hỗ trợ sinh viên thi pitch | Công cụ pre-screen ý tưởng nhanh |

---

## 3. Tính năng (Features)

### 3.1 Tính năng cốt lõi (MVP — Must Have)

#### F1: Form nhập ý tưởng
- **Mô tả**: Form đơn giản để người dùng nhập ý tưởng và chọn ngành
- **Components**:
  - `Dropdown` chọn sector: AI, SaaS, FinTech, EdTech, E-Commerce
  - `Textarea` nhập mô tả ý tưởng (tối thiểu 50 ký tự)
  - `Button` "Thẩm Định Dự Án" với loading state
- **Acceptance Criteria**:
  - [ ] Validate không cho submit khi textarea trống
  - [ ] Hiển thị spinner / loading animation khi đang xử lý
  - [ ] Disable button khi đang fetch

#### F2: Viability Score Card
- **Mô tả**: Hiển thị điểm khả thi tổng thể của ý tưởng
- **Components**:
  - Số điểm lớn (0–100) với font size nổi bật
  - Progress bar đổi màu động:
    - 🟢 Xanh lá: ≥ 70 điểm ("Tiềm năng cao")
    - 🟡 Vàng: 50–69 điểm ("Cần cải thiện")
    - 🔴 Đỏ: < 50 điểm ("Rủi ro cao")
  - Label mô tả mức độ
- **Acceptance Criteria**:
  - [ ] Màu score thay đổi đúng theo ngưỡng
  - [ ] Animation khi số chạy từ 0 → giá trị thực
  - [ ] Responsive trên mobile

#### F3: Problem-Solution Fit Analysis
- **Mô tả**: Card phân tích độ khớp giữa vấn đề và giải pháp
- **Components**:
  - Icon + Title "🎯 Problem-Solution Fit"
  - Text 1–2 câu từ Gemini
- **Acceptance Criteria**:
  - [ ] Render đúng nội dung từ `problemSolutionFit` field
  - [ ] Card có hover effect

#### F4: Competitive Landscape Analysis
- **Mô tả**: Card phân tích bức tranh đối thủ cạnh tranh
- **Components**:
  - Icon + Title "⚔️ Competitive Landscape"
  - Text từ Gemini dựa trên market knowledge
- **Acceptance Criteria**:
  - [ ] Render đúng nội dung từ `competitiveLandscape` field
  - [ ] Đề cập đúng đối thủ của ngành được chọn

#### F5: Action Plan Checklist
- **Mô tả**: Danh sách các bước hành động cụ thể
- **Components**:
  - List item dạng checklist (có thể tick)
  - Numbered steps từ Gemini
- **Acceptance Criteria**:
  - [ ] Render tất cả items trong `actionPlan` array
  - [ ] Có thể checkbox từng bước (local state)
  - [ ] Tối thiểu 3 bước action

### 3.2 Tính năng mở rộng (Nice to Have)

| Feature | Mô tả | Độ ưu tiên |
|---|---|---|
| **F6: Strengths & Risks** | Highlight điểm mạnh và rủi ro riêng | Medium |
| **F7: Share Result** | Copy link hoặc export PDF | Low |
| **F8: Compare Ideas** | Lưu và so sánh nhiều ý tưởng | Low |
| **F9: Detailed Framework View** | Xem đầy đủ YC checklist | Medium |

---

## 4. Luồng người dùng (User Flow)

```
[Trang chủ]
    │
    ├─ Xem giới thiệu & CTA
    │
    └─ [Form Đánh Giá]
           │
           ├─ Chọn Sector (Dropdown)
           ├─ Nhập Ý Tưởng (Textarea)
           └─ Click "Thẩm Định Dự Án"
                  │
                  ├─ Loading State (Spinner)
                  │
                  └─ [Kết Quả Đánh Giá]
                         │
                         ├─ Viability Score Card
                         ├─ Problem-Solution Fit
                         ├─ Competitive Landscape
                         └─ Action Plan Checklist
                                │
                                └─ [Đánh Giá Lại] → Quay lại Form
```

---

## 5. Technical Requirements

### 5.1 API Endpoint

**POST** `/api/evaluate`

**Request Body:**
```json
{
  "idea": "string (mô tả ý tưởng startup)",
  "sector": "ai | saas | fintech | edtech | ecommerce"
}
```

**Response:**
```json
{
  "problemSolutionFit": "string",
  "competitiveLandscape": "string",
  "viabilityScore": 0–100,
  "actionPlan": ["string", "string", "string"],
  "strengths": ["string"],
  "risks": ["string"]
}
```

**Error Response:**
```json
{ "error": "string", "code": "number" }
```

### 5.2 Knowledge Base Schema (data/knowledge-base.json)

```json
{
  "sector_key": {
    "name": "Tên ngành hiển thị",
    "competitors": "Danh sách đối thủ",
    "barriers": "Rào cản ngành",
    "marketSize": "Quy mô thị trường",
    "framework": "Triết lý YC/Lean Canvas cho ngành"
  }
}
```

### 5.3 Non-Functional Requirements

| Requirement | Target |
|---|---|
| **Response Time** | < 3 giây (P95) |
| **Availability** | 99% (Vercel hosting) |
| **Mobile Responsive** | ✅ Breakpoints: 375px, 768px, 1280px |
| **Browser Support** | Chrome, Firefox, Safari (latest 2 versions) |
| **Accessibility** | WCAG 2.1 AA cơ bản |

---

## 6. Tech Stack

| Layer | Technology | Lý do chọn |
|---|---|---|
| **Frontend** | Next.js 14 (App Router) | SSR + API routes trong 1 project |
| **Styling** | Tailwind CSS | Nhanh, đẹp, utility-first |
| **AI Model** | Gemini 1.5 Flash | Nhanh, rẻ, hỗ trợ Structured Output |
| **RAG** | In-Memory JSON | Không cần vector DB, đủ nhanh cho hackathon |
| **Deploy** | Vercel | Zero-config deploy với Next.js |

---

## 7. Định nghĩa hoàn thành (Definition of Done)

- [ ] API `/api/evaluate` trả về JSON hợp lệ với tất cả fields
- [ ] UI render đúng Score, Analysis cards, Action Plan
- [ ] Score bar đổi màu theo ngưỡng (green/yellow/red)
- [ ] Loading state hiển thị khi fetch
- [ ] Error handling hiển thị message thân thiện
- [ ] Deploy thành công lên Vercel với production URL
- [ ] Demo không crash trong 10 lần thử liên tiếp

---

## 8. Rủi ro & Giải pháp

| Rủi ro | Xác suất | Giải pháp |
|---|---|---|
| Gemini API rate limit | Thấp | Dùng Flash model, ít token |
| AI không trả JSON chuẩn | Trung bình | Sanitize + try/catch + fallback |
| Deploy Vercel thất bại | Thấp | Test local trước, env vars setup sẵn |
| UI xấu không ăn điểm | Thấp | Dùng Tailwind + component library |

---

*Tài liệu này là living document, cập nhật theo tiến độ hackathon.*

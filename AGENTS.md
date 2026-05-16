# 🤖 AGENTS.md — Định nghĩa AI Agents

> Mô tả các AI Agent trong **GCP Startup Validator** (AI20K-128).

---

## Tổng quan kiến trúc

```
User Input (idea + sector)
       │
       ▼
[Agent 1: Knowledge Retriever]  ← Lookup JSON Knowledge Base
       │
       ▼
[Agent 2: Evaluation Agent]     ← Gemini 1.5 Flash + Structured Output
       │
       ▼
[Agent 3: Output Validator]     ← Validate JSON schema
       │
       ▼
Response to Frontend
```

---

## Agent 1: Knowledge Retriever (RAG Module)

**Vị trí:** `src/app/api/evaluate/route.js`

**Mô tả:** Truy xuất thông tin thị trường từ Knowledge Base cục bộ theo sector.

```
Input:  sector ("ai" | "saas" | "fintech" | "edtech" | "ecommerce")
Output: { competitors, barriers, marketSize, framework }
Fallback: Nếu sector không tồn tại → dùng "ai"
```

---

## Agent 2: Startup Evaluation Agent

**Model:** `gemini-1.5-flash`  
**Endpoint:** `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent`

**Nhiệm vụ:** Đánh giá ý tưởng startup dựa trên framework YC + Lean Canvas.

**System Prompt:** Đóng vai Nhà thẩm định YC, bắt buộc trả về JSON thuần.

**Output Schema (Strict JSON):**
```json
{
  "problemSolutionFit": "string (max 2 câu)",
  "competitiveLandscape": "string (max 2 câu)",
  "viabilityScore": 85,
  "actionPlan": ["Bước 1", "Bước 2", "Bước 3"],
  "strengths": ["Điểm mạnh 1", "Điểm mạnh 2"],
  "risks": ["Rủi ro 1", "Rủi ro 2"]
}
```

**Config:**
- Temperature: 0.7
- Timeout: 10s (Vercel limit)

---

## Agent 3: Output Validator

**Nhiệm vụ:** Validate JSON từ Gemini trước khi trả về frontend.

```javascript
// Required fields
const required = ['problemSolutionFit', 'competitiveLandscape', 'viabilityScore', 'actionPlan'];
// viabilityScore phải là number (0-100)
// actionPlan phải là array
```

---

## Môi trường

```env
GEMINI_API_KEY=AIza...   # Lấy từ Google AI Studio
```

---

## Test Agent

```bash
curl -X POST http://localhost:3000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"idea": "App kết nối gia sư và học sinh", "sector": "edtech"}'
```

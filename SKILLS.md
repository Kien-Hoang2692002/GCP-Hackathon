# 🛠️ SKILLS.md — Kỹ năng & Kỹ thuật sử dụng

> Tài liệu này mô tả các kỹ thuật, pattern và skill được áp dụng trong **GCP Startup Validator** (AI20K-128).

---

## 1. Core Skills

### 1.1 Structured Output (⭐ Key Technique)

**Là gì?** Kỹ thuật **ép AI trả về dữ liệu theo cấu trúc JSON cố định** thay vì text tự do.

**Tại sao quan trọng?**
- Frontend render trực tiếp từ JSON — không cần parse text phức tạp
- Kết quả nhất quán, dễ debug
- Thể hiện tư duy engineering chuyên nghiệp với BGK

**Cách triển khai:**
```javascript
const systemPrompt = `
...
BẮT BUỘC: Trả về JSON thuần, không có \`\`\`json, không có markdown.
Cấu trúc chính xác:
{
  "viabilityScore": <số nguyên 0-100>,
  "problemSolutionFit": "<chuỗi max 2 câu>",
  "competitiveLandscape": "<chuỗi max 2 câu>",
  "actionPlan": ["<bước 1>", "<bước 2>", "<bước 3>"],
  "strengths": ["<điểm mạnh 1>", "<điểm mạnh 2>"],
  "risks": ["<rủi ro 1>", "<rủi ro 2>"]
}`;
```

**Sanitization pattern:**
```javascript
let text = raw.trim();
if (text.startsWith("```json")) text = text.slice(7);
if (text.startsWith("```")) text = text.slice(3);
if (text.endsWith("```")) text = text.slice(0, -3);
return JSON.parse(text.trim());
```

---

### 1.2 RAG — Retrieval-Augmented Generation

**Là gì?** Kỹ thuật **truy xuất thông tin từ Knowledge Base** rồi nhúng vào prompt trước khi gọi LLM.

**Pattern sử dụng (In-Memory RAG):**
```
User Query (sector)
      │
      ▼
Knowledge Base Lookup  ←── data/knowledge-base.json
      │
      ▼
Context Injection (vào prompt)
      │
      ▼
LLM Generation (Gemini)
      │
      ▼
Structured Response
```

**Ưu điểm so với web search:**
- ✅ Không bị rate limit API ngoài
- ✅ Phản hồi < 2 giây (không có network overhead)
- ✅ Dữ liệu curated, đáng tin cậy
- ✅ Không timeout khi deploy

**Knowledge Base Structure:**
```json
{
  "sector": {
    "name": "Tên hiển thị",
    "competitors": "Danh sách đối thủ chính",
    "barriers": "Rào cản ngành",
    "marketSize": "Quy mô thị trường ước tính",
    "framework": "Insight từ YC/Lean Canvas cho ngành này"
  }
}
```

---

### 1.3 Prompt Engineering

**Kỹ thuật áp dụng:**

| Kỹ thuật | Mô tả | Áp dụng ở đâu |
|---|---|---|
| **Role Prompting** | Gán vai trò "Nhà thẩm định YC" cho AI | System prompt |
| **Few-shot Examples** | Cung cấp ví dụ JSON output mẫu | System prompt |
| **Constraint Setting** | Giới hạn số câu, format bắt buộc | System prompt |
| **Context Injection** | Nhúng market data vào prompt | Trước khi gọi API |
| **Chain of Thought** | Hướng dẫn AI suy nghĩ theo framework | Trong prompt |

---

### 1.4 Next.js App Router

**Kiến thức cần có:**

```
src/app/
├── page.js              # Server Component (default)
├── layout.js            # Root layout
├── globals.css          # Global styles
└── api/
    └── evaluate/
        └── route.js     # API Route Handler
```

**API Route pattern:**
```javascript
// route.js
import { NextResponse } from 'next/server';

export async function POST(request) {
  const body = await request.json();
  // ... xử lý
  return NextResponse.json(data);
}
```

**Client Component (cần "use client"):**
```javascript
'use client';
import { useState } from 'react';

export default function EvaluationForm() {
  const [loading, setLoading] = useState(false);
  // ...
}
```

---

### 1.5 React Patterns

**Custom Hooks cho API calls:**
```javascript
// hooks/useEvaluate.js
export function useEvaluate() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const evaluate = async (idea, sector) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idea, sector })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { result, loading, error, evaluate };
}
```

---

## 2. Frontend Skills

### 2.1 Tailwind CSS Patterns

**Score color với dynamic class:**
```javascript
// ❌ SAI — Tailwind không hỗ trợ dynamic class concatenation
const colorClass = `text-${score > 70 ? 'green' : 'red'}-500`;

// ✅ ĐÚNG — Map đầy đủ
const getScoreColor = (score) => {
  if (score >= 70) return 'text-green-500 bg-green-500';
  if (score >= 50) return 'text-yellow-500 bg-yellow-500';
  return 'text-red-500 bg-red-500';
};
```

**Progress bar animation:**
```jsx
<div className="w-full bg-gray-200 rounded-full h-4">
  <div
    className={`h-4 rounded-full transition-all duration-1000 ${barColor}`}
    style={{ width: `${score}%` }}
  />
</div>
```

### 2.2 Loading States
```jsx
{loading ? (
  <div className="flex items-center gap-2">
    <div className="animate-spin h-5 w-5 border-2 border-blue-500 rounded-full border-t-transparent" />
    <span>Đang thẩm định...</span>
  </div>
) : (
  <span>Thẩm Định Dự Án</span>
)}
```

---

## 3. Backend Skills

### 3.1 Error Handling Pattern
```javascript
export async function POST(req) {
  try {
    // 1. Parse & validate input
    const { idea, sector } = await req.json();
    if (!idea || !sector) {
      return NextResponse.json({ error: "Thiếu thông tin đầu vào" }, { status: 400 });
    }

    // 2. RAG retrieval
    // 3. LLM call
    // 4. Parse & validate output
    // 5. Return success

  } catch (error) {
    console.error('[/api/evaluate]', error);
    return NextResponse.json(
      { error: "Có lỗi xảy ra, vui lòng thử lại!" },
      { status: 500 }
    );
  }
}
```

### 3.2 Gemini API Call Pattern
```javascript
const response = await fetch(
  `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${process.env.GEMINI_API_KEY}`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contents: [{
        parts: [{ text: fullPrompt }]
      }],
      generationConfig: {
        temperature: 0.7,
        maxOutputTokens: 1024
      }
    })
  }
);

const data = await response.json();
const rawText = data.candidates[0].content.parts[0].text;
```

---

## 4. DevOps Skills

### 4.1 Vercel Deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Set environment variables
vercel env add GEMINI_API_KEY
```

### 4.2 Environment Variables
```bash
# Development
# File: .env.local (KHÔNG commit)
GEMINI_API_KEY=AIza...

# Production (Vercel Dashboard)
# Settings → Environment Variables → Add
```

---

## 5. Công cụ Debug

### Debug API response
```javascript
// Tạm thời thêm vào route.js để debug
console.log('[Debug] Raw AI response:', aiText.substring(0, 200));
console.log('[Debug] Parsed result:', JSON.stringify(result, null, 2));
```

### Test với curl
```bash
# Test local
curl -X POST http://localhost:3000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"idea":"Ứng dụng học tiếng Anh với AI","sector":"edtech"}' | python3 -m json.tool

# Test production
curl -X POST https://your-app.vercel.app/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"idea":"Test idea","sector":"ai"}'
```

---

## 6. Tham khảo & Tài nguyên

| Tài nguyên | Link |
|---|---|
| Gemini API Docs | https://ai.google.dev/docs |
| Next.js App Router | https://nextjs.org/docs/app |
| Tailwind CSS | https://tailwindcss.com/docs |
| YC Startup School | https://www.startupschool.org |
| Lean Canvas | https://leanstack.com/lean-canvas |
| Vercel Deploy Docs | https://vercel.com/docs |

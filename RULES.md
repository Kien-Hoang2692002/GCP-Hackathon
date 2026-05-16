# 📏 RULES.md — Quy tắc phát triển dự án

> Quy tắc bắt buộc cho tất cả contributors của **GCP Startup Validator** (AI20K-128).

---

## 1. Quy tắc Code

### 1.1 Ngôn ngữ & Frameworks
- **Frontend**: Next.js 14 (App Router), React, Tailwind CSS
- **Backend**: Next.js API Routes (không dùng Express riêng)
- **AI**: Chỉ dùng Gemini API — không dùng OpenAI hay Anthropic
- **Database**: Không dùng DB — tất cả knowledge base là JSON cục bộ

### 1.2 Cấu trúc file
```
src/app/api/          # API routes (server-side only)
src/app/              # Pages (App Router)
components/           # Shared React components
data/                 # JSON knowledge base files
public/               # Static assets
```

### 1.3 Naming conventions
- **Files/Folders**: `camelCase` cho JS/JSX, `kebab-case` cho CSS
- **Components**: `PascalCase` (ví dụ: `ScoreCard.jsx`)
- **API Routes**: `route.js` (Next.js convention)
- **Constants**: `UPPER_SNAKE_CASE`
- **Functions**: `camelCase`, bắt đầu bằng động từ (`getMarketData`, `evaluateIdea`)

### 1.4 Quy tắc React
- Dùng **functional components** + hooks, không dùng class components
- Mỗi component chỉ làm **một nhiệm vụ duy nhất** (Single Responsibility)
- Props phải có **default values** hoặc validation rõ ràng
- Không để logic business trong UI components — tách sang hooks hoặc utils

---

## 2. Quy tắc AI / LLM

### 2.1 Structured Output (Bắt buộc)
- **LUÔN LUÔN** yêu cầu AI trả về JSON thuần trong system prompt
- **LUÔN LUÔN** sanitize response trước khi `JSON.parse()`
- **LUÔN LUÔN** wrap `JSON.parse()` trong `try/catch`

```javascript
// ✅ ĐÚNG
let aiText = response.trim();
if (aiText.startsWith("```json")) aiText = aiText.slice(7);
if (aiText.endsWith("```")) aiText = aiText.slice(0, -3);
const result = JSON.parse(aiText.trim());

// ❌ SAI — không sanitize
const result = JSON.parse(response);
```

### 2.2 Prompt Engineering
- System prompt phải nêu rõ **format output mong muốn**
- Cung cấp **ví dụ JSON** trong prompt để AI học theo
- **Không** để user input ảnh hưởng trực tiếp vào system prompt (prompt injection)

### 2.3 Knowledge Base
- Dữ liệu trong `data/knowledge-base.json` phải **chuẩn xác và không bias**
- Mỗi sector cần có ít nhất: `competitors`, `barriers`, `framework`
- **Không hardcode** API key trong Knowledge Base hay bất kỳ file nào

---

## 3. Quy tắc Security

### 3.1 API Keys
- **TUYỆT ĐỐI KHÔNG** commit API key lên Git
- Tất cả secrets phải trong `.env.local` (đã có trong `.gitignore`)
- Trên Vercel: dùng Environment Variables trong Settings

### 3.2 Input Validation
- Validate **tất cả** input từ user trước khi xử lý
- Sanitize `idea` input: strip HTML tags, limit length (max 2000 chars)
- Validate `sector` nằm trong whitelist: `["ai", "saas", "fintech", "edtech", "ecommerce"]`

```javascript
// ✅ ĐÚNG
const VALID_SECTORS = ["ai", "saas", "fintech", "edtech", "ecommerce"];
if (!VALID_SECTORS.includes(sector)) {
  return NextResponse.json({ error: "Invalid sector" }, { status: 400 });
}
```

### 3.3 Error Handling
- **Không bao giờ** expose stack trace hoặc error detail ra client
- Log đầy đủ ở server, trả về message thân thiện cho user

```javascript
// ✅ ĐÚNG
} catch (error) {
  console.error('[evaluate] Error:', error.message);
  return NextResponse.json({ error: "Có lỗi xảy ra, vui lòng thử lại!" }, { status: 500 });
}
```

---

## 4. Quy tắc Git

### 4.1 Commit Message Format
```
<type>(<scope>): <mô tả ngắn>

type: feat | fix | style | refactor | docs | chore
scope: api | ui | data | config | deploy

Ví dụ:
feat(api): add fintech sector to knowledge base
fix(ui): fix score bar color not updating
docs: update AGENTS.md with validator logic
```

### 4.2 Branch Strategy (Hackathon — Simplified)
- `main`: Production-ready code (deploy lên Vercel)
- `dev`: Active development
- Feature branches: `feat/<tên-tính-năng>`

### 4.3 Không commit
- `.env.local`, `.env*` (đã có trong `.gitignore`)
- `node_modules/`
- `.next/` build folder
- Bất kỳ file chứa API key

---

## 5. Quy tắc UX/UI

### 5.1 Design System
- **Color Palette**: Dùng màu từ Tailwind (không custom màu nếu không cần thiết)
- **Score Colors**:
  - ≥ 70: `green-500` ("Tiềm năng cao")
  - 50–69: `yellow-500` ("Cần cải thiện")
  - < 50: `red-500` ("Rủi ro cao")

### 5.2 Loading States
- **Mọi** action async phải có loading indicator
- Button phải disabled khi đang loading
- Hiển thị skeleton hoặc spinner

### 5.3 Responsive
- Mobile-first design (min-width: 375px)
- Test trên: 375px (mobile), 768px (tablet), 1280px (desktop)

### 5.4 Accessibility
- Mọi button phải có `aria-label` hoặc text rõ ràng
- Form inputs phải có `label` tương ứng
- Score card phải accessible cho screen readers

---

## 6. Quy tắc Performance

- Tránh re-render không cần thiết (dùng `useMemo`, `useCallback` khi cần)
- Không để blocking operations trong render
- API response nên về trong **< 3 giây** — nếu không, kiểm tra prompt length
- Không import toàn bộ thư viện khi chỉ cần một function

---

## 7. Checklist trước khi Demo

- [ ] `.env.local` đã config đúng GEMINI_API_KEY
- [ ] Test API với tất cả 5 sectors
- [ ] Score bar đổi màu đúng
- [ ] Mobile responsive OK
- [ ] Không có console errors
- [ ] Production URL trên Vercel hoạt động
- [ ] Form validation hoạt động (không submit khi trống)

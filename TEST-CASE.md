# 🧪 TEST-CASE.md — Kịch bản kiểm thử GCP Startup Validator

**Dự án:** AI20K-128 — GCP Startup Validator  
**Phiên bản:** 1.0  
**Môi trường:** Local (`http://localhost:3000`) & Production (Vercel URL)

---

## Chuẩn bị trước khi test

```bash
# 1. Điền API key thật vào .env.local
echo "GEMINI_API_KEY=your_real_key_here" > app/.env.local

# 2. Khởi động dev server
cd app && npm run dev

# 3. Mở trình duyệt tại http://localhost:3000
```

---

## 🔵 NHÓM 1: Test Giao diện (UI)

### TC-UI-01 — Hero Section hiển thị đúng
**Mục tiêu:** Kiểm tra phần hero render đầy đủ  
**Bước thực hiện:**
1. Mở `http://localhost:3000`
2. Quan sát màn hình

**Kết quả mong đợi:**
- [ ] Badge "AI20K-128 · GCP Hackathon 2025" hiển thị với dot nhấp nháy
- [ ] Tiêu đề chính có gradient màu tím-hồng trên chữ "Khởi Nghiệp"
- [ ] Subtitle có text đề cập Y Combinator và Lean Canvas
- [ ] 3 stat blocks: "5 Ngành", "< 3s", "100%"
- [ ] Background tối với glow effect màu tím

---

### TC-UI-02 — Form nhập liệu hiển thị đúng
**Mục tiêu:** Form components render và interactive  
**Bước thực hiện:**
1. Scroll xuống phần form

**Kết quả mong đợi:**
- [ ] Dropdown `#sector-select` hiển thị 5 options: AI, SaaS, FinTech, EdTech, E-Commerce
- [ ] Textarea `#idea-textarea` có placeholder text mô tả ví dụ
- [ ] Button `#submit-btn` có text "🚀 Thẩm Định Dự Án"
- [ ] Bộ đếm ký tự "0 / 2000 ký tự" hiển thị bên dưới textarea

---

### TC-UI-03 — Button disabled khi textarea trống
**Mục tiêu:** Validation ngăn submit khi chưa nhập đủ  
**Bước thực hiện:**
1. Không nhập gì vào textarea
2. Kiểm tra trạng thái button

**Kết quả mong đợi:**
- [ ] Button `#submit-btn` bị disabled (mờ, không click được)
- [ ] Thử nhập 1-9 ký tự → button vẫn disabled
- [ ] Nhập đúng 10 ký tự → button enable

---

### TC-UI-04 — Character counter cập nhật realtime
**Bước thực hiện:**
1. Click vào textarea `#idea-textarea`
2. Gõ "Hello World" (11 ký tự)

**Kết quả mong đợi:**
- [ ] Counter hiển thị "11 / 2000 ký tự"
- [ ] Counter cập nhật ngay sau mỗi ký tự gõ

---

### TC-UI-05 — Dropdown chọn sector
**Bước thực hiện:**
1. Click vào dropdown `#sector-select`
2. Lần lượt chọn từng option

**Kết quả mong đợi:**
- [ ] Dropdown mở ra 5 options có icon emoji
- [ ] Chọn được từng option không bị lỗi
- [ ] Giá trị hiển thị đúng sau khi chọn

---

## 🟢 NHÓM 2: Test API Backend

### TC-API-01 — Happy Path: Sector AI
**Mục tiêu:** API trả về JSON hợp lệ cho sector AI  
**Lệnh test:**
```bash
curl -X POST http://localhost:3000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"idea": "Nền tảng AI giúp doanh nghiệp vừa và nhỏ tự động hóa quy trình kế toán, giảm 80% thời gian nhập liệu thủ công", "sector": "ai"}' \
  | python3 -m json.tool
```

**Kết quả mong đợi:**
- [ ] HTTP Status: `200 OK`
- [ ] Response có field `problemSolutionFit` (string, không rỗng)
- [ ] Response có field `competitiveLandscape` (string, không rỗng)
- [ ] Response có field `viabilityScore` (integer, 0-100)
- [ ] Response có field `actionPlan` (array, ≥ 3 items)
- [ ] Response có field `strengths` (array)
- [ ] Response có field `risks` (array)
- [ ] Response có field `sectorName` = "AI / Machine Learning"
- [ ] Thời gian phản hồi < 5 giây

---

### TC-API-02 — Happy Path: Sector EdTech
```bash
curl -X POST http://localhost:3000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"idea": "App kết nối gia sư và học sinh theo yêu cầu, dùng AI để gợi ý gia sư phù hợp phong cách học tập", "sector": "edtech"}'
```

**Kết quả mong đợi:**
- [ ] HTTP 200 với JSON hợp lệ
- [ ] `competitiveLandscape` đề cập đến đối thủ EdTech (Duolingo, Hocmai, v.v.)
- [ ] `sectorName` = "EdTech / Giáo dục"

---

### TC-API-03 — Happy Path: Sector FinTech
```bash
curl -X POST http://localhost:3000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"idea": "Ví điện tử cho người dân nông thôn chưa có tài khoản ngân hàng, dùng CCCD để xác thực KYC", "sector": "fintech"}'
```

**Kết quả mong đợi:**
- [ ] HTTP 200 với JSON hợp lệ
- [ ] `competitiveLandscape` đề cập đến MoMo, ZaloPay hoặc VNPay
- [ ] `sectorName` = "FinTech / Financial Services"

---

### TC-API-04 — Happy Path: Sector SaaS
```bash
curl -X POST http://localhost:3000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"idea": "Phần mềm quản lý nhà hàng tích hợp AI để dự báo lượng khách, tối ưu tồn kho và giảm lãng phí thực phẩm", "sector": "saas"}'
```

**Kết quả mong đợi:**
- [ ] HTTP 200 với JSON hợp lệ
- [ ] `sectorName` = "SaaS / B2B Software"

---

### TC-API-05 — Happy Path: Sector E-Commerce
```bash
curl -X POST http://localhost:3000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"idea": "Marketplace chuyên bán đồ handmade, kết nối nghệ nhân Việt với khách hàng toàn cầu qua livestream", "sector": "ecommerce"}'
```

**Kết quả mong đợi:**
- [ ] HTTP 200 với JSON hợp lệ
- [ ] `sectorName` = "E-Commerce / Marketplace"

---

### TC-API-06 — Fallback sector không hợp lệ
```bash
curl -X POST http://localhost:3000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"idea": "Ứng dụng giao đồ ăn siêu tốc trong 10 phút cho khu vực nội thành", "sector": "invalid_sector"}'
```

**Kết quả mong đợi:**
- [ ] HTTP 200 (không lỗi — fallback về "ai")
- [ ] Response JSON hợp lệ
- [ ] `sector` = "ai" trong response

---

### TC-API-07 — Lỗi khi idea quá ngắn
```bash
curl -X POST http://localhost:3000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"idea": "App game", "sector": "ai"}'
```

**Kết quả mong đợi:**
- [ ] HTTP Status: `400 Bad Request`
- [ ] Response: `{"error": "Vui lòng mô tả ý tưởng ít nhất 10 ký tự!"}`

---

### TC-API-08 — Lỗi khi body thiếu field
```bash
curl -X POST http://localhost:3000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Kết quả mong đợi:**
- [ ] HTTP Status: `400 Bad Request`
- [ ] Response có `error` field

---

### TC-API-09 — Lỗi khi không có API key
**Bước thực hiện:**
1. Đặt `GEMINI_API_KEY=invalid_key_12345` trong `.env.local`
2. Restart dev server
3. Gửi request hợp lệ

```bash
curl -X POST http://localhost:3000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"idea": "Test với API key sai để kiểm tra error handling", "sector": "ai"}'
```

**Kết quả mong đợi:**
- [ ] HTTP Status: `502` hoặc `500`
- [ ] Response có `error` field (message thân thiện, không lộ stack trace)
- [ ] Không crash server

---

## 🟡 NHÓM 3: Test Luồng người dùng (E2E Flow)

### TC-E2E-01 — Happy Path: Submit → Nhận kết quả
**Bước thực hiện:**
1. Mở `http://localhost:3000`
2. Chọn sector "📚 EdTech / Giáo dục" trong dropdown `#sector-select`
3. Nhập vào textarea `#idea-textarea`:
   > "Nền tảng học lập trình cho trẻ em 6-12 tuổi qua game tương tác, dùng AI để cá nhân hóa lộ trình học"
4. Click button `#submit-btn`

**Kết quả mong đợi:**
- [ ] Button chuyển sang trạng thái loading ("Đang thẩm định..." + spinner)
- [ ] Button bị disabled trong lúc loading
- [ ] Skeleton cards xuất hiện phía dưới
- [ ] Sau 1-5 giây: trang scroll xuống khu vực kết quả `#results-section`
- [ ] `#score-card` hiển thị với số điểm từ 0 đến N (animation count-up)
- [ ] Progress bar fill theo chiều ngang
- [ ] Badge sector "EdTech / Giáo dục" hiển thị trong score card
- [ ] `#problem-solution-fit` card hiển thị nội dung phân tích
- [ ] `#competitive-landscape` card hiển thị nội dung phân tích
- [ ] `#strengths-list` hiển thị các điểm mạnh (nếu có)
- [ ] `#risks-list` hiển thị các rủi ro (nếu có)
- [ ] `#action-plan` hiển thị ≥ 3 bước checklist
- [ ] Button "🔄 Đánh giá ý tưởng khác" (`#re-evaluate-btn`) hiển thị

---

### TC-E2E-02 — Score color đúng theo ngưỡng
**Test 3 kịch bản ý tưởng có score dự kiến khác nhau:**

| Kịch bản | Ý tưởng | Score dự kiến | Màu mong đợi |
|---|---|---|---|
| High | "AI tích hợp sâu vào ERP, sở hữu dữ liệu độc quyền 10 năm" | ≥ 70 | 🟢 Xanh |
| Medium | "App giao đồ ăn trong khu vực nhỏ" | 50-69 | 🟡 Vàng |
| Low | "Mạng xã hội mới cạnh tranh với Facebook" | < 50 | 🔴 Đỏ |

**Kết quả mong đợi:** Score bar và số điểm đổi màu đúng theo ngưỡng.

---

### TC-E2E-03 — Action Plan Checklist tương tác
**Bước thực hiện:**
1. Sau khi có kết quả, scroll đến `#action-plan`
2. Click vào step đầu tiên `#action-step-1`

**Kết quả mong đợi:**
- [ ] Icon thay đổi từ ⬜ → ✅
- [ ] Text của step bị strikethrough (gạch ngang)
- [ ] Counter "X/N hoàn thành" tăng lên 1
- [ ] Click lại → bỏ check (toggle)

---

### TC-E2E-04 — Nút "Đánh giá lại"
**Bước thực hiện:**
1. Sau khi có kết quả
2. Click `#re-evaluate-btn`

**Kết quả mong đợi:**
- [ ] Khu vực kết quả biến mất
- [ ] Trang scroll về đầu
- [ ] Form hiển thị lại bình thường
- [ ] Textarea còn nội dung cũ (không bị xóa)

---

### TC-E2E-05 — Error message hiển thị đúng
**Bước thực hiện:**
1. Nhập đúng 10 ký tự (đủ để enable button)
2. Submit form
3. Đợi response lỗi (nếu API key sai)

**Kết quả mong đợi:**
- [ ] `#form-error` box hiển thị với icon ⚠️ và message rõ ràng
- [ ] Button trở về trạng thái bình thường (không còn loading)
- [ ] Người dùng có thể submit lại

---

## 🔵 NHÓM 4: Test Responsive (Mobile)

### TC-RESP-01 — Mobile 375px
**Bước thực hiện:**
1. Mở DevTools (F12) → Toggle device toolbar
2. Chọn `iPhone SE` (375x667)

**Kết quả mong đợi:**
- [ ] Hero text không bị tràn
- [ ] Form card padding hợp lý
- [ ] Cards grid hiển thị 1 cột (không 2 cột)
- [ ] Score number không bị cắt
- [ ] Action plan items readable

---

### TC-RESP-02 — Tablet 768px
**Bước thực hiện:**
1. DevTools → 768px width

**Kết quả mong đợi:**
- [ ] Layout chuyển sang 2 cột cho cards
- [ ] Hero stats hiển thị đẹp
- [ ] Form có padding vừa phải

---

## 🟣 NHÓM 5: Test Performance

### TC-PERF-01 — Thời gian phản hồi API
**Bước thực hiện:**
```bash
time curl -X POST http://localhost:3000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"idea": "Ứng dụng đặt lịch khám bác sĩ online tích hợp AI để gợi ý bác sĩ phù hợp theo triệu chứng", "sector": "saas"}'
```

**Kết quả mong đợi:**
- [ ] Total time < 5 giây (mạng tốt)
- [ ] Total time < 10 giây (mạng chậm)

---

### TC-PERF-02 — Stress test 5 request liên tiếp
```bash
for i in {1..5}; do
  curl -s -o /dev/null -w "Request $i: %{time_total}s\n" \
    -X POST http://localhost:3000/api/evaluate \
    -H "Content-Type: application/json" \
    -d "{\"idea\": \"Test idea number $i cho startup công nghệ\", \"sector\": \"saas\"}"
done
```

**Kết quả mong đợi:**
- [ ] Không có request nào timeout
- [ ] Không có lỗi 500 unexpeced
- [ ] Thời gian mỗi request tương đương nhau

---

## 📋 CHECKLIST TỔNG THỂ TRƯỚC KHI NỘP

| # | Mục kiểm tra | Kết quả |
|---|---|---|
| 1 | Production URL (Vercel) hoạt động | ⬜ |
| 2 | API trả JSON đúng cho cả 5 sectors | ⬜ |
| 3 | Score bar đổi màu đúng ngưỡng | ⬜ |
| 4 | Loading state hiển thị khi fetch | ⬜ |
| 5 | Error handling không crash | ⬜ |
| 6 | Action plan checklist tương tác được | ⬜ |
| 7 | Mobile responsive OK (375px) | ⬜ |
| 8 | Không có console errors | ⬜ |
| 9 | API key không bị lộ trong source | ⬜ |
| 10 | Demo mượt qua 10 lần submit liên tiếp | ⬜ |

---

## 🐛 Bug Report Template

Nếu phát hiện bug, ghi lại theo format:

```
Bug ID: BUG-XXX
Mô tả: ...
Bước tái hiện:
  1. ...
  2. ...
Kết quả thực tế: ...
Kết quả mong đợi: ...
Severity: Critical / High / Medium / Low
Screenshot: (đính kèm nếu có)
```

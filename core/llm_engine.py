import json
import requests
import os

def evaluate_idea_with_llm(idea: str, framework: dict) -> dict:
    """Chạy Engine 2: Gọi Gemini LLM với Structured Output JSON"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chưa cấu hình GEMINI_API_KEY")

    system_prompt = f"""Bạn là một AI Agent đóng vai trò Giám đốc Thẩm định Đầu tư.
Dựa trên thuật toán mã nguồn của hệ thống, ý tưởng này đã được phân loại vào Khung Thẩm Định: [{framework['name']}].

BỘ QUY TẮC BẮT BUỘC PHẢI ĐỐI CHIẾU DÀNH CHO FRAMEWORK NÀY:
"{framework['rules']}"

Hãy phân tích ý tưởng của người dùng thật nghiêm ngặt và BẮT BUỘC trả về chuỗi JSON thuần (không có ```json ở đầu/cuối), khớp chính xác với cấu trúc sau:
{{
  "marketSizeAnalysis": "Phân tích quy mô và tiềm năng thị trường dựa trên framework (tối đa 2 câu)",
  "competitiveRisk": "Rủi ro cạnh tranh và rào cản gia nhập ngành (tối đa 2 câu)",
  "problemSolutionScore": 80,
  "marketFitScore": 75,
  "scalabilityScore": 90,
  "criticalFlaw": "Điểm yếu chí mạng nhất của ý tưởng này là gì? (Viết thẳng thắn, không né tránh)",
  "nextSteps": ["Hành động 1", "Hành động 2", "Hành động 3"]
}}

Lưu ý: Các điểm số phải là số nguyên (0-100)."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": f"{system_prompt}\n\nÝ TƯỞNG CỦA USER: {idea}"}]}],
        "generationConfig": {
            "temperature": 0.7,
            "responseMimeType": "application/json"
        }
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    if not response.ok:
        raise ConnectionError(f"Lỗi API LLM: {response.text}")
        
    data = response.json()
    try:
        text_content = data['candidates'][0]['content']['parts'][0]['text'].strip()
        # Dọn dẹp markdown nếu có
        if text_content.startswith("```json"): text_content = text_content[7:]
        if text_content.startswith("```"): text_content = text_content[3:]
        if text_content.endswith("```"): text_content = text_content[:-3]
            
        return json.loads(text_content.strip())
    except Exception as e:
        raise ValueError(f"Lỗi Parse JSON: {e}\nRaw output: {text_content}")

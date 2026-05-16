import math
import requests
import os

def cosine_similarity(vecA, vecB):
    """Tính toán độ tương đồng giữa hai vector (In-Memory Vector Math)"""
    dot_product = sum(a * b for a, b in zip(vecA, vecB))
    norm_a = math.sqrt(sum(a * a for a in vecA))
    norm_b = math.sqrt(sum(b * b for b in vecB))
    return dot_product / (norm_a * norm_b or 1)

def get_vector(text: str) -> list[float]:
    """Gọi Gemini API để lấy Vector Embedding cho một đoạn text"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chưa cấu hình GEMINI_API_KEY")
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-2:embedContent?key={api_key}"
    payload = {"content": {"parts": [{"text": text}]}}
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    if not response.ok:
        raise ConnectionError(f"Lỗi API Embedding: {response.text}")
        
    data = response.json()
    return data['embedding']['values']

def keyword_match_score(idea_text: str, keywords: list) -> float:
    """Tìm kiếm từ khóa chính xác (Mô phỏng BM25 cơ bản) - Normalize về [0, 1]"""
    idea_lower = idea_text.lower()
    match_count = 0
    for kw in keywords:
        if kw.lower() in idea_lower:
            match_count += 1
            
    # Normalize điểm dựa trên tổng số lượng keyword của framework
    return match_count / max(len(keywords), 1)

def find_best_framework(idea_input: str, frameworks: list) -> tuple[dict, int]:
    """Chạy Engine 1: Quét ma trận bằng Hybrid Search (Vector + Keyword)"""
    idea_vector = get_vector(idea_input)
    selected_fw = frameworks[0]
    max_hybrid_score = -1
    
    for fw in frameworks:
        # 1. Điểm Semantic (Cosine Similarity)
        fw_text = " ".join(fw['keywords']) + " " + fw['rules']
        fw_vector = get_vector(fw_text)
        sim = cosine_similarity(idea_vector, fw_vector)
        
        # 2. Điểm Exact Match (Keyword Matching)
        kw_score = keyword_match_score(idea_input, fw['keywords'])
        
        # 3. Hybrid Score (70% Semantic + 30% Keyword)
        hybrid_score = (sim * 0.7) + (kw_score * 0.3)
        
        if hybrid_score > max_hybrid_score:
            max_hybrid_score = hybrid_score
            selected_fw = fw
            
    confidence = round(max_hybrid_score * 100)
    return selected_fw, confidence

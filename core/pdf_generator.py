from fpdf import FPDF
import os
import re

def clean_text(text: str) -> str:
    """Loại bỏ các ký tự Emoji hoặc Unicode dị có thể làm crash FPDF"""
    if not text: return ""
    return re.sub(r'[^\w\s\.,;:!?()"\'-/]+', ' ', text)

def create_pdf_report(result: dict, framework: str, idea: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    
    # Check if font exists
    font_path = "fonts/Roboto-Regular.ttf"
    if os.path.exists(font_path):
        pdf.add_font("Roboto", "", font_path, uni=True)
        pdf.set_font("Roboto", size=16)
    else:
        # Fallback if font is missing
        pdf.set_font("Arial", size=16)
        
    # Title
    pdf.cell(200, 10, txt="BAO CAO THAM DINH Y TUONG KHOI NGHIEP", ln=True, align="C")
    pdf.ln(10)
    
    # Body font
    if os.path.exists(font_path):
        pdf.set_font("Roboto", size=12)
    else:
        pdf.set_font("Arial", size=12)
        
    # Content
    pdf.multi_cell(190, 8, txt=f"Y tuong: {clean_text(idea)}")
    pdf.multi_cell(190, 8, txt=f"Framework ap dung: {clean_text(framework)}")
    pdf.ln(5)
    
    pdf.multi_cell(190, 8, txt="--- DIEM SO CHUYEN SAU ---")
    viability = round((result['problemSolutionScore'] + result['marketFitScore'] + result['scalabilityScore']) / 3)
    pdf.multi_cell(190, 8, txt=f"Diem tong quan (Viability Score): {viability}/100")
    pdf.multi_cell(190, 8, txt=f"- Problem-Solution Fit: {result['problemSolutionScore']}/100")
    pdf.multi_cell(190, 8, txt=f"- Market Fit: {result['marketFitScore']}/100")
    pdf.multi_cell(190, 8, txt=f"- Scalability: {result['scalabilityScore']}/100")
    pdf.ln(5)
    
    if result.get('criticalFlaw'):
        pdf.multi_cell(190, 8, txt="DIEM YEU CHI MANG (CRITICAL FLAW):")
        pdf.multi_cell(190, 8, txt=clean_text(result['criticalFlaw']))
        pdf.ln(5)
        
    pdf.multi_cell(190, 8, txt="QUY MO THI TRUONG:")
    pdf.multi_cell(190, 8, txt=clean_text(result['marketSizeAnalysis']))
    pdf.ln(5)
    
    pdf.multi_cell(190, 8, txt="RUI RO CANH TRANH:")
    pdf.multi_cell(190, 8, txt=clean_text(result['competitiveRisk']))
    pdf.ln(5)
    
    pdf.multi_cell(190, 8, txt="KE HOACH HANH DONG:")
    for i, step in enumerate(result['nextSteps']):
        pdf.multi_cell(190, 8, txt=f"{i+1}. {clean_text(step)}")
        
    # Export to bytes instead of file
    return pdf.output(dest="S").encode("latin-1")

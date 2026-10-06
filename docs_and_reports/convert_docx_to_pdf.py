"""
Script to reliably convert DOCX to PDF using win32com and verify page count.
"""

import os
import sys
import win32com.client
import pythoncom
import PyPDF2

def convert(docx_path, pdf_path):
    docx_path = os.path.abspath(docx_path)
    pdf_path = os.path.abspath(pdf_path)
    
    pythoncom.CoInitialize()
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = False
    
    try:
        print(f"[*] Opening: {docx_path}")
        doc = word.Documents.Open(docx_path, ReadOnly=True)
        print(f"[*] Saving as PDF: {pdf_path}")
        doc.SaveAs(pdf_path, FileFormat=17) # 17 = wdFormatPDF
        doc.Close(False)
        print("[*] Conversion successful!")
    finally:
        word.Quit()
        pythoncom.CoUninitialize()
        
    if os.path.exists(pdf_path):
        reader = PyPDF2.PdfReader(pdf_path)
        print(f"TOTAL PDF PAGES: {len(reader.pages)}")
        return len(reader.pages)
    return 0

if __name__ == "__main__":
    convert("SmartCare_AI_Final_Year_Project_Report.docx", "SmartCare_AI_Final_Year_Project_Report.pdf")

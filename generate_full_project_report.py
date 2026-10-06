"""
Master Script to Generate the Complete SmartCare AI Final Year Project Report DOCX.
"""

import os
import sys
import docx
from generate_final_docx_report import create_full_report
from report_chapters_1_to_3 import build_chapter_1, build_chapter_2, build_chapter_3
from report_chapters_4_to_6 import build_chapter_4, build_chapter_5, build_chapter_6
from report_appendices_and_refs import build_references, build_appendices

def main():
    print("Initializing SmartCare AI Final Year Project Report Generation...")
    
    # 1. Initialize Document & Front Matter
    doc = create_full_report()
    
    # 2. Build Chapters 1, 2, 3
    print("Building Chapter 1: Introduction...")
    build_chapter_1(doc)
    
    print("Building Chapter 2: Literature Survey...")
    build_chapter_2(doc)
    
    print("Building Chapter 3: System Design...")
    build_chapter_3(doc)
    
    # 3. Build Chapters 4, 5, 6
    print("Building Chapter 4: Project Description...")
    build_chapter_4(doc)
    
    print("Building Chapter 5: Result and Discussion...")
    build_chapter_5(doc)
    
    print("Building Chapter 6: Conclusion and Future Work...")
    build_chapter_6(doc)
    
    # 4. Build References & Appendices
    print("Building References...")
    build_references(doc)
    
    print("Building Appendices...")
    build_appendices(doc)
    
    # 5. Save Document
    output_docx_path = os.path.abspath("SmartCare_AI_Final_Year_Project_Report.docx")
    doc.save(output_docx_path)
    print(f"\nSUCCESS: Report successfully generated at:\n{output_docx_path}")
    
    file_size_kb = os.path.getsize(output_docx_path) / 1024
    print(f"File Size: {file_size_kb:.2f} KB")

if __name__ == "__main__":
    main()

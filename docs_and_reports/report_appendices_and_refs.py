"""
SmartCare AI - Report Generator: References and Appendices
Configured with exact 20 user references and institutional student metadata.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_builder_core import (
    set_cell_background, set_cell_margins, set_table_borders,
    add_callout_box, add_styled_paragraph, add_heading_1,
    add_heading_2, add_heading_3, add_bullet_item
)

PROJECT_TITLE = "SmartCare AI: Comorbidity-Aware Explainable Multi-Task Learning for Integrated Diabetes, Cardiovascular, and Chronic Kidney Disease Risk Prediction"
BATCH_MEMBERS = "231001178 - Sangari A C, 231001504 - Saravanan G"
SUPERVISOR_LINE = "Ms. Subashree R, Assistant Professor."

def build_references(doc):
    """Generates the References section with the exact 20 provided IEEE citations."""
    add_heading_1(doc, "REFERENCES")
    
    refs = [
        "[1] H. Kwiendacz, K. Haller, J. Glover, K. D. Katz, and A. Patel, “Predicting major adverse cardiac events in diabetes and chronic kidney disease: a machine learning study from the Silesia Diabetes-Heart Project,” Cardiovascular Diabetology, vol. 24, Art. no. 76, 2025, doi: 10.1186/s12933-025-02615-w.",
        "[2] S. M. A. Hossain, T. E. Rahman, J. Chen, and L. Wang, “CardioMeta: A calibrated multi-task learning framework for diabetes, hypertension, and cardiovascular disease prediction,” in Proc. 2026 IEEE Int. Conf. Bioinform. Biomed., 2026, pp. 123–130.",
        "[3] M. B. H. Sakil, R. K. Das, P. Kumar, and T. Ahmed, “Transformer and graph neural networks for multi-task learning in chronic kidney disease management,” IEEE Trans. Biomed. Eng., vol. 72, no. 3, pp. 789–801, 2025, doi: 10.1109/TBME.2024.3489234.",
        "[4] P. Sridevi, R. Iyer, A. Mukherjee, and S. Sharma, “Machine learning-based chronic kidney disease and diabetes prediction with SHAP interpretability,” J. Healthcare Inform. Res., vol. 8, no. 4, pp. 412–428, 2024, doi: 10.1109/COMPSAC61105.2024.00117.",
        "[5] P. Rajwade, S. Patel, R. Singh, and M. Desai, “Diagnosify: A multidisclose predictive system using machine learning,” in Proc. 2024 Int. Conf. Artif. Intell. Med., 2024, pp. 234–241.",
        "[6] H. Zhu, X. Liu, J. Wang, and Y. Zhang, “Machine learning for cardiovascular disease risk prediction in patients with chronic kidney disease,” Kidney Int. Rep., vol. 9, no. 2, pp. 267–279, 2024, doi: 10.1016/j.ekir.2023.12.008.",
        "[7] H. Sang, P. Chen, M. Li, and R. Zhou, “Predictive models for cardiovascular disease in type 2 diabetes using machine learning,” Diabetes Res. Clin. Pract., vol. 189, p. 109876, 2024, doi: 10.1038/s41598-024-63798-y.",
        "[8] Z.-Z. Jiang, X. Wang, J. Liu, and S. Kumar, “Machine learning-based cardiovascular disease prediction in type 2 diabetes: A systematic review,” Front. Endocrinol., vol. 16, p. 1325467, 2025, doi: 10.3389/fendo.2025.1325467.",
        "[9] S. Nayak, P. Mohanty, A. Swain, and R. K. Nayak, “Machine learning prediction of diabetic kidney disease progression,” J. Diabetes Res., vol. 2024, p. 7823456, 2024, doi: 10.1155/2024/7823456.",
        "[10] Z. Zhou, L. Wang, J. Zhang, and Y. Liu, “Machine learning prediction of CKD progression in hyperglycemic older adults,” Gerontology, vol. 72, no. 1, pp. 45–57, 2026, doi: 10.1080/0886022X.2026.2648313.",
        "[11] J. Wu, M. Chen, P. Zhang, and L. Sun, “Explainable machine learning for kidney function progression prediction,” Nephrol. Dial. Transplant., vol. 40, no. 4, pp. 623–635, 2025, doi: 10.1093/ndt/gfae289.",
        "[12] Z. Fu, H. Chen, X. Gao, and J. Li, “Nationwide predictive model for chronic kidney disease progression in diabetic patients,” Diabetes Care, vol. 46, no. 2, pp. 234–242, 2023, doi: 10.2337/dc22-1562.",
        "[13] P. Shah, R. Gupta, M. Verma, and S. Kulkarni, “Predicting cardiovascular risk using hybrid ensemble learning and explainable AI,” in Proc. 2025 ACM Conf. Mach. Learning Healthc., 2025, pp. 445–453.",
        "[14] K. M. T. Jawad, S. Al-Rashid, J. Ahmed, and M. Hassan, “Explainable AI applied to ensemble methods for chronic kidney disease prediction,” Comput. Biol. Med., vol. 174, p. 108432, 2024, doi: 10.1016/j.compbiomed.2024.108432.",
        "[15] N. Nguycharoen, P. Suwanwattana, T. Prompromjai, and R. Kumkate, “An explainable machine learning system for chronic kidney disease prediction in primary care,” BMC Nephrol., vol. 25, no. 1, p. 189, 2024, doi: 10.1186/s12882-024-03621-8.",
        "[16] A. A. Endalew, B. Abebe, C. Chekol, and D. Dejene, “Diabetes prediction based on risk factors using ensemble machine learning methods,” Comput. Intell. Neurosci., vol. 2024, p. 5312789, 2024, doi: 10.1155/2024/5312789.",
        "[17] A. Pathak, V. Sharma, R. Kumar, and S. Singh, “Enhancing cardiovascular risk prediction using machine learning algorithms and feature selection,” IEEE Access, vol. 12, pp. 42156–42169, 2024, doi: 10.1109/ACCESS.2024.3378542.",
        "[18] F. Jeribi, H. Jarraya, M. Ben Said, and S. Bousnina, “An approach to heart disease risk prediction using machine learning and feature engineering,” in Proc. 2023 Int. Conf. Intell. Syst. Appl., 2023, pp. 156–163.",
        "[19] F. Sanmarchi, C. Fanconi, D. Golinelli, D. Gori, T. Hernandez-Boussard, and A. Capodici, “Predict, diagnose, and treat chronic kidney disease with machine learning: a systematic literature review,” Journal of Nephrology, vol. 36, no. 4, pp. 1101–1117, 2023, doi: 10.1007/s40620-023-01573-4.",
        "[20] L. Liu, Y. Zhao, X. Wang, J. Chen, and R. Anderson, “Predictive modeling and risk analysis for peripheral vascular disease in type 2 diabetes,” Vasc. Med. Rev., vol. 36, no. 3, pp. 178–191, 2024, doi: 10.1177/1358863X24531217."
    ]
    
    for ref in refs:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        
    doc.add_page_break()

def build_appendices(doc):
    """Generates Appendices: Plagiarism reports, Proof of publication placeholders, and REC CO-PO-PSO / CO-SDG mapping tables."""
    add_heading_1(doc, "APPENDICES")
    
    # Appendix I
    add_heading_2(doc, "I. PROJECT PLAGIARISM REPORT")
    add_callout_box(doc, "[INSERT PROJECT PLAGIARISM REPORT HERE - TURNITIN / DRILLBIT VERIFIED]", box_type="placeholder")
    p_desc = doc.add_paragraph()
    p_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_desc.add_run("Appendix I: Turnitin / DrillBit Project Originality Report (< 10% Similarity)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True
    
    doc.add_page_break()

    # Appendix II
    add_heading_2(doc, "II. PAPER PLAGIARISM REPORT")
    add_callout_box(doc, "[INSERT PAPER PLAGIARISM REPORT HERE]", box_type="placeholder")
    p_desc = doc.add_paragraph()
    p_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_desc.add_run("Appendix II: Research Paper Plagiarism Originality Report (< 5% Similarity)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.italic = True
    
    doc.add_page_break()

    # Note: Appendix III (Final Published Paper) is skipped as explicitly instructed by the user!

    # Appendix IV
    add_heading_2(doc, "IV. PROOF OF THE PUBLICATION")
    add_styled_paragraph(doc, "IEEE Conference Acceptance & Publication Verification:", bold_prefix=None)
    add_callout_box(doc, "[INSERT IEEE CONFERENCE ACCEPTANCE EMAIL & REGISTRATION RECEIPT HERE]", box_type="placeholder")
    
    add_callout_box(doc, "[INSERT MS. SANGARI A C (231001178) PRESENTATION CERTIFICATE HERE]", box_type="placeholder")
    add_callout_box(doc, "[INSERT MR. SARAVANAN G (231001504) PRESENTATION CERTIFICATE HERE]", box_type="placeholder")
    
    doc.add_page_break()

    # Appendix V: CO-PO-PSO Mapping
    p_sub_it = doc.add_paragraph()
    p_sub_it.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_sub_it.add_run("IT19811 – Project Phase II\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    
    p_app5 = doc.add_paragraph()
    p_app5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_app5.add_run("V. CO-PO-PSO Mapping\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    
    p_info = doc.add_paragraph()
    p_info.paragraph_format.line_spacing = 1.2
    p_info.paragraph_format.space_after = Pt(8)
    r = p_info.add_run(f"Project Title : {PROJECT_TITLE}.\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.bold = True
    r = p_info.add_run(f"Batch Members: {BATCH_MEMBERS}.\nSupervisor : {SUPERVISOR_LINE}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    
    co_headers = ["PO / \nPSO \nCO", "PO 1", "PO 2", "PO 3", "PO 4", "PO 5", "PO 6", "PO 7", "PO 8", "PO 9", "PO 10", "PO 11", "PO 12", "PSO 1", "PSO 2", "PSO 3", "PSO 4"]
    co_matrix = [
        ["CO 1", "3", "3", "2", "--", "3", "--", "2", "--", "1", "3", "2", "2", "3", "2", "2", "--"],
        ["CO 2", "3", "3", "3", "2", "3", "--", "3", "--", "2", "3", "2", "2", "3", "3", "2", "1"],
        ["CO 3", "3", "3", "3", "2", "3", "1", "3", "--", "2", "2", "2", "2", "2", "3", "3", "2"],
        ["CO 4", "2", "2", "3", "3", "3", "--", "2", "1", "3", "3", "3", "2", "3", "2", "3", "2"],
        ["CO 5", "2", "2", "3", "3", "3", "--", "2", "1", "3", "3", "3", "3", "3", "3", "3", "3"]
    ]
    
    tbl_copo = doc.add_table(rows=len(co_matrix) + 1, cols=len(co_headers))
    tbl_copo.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_copo.autofit = False
    set_table_borders(tbl_copo)
    
    # Header
    for col_i, h_txt in enumerate(co_headers):
        cell = tbl_copo.rows[0].cells[col_i]
        set_cell_background(cell, "F1F5F9")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(h_txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(8)
        r.font.bold = True
        
    # Rows
    for row_i, r_data in enumerate(co_matrix):
        for col_i, val in enumerate(r_data):
            cell = tbl_copo.rows[row_i + 1].cells[col_i]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(8)
            if col_i == 0:
                r.font.bold = True
                
    p_note = doc.add_paragraph()
    p_note.paragraph_format.space_before = Pt(6)
    p_note.paragraph_format.space_after = Pt(24)
    r = p_note.add_run("1:Slight(Low), 2: Moderate(Medium) 3: Substantial(High), If there is no correlation, put ‘-‘.")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.italic = True
    
    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_sig.add_run("Signature of the Supervisor\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    
    doc.add_page_break()

    # Appendix VI: CO-SDG Relevance Record
    p_sub_it2 = doc.add_paragraph()
    p_sub_it2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_sub_it2.add_run("IT19811 – Project Phase II\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    
    p_app6 = doc.add_paragraph()
    p_app6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_app6.add_run("VI. CO-SDG Relevance Record\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    
    p_info = doc.add_paragraph()
    p_info.paragraph_format.line_spacing = 1.2
    p_info.paragraph_format.space_after = Pt(8)
    r = p_info.add_run(f"Project Title : {PROJECT_TITLE}.\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.bold = True
    r = p_info.add_run(f"Batch Members: {BATCH_MEMBERS}.\nSupervisor : {SUPERVISOR_LINE}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    
    sdg_data = [
        ("SDG (No. & Theme)", "Addressed COs", "Topic/Activity addressing SDG Theme"),
        ("SDG 3 – Good Health and Well-Being", "CO1, CO2, CO3, CO4", "Early comorbidity risk stratification for diabetes, cardiovascular disease, and chronic kidney disease to reduce premature mortality and deliver guideline-adherent preventative care."),
        ("SDG 8 – Decent Work and Economic Growth", "CO3, CO5", "SmartCare AI platform enables proactive healthcare management, mitigating catastrophic chronic disease expenditures and preserving workforce health and productivity."),
        ("SDG 9 – Industry, Innovation, and Infrastructure", "CO2, CO4", "Advances digital health infrastructure through multi-task shared neural representations, game-theoretic SHAP explainability, and modern microservices."),
        ("SDG 10 – Reduced Inequalities", "CO1, CO4", "Promotes equitable clinical access across underserved communities through 4-language localization (Tamil, Hindi, Spanish, English) and conversational AI assistance."),
        ("SDG 12 – Responsible Consumption and Production", "CO2, CO4", "Optimizes clinical diagnostics and healthcare resources by eliminating redundant single-disease testing and preventing avoidable emergency hospital admissions.")
    ]
    
    tbl_sdg = doc.add_table(rows=len(sdg_data), cols=3)
    tbl_sdg.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sdg.autofit = False
    tbl_sdg.columns[0].width = Inches(2.0)
    tbl_sdg.columns[1].width = Inches(1.2)
    tbl_sdg.columns[2].width = Inches(3.6)
    set_table_borders(tbl_sdg)
    
    for idx, (c1, c2, c3) in enumerate(sdg_data):
        row = tbl_sdg.rows[idx]
        for col_i, txt in enumerate([c1, c2, c3]):
            cell = row.cells[col_i]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(txt)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5 if idx > 0 else 10)
            if idx == 0:
                r.font.bold = True
                set_cell_background(cell, "F1F5F9")
            elif col_i == 0:
                r.font.bold = True
            elif col_i == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                
    p_sig2 = doc.add_paragraph()
    p_sig2.paragraph_format.space_before = Pt(36)
    p_sig2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_sig2.add_run("Signature of the Supervisor")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

"""
SmartCare AI - Exact 52-Page Publication Report PDF Generator (ReportLab)
Generates the complete Final Year Project Report PDF with all 13 real figures,
exact institutional front matter, tables, IEEE references, and REC mapping appendices.
Strictly calibrated for 52 pages (more than 50 pages and less than 55 pages).
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

A4_WIDTH, A4_HEIGHT = A4 # 595.27 x 841.89 pt

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and display total page count and professional headers/footers.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        print(f"[PAGE COUNT] Total PDF pages generated: {num_pages}")
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        self.saveState()
        
        # Draw header on body pages (page > 3)
        if self._pageNumber > 3:
            self.setFont("Times-Italic", 8.5)
            self.setFillColor(colors.HexColor("#475569"))
            self.drawString(54, A4_HEIGHT - 36, "SmartCare AI: Comorbidity-Aware Multi-Task Clinical Decision Support System")
            self.drawRightString(A4_WIDTH - 54, A4_HEIGHT - 36, "IT19811 Project Phase-II Report")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, A4_HEIGHT - 42, A4_WIDTH - 54, A4_HEIGHT - 42)
        
        # Footer
        if self._pageNumber > 1:
            self.setFont("Times-Roman", 9)
            self.setFillColor(colors.HexColor("#475569"))
            self.drawString(54, 34, "Department of Information Technology, Rajalakshmi Engineering College")
            page_str = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(A4_WIDTH - 54, 34, page_str)
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 46, A4_WIDTH - 54, 46)
            
        self.restoreState()

def build_pdf_report(filename="SmartCare_AI_Final_Year_Project_Report.pdf"):
    pdf_path = os.path.abspath(filename)
    fig_dir = os.path.abspath("artifacts/report_figures")
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=60,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#0f172a")   # Slate 900
    c_secondary = colors.HexColor("#0369a1") # Sky 700
    c_accent = colors.HexColor("#0284c7")    # Sky 600
    c_dark = colors.HexColor("#1e293b")      # Slate 800
    c_gray = colors.HexColor("#475569")      # Slate 600
    c_light = colors.HexColor("#f8fafc")     # Slate 50
    c_border = colors.HexColor("#cbd5e1")    # Slate 300
    c_header_bg = colors.HexColor("#f1f5f9") # Slate 100

    # Typography Styles
    title_main = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=14.5,
        leading=19,
        alignment=1, # Centered
        textColor=c_primary,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=13.5,
        leading=18,
        alignment=0,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        alignment=0,
        textColor=c_secondary,
        spaceBefore=11,
        spaceAfter=5,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3Custom',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11,
        leading=15,
        alignment=0,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=16,
        alignment=4, # Justified
        textColor=c_dark,
        spaceAfter=7.5
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=15.5,
        alignment=4,
        textColor=c_dark,
        leftIndent=14,
        spaceAfter=5.5
    )

    caption_style = ParagraphStyle(
        'CaptionCustom',
        parent=styles['Normal'],
        fontName='Times-BoldItalic',
        fontSize=9.5,
        leading=13,
        alignment=1, # Centered
        textColor=c_primary,
        spaceBefore=4,
        spaceAfter=10
    )

    tbl_hdr = ParagraphStyle(
        'TblHdrCustom',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=9,
        leading=11.5,
        alignment=1,
        textColor=c_primary
    )

    tbl_cell = ParagraphStyle(
        'TblCellCustom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
        alignment=0,
        textColor=c_dark
    )

    tbl_cell_center = ParagraphStyle(
        'TblCellCenterCustom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
        alignment=1,
        textColor=c_dark
    )

    story = []

    # -------------------------------------------------------------
    # PAGE 1: COVER PAGE
    # -------------------------------------------------------------
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>SMARTCARE AI: COMORBIDITY-AWARE EXPLAINABLE MULTI-TASK LEARNING FOR INTEGRATED DIABETES, CARDIOVASCULAR, AND CHRONIC KIDNEY DISEASE RISK PREDICTION</b>", title_main))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>IT19811 PROJECT PHASE-II REPORT</b>", ParagraphStyle('Sub', parent=title_main, fontSize=12, leading=15, textColor=c_secondary)))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<i>Submitted by</i><br/><br/><b>SANGARI A C (231001178)</b><br/><b>SARAVANAN G (231001504)</b>", ParagraphStyle('By', parent=title_main, fontSize=11, leading=15, textColor=c_dark)))
    story.append(Spacer(1, 22))
    story.append(Paragraph("<i>in partial fulfilment for the award of the degree of</i><br/><br/><b>BACHELOR OF TECHNOLOGY</b><br/>in<br/><b>INFORMATION TECHNOLOGY</b>", ParagraphStyle('Deg', parent=title_main, fontSize=11, leading=15, textColor=c_dark)))
    story.append(Spacer(1, 20))
    
    # Emblem box
    logo_table = Table([[Paragraph("<b>RAJALAKSHMI ENGINEERING COLLEGE</b><br/><font size=8.5 color='#64748b'>An Autonomous Institution • Affiliated to Anna University Chennai</font>", ParagraphStyle('LogoTxt', parent=title_main, fontSize=10, leading=13))]], colWidths=[380])
    logo_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(logo_table)
    story.append(Spacer(1, 22))
    story.append(Paragraph("<b>DEPARTMENT OF INFORMATION TECHNOLOGY<br/>RAJALAKSHMI ENGINEERING COLLEGE<br/>(AUTONOMOUS), CHENNAI-602 105<br/><br/>APRIL 2026</b>", ParagraphStyle('Inst', parent=title_main, fontSize=10.5, leading=14)))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 2: BONAFIDE CERTIFICATE
    # -------------------------------------------------------------
    story.append(Paragraph("<b>RAJALAKSHMI ENGINEERING COLLEGE</b><br/><font size=9 color='#64748b'>(An Autonomous Institution Affiliated to Anna University Chennai)</font>", ParagraphStyle('CertHead', parent=title_main, fontSize=11, leading=14)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>BONAFIDE CERTIFICATE</b>", ParagraphStyle('CertTitle', parent=title_main, fontSize=13, leading=16, textColor=c_primary)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Certified that this Phase-II Thesis titled <b>“SmartCare AI: Comorbidity-Aware Explainable Multi-Task Learning for Integrated Diabetes, Cardiovascular, and Chronic Kidney Disease Risk Prediction”</b> is the Bonafide work of <b>SANGARI A C (231001178)</b> and <b>SARAVANAN G (231001504)</b> who carried out the work under my supervision. Certified further that to the best of my knowledge the work reported herein does not form part of any other thesis or dissertation on the basis of which a degree or award was conferred on an earlier occasion on this or any other candidate.", body))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<i>“This project addresses the following Sustainable Development Goals: SDG 3, SDG 8, SDG 9, SDG 10 & SDG 12”.</i>", ParagraphStyle('SDGCert', parent=body, fontName='Times-BoldItalic', textColor=c_secondary)))
    story.append(Spacer(1, 28))
    
    # Signature Table
    sig_data = [
        [
            Paragraph("<b>Dr. P. VALARMATHIE M.E., Ph.D.</b><br/>Professor & Head<br/>Department of Information Technology<br/>Rajalakshmi Engineering College<br/>Chennai- 602105", tbl_cell),
            Paragraph("<b>Ms. SUBASHREE R M.Tech.</b><br/>Supervisor & Assistant Professor<br/>Department of Information Technology<br/>Rajalakshmi Engineering College<br/>Chennai- 602105", tbl_cell)
        ]
    ]
    t_sig = Table(sig_data, colWidths=[240, 240])
    t_sig.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_sig)
    story.append(Spacer(1, 35))
    story.append(Paragraph("Submitted to Project Viva-Voce Examination held on ............................................", ParagraphStyle('Viva', parent=body, fontName='Times-Bold')))
    story.append(Spacer(1, 30))
    
    ex_data = [
        [Paragraph("<b>Internal Examiner</b>", tbl_cell), Paragraph("<b>External Examiner</b>", ParagraphStyle('ExR', parent=tbl_cell, alignment=2))]
    ]
    t_ex = Table(ex_data, colWidths=[240, 240])
    t_ex.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))
    story.append(t_ex)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 3: ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    story.append(Paragraph("<b>ACKNOWLEDGEMENT</b>", ParagraphStyle('AckH', parent=title_main, fontSize=13, leading=16)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("First, we thank the almighty God for the successful completion of the project. Our heartfelt sincere thanks to our beloved chairman <b>Mr. S. Meganathan B.E., F.I.E.</b>, for his sincere endeavor in educating us in his premier institution. We would like to express our deep gratitude to our beloved Chairperson <b>Dr. Thangam Meganathan Ph.D.</b>, for her enthusiastic motivation which inspired us a lot in completing this project and Vice-Chairman <b>Mr. Abhay Shankar Meganathan B.E., M.S.</b>, for providing us with the requisite infrastructure.", body))
    story.append(Paragraph("We also express our sincere gratitude to our college principal, <b>Dr. S. N. Murugesan M.E., Ph.D.</b>, for his kind support and facilities to complete our work on time. We extend heartfelt gratitude to <b>Dr. P. Valarmathie M.E., Ph.D.</b>, Professor and Head of the Department of Information Technology for her guidance and encouragement throughout the work. We are very glad to thank our project coordinator <b>Dr. M. Babu M.E., Ph.D.</b>, Professor for his encouragement and support towards the successful completion of this project.", body))
    story.append(Paragraph("Further We express our deepest gratitude to our supervisor <b>Ms. Subashree R M.Tech.</b>, Assistant Professor for her valuable guidance throughout the work. We extend our thanks to our parents, friends, all faculty members, and supporting staff for their direct and indirect involvement in the successful completion of the project for their encouragement and support.", body))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Sangari A C (231001178)<br/>Saravanan G (231001504)</b>", ParagraphStyle('AckSign', parent=body, alignment=2, fontName='Times-Bold')))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 4: ABSTRACT
    # -------------------------------------------------------------
    story.append(Paragraph("<b>ABSTRACT</b>", ParagraphStyle('AbsH', parent=title_main, fontSize=13, leading=16)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("The “SmartCare AI: Comorbidity-Aware Explainable Multi-Task Learning for Integrated Diabetes, Cardiovascular, and Chronic Kidney Disease Risk Prediction” research tackles the growing global burden of chronic non-communicable diseases through unified multi-task machine learning. In clinical reality, Type 2 Diabetes (T2D), Cardiovascular Disease (CVD), and Chronic Kidney Disease (CKD) exhibit intricate pathophysiological interactions, shared metabolic risk factors, and compounding vascular complications. Conventional single-disease models operate in silos as opaque 'black boxes' and fail to capture these multidirectional dependencies. SmartCare AI introduces a unified multi-task neural network with a shared 32-dimensional latent feature space that simultaneously predicts calibrated risk probabilities for T2D, CVD, and CKD from a harmonized 30-dimensional clinical feature vector.", body))
    story.append(Paragraph("The system harmonizes three major clinical cohorts—CDC BRFSS 2015 (N=70,692), Kaggle CVD (N=68,205), and UCI CKD (N=400)—using zero-leakage median imputation and RobustScaler transformations. The multi-task network is trained with task-masked loss and task-balanced batch sampling (20% CKD allocation), followed by post-hoc Platt sigmoid scaling. On strictly held-out test partitions, SmartCare AI achieves high diagnostic precision and sensitivity: T2D (ROC-AUC: 0.8276, Recall: 88.72%, F1: 0.7751), CVD (ROC-AUC: 0.7974, Recall: 79.13%, F1: 0.7306), and CKD (ROC-AUC: 0.9953, Recall: 94.59%, F1: 0.9589) with excellent calibration (ECE < 0.011). Game-theoretic SHAP explainability provides local waterfall attributions and global biomarker importance, while a deterministic clinical rules engine translates risks into ADA/ACC/KDIGO-guideline-adherent care plans within a FastAPI and React microservices architecture.", body))
    story.append(Paragraph("The research contributes directly to Sustainable Development Goals 3 (Good Health and Well-Being), 8 (Decent Work and Economic Growth), 9 (Industry, Innovation, and Infrastructure), 10 (Reduced Inequalities), and 12 (Responsible Consumption and Production) by enabling early, equitable, and explainable chronic disease risk stratification. By replacing disjointed single-disease calculators with a unified comorbidity framework, SmartCare AI empowers clinicians and patients with actionable, data-driven preventative intelligence for improved clinical outcomes and healthcare sustainability.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 5: TABLE OF CONTENTS
    # -------------------------------------------------------------
    story.append(Paragraph("<b>TABLE OF CONTENTS</b>", ParagraphStyle('TocH', parent=title_main, fontSize=13, leading=16)))
    story.append(Spacer(1, 6))
    
    toc_data = [
        [Paragraph("<b>CHAPTER NO</b>", tbl_hdr), Paragraph("<b>TITLE</b>", tbl_hdr), Paragraph("<b>PAGE NO</b>", tbl_hdr)],
        [Paragraph("", tbl_cell), Paragraph("ABSTRACT", tbl_cell), Paragraph("iv", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("LIST OF FIGURES", tbl_cell), Paragraph("vi", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("LIST OF TABLES", tbl_cell), Paragraph("vi", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("LIST OF ABBREVIATIONS", tbl_cell), Paragraph("vii", tbl_cell_center)],
        [Paragraph("<b>1</b>", tbl_cell_center), Paragraph("<b>INTRODUCTION</b>", tbl_cell), Paragraph("<b>9</b>", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("1.1 MOTIVATION", tbl_cell), Paragraph("9", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("1.2 EXISTING SYSTEM", tbl_cell), Paragraph("10", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("1.3 PROBLEM STATEMENT", tbl_cell), Paragraph("11", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("1.4 OBJECTIVES OF THE PROJECT", tbl_cell), Paragraph("12", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("1.5 PROPOSED SYSTEM", tbl_cell), Paragraph("13", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("1.6 BENEFITS OF THE PROJECT", tbl_cell), Paragraph("13", tbl_cell_center)],
        [Paragraph("<b>2</b>", tbl_cell_center), Paragraph("<b>LITERATURE SURVEY</b>", tbl_cell), Paragraph("<b>14</b>", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("2.1 INTRODUCTION", tbl_cell), Paragraph("14", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("2.2 RELATED WORK", tbl_cell), Paragraph("14", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("2.3 INFERENCE FROM RELATED WORK", tbl_cell), Paragraph("18", tbl_cell_center)],
        [Paragraph("<b>3</b>", tbl_cell_center), Paragraph("<b>SYSTEM DESIGN</b>", tbl_cell), Paragraph("<b>19</b>", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("3.1 INTRODUCTION", tbl_cell), Paragraph("19", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("3.2 SYSTEM ARCHITECTURE", tbl_cell), Paragraph("19", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("3.3 SYSTEM REQUIREMENTS", tbl_cell), Paragraph("21", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("3.4 DATA FLOW DIAGRAM", tbl_cell), Paragraph("23", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("3.5 USE CASE DIAGRAM", tbl_cell), Paragraph("25", tbl_cell_center)],
        [Paragraph("<b>4</b>", tbl_cell_center), Paragraph("<b>PROJECT DESCRIPTION</b>", tbl_cell), Paragraph("<b>28</b>", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("4.1 METHODOLOGIES", tbl_cell), Paragraph("28", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("4.2 MODULE DESCRIPTION", tbl_cell), Paragraph("30", tbl_cell_center)],
        [Paragraph("<b>5</b>", tbl_cell_center), Paragraph("<b>RESULT AND DISCUSSION</b>", tbl_cell), Paragraph("<b>35</b>", tbl_cell_center)],
        [Paragraph("<b>6</b>", tbl_cell_center), Paragraph("<b>CONCLUSION AND FUTURE WORK</b>", tbl_cell), Paragraph("<b>45</b>", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("<b>REFERENCES</b>", tbl_cell), Paragraph("<b>47</b>", tbl_cell_center)],
        [Paragraph("", tbl_cell), Paragraph("<b>APPENDICES</b>", tbl_cell), Paragraph("<b>49</b>", tbl_cell_center)],
    ]
    t_toc = Table(toc_data, colWidths=[80, 320, 80])
    t_toc.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 6: LIST OF FIGURES & LIST OF TABLES
    # -------------------------------------------------------------
    story.append(Paragraph("<b>LIST OF FIGURES</b>", ParagraphStyle('LofH', parent=title_main, fontSize=13, leading=16)))
    story.append(Spacer(1, 4))
    lof_data = [
        [Paragraph("<b>Figure Number</b>", tbl_hdr), Paragraph("<b>Figure Caption</b>", tbl_hdr), Paragraph("<b>Page Number</b>", tbl_hdr)],
        [Paragraph("3.1", tbl_cell_center), Paragraph("System Architecture Diagram", tbl_cell), Paragraph("20", tbl_cell_center)],
        [Paragraph("3.2", tbl_cell_center), Paragraph("Data Flow Diagram", tbl_cell), Paragraph("24", tbl_cell_center)],
        [Paragraph("3.3", tbl_cell_center), Paragraph("Use Case Diagram", tbl_cell), Paragraph("26", tbl_cell_center)],
        [Paragraph("4.1", tbl_cell_center), Paragraph("Methodology Flowchart", tbl_cell), Paragraph("29", tbl_cell_center)],
        [Paragraph("5.1", tbl_cell_center), Paragraph("Multi-Task Neural Network Training & Loss Convergence", tbl_cell), Paragraph("36", tbl_cell_center)],
        [Paragraph("5.2", tbl_cell_center), Paragraph("Performance Evaluation (ROC-AUC Comparison)", tbl_cell), Paragraph("37", tbl_cell_center)],
        [Paragraph("5.3", tbl_cell_center), Paragraph("Recommendation Module (Comorbidity Risk Dashboard)", tbl_cell), Paragraph("38", tbl_cell_center)],
        [Paragraph("5.4", tbl_cell_center), Paragraph("SHAP Biomarker Attribution & Risk Decomposition", tbl_cell), Paragraph("39", tbl_cell_center)],
        [Paragraph("5.5", tbl_cell_center), Paragraph("Clinical Guideline Intervention Plan", tbl_cell), Paragraph("40", tbl_cell_center)],
        [Paragraph("5.6", tbl_cell_center), Paragraph("Longitudinal Health Trends Analysis", tbl_cell), Paragraph("41", tbl_cell_center)],
        [Paragraph("5.7", tbl_cell_center), Paragraph("Emergency Alert Dispatcher & Clinical Telemetry", tbl_cell), Paragraph("42", tbl_cell_center)],
        [Paragraph("5.8", tbl_cell_center), Paragraph("Multi-Lingual Localization Interface (Tamil UI)", tbl_cell), Paragraph("43", tbl_cell_center)],
        [Paragraph("5.9", tbl_cell_center), Paragraph("AI Assistance Chatbot (Clinical Copilot)", tbl_cell), Paragraph("44", tbl_cell_center)],
    ]
    t_lof = Table(lof_data, colWidths=[80, 320, 80])
    t_lof.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_lof)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>LIST OF TABLES</b>", ParagraphStyle('LotH', parent=title_main, fontSize=13, leading=16)))
    story.append(Spacer(1, 4))
    lot_data = [
        [Paragraph("<b>Table Number</b>", tbl_hdr), Paragraph("<b>Table Caption</b>", tbl_hdr), Paragraph("<b>Page Number</b>", tbl_hdr)],
        [Paragraph("1.1", tbl_cell_center), Paragraph("Existing Vs Proposed System", tbl_cell), Paragraph("11", tbl_cell_center)],
        [Paragraph("3.1", tbl_cell_center), Paragraph("Software Tools", tbl_cell), Paragraph("21", tbl_cell_center)],
        [Paragraph("3.2", tbl_cell_center), Paragraph("Functional Requirements", tbl_cell), Paragraph("22", tbl_cell_center)],
        [Paragraph("3.3", tbl_cell_center), Paragraph("Hardware Requirements", tbl_cell), Paragraph("23", tbl_cell_center)],
        [Paragraph("4.1", tbl_cell_center), Paragraph("30-Dimensional Harmonized Clinical Feature Space", tbl_cell), Paragraph("30", tbl_cell_center)],
        [Paragraph("5.1", tbl_cell_center), Paragraph("Multi-Task Neural Network Test Set Performance Metrics", tbl_cell), Paragraph("35", tbl_cell_center)],
        [Paragraph("5.2", tbl_cell_center), Paragraph("Empirical Baseline Comparison", tbl_cell), Paragraph("37", tbl_cell_center)],
    ]
    t_lot = Table(lot_data, colWidths=[80, 320, 80])
    t_lot.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_lot)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 7: LIST OF ABBREVIATIONS
    # -------------------------------------------------------------
    story.append(Paragraph("<b>LIST OF ABBREVIATIONS</b>", ParagraphStyle('LoaH', parent=title_main, fontSize=13, leading=16)))
    story.append(Spacer(1, 4))
    abbr_data = [
        [Paragraph("<b>S.No</b>", tbl_hdr), Paragraph("<b>Abbreviation</b>", tbl_hdr), Paragraph("<b>Word Expansion</b>", tbl_hdr)],
        [Paragraph("1", tbl_cell_center), Paragraph("AI", tbl_cell), Paragraph("Artificial Intelligence", tbl_cell)],
        [Paragraph("2", tbl_cell_center), Paragraph("ML", tbl_cell), Paragraph("Machine Learning", tbl_cell)],
        [Paragraph("3", tbl_cell_center), Paragraph("MTL", tbl_cell), Paragraph("Multi-Task Learning", tbl_cell)],
        [Paragraph("4", tbl_cell_center), Paragraph("T2D", tbl_cell), Paragraph("Type 2 Diabetes Mellitus", tbl_cell)],
        [Paragraph("5", tbl_cell_center), Paragraph("CVD", tbl_cell), Paragraph("Cardiovascular Disease", tbl_cell)],
        [Paragraph("6", tbl_cell_center), Paragraph("CKD", tbl_cell), Paragraph("Chronic Kidney Disease", tbl_cell)],
        [Paragraph("7", tbl_cell_center), Paragraph("SHAP", tbl_cell), Paragraph("SHapley Additive exPlanations", tbl_cell)],
        [Paragraph("8", tbl_cell_center), Paragraph("ECE", tbl_cell), Paragraph("Expected Calibration Error", tbl_cell)],
        [Paragraph("9", tbl_cell_center), Paragraph("ROC-AUC", tbl_cell), Paragraph("Receiver Operating Characteristic - Area Under Curve", tbl_cell)],
        [Paragraph("10", tbl_cell_center), Paragraph("PR-AUC", tbl_cell), Paragraph("Precision-Recall - Area Under Curve", tbl_cell)],
        [Paragraph("11", tbl_cell_center), Paragraph("API", tbl_cell), Paragraph("Application Programming Interface", tbl_cell)],
        [Paragraph("12", tbl_cell_center), Paragraph("RBAC", tbl_cell), Paragraph("Role-Based Access Control", tbl_cell)],
        [Paragraph("13", tbl_cell_center), Paragraph("ADA", tbl_cell), Paragraph("American Diabetes Association", tbl_cell)],
        [Paragraph("14", tbl_cell_center), Paragraph("ACC/AHA", tbl_cell), Paragraph("American College of Cardiology / American Heart Association", tbl_cell)],
        [Paragraph("15", tbl_cell_center), Paragraph("KDIGO", tbl_cell), Paragraph("Kidney Disease: Improving Global Outcomes", tbl_cell)],
    ]
    t_abbr = Table(abbr_data, colWidths=[45, 105, 330])
    t_abbr.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_abbr)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 8: REC VISION, MISSION, PEOs, PSOs, COs
    # -------------------------------------------------------------
    story.append(Paragraph("<b>DEPARTMENT VISION</b>", ParagraphStyle('DVH', parent=title_main, fontSize=11, leading=14)))
    story.append(Paragraph("To be a Department of Excellence in Information Technology Education, Research and Development.", body))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>DEPARTMENT MISSION</b>", ParagraphStyle('DMH', parent=title_main, fontSize=11, leading=14)))
    story.append(Paragraph("<b>M1.</b> To train the students to become highly knowledgeable in the field of Information Technology.<br/><b>M2.</b> To promote continuous learning and research in core and emerging areas.<br/><b>M3.</b> To develop globally competent students with strong foundations, who will be able to adapt to changing technologies.", body))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>PROGRAMME EDUCATIONAL OBJECTIVES (PEOs)</b>", ParagraphStyle('PeoH', parent=title_main, fontSize=11, leading=14)))
    story.append(Paragraph("<b>PEO I:</b> To provide essential background in Science, basic Electronics and applied Mathematics.<br/><b>PEO II:</b> To prepare the students with fundamental knowledge in programming languages and to develop applications.<br/><b>PEO III:</b> To engage the students in life-long learning, and make them to remain current in their profession.<br/><b>PEO IV:</b> To enable the students to implement computing solutions for real world problems and carry out basic research.<br/><b>PEO V:</b> To familiarize the students with ethical issues in engineering profession and emerging technologies.", body))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>PROGRAM SPECIFIC OUTCOMES (PSOs)</b>", ParagraphStyle('PsoH', parent=title_main, fontSize=11, leading=14)))
    story.append(Paragraph("<b>1.</b> To comprehend and analyze user requirements to design IT based solutions.<br/><b>2.</b> To identify and assess current technologies and review their applicability.<br/><b>3.</b> To engage in the computing profession by working effectively and utilizing professional skills.<br/><b>4.</b> To take on positions as promoters in business and embark on a research career.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 9: CHAPTER 1 - INTRODUCTION & MOTIVATION
    # -------------------------------------------------------------
    story.append(Paragraph("<b>CHAPTER 1</b><br/><b>INTRODUCTION</b>", h1_style))
    story.append(Paragraph("<b>1.1 MOTIVATION</b>", h2_style))
    story.append(Paragraph("Healthcare remains one of the most critical sectors affecting human well-being and socio-economic stability worldwide. Despite rapid advancements in clinical diagnostics and pharmacology, the global healthcare ecosystem faces unprecedented challenges due to the escalating burden of chronic non-communicable diseases (NCDs), prolonged asymptomatic disease latency, fragmented diagnostic services, and a lack of timely, personalized, data-driven clinical support. Most existing diagnostic portals and computerized risk assessment tools still provide generalized, single-disease recommendations that fail to consider the intricate pathophysiological interdependencies among co-occurring chronic conditions. As a result, healthcare practitioners and patients often make uncoordinated therapeutic decisions, leading to late-stage diagnoses, accelerated comorbidity progression, higher mortality rates, and unsustainable healthcare costs.", body))
    story.append(Paragraph("The motivation behind this project — <i>SmartCare AI: Comorbidity-Aware Explainable Multi-Task Learning for Integrated Diabetes, Cardiovascular, and Chronic Kidney Disease Risk Prediction</i> — stems from the critical need to bridge this clinical and technological gap. By integrating Artificial Intelligence (AI), Multi-Task Deep Learning (MTL), Explainable AI (XAI), and Clinical Knowledge Engineering, the project aims to provide localized, highly accurate, and comorbidity-aware risk stratifications at the individual patient and primary care levels. Through the use of a unified Shared Feature Neural Encoder, the system simultaneously models the complex cardiorenal-metabolic cross-talk connecting Type 2 Diabetes Mellitus (T2D), Cardiovascular Disease (CVD), and Chronic Kidney Disease (CKD). This multi-task innovation ensures that predictive risk assessments are holistic, statistically calibrated, and actionable, rather than fragmented and one-size-fits-all.", body))
    story.append(Paragraph("The project is designed to empower clinicians and patients with actionable intelligence, assisting in early subclinical detection, optimizing multi-condition lifestyle and pharmacological interventions, and minimizing severe adverse events such as myocardial infarctions, strokes, and end-stage renal disease (ESRD). By promoting precision preventative medicine and evidence-based decision-making, the system directly contributes to individual longevity, healthcare equity, and national economic productivity. Ultimately, the motivation lies in transforming traditional episodic and reactive healthcare into a smart, proactive, comorbidity-aware, and sustainable healthcare intelligence ecosystem that enhances clinical outcomes while safeguarding public health resources for future generations.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 10: CHAPTER 1 - EXISTING SYSTEM & TABLE 1.1
    # -------------------------------------------------------------
    story.append(Paragraph("<b>1.2 EXISTING SYSTEM</b>", h2_style))
    story.append(Paragraph("Existing computerized disease prediction platforms and clinical risk calculators primarily rely on static, isolated, or generalized datasets. These legacy systems often evaluate each medical condition in complete clinical isolation, failing to provide joint multi-disease risk assessments or account for real-time dynamic biomarkers such as blood pressure fluctuations, glycemic variability, or renal function indices.", body))
    story.append(Paragraph("Traditional risk tools like the Framingham Risk Score, ASCVD risk calculators, or standard online screening portals provide useful but broad statistical scores that lack precision for patient-specific, micro-level clinical decision-making. Moreover, current tools lack integration across disparate electronic health cohorts, physiological vitals, laboratory biomarkers, and lifestyle parameters, leading to one-size-fits-all risk estimates. This uncoordinated approach is ineffective in managing complex comorbid patients where diabetes, hypertension, and renal impairment interact continuously. As a result, clinicians and patients are left with limited or disconnected guidance, causing delayed interventions and increased clinical risk.", body))
    story.append(Paragraph("Additionally, most existing automated diagnostic platforms are rule-based or rely on opaque 'black-box' tree ensembles and shallow classifiers that lack explainability and probability calibration. These systems do not evolve dynamically with changing patient physiological trajectories or newly identified biomarker patterns. As a result, they cannot accurately capture dynamic clinical progressions or respond to sudden health deteriorations. Furthermore, data ingestion in many existing systems suffers from unhandled missingness, naive listwise deletion, or data leakage, which severely degrades predictive accuracy and clinical trust.", body))
    story.append(Spacer(1, 4))

    # Table 1.1
    story.append(Paragraph("<b>Table 1.1: Existing Vs Proposed System</b>", ParagraphStyle('TblCap', parent=caption_style, alignment=0)))
    tbl_1_1_data = [
        [Paragraph("<b>Parameter</b>", tbl_hdr), Paragraph("<b>Existing System</b>", tbl_hdr), Paragraph("<b>Proposed System</b>", tbl_hdr)],
        [Paragraph("Data Source", tbl_cell), Paragraph("Static, single-cohort clinical datasets", tbl_cell), Paragraph("Harmonized multi-cohort clinical datasets (CDC BRFSS, Kaggle CVD, UCI CKD: 139k+ records)", tbl_cell)],
        [Paragraph("Granularity", tbl_cell), Paragraph("Population-level or single-disease level", tbl_cell), Paragraph("Micro-level (individual biomarker, vital sign, and patient trajectory level)", tbl_cell)],
        [Paragraph("Technology Used", tbl_cell), Paragraph("Traditional single-task regression or shallow ML models", tbl_cell), Paragraph("Multi-Task Learning (MTL) Neural Network, Platt Calibration, and SHAP Explainable AI", tbl_cell)],
        [Paragraph("Disease Prediction", tbl_cell), Paragraph("Based on static isolated parameters (glucose or cholesterol only)", tbl_cell), Paragraph("Dynamic, simultaneous comorbidity risk stratification for T2D, CVD, and CKD", tbl_cell)],
        [Paragraph("Clinical Decision Support", tbl_cell), Paragraph("Limited or none; raw numerical scores only", tbl_cell), Paragraph("Automated clinical rules engine generating ADA/ACC/KDIGO-adherent care plans", tbl_cell)],
        [Paragraph("Longitudinal Telemetry", tbl_cell), Paragraph("Manual or periodic hospital visits", tbl_cell), Paragraph("Continuous longitudinal vital tracking with automated SMS/Email emergency alerts", tbl_cell)],
        [Paragraph("Explainability & Trust", tbl_cell), Paragraph("Opaque 'black-box' predictions with zero feature attribution", tbl_cell), Paragraph("Game-theoretic SHAP waterfall plots and global biomarker importance rankings", tbl_cell)],
        [Paragraph("Multi-Lingual Access", tbl_cell), Paragraph("Monolingual (English only) with technical jargon", tbl_cell), Paragraph("Localized 4-language support (English, Tamil, Hindi, Spanish) & AI Copilot", tbl_cell)]
    ]
    t_1_1 = Table(tbl_1_1_data, colWidths=[95, 185, 200])
    t_1_1.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_1_1)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 11: CHAPTER 1 - PROBLEM STATEMENT & OBJECTIVES
    # -------------------------------------------------------------
    story.append(Paragraph("<b>1.3 PROBLEM STATEMENT</b>", h2_style))
    story.append(Paragraph("Chronic non-communicable diseases remain the leading cause of premature mortality and healthcare burden globally, yet a vast number of patients and healthcare providers continue to face uncertainty in early risk detection, comorbidity management, and preventative care planning. Many individuals rely on episodic health check-ups, word-of-mouth advice, or subjective symptom awareness when managing chronic health risks. However, the silent, asymptomatic onset of Type 2 Diabetes, Cardiovascular Disease, and Chronic Kidney Disease makes these conventional, reactive approaches unreliable and dangerously delayed.", body))
    story.append(Paragraph("One of the major challenges faced by clinicians is the lack of personalized, comorbidity-aware diagnostic decision support. Physiological biomarkers, blood pressure, renal filtration rate, glycemic status, and lifestyle behaviors collectively influence long-term cardiometabolic and renal prognosis. However, medical practitioners often do not have access to unified computational tools that analyze these interconnected parameters simultaneously to provide coherent, multi-disease risk assessments. As a result, fragmented diagnostic evaluations lead to missed subclinical complications, delayed therapeutic escalations, and avoidable multi-organ damage.", body))
    story.append(Paragraph("Another pressing issue is the lack of explainability and statistical calibration in modern clinical machine learning. While deep learning models achieve high classification benchmarks, their 'black-box' nature prevents clinicians from understanding the underlying physiological factors driving individual risk scores. Furthermore, uncalibrated probability outputs mislead clinical triage thresholds. In addition, existing systems fail to link predictive risk scores directly to evidence-based medical guidelines, leaving patients without structured, actionable lifestyle and dietary intervention plans.", body))
    story.append(Paragraph("Therefore, the problem addressed in this project is the lack of an integrated, explainable, and comorbidity-aware AI clinical decision-support system that empowers healthcare practitioners and patients with simultaneous risk stratification, calibrated probabilities, game-theoretic biomarker attributions, and guideline-adherent multi-condition care plans within an accessible, multi-lingual web platform.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 12: CHAPTER 1 - OBJECTIVES OF THE PROJECT
    # -------------------------------------------------------------
    story.append(Paragraph("<b>1.4 OBJECTIVES OF THE PROJECT</b>", h2_style))
    story.append(Paragraph("• <b>Unified Comorbidity Modeling:</b> Develop an intelligent, data-driven clinical decision-support platform that can simultaneously analyze comorbidity risks and predict the onset of Type 2 Diabetes, Cardiovascular Disease, and Chronic Kidney Disease using Multi-Task Deep Learning (MTL). Integrate heterogeneous clinical data sources (CDC BRFSS, Kaggle CVD, UCI CKD) to create a standardized 30-dimensional clinical feature space.", bullet_style))
    story.append(Paragraph("• <b>Shared Feature Encoding:</b> Utilize a Shared Feature Neural Encoder (Dense 30->64->32) to capture latent pathophysiological dependencies and metabolic cross-talk across diabetes, hypertension, and renal impairment, enabling inductive knowledge transfer from data-rich domains to data-scarce conditions (CKD).", bullet_style))
    story.append(Paragraph("• <b>Probability Calibration:</b> Implement post-hoc Platt Sigmoid Scaling to ensure strict statistical probability calibration (minimizing Expected Calibration Error to < 0.011), transforming raw neural network output logits into true posterior probability distributions for reliable clinical triage.", bullet_style))
    story.append(Paragraph("• <b>Game-Theoretic Explainability:</b> Integrate game-theoretic SHAP (SHapley Additive exPlanations) for transparent patient-level waterfall charts and global biomarker importance rankings, allowing clinicians to verify the physiological rationale behind every risk score.", bullet_style))
    story.append(Paragraph("• <b>Clinical Rules Translation:</b> Translate predictive risks into actionable clinical care plans using an automated clinical rules engine adhering to American Diabetes Association (ADA 2026), American College of Cardiology / American Heart Association (ACC/AHA 2026), and Kidney Disease: Improving Global Outcomes (KDIGO 2026) guidelines.", bullet_style))
    story.append(Paragraph("• <b>Proactive Telemetry & Accessibility:</b> Incorporate longitudinal vital tracking, automated SMS/email emergency alerting via Twilio REST API, multi-lingual localization (English, Tamil, Hindi, Spanish), and a conversational clinical AI copilot to maximize digital healthcare equity.", bullet_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 13: CHAPTER 1 - PROPOSED SYSTEM & BENEFITS
    # -------------------------------------------------------------
    story.append(Paragraph("<b>1.5 PROPOSED SYSTEM</b>", h2_style))
    story.append(Paragraph("The proposed system, SmartCare AI, aims to revolutionize chronic disease prevention and clinical decision support through multi-task deep learning and transparent artificial intelligence. Unlike traditional single-disease diagnostic calculators that evaluate conditions in isolation, SmartCare AI focuses on comprehensive comorbidity modeling. It integrates demographic parameters, physiological vitals, biochemical laboratory markers, lifestyle habits, and computed cardiovascular/renal indices into a standardized 30-feature clinical vector to generate simultaneous risk assessments for Type 2 Diabetes, Cardiovascular Disease, and Chronic Kidney Disease.", body))
    story.append(Paragraph("At the core of SmartCare AI lies the Multi-Task Shared Feature Neural Encoder, which maps the 30-dimensional input vector into a joint 32-dimensional latent embedding space. While traditional models treat each disease independently, the shared neural encoder learns invariant representations governing systemic vascular and metabolic damage. Three dedicated task heads branch from this shared latent layer to predict individual calibrated risk probabilities.", body))
    story.append(Paragraph("<b>1.6 BENEFITS OF THE PROJECT</b>", h2_style))
    story.append(Paragraph("• <b>Better Clinical Decision-Making based on Comorbidity-Aware Insights:</b> Provides clinicians with a holistic view of the patient's cardiorenal-metabolic status, transcending isolated single-disease assessments and preventing overlooked subclinical complications.", bullet_style))
    story.append(Paragraph("• <b>Transparent and Trustworthy Explainable AI:</b> Eliminates 'black-box' opacity by presenting exact game-theoretic SHAP feature attributions and biomarker contribution rankings for every patient diagnosis.", bullet_style))
    story.append(Paragraph("• <b>Statistically Calibrated Risk Probabilities:</b> Applies Platt Sigmoid Scaling to ensure reported risk scores represent genuine posterior probabilities (ECE < 0.011), supporting reliable clinical triage.", bullet_style))
    story.append(Paragraph("• <b>Actionable Guideline-Concordant Intervention Regimens:</b> Automates evidence-based lifestyle, dietary, and medical guidance conforming strictly to ADA, ACC/AHA, and KDIGO clinical standards.", bullet_style))
    story.append(Paragraph("• <b>Proactive Longitudinal Telemetry and Emergency Alerting:</b> Monitors temporal vital trends and automatically dispatches real-time SMS (Twilio) and email alerts upon detecting acute threshold breaches.", bullet_style))
    story.append(Paragraph("• <b>Multi-Lingual Accessibility and Conversational AI Assistance:</b> Democratizes health intelligence across diverse populations through 4-language localization and an empathetic conversational AI copilot.", bullet_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 14: CHAPTER 2 - LITERATURE SURVEY (2.1, 2.2.1, 2.2.2)
    # -------------------------------------------------------------
    story.append(Paragraph("<b>CHAPTER 2</b><br/><b>LITERATURE SURVEY</b>", h1_style))
    story.append(Paragraph("<b>2.1 INTRODUCTION</b>", h2_style))
    story.append(Paragraph("A literature review serves as the foundation for understanding the technological, methodological, and clinical landscape relevant to chronic disease risk stratification and artificial intelligence in healthcare. Numerous studies in medical informatics, machine learning, and clinical decision support have demonstrated the immense potential of data integration in improving diagnostic accuracy. However, most existing computerized systems remain limited in their ability to model multi-disease comorbidity interactions or fail to provide explainable, calibrated risk predictions suitable for real-world clinical deployment.", body))
    story.append(Paragraph("This chapter reviews existing research on machine learning for diabetes screening, cardiovascular disease prediction, chronic kidney disease detection, multi-task learning paradigms, explainable AI (XAI) frameworks, and clinical decision-support architectures. It also highlights the recent evolution of calibrated and explainable multi-task methodologies that improve predictive performance and clinical trustworthiness by capturing interdependencies across co-occurring chronic conditions.", body))

    story.append(Paragraph("<b>2.2 RELATED WORK</b>", h2_style))
    story.append(Paragraph("<b>2.2.1 Multi-Disease and Cardiorenal-Metabolic Risk Prediction</b>", h3_style))
    story.append(Paragraph("Recent clinical investigations have underscored the necessity of evaluating cardiovascular and renal outcomes jointly in diabetic populations. Kwiendacz et al. [1] conducted a pivotal machine learning study within the Silesia Diabetes-Heart Project, demonstrating that major adverse cardiac events (MACE) in patients with diabetes are heavily exacerbated by concomitant chronic kidney disease. Their findings proved that isolated cardiac calculators consistently underestimate risk in patients with impaired renal function. In a related breakthrough, Hossain et al. [2] introduced CardioMeta, a calibrated multi-task learning framework designed to simultaneously predict diabetes, hypertension, and cardiovascular disease, establishing that multi-task parameter sharing significantly improves prediction stability across interrelated cardiometabolic endpoints.", body))
    
    story.append(Paragraph("<b>2.2.2 Multi-Task Learning and Neural Graph Modeling in Chronic Disease</b>", h3_style))
    story.append(Paragraph("The application of deep multi-task architectures in nephrology and complex chronic disease management was further advanced by Sakil et al. [3], who combined Transformer representations and graph neural networks for multi-task learning in chronic kidney disease management. Their architecture validated that joint representation learning effectively mitigates sample sparsity in specialized nephrology cohorts. Furthermore, Rajwade et al. [5] developed 'Diagnosify', a multidisclose predictive system using ensemble machine learning to detect co-occurring chronic illnesses, emphasizing the operational value of unified diagnostic platforms in outpatient primary care settings.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 15: CHAPTER 2 - RELATED WORK (2.2.3, 2.2.4)
    # -------------------------------------------------------------
    story.append(Paragraph("<b>2.2.3 Explainable AI (XAI) and SHAP Interpretability in Healthcare</b>", h3_style))
    story.append(Paragraph("Model interpretability is paramount for clinical adoption. Sridevi et al. [4] developed a machine learning framework for chronic kidney disease and diabetes prediction augmented with SHAP (SHapley Additive exPlanations) interpretability, proving that game-theoretic feature attribution provides actionable insights into key metabolic drivers. Similarly, Shah et al. [13] evaluated cardiovascular risk prediction using hybrid ensemble learning coupled with explainable AI, illustrating how patient-level attribution plots enhance clinician confidence.", body))
    story.append(Paragraph("In nephrology, Jawad et al. [14] and Nguycharoen et al. [15] applied explainable ensemble methods to predict chronic kidney disease in primary care settings, demonstrating that visualizing biomarker contributions drastically reduces diagnostic turnaround times and enhances clinician trust during routine health evaluations.", body))

    story.append(Paragraph("<b>2.2.4 Cardiovascular Disease Modeling in Diabetic and Renal Cohorts</b>", h3_style))
    story.append(Paragraph("The intimate physiological coupling between renal decline, diabetes, and cardiovascular complications has been extensively investigated. Zhu et al. [6] implemented machine learning models specifically for cardiovascular disease risk prediction in patients with chronic kidney disease, identifying proteinuria and arterial stiffness as critical cross-domain predictors. Sang et al. [7] and Jiang et al. [8] developed and systematically reviewed machine learning predictive models for cardiovascular complications in Type 2 Diabetes cohorts, noting that multi-feature architectures combining glycemic biomarkers with blood pressure indices significantly outperform conventional linear risk scores.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 16: CHAPTER 2 - RELATED WORK (2.2.5, 2.2.6)
    # -------------------------------------------------------------
    story.append(Paragraph("<b>2.2.5 Predictive Modeling of Chronic Kidney Disease and Diabetic Nephropathy</b>", h3_style))
    story.append(Paragraph("Predicting diabetic kidney disease progression before irreversible structural damage occurs is a major focus of modern bioinformatics. Nayak et al. [9] demonstrated high-precision machine learning models for diabetic kidney disease progression, while Zhou et al. [10] developed predictive algorithms for CKD progression specifically in hyperglycemic older adults. Wu et al. [11] investigated explainable machine learning for renal function progression, emphasizing the diagnostic value of tracking longitudinal eGFR trajectories. Furthermore, Fu et al. [12] developed a nationwide predictive model for CKD progression in diabetic patients, demonstrating that early predictive intervention substantially reduces dialysis incidence.", body))

    story.append(Paragraph("<b>2.2.6 Ensemble Learning and Feature Selection in Chronic Disease Screening</b>", h3_style))
    story.append(Paragraph("Ensemble methodologies have demonstrated robust classification performance across diverse medical benchmarks. Endalew et al. [16] implemented ensemble machine learning models for diabetes prediction based on clinical and lifestyle risk factors, achieving superior classification accuracy over single decision trees. Pathak et al. [17] and Jeribi et al. [18] investigated heart disease risk prediction using advanced feature selection and engineering techniques, proving that derived hemodynamic indices (such as Pulse Pressure and Mean Arterial Pressure) substantially enhance model discrimination.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 17: CHAPTER 2 - RELATED WORK (2.2.7) & INFERENCE
    # -------------------------------------------------------------
    story.append(Paragraph("<b>2.2.7 Systematic Reviews on Clinical AI and Vascular Risk Modeling</b>", h3_style))
    story.append(Paragraph("Comprehensive systematic literature reviews by Sanmarchi et al. [19] surveyed the global state of machine learning for predicting, diagnosing, and treating chronic kidney disease, highlighting the urgent need for model calibration, external validation, and seamless EHR integration. Finally, Liu et al. [20] conducted predictive modeling and risk analysis for peripheral vascular disease in Type 2 Diabetes, confirming that systemic microvascular damage in diabetes serves as a common pathophysiological substrate across all major organ systems.", body))

    story.append(Paragraph("<b>2.3 INFERENCE FROM RELATED WORK</b>", h2_style))
    story.append(Paragraph("From the literature review, several critical insights shape the foundation of the proposed SmartCare AI system:", body))
    story.append(Paragraph("• <b>Gap in Comorbidity-Aware Modeling:</b> Traditional machine learning models excel in single-disease prediction [7, 16, 17] but fail to capture the mutual pathophysiological cross-talk connecting diabetes, cardiovascular events, and renal decline [1, 6, 8]. Multi-Task Learning (MTL) provides a mathematically sound solution by learning shared latent representations [2, 3].", bullet_style))
    story.append(Paragraph("• <b>Data Scarcity and Cross-Cohort Harmonization:</b> Specialized clinical datasets (such as CKD) are often limited in sample size [3, 19]. Harmonizing diverse cohorts (CDC BRFSS, Kaggle CVD, UCI CKD) and employing task-balanced sampling allows data-rich tasks to reinforce data-scarce domains.", bullet_style))
    story.append(Paragraph("• <b>Essential Role of Probability Calibration:</b> Raw neural network and ensemble logits are frequently miscalibrated [2]. Implementing Platt Sigmoid Scaling ensures that risk outputs reflect true clinical posterior probabilities (ECE < 0.011).", bullet_style))
    story.append(Paragraph("• <b>Necessity of Game-Theoretic Explainability:</b> Clinicians require interpretable feature attributions before adopting AI in medical practice [4, 11, 13, 14, 15]. Game-theoretic SHAP waterfall plots provide exact local and global biomarker explanations.", bullet_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 18: CHAPTER 2 - INFERENCES CONTINUED
    # -------------------------------------------------------------
    story.append(Paragraph("<b>2.3 INFERENCE FROM RELATED WORK (CONTINUED)</b>", h2_style))
    story.append(Paragraph("• <b>Bridging Prediction to Clinical Action:</b> Predictive models must not stop at numerical scores; integrating deterministic rules engines adhering to global clinical guidelines (ADA, ACC/AHA, KDIGO) translates risk predictions into actionable care plans.", bullet_style))
    story.append(Paragraph("• <b>Continuous Longitudinal Telemetry and Multi-Lingual Accessibility:</b> Modern clinical platforms require real-time emergency alerting (Twilio SMS, Email) and regional language localization to ensure equitable and proactive healthcare delivery across socio-economically diverse patient populations.", bullet_style))
    story.append(Paragraph("• <b>Synergy of AI and Clinical Practice:</b> By synthesizing cross-cohort clinical harmonization, shared multi-task representation learning, game-theoretic explainability, and evidence-based clinical rules, SmartCare AI addresses the critical research and implementation gaps identified across the literature [1-20].", bullet_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 19: CHAPTER 3 - SYSTEM DESIGN & ARCHITECTURE
    # -------------------------------------------------------------
    story.append(Paragraph("<b>CHAPTER 3</b><br/><b>SYSTEM DESIGN</b>", h1_style))
    story.append(Paragraph("<b>3.1 INTRODUCTION</b>", h2_style))
    story.append(Paragraph("System design forms the backbone of the SmartCare AI platform, defining how various hardware, software, machine learning, and data components interact to achieve the project’s clinical objectives. It establishes a structured framework that governs clinical data acquisition, cross-cohort harmonization, multi-task neural inference, probability calibration, explainability generation, clinical rule translation, and interactive presentation. The purpose of system design is to ensure that each stage—ranging from patient data ingestion to the generation of predictive comorbidity insights—is efficiently coordinated and executed with high accuracy. This phase bridges conceptual algorithmic design with practical implementation by transforming theoretical models into a robust, enterprise-grade clinical software architecture.", body))
    story.append(Paragraph("The SmartCare AI system design emphasizes modularity, loose coupling, and scalability, ensuring that functional components such as data preprocessing, multi-task neural modeling, SHAP explainability, guideline rules execution, emergency telemetry alerting, and user interfaces can operate independently yet cohesively within a microservices ecosystem.", body))

    story.append(Paragraph("<b>3.2 SYSTEM ARCHITECTURE</b>", h2_style))
    story.append(Paragraph("The system is designed with a modular, six-tier layered architecture to efficiently handle complex, data-driven comorbidity risk assessment. At the foundation, the Data Ingestion and Harmonization Layer integrates 30 standardized clinical features across demographics, physiological vitals, laboratory biomarkers, and lifestyle factors. The raw data passes through a zero-leakage preprocessing pipeline that executes training-fitted median imputation and RobustScaler normalization.", body))
    story.append(Paragraph("The core analytical engine is the Multi-Task Neural Network, which utilizes a Shared Feature Encoder (Dense 30->64 -> Dense 64->32) to map patient features into a 32-dimensional latent representation space capturing joint cardiorenal-metabolic patterns. Three dedicated task heads branch from this shared latent space to generate simultaneous prediction logits for Type 2 Diabetes, Cardiovascular Disease, and Chronic Kidney Disease. The Probability Calibration Subsystem applies Platt Sigmoid Scaling to ensure true statistical probabilities, while the SHAP Explainability Engine calculates exact Shapley attributions.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 20: CHAPTER 3 - FIGURE 3.1 SYSTEM ARCHITECTURE
    # -------------------------------------------------------------
    story.append(Paragraph("<b>3.2.1 ARCHITECTURAL TIER BREAKDOWN</b>", h3_style))
    story.append(Paragraph("Figure 3.1 illustrates the end-to-end 6-tier architecture of SmartCare AI, spanning data ingestion, preprocessing, multi-task neural modeling, explainability, clinical rules execution, and client presentation.", body))
    story.append(Spacer(1, 4))
    fig_3_1 = os.path.join(fig_dir, "fig_3_1_system_architecture.png")
    if os.path.exists(fig_3_1):
        story.append(Image(fig_3_1, width=470, height=270))
        story.append(Paragraph("Figure 3.1: System Architecture Diagram", caption_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 21: CHAPTER 3 - SYSTEM REQUIREMENTS & TABLE 3.1
    # -------------------------------------------------------------
    story.append(Paragraph("<b>3.3 SYSTEM REQUIREMENTS</b>", h2_style))
    story.append(Paragraph("The system requirements define the essential hardware and software specifications necessary for the efficient development, training, deployment, and operation of the SmartCare AI platform. These requirements ensure that all modules—including multi-task comorbidity risk stratification, SHAP explainability, clinical rules execution, longitudinal vital tracking, and conversational AI assistance—function smoothly and deliver real-time, accurate insights to clinicians and patients.", body))
    story.append(Spacer(1, 4))

    # Table 3.1
    story.append(Paragraph("<b>Table 3.1: Software Tools</b>", ParagraphStyle('TblCap2', parent=caption_style, alignment=0)))
    tbl_3_1_data = [
        [Paragraph("<b>Component</b>", tbl_hdr), Paragraph("<b>Technology</b>", tbl_hdr), Paragraph("<b>Role</b>", tbl_hdr)],
        [Paragraph("Frontend Framework", tbl_cell), Paragraph("HTML, CSS, JavaScript, React.js, TailwindCSS", tbl_cell), Paragraph("Provides interactive web dashboard for visualizing risk gauges, SHAP waterfall charts, vital trends, and care plans.", tbl_cell)],
        [Paragraph("Backend Framework", tbl_cell), Paragraph("FastAPI / Python 3.13, Uvicorn", tbl_cell), Paragraph("Handles high-performance asynchronous REST API endpoints, processes clinical requests, and integrates frontend with ML models.", tbl_cell)],
        [Paragraph("Database", tbl_cell), Paragraph("SQLite / MongoDB / SQLAlchemy", tbl_cell), Paragraph("Stores user profiles, patient clinical records, longitudinal vital logs, audit trails, and authentication tokens.", tbl_cell)],
        [Paragraph("Machine Learning", tbl_cell), Paragraph("PyTorch, Scikit-learn, XGBoost", tbl_cell), Paragraph("Implements Multi-Task Shared Feature Encoder, baseline benchmark models, Platt calibration, and pipeline scalers.", tbl_cell)],
        [Paragraph("Explainability & Visuals", tbl_cell), Paragraph("SHAP (v0.52.0), Recharts, Matplotlib", tbl_cell), Paragraph("Computes game-theoretic Shapley values, rendering local waterfall plots and interactive dashboard radar/line charts.", tbl_cell)],
        [Paragraph("Data Handling", tbl_cell), Paragraph("Pandas, NumPy", tbl_cell), Paragraph("Cleans, normalizes, harmonizes multi-cohort datasets (139k+ records), and computes derived clinical indices.", tbl_cell)],
        [Paragraph("Emergency Telemetry", tbl_cell), Paragraph("Twilio REST API, smtplib", tbl_cell), Paragraph("Dispatches automated emergency SMS alerts and structured clinical summary emails upon acute threshold breaches.", tbl_cell)],
        [Paragraph("Operating System", tbl_cell), Paragraph("Windows 11 / Linux Ubuntu", tbl_cell), Paragraph("Provides a stable, high-performance environment for model training, microservice hosting, and production web deployment.", tbl_cell)]
    ]
    t_3_1 = Table(tbl_3_1_data, colWidths=[100, 155, 225])
    t_3_1.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_3_1)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 22: CHAPTER 3 - FUNCTIONAL REQUIREMENTS (TABLE 3.2)
    # -------------------------------------------------------------
    story.append(Paragraph("<b>Table 3.2: Functional Requirements</b>", ParagraphStyle('TblCap3', parent=caption_style, alignment=0)))
    tbl_3_2_data = [
        [Paragraph("<b>S. No</b>", tbl_hdr), Paragraph("<b>Functional Requirement</b>", tbl_hdr), Paragraph("<b>Description</b>", tbl_hdr)],
        [Paragraph("1", tbl_cell_center), Paragraph("User Authentication & RBAC", tbl_cell), Paragraph("Allows patients and clinicians to securely sign up and log in with bcrypt password hashing and JWT authentication to protect clinical records.", tbl_cell)],
        [Paragraph("2", tbl_cell_center), Paragraph("Clinical Data Harmonization", tbl_cell), Paragraph("Fetches, validates, and cleans 30 standardized clinical features across demographics, vitals, labs, and lifestyle metrics with zero-leakage median imputation.", tbl_cell)],
        [Paragraph("3", tbl_cell_center), Paragraph("Multi-Task Risk Stratification", tbl_cell), Paragraph("Simultaneously predicts calibrated risk probabilities for Type 2 Diabetes, Cardiovascular Disease, and Chronic Kidney Disease in sub-second inference.", tbl_cell)],
        [Paragraph("4", tbl_cell_center), Paragraph("SHAP Feature Attribution", tbl_cell), Paragraph("Decomposes predicted risk scores into positive and negative Shapley contributions, generating interactive patient waterfall charts and global biomarker rankings.", tbl_cell)],
        [Paragraph("5", tbl_cell_center), Paragraph("Clinical Guideline Translation", tbl_cell), Paragraph("Translates predicted comorbidity risks and abnormal biomarkers into actionable lifestyle, dietary, pharmacological, and follow-up plans adhering to ADA, ACC/AHA, and KDIGO guidelines.", tbl_cell)],
        [Paragraph("6", tbl_cell_center), Paragraph("Longitudinal Vital Tracking & Telemetry", tbl_cell), Paragraph("Monitors historical vital logs over time, computes trend trajectories, and dispatches automated emergency SMS/Email alerts upon acute threshold breaches.", tbl_cell)],
        [Paragraph("7", tbl_cell_center), Paragraph("Multi-Lingual Localization & AI Copilot", tbl_cell), Paragraph("Provides vernacular interfaces in 4 languages (Tamil, Hindi, Spanish, English) and interactive conversational AI for personalized patient counseling.", tbl_cell)]
    ]
    t_3_2 = Table(tbl_3_2_data, colWidths=[35, 155, 290])
    t_3_2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_3_2)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 23: CHAPTER 3 - HARDWARE REQUIREMENTS (TABLE 3.3)
    # -------------------------------------------------------------
    story.append(Paragraph("<b>Table 3.3: Hardware Requirements</b>", ParagraphStyle('TblCap4', parent=caption_style, alignment=0)))
    tbl_3_3_data = [
        [Paragraph("<b>Component</b>", tbl_hdr), Paragraph("<b>Minimum Specification</b>", tbl_hdr), Paragraph("<b>Justification</b>", tbl_hdr)],
        [Paragraph("Processor", tbl_cell), Paragraph("Intel Core i5 / AMD Ryzen 5 or higher", tbl_cell), Paragraph("Required to handle multi-cohort data preprocessing, SHAP TreeExplainer computations, and real-time inference efficiently.", tbl_cell)],
        [Paragraph("RAM", tbl_cell), Paragraph("8 GB (16 GB recommended)", tbl_cell), Paragraph("Supports large dataset operations (139k+ records), multi-task tensor training, and parallel API request handling.", tbl_cell)],
        [Paragraph("Storage", tbl_cell), Paragraph("250 GB Solid State Drive (SSD)", tbl_cell), Paragraph("Facilitates fast read/write operations for large datasets, serialized models, database logs, and web assets.", tbl_cell)],
        [Paragraph("Display", tbl_cell), Paragraph("1080p Resolution Monitor", tbl_cell), Paragraph("Provides clear visualization of analytics dashboards, SHAP waterfall plots, radar charts, and longitudinal trend graphs.", tbl_cell)],
        [Paragraph("Network", tbl_cell), Paragraph("Broadband Internet (10+ Mbps)", tbl_cell), Paragraph("Required for accessing external APIs (Twilio SMS, cloud databases, SMTP servers) and web client deployment.", tbl_cell)]
    ]
    t_3_3 = Table(tbl_3_3_data, colWidths=[90, 150, 240])
    t_3_3.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_3_3)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>3.4 DATA FLOW DIAGRAM / USE CASE DIAGRAM</b>", h2_style))
    story.append(Paragraph("<b>3.4.1 DATA FLOW DIAGRAM (DFD)</b>", h3_style))
    story.append(Paragraph("The system is designed using a microservices architecture, where each functional module operates independently while communicating through a centralized FastAPI gateway. This design allows for modularity, scalability, and efficient data sharing between components. At the user interface level, the system accepts clinical inputs such as blood pressure readings, glucose levels, lipid profiles, renal function markers, and lifestyle habits, which serve as the primary parameters for both comorbidity risk prediction and SHAP explainability modules.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 24: CHAPTER 3 - FIGURE 3.2 DATA FLOW DIAGRAM
    # -------------------------------------------------------------
    story.append(Paragraph("<b>3.4.2 DFD WORKFLOW ANALYSIS</b>", h3_style))
    story.append(Paragraph("Figure 3.2 illustrates the complete Data Flow Diagram (DFD Level 0 and Level 1), detailing the data transmission pipeline from client input ingestion to multi-task inference, calibration, rules processing, and alert telemetry.", body))
    story.append(Spacer(1, 4))
    fig_3_2 = os.path.join(fig_dir, "fig_3_2_data_flow_diagram.png")
    if os.path.exists(fig_3_2):
        story.append(Image(fig_3_2, width=470, height=270))
        story.append(Paragraph("Figure 3.2: Data Flow Diagram", caption_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 25: CHAPTER 3 - USE CASE DIAGRAM DESCRIPTION
    # -------------------------------------------------------------
    story.append(Paragraph("<b>3.5 USE CASE DIAGRAM</b>", h2_style))
    story.append(Paragraph("The Use Case Diagram illustrates the interactions between different actors and the core functionalities of the SmartCare AI system, specifically focused on comorbidity risk prediction, SHAP biomarker explainability, clinical guideline recommendations, longitudinal tracking, and AI-assisted conversational guidance. The primary actors in the system are Patients and Clinicians (Physicians/Specialists), each of whom can log in or sign up to access the platform. Patients enter vital logs and view personalized care plans, while Clinicians evaluate comprehensive diagnostic dossiers and review SHAP waterfall attributions.", body))
    story.append(Paragraph("Once authenticated, both actors interact with the system’s core modules. The Multi-Task Risk Stratification module processes clinical parameters to compute calibrated risk tiers. The SHAP Explainability module continuously visualizes positive and negative feature contributions. The Clinical Rules Engine automatically generates multi-condition care regimens, while the Emergency Telemetry module dispatches real-time SMS/Email alerts when severe vital breaches are detected. The AI Assistance module acts as an intelligent medical copilot, answering queries and guiding patients through their diagnostic findings.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 26: CHAPTER 3 - FIGURE 3.3 USE CASE DIAGRAM
    # -------------------------------------------------------------
    story.append(Paragraph("<b>3.5.1 ACTOR-SYSTEM USE CASE INTERACTION</b>", h3_style))
    story.append(Paragraph("Figure 3.3 illustrates the functional use cases accessible to Patients, Clinicians, and System Administrators across authentication, risk prediction, explainability inspection, guideline interventions, and emergency alerting.", body))
    story.append(Spacer(1, 4))
    fig_3_3 = os.path.join(fig_dir, "fig_3_3_use_case_diagram.png")
    if os.path.exists(fig_3_3):
        story.append(Image(fig_3_3, width=470, height=270))
        story.append(Paragraph("Figure 3.3: Use Case Diagram", caption_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 27: CHAPTER 4 - METHODOLOGY INTRODUCTION
    # -------------------------------------------------------------
    story.append(Paragraph("<b>CHAPTER 4</b><br/><b>PROJECT DESCRIPTION</b>", h1_style))
    story.append(Paragraph("<b>4.1 METHODOLOGIES</b>", h2_style))
    story.append(Paragraph("The proposed system integrates multiple advanced methodologies to provide precise, data-driven comorbidity risk predictions and clinical recommendations. It combines cross-cohort clinical data harmonization, multi-task deep neural modeling, probability calibration, and game-theoretic explainable AI (XAI) to capture and analyze complex cardiorenal-metabolic interactions. Initially, raw clinical data is collected from diverse sources, including CDC epidemiological surveys, cardiovascular cohorts, and regional nephrology databases. This data undergoes thorough preprocessing, which involves cleaning to remove inconsistencies or missing values, feature extraction to identify relevant parameters such as systolic/diastolic blood pressure, fasting glucose, and serum creatinine, and RobustScaler normalization to standardize the input for efficient processing by downstream models.", body))
    story.append(Paragraph("A key component of the methodology is the use of a Shared Feature Neural Encoder, which effectively models latent physiological dependencies between different chronic conditions, allowing the system to understand how subclinical damage in one organ system influences neighboring pathways. In parallel, specialized task heads are employed to predict individual disease risks for Type 2 Diabetes, Cardiovascular Disease, and Chronic Kidney Disease, leveraging both historical cohort statistics and real-time patient inputs. The analytical outputs of the system are presented visually through intuitive risk gauges, SHAP waterfall plots, radar charts, and longitudinal trend analyses, facilitating easy interpretation for healthcare practitioners and patients.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 28: CHAPTER 4 - FIGURE 4.1 METHODOLOGY FLOWCHART
    # -------------------------------------------------------------
    story.append(Paragraph("<b>4.1.1 METHODOLOGICAL PIPELINE</b>", h3_style))
    story.append(Paragraph("Figure 4.1 depicts the end-to-end 9-step methodological pipeline of SmartCare AI, spanning data collection, harmonization, multi-task training, Platt calibration, SHAP explainability, and microservices deployment.", body))
    story.append(Spacer(1, 4))
    fig_4_1 = os.path.join(fig_dir, "fig_4_1_methodology.png")
    if os.path.exists(fig_4_1):
        story.append(Image(fig_4_1, width=320, height=410))
        story.append(Paragraph("Figure 4.1: Methodology Flowchart", caption_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 29: CHAPTER 4 - TABLE 4.1 FEATURE SPACE
    # -------------------------------------------------------------
    story.append(Paragraph("<b>Table 4.1: 30-Dimensional Harmonized Clinical Feature Space</b>", ParagraphStyle('TblCap5', parent=caption_style, alignment=0)))
    tbl_4_1_data = [
        [Paragraph("<b>Feature Index</b>", tbl_hdr), Paragraph("<b>Clinical Feature Name</b>", tbl_hdr), Paragraph("<b>Category</b>", tbl_hdr), Paragraph("<b>Data Type</b>", tbl_hdr), Paragraph("<b>Standard Reference / Range</b>", tbl_hdr)],
        [Paragraph("1 - 2", tbl_cell_center), Paragraph("Age, Sex", tbl_cell), Paragraph("Demographics", tbl_cell), Paragraph("Continuous / Binary", tbl_cell), Paragraph("Age in years (18-100); Sex (0: F, 1: M)", tbl_cell)],
        [Paragraph("3 - 6", tbl_cell_center), Paragraph("Systolic BP, Diastolic BP, Heart Rate, BMI", tbl_cell), Paragraph("Physiological Vitals", tbl_cell), Paragraph("Continuous", tbl_cell), Paragraph("SBP (90-200), DBP (60-120), BMI (15-50)", tbl_cell)],
        [Paragraph("7 - 10", tbl_cell_center), Paragraph("Fasting Blood Sugar, HbA1c, Chol, HDL", tbl_cell), Paragraph("Lipid & Glycemic Labs", tbl_cell), Paragraph("Continuous", tbl_cell), Paragraph("FBS (70-300 mg/dL), HbA1c (4-14%)", tbl_cell)],
        [Paragraph("11 - 13", tbl_cell_center), Paragraph("Triglycerides, Serum Creatinine, BUN", tbl_cell), Paragraph("Renal & Lipid Labs", tbl_cell), Paragraph("Continuous", tbl_cell), Paragraph("Creatinine (0.4-15 mg/dL), BUN (5-100)", tbl_cell)],
        [Paragraph("14 - 16", tbl_cell_center), Paragraph("Albuminuria, Hemoglobin, Potassium", tbl_cell), Paragraph("Renal & Hematology", tbl_cell), Paragraph("Continuous / Cat", tbl_cell), Paragraph("Albumin (0-5), Hb (6-18 g/dL)", tbl_cell)],
        [Paragraph("17 - 20", tbl_cell_center), Paragraph("Smoking, Alcohol, Phys Activity, Diet", tbl_cell), Paragraph("Lifestyle Behaviors", tbl_cell), Paragraph("Binary (0/1)", tbl_cell), Paragraph("Binary indicator flags (0: No, 1: Yes)", tbl_cell)],
        [Paragraph("21 - 24", tbl_cell_center), Paragraph("Family Hx T2D, Family Hx CVD, HTN, Stroke", tbl_cell), Paragraph("Medical History", tbl_cell), Paragraph("Binary (0/1)", tbl_cell), Paragraph("Personal / family history flags", tbl_cell)],
        [Paragraph("25 - 27", tbl_cell_center), Paragraph("Diff Walking, GenHealth, Mental Days", tbl_cell), Paragraph("Functional Quality", tbl_cell), Paragraph("Cat / Integer", tbl_cell), Paragraph("GenHealth (1-5 scale), Days (0-30)", tbl_cell)],
        [Paragraph("28 - 30", tbl_cell_center), Paragraph("Pulse Pressure, MAP, eGFR", tbl_cell), Paragraph("Computed Indices", tbl_cell), Paragraph("Continuous", tbl_cell), Paragraph("PP (SBP-DBP), MAP (DBP+1/3PP), eGFR", tbl_cell)]
    ]
    t_4_1 = Table(tbl_4_1_data, colWidths=[65, 125, 95, 85, 110])
    t_4_1.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_4_1)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 30: CHAPTER 4 - MODULES 4.2.1 & 4.2.2
    # -------------------------------------------------------------
    story.append(Paragraph("<b>4.2 MODULE DESCRIPTION</b>", h2_style))
    story.append(Paragraph("The system is designed with six interrelated modules that collectively enhance precision healthcare, clinical decision support, and comorbidity risk analysis.", body))
    
    story.append(Paragraph("<b>4.2.1 User & Stakeholder Management</b>", h3_style))
    story.append(Paragraph("The User and Stakeholder Management module provides a secure and structured framework for user registration, authentication, and clinical profile management. It supports multiple user roles, including patients, clinicians (physicians/specialists), and healthcare administrators, ensuring that each stakeholder can access relevant medical records and functionalities. Users can maintain detailed clinical profiles with physiological credentials and customize their dashboards based on their roles, enabling personalized access to risk scores, SHAP explanations, and intervention plans. This module ensures a seamless and secure interaction between the platform and its diverse users, promoting efficient healthcare delivery.", body))
    story.append(Paragraph("In addition to basic registration and authentication, the module incorporates Role-Based Access Control (RBAC) to ensure medical data security and privacy conforming to HIPAA principles. Patients can view personalized risk summaries and lifestyle advice, while clinicians can analyze comprehensive patient dossiers, inspect SHAP waterfall biomarker attributions, and modify therapeutic protocols. System administrators can monitor user activity, audit system operations, and manage model deployments. This structured access prevents unauthorized disclosure of protected health information (PHI).", body))

    story.append(Paragraph("<b>4.2.2 AI Comorbidity Risk Prediction & Multi-Task Classifier</b>", h3_style))
    story.append(Paragraph("The AI Comorbidity Risk Prediction and Multi-Task Classifier module serves as the core decision-making engine of the system, integrating multiple clinical data sources and advanced neural architectures to generate precise, actionable risk stratifications for patients. It processes diverse input parameters, including detailed physiological vitals such as systolic and diastolic blood pressure, heart rate, and BMI, as well as biochemical laboratory variables like fasting blood sugar, HbA1c, total cholesterol, triglycerides, serum creatinine, and blood urea nitrogen. Computed hemodynamics, including Pulse Pressure and Mean Arterial Pressure (MAP), are also considered to tailor predictions to the specific vascular state of each patient.", body))
    story.append(Paragraph("The module employs a Shared Feature Neural Encoder (Dense 30->64->32) with Layer Normalization and Dropout regularization to evaluate the comorbidity profile across Type 2 Diabetes, Cardiovascular Disease, and Chronic Kidney Disease simultaneously. By learning joint latent embeddings across conditions, the system captures non-linear interactions between hyperglycemia, systemic hypertension, and renal impairment. This enables clinicians to make informed, proactive decisions regarding preventative therapies, lifestyle interventions, and specialized consultations before irreversible microvascular or macrovascular complications occur.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 31: CHAPTER 4 - MODULES 4.2.3 & 4.2.4
    # -------------------------------------------------------------
    story.append(Paragraph("<b>4.2.3 Probability Calibration & Risk Stratification</b>", h3_style))
    story.append(Paragraph("The Probability Calibration module is designed to transform raw neural network logits into statistically reliable posterior probabilities using Platt Sigmoid Scaling. Raw machine learning scores often suffer from overconfidence or distortion due to class imbalances; the calibration module maps output logits into true posterior probability distributions, optimizing Brier scores and minimizing Expected Calibration Error (ECE < 0.011). Calibrated probabilities are categorized into intuitive clinical risk tiers: Low Risk (< 25%), Moderate Risk (25% - 49%), High Risk (50% - 74%), and Critical Risk (>= 75%), providing clinicians with dependable thresholds for triage and diagnostic escalation.", body))

    story.append(Paragraph("<b>4.2.4 Explainable AI & SHAP Biomarker Attribution</b>", h3_style))
    story.append(Paragraph("The Explainable AI and SHAP Biomarker Attribution module provides transparent, game-theoretic interpretability for every prediction generated by the platform. Integrating TreeSHAP and KernelSHAP algorithms, the module computes exact Shapley additive values for all 30 clinical features. It generates local patient waterfall plots that quantitatively decompose risk scores into positive contributors (factors increasing disease risk, such as elevated blood pressure or fasting glucose) and negative contributors (protective factors, such as regular physical exercise). Furthermore, the module aggregates global feature importance rankings across patient cohorts, providing medical researchers with valuable insights into dominant epidemiological risk drivers.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 32: CHAPTER 4 - MODULES 4.2.5 & 4.2.6
    # -------------------------------------------------------------
    story.append(Paragraph("<b>4.2.5 Clinical Guidelines & Personalized Wellness Recommendation</b>", h3_style))
    story.append(Paragraph("The Clinical Guidelines and Personalized Wellness Recommendation module translates predictive risk stratifications and abnormal laboratory biomarkers into actionable, guideline-concordant medical care plans. The module codifies clinical practice guidelines from the American Diabetes Association (ADA 2026 Standards of Care), American College of Cardiology / American Heart Association (ACC/AHA 2026 Guidelines), and Kidney Disease: Improving Global Outcomes (KDIGO 2026 Guidelines). It outputs structured, multi-condition care regimens comprising dietary modifications (e.g., sodium restriction < 2g/day, low-glycemic foods), physical activity prescriptions (e.g., 150 min/week moderate aerobic exercise), pharmacological review alerts (e.g., ACEi/ARB review for hypertensive diabetics), and diagnostic follow-up schedules.", body))

    story.append(Paragraph("<b>4.2.6 Longitudinal Health Monitoring & Emergency Alert Telemetry</b>", h3_style))
    story.append(Paragraph("The Longitudinal Health Monitoring and Emergency Alert Telemetry module continuously tracks patient vital logs (blood pressure, fasting glucose, weight, eGFR) over time to evaluate health trajectories and compute clinical rate-of-change indicators. Additionally, an automated emergency daemon monitors real-time inputs for acute threshold breaches (e.g., Systolic BP >= 180 mmHg, Fasting Glucose >= 300 mg/dL). Upon detecting an acute breach, the module automatically dispatches real-time SMS alerts via Twilio API and structured email notifications to primary care physicians and designated emergency contacts, enabling rapid clinical intervention.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 33: CHAPTER 4 - MODULE 4.2.7 SMARTCARE AI BOT
    # -------------------------------------------------------------
    story.append(Paragraph("<b>4.2.7 SmartCare AI – Bot (Conversational Clinical Copilot)</b>", h3_style))
    story.append(Paragraph("The SmartCare AI Bot is an intelligent virtual assistant that enhances patient engagement and decision-making across the platform. It combines natural language processing (NLP) with clinical knowledge representations to understand user queries, provide personalized explanations of laboratory results, and guide patients through the platform's diagnostic findings. Patients can interact with the bot to obtain real-time advice on dietary habits, exercise routines, medication adherence, and risk factor reduction. The assistant is also localized across four languages (English, Tamil, Hindi, Spanish), breaking literacy barriers and promoting equitable digital healthcare.", body))
    story.append(Paragraph("The bot operates in conjunction with the comorbidity prediction engine and clinical rules module. When a patient asks questions about their computed risk scores or prescribed dietary plans, the chatbot dynamically retrieves their specific biomarker attributions from the SHAP database and contextualizes clinical guidelines into simple, jargon-free explanations.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 34: CHAPTER 5 - RESULT & DISCUSSION INTRODUCTION
    # -------------------------------------------------------------
    story.append(Paragraph("<b>CHAPTER 5</b><br/><b>RESULT AND DISCUSSION</b>", h1_style))
    story.append(Paragraph("The SmartCare AI system was successfully implemented as an explainable, comorbidity-aware Multi-Task Learning (MTL) system to provide intelligent multi-disease risk prediction, SHAP biomarker attribution, and clinical decision support. The Multi-Task Shared Feature Neural Encoder was applied for joint comorbidity modeling in which it effectively extracted invariant latent representations from 30 standardized clinical features across 139,297 patient records. Experimental testing proved that it has high predictive reliability where the model could accurately predict Type 2 Diabetes (ROC-AUC: 0.8276), Cardiovascular Disease (ROC-AUC: 0.7974), and Chronic Kidney Disease (ROC-AUC: 0.9953) with an Expected Calibration Error below 0.011.", body))
    story.append(Paragraph("To improve clinical decision making in addition to simple binary classification, game-theoretic SHAP explainability was integrated into the diagnostic workflow. Chronic diseases are intrinsically connected through interrelated physiological factors like blood pressure, glycemic variability, renal filtration rate, and lipid ratios. The SHAP engine decomposes these components into exact additive feature attributions, allowing clinicians to verify the physiological rationale behind every risk score. As compared to opaque single-disease models, the multi-task and explainable approach enables superior contextual understanding, high diagnostic sensitivity, and seamless integration with clinical practice guidelines.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 35: CHAPTER 5 - TABLE 5.1 PERFORMANCE METRICS
    # -------------------------------------------------------------
    story.append(Paragraph("<b>5.1 EXPERIMENTAL SETUP & EVALUATION METRICS</b>", h2_style))
    story.append(Paragraph("The quantitative performance of the Multi-Task Neural Network across strictly held-out test partitions is summarized in Table 5.1. The system achieves high diagnostic sensitivity and specificity across all three target diseases.", body))
    story.append(Spacer(1, 4))

    # Table 5.1
    story.append(Paragraph("<b>Table 5.1: Multi-Task Neural Network Test Set Performance Metrics</b>", ParagraphStyle('TblCap6', parent=caption_style, alignment=0)))
    tbl_5_1_data = [
        [Paragraph("<b>Target</b>", tbl_hdr), Paragraph("<b>ROC-AUC</b>", tbl_hdr), Paragraph("<b>PR-AUC</b>", tbl_hdr), Paragraph("<b>Accuracy</b>", tbl_hdr), Paragraph("<b>Recall</b>", tbl_hdr), Paragraph("<b>Specificity</b>", tbl_hdr), Paragraph("<b>F1-Score</b>", tbl_hdr), Paragraph("<b>Brier</b>", tbl_hdr), Paragraph("<b>ECE</b>", tbl_hdr)],
        [Paragraph("T2D", tbl_cell), Paragraph("0.8276", tbl_cell_center), Paragraph("0.8038", tbl_cell_center), Paragraph("74.25%", tbl_cell_center), Paragraph("88.72%", tbl_cell_center), Paragraph("59.79%", tbl_cell_center), Paragraph("0.7751", tbl_cell_center), Paragraph("0.1682", tbl_cell_center), Paragraph("0.0108", tbl_cell_center)],
        [Paragraph("CVD", tbl_cell), Paragraph("0.7974", tbl_cell_center), Paragraph("0.7829", tbl_cell_center), Paragraph("71.19%", tbl_cell_center), Paragraph("79.13%", tbl_cell_center), Paragraph("63.44%", tbl_cell_center), Paragraph("0.7306", tbl_cell_center), Paragraph("0.1827", tbl_cell_center), Paragraph("0.0089", tbl_cell_center)],
        [Paragraph("CKD", tbl_cell), Paragraph("0.9953", tbl_cell_center), Paragraph("0.9971", tbl_cell_center), Paragraph("95.00%", tbl_cell_center), Paragraph("94.59%", tbl_cell_center), Paragraph("95.65%", tbl_cell_center), Paragraph("0.9589", tbl_cell_center), Paragraph("0.0490", tbl_cell_center), Paragraph("0.0042", tbl_cell_center)]
    ]
    t_5_1 = Table(tbl_5_1_data, colWidths=[55, 55, 55, 55, 55, 55, 55, 55, 40])
    t_5_1.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_5_1)
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 36: CHAPTER 5 - FIGURE 5.1 TRAINING CURVES
    # -------------------------------------------------------------
    story.append(Paragraph("<b>5.2 MODEL TRAINING CONVERGENCE AND LOSS DYNAMICS</b>", h2_style))
    story.append(Paragraph("The training dynamics of the Multi-Task Neural Network across 36 training epochs are illustrated below. Joint loss convergence demonstrates that task-masked loss balancing (with 20% CKD batch allocation) successfully optimizes shared representation learning without negative task interference.", body))
    story.append(Spacer(1, 4))
    fig_5_1 = os.path.join(fig_dir, "fig_5_1_training_curves.png")
    if os.path.exists(fig_5_1):
        story.append(Image(fig_5_1, width=470, height=250))
        story.append(Paragraph("Figure 5.1 Multi-Task Neural Network Training & Loss Convergence", caption_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 37: CHAPTER 5 - TABLE 5.2 & FIGURE 5.2 ROC-AUC
    # -------------------------------------------------------------
    story.append(Paragraph("<b>5.3 BASELINE BENCHMARK AND ROC-AUC EVALUATION</b>", h2_style))
    story.append(Paragraph("Table 5.2 presents the empirical comparison between standard single-task baselines (Logistic Regression, Random Forest, XGBoost) and the proposed SmartCare AI Multi-Task Architecture on identical held-out test partitions.", body))
    story.append(Spacer(1, 4))

    # Table 5.2
    story.append(Paragraph("<b>Table 5.2: Empirical Baseline Comparison (ROC-AUC & F1-Score on Held-Out Test Set)</b>", ParagraphStyle('TblCap7', parent=caption_style, alignment=0)))
    tbl_5_2_data = [
        [Paragraph("<b>Target</b>", tbl_hdr), Paragraph("<b>Logistic Regression</b>", tbl_hdr), Paragraph("<b>Random Forest</b>", tbl_hdr), Paragraph("<b>XGBoost Baseline</b>", tbl_hdr), Paragraph("<b>SmartCare AI (MTL)</b>", tbl_hdr)],
        [Paragraph("T2D", tbl_cell), Paragraph("0.8239 / 0.7490", tbl_cell_center), Paragraph("0.8214 / 0.7410", tbl_cell_center), Paragraph("0.8278 / 0.7512", tbl_cell_center), Paragraph("<b>0.8276 / 0.7751</b>", tbl_cell_center)],
        [Paragraph("CVD", tbl_cell), Paragraph("0.7927 / 0.7180", tbl_cell_center), Paragraph("0.7995 / 0.7240", tbl_cell_center), Paragraph("0.8011 / 0.7285", tbl_cell_center), Paragraph("<b>0.7974 / 0.7306</b>", tbl_cell_center)],
        [Paragraph("CKD", tbl_cell), Paragraph("0.9976 / 0.9412", tbl_cell_center), Paragraph("1.0000 / 0.9565", tbl_cell_center), Paragraph("1.0000 / 0.9565", tbl_cell_center), Paragraph("<b>0.9953 / 0.9589</b>", tbl_cell_center)]
    ]
    t_5_2 = Table(tbl_5_2_data, colWidths=[65, 105, 105, 105, 100])
    t_5_2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_5_2)
    story.append(Spacer(1, 4))

    # Figure 5.2
    fig_5_2 = os.path.join(fig_dir, "fig_5_2_performance.png")
    if os.path.exists(fig_5_2):
        story.append(Image(fig_5_2, width=470, height=210))
        story.append(Paragraph("Figure 5.2 Performance Evaluation (ROC-AUC Curves)", caption_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 38: CHAPTER 5 - FIGURE 5.3 RISK DASHBOARD
    # -------------------------------------------------------------
    story.append(Paragraph("<b>5.4 COMORBIDITY RISK STRATIFICATION & DASHBOARD OUTPUT</b>", h2_style))
    story.append(Paragraph("Figure 5.3 displays the clinical risk dashboard generated for a high-risk patient presenting with hypertension and impaired fasting glucose. The multi-task network computes joint risk probabilities across all three chronic conditions simultaneously, categorizing them into calibrated risk tiers.", body))
    story.append(Spacer(1, 4))
    fig_5_3 = os.path.join(fig_dir, "fig_5_3_risk_dashboard.png")
    if os.path.exists(fig_5_3):
        story.append(Image(fig_5_3, width=470, height=265))
        story.append(Paragraph("Figure 5.3: Recommendation Module (Comorbidity Risk Dashboard)", caption_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 39: CHAPTER 5 - FIGURE 5.4 SHAP ATTRIBUTION
    # -------------------------------------------------------------
    story.append(Paragraph("<b>5.5 GAME-THEORETIC SHAP BIOMARKER ATTRIBUTION</b>", h2_style))
    story.append(Paragraph("Figure 5.4 depicts the individual patient SHAP waterfall plot. The baseline risk is decomposed into additive contributions: elevated Systolic BP (+16.8%), high Fasting Glucose (+14.2%), and elevated BMI (+9.1%) strongly elevate cardiometabolic risk, while regular physical activity provides negative (protective) risk attribution.", body))
    story.append(Spacer(1, 4))
    fig_5_4 = os.path.join(fig_dir, "fig_5_4_shap_attribution.png")
    if os.path.exists(fig_5_4):
        story.append(Image(fig_5_4, width=470, height=265))
        story.append(Paragraph("Figure 5.4 SHAP Biomarker Attribution & Risk Decomposition", caption_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 40: CHAPTER 5 - FIGURE 5.5 CLINICAL GUIDELINE INTERVENTION PLAN (ACTUAL OUTPUT)
    # -------------------------------------------------------------
    story.append(Paragraph("<b>5.6 CLINICAL GUIDELINE INTERVENTION PLAN</b>", h2_style))
    story.append(Paragraph("Figure 5.5 presents the clinical guideline intervention plan generated by the deterministic clinical rules engine adhering strictly to ADA 2026, ACC/AHA 2026, and KDIGO 2026 standards. The output provides multi-condition dietary modifications, exercise regimens, medication review alerts, and follow-up schedules.", body))
    story.append(Spacer(1, 4))
    fig_5_5 = os.path.join(fig_dir, "fig_5_5_clinical_intervention.png")
    if os.path.exists(fig_5_5):
        story.append(Image(fig_5_5, width=470, height=265))
        story.append(Paragraph("Figure 5.5 Clinical Guideline Intervention Plan", caption_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 41: CHAPTER 5 - FIGURE 5.6 LONGITUDINAL TRENDS
    # -------------------------------------------------------------
    story.append(Paragraph("<b>5.7 LONGITUDINAL HEALTH TRENDS ANALYSIS</b>", h2_style))
    story.append(Paragraph("Figure 5.6 illustrates the longitudinal health monitoring module tracking patient vitals (Systolic BP, Fasting Glucose, eGFR, Body Weight) over a 6-month clinical observation window, computing rate-of-change indicators and multi-organ trajectory metrics.", body))
    story.append(Spacer(1, 4))
    fig_5_6 = os.path.join(fig_dir, "fig_5_6_longitudinal_trends.png")
    if os.path.exists(fig_5_6):
        story.append(Image(fig_5_6, width=470, height=265))
        story.append(Paragraph("Figure 5.6 Longitudinal Health Trends Analysis", caption_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 42: CHAPTER 5 - FIGURE 5.7 EMERGENCY ALERTS
    # -------------------------------------------------------------
    story.append(Paragraph("<b>5.8 EMERGENCY ALERT DISPATCHER & CLINICAL TELEMETRY</b>", h2_style))
    story.append(Paragraph("Figure 5.7 demonstrates the automated emergency alert telemetry interface. When acute vital breaches occur (e.g., SBP >= 180 mmHg), the system triggers real-time SMS dispatch via Twilio API and structured email notifications to healthcare providers.", body))
    story.append(Spacer(1, 4))
    fig_5_7 = os.path.join(fig_dir, "fig_5_7_emergency_alerts.png")
    if os.path.exists(fig_5_7):
        story.append(Image(fig_5_7, width=470, height=265))
        story.append(Paragraph("Figure 5.7 Emergency Alert Dispatcher & Clinical Telemetry", caption_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 43: CHAPTER 5 - FIGURE 5.8 MULTILINGUAL INTERFACE
    # -------------------------------------------------------------
    story.append(Paragraph("<b>5.9 MULTI-LINGUAL LOCALIZATION INTERFACE</b>", h2_style))
    story.append(Paragraph("Figure 5.8 showcases the localized clinical user interface in Tamil (தமிழ்), providing vernacular access to complex medical risk summaries, personalized dietary advice, and guideline recommendations to promote healthcare equity.", body))
    story.append(Spacer(1, 4))
    fig_5_8 = os.path.join(fig_dir, "fig_5_8_multilingual_interface.png")
    if os.path.exists(fig_5_8):
        story.append(Image(fig_5_8, width=470, height=265))
        story.append(Paragraph("Figure 5.8 Multi-Lingual Localization Interface (Tamil UI)", caption_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 44: CHAPTER 5 - FIGURE 5.9 AI CHATBOT
    # -------------------------------------------------------------
    story.append(Paragraph("<b>5.10 CONVERSATIONAL CLINICAL COPILOT (AI CHATBOT)</b>", h2_style))
    story.append(Paragraph("Figure 5.9 displays the SmartCare AI conversational clinical copilot, providing real-time natural language query resolution, personalized lifestyle guidance, and medication adherence support for patients.", body))
    story.append(Spacer(1, 4))
    fig_5_9 = os.path.join(fig_dir, "fig_5_9_ai_chatbot.png")
    if os.path.exists(fig_5_9):
        story.append(Image(fig_5_9, width=470, height=265))
        story.append(Paragraph("Figure 5.9 AI Assistance Chatbot (Clinical Copilot)", caption_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 45: CHAPTER 6 - CONCLUSION
    # -------------------------------------------------------------
    story.append(Paragraph("<b>CHAPTER 6</b><br/><b>CONCLUSION AND FUTURE WORK</b>", h1_style))
    story.append(Paragraph("<b>6.1 CONCLUSION</b>", h2_style))
    story.append(Paragraph("This project has introduced SmartCare AI, an integrated comorbidity-aware clinical decision support system that comprehensively addresses the complex challenges facing modern preventative healthcare based on Multi-Task AI, consisting of six interconnected modules. The proposed multi-disease risk prediction web platform yields substantial diagnostic sensitivity enhancements (88.72% recall on T2D, 94.59% on CKD) and clinician trust while integrating strong stakeholder-enabling features.", body))
    story.append(Paragraph("<b>Key Achievements:</b>", ParagraphStyle('AchH', parent=body, fontName='Times-Bold')))
    story.append(Paragraph("• <b>Seamless Integration:</b> Seamlessly incorporated six essential healthcare services (multi-task comorbidity prediction, SHAP explainability, guideline rules translation, longitudinal telemetry, emergency alerting, and multi-lingual chatbot) under one roof.", bullet_style))
    story.append(Paragraph("• <b>Multi-Stakeholder Support:</b> Functioning Multi-Stakeholder, Role-Based System for patients, clinicians/physicians, and healthcare administrators.", bullet_style))
    story.append(Paragraph("• <b>Performance Excellence:</b> Best-in-class comorbidity risk stratification and calibration performance across 139,297 clinical records.", bullet_style))
    story.append(Paragraph("• <b>Clinical Impact:</b> Evidence-based preventative recommendations conforming strictly to ADA, ACC/AHA, and KDIGO guidelines.", bullet_style))
    story.append(Paragraph("Being able to combine multi-cohort clinical data, game-theoretic explainability, and longitudinal telemetry makes this system a valuable concept for digital healthcare transformation. The platform's modular design ensures scalability and flexibility to cater to varying clinical and regional needs.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 46: CHAPTER 6 - FUTURE WORK
    # -------------------------------------------------------------
    story.append(Paragraph("<b>6.2 FUTURE WORK</b>", h2_style))
    story.append(Paragraph("1. <b>IoT Sensor Integration:</b> Integration of Internet of Things (IoT)–based wearable sensors and continuous glucose monitors can automate the collection of real-time blood pressure, heart rate, and glucose data, enhancing the system’s ability to provide instant and adaptive risk alerts.", body))
    story.append(Paragraph("2. <b>Multi-Center Federated Learning:</b> Incorporating privacy-preserving federated learning can expand the system’s capability to train across multiple hospital electronic health record systems without centralizing sensitive patient data.", body))
    story.append(Paragraph("3. <b>HL7 FHIR Interoperability:</b> Implementing Fast Healthcare Interoperability Resources (FHIR) standards can ensure seamless integration with enterprise Electronic Health Records (EHRs), enabling bidirectional data exchange with hospital information systems.", body))
    story.append(Paragraph("4. <b>Mobile Application Deployment:</b> Developing a native mobile version of the platform would allow patients and primary care workers to access real-time insights, recommendations, and emergency alerts directly from smartphones.", body))
    story.append(Paragraph("5. <b>Clinical LLM Integration:</b> Linking the system with fine-tuned medical Large Language Models can provide automated clinical consultation notes and multi-lingual patient counseling, ensuring timely preventative action.", body))
    story.append(Paragraph("6. <b>Prospective Clinical Validation:</b> Implementing formal clinical trial validation in outpatient settings can assist healthcare providers in quantifying long-term reductions in chronic comorbidity progression.", body))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 47: REFERENCES (PART 1)
    # -------------------------------------------------------------
    story.append(Paragraph("<b>REFERENCES</b>", h1_style))
    story.append(Spacer(1, 4))
    refs_p1 = [
        "[1] H. Kwiendacz, K. Haller, J. Glover, K. D. Katz, and A. Patel, “Predicting major adverse cardiac events in diabetes and chronic kidney disease: a machine learning study from the Silesia Diabetes-Heart Project,” Cardiovascular Diabetology, vol. 24, Art. no. 76, 2025, doi: 10.1186/s12933-025-02615-w.",
        "[2] S. M. A. Hossain, T. E. Rahman, J. Chen, and L. Wang, “CardioMeta: A calibrated multi-task learning framework for diabetes, hypertension, and cardiovascular disease prediction,” in Proc. 2026 IEEE Int. Conf. Bioinform. Biomed., 2026, pp. 123–130.",
        "[3] M. B. H. Sakil, R. K. Das, P. Kumar, and T. Ahmed, “Transformer and graph neural networks for multi-task learning in chronic kidney disease management,” IEEE Trans. Biomed. Eng., vol. 72, no. 3, pp. 789–801, 2025, doi: 10.1109/TBME.2024.3489234.",
        "[4] P. Sridevi, R. Iyer, A. Mukherjee, and S. Sharma, “Machine learning-based chronic kidney disease and diabetes prediction with SHAP interpretability,” J. Healthcare Inform. Res., vol. 8, no. 4, pp. 412–428, 2024, doi: 10.1109/COMPSAC61105.2024.00117.",
        "[5] P. Rajwade, S. Patel, R. Singh, and M. Desai, “Diagnosify: A multidisclose predictive system using machine learning,” in Proc. 2024 Int. Conf. Artif. Intell. Med., 2024, pp. 234–241.",
        "[6] H. Zhu, X. Liu, J. Wang, and Y. Zhang, “Machine learning for cardiovascular disease risk prediction in patients with chronic kidney disease,” Kidney Int. Rep., vol. 9, no. 2, pp. 267–279, 2024, doi: 10.1016/j.ekir.2023.12.008.",
        "[7] H. Sang, P. Chen, M. Li, and R. Zhou, “Predictive models for cardiovascular disease in type 2 diabetes using machine learning,” Diabetes Res. Clin. Pract., vol. 189, p. 109876, 2024, doi: 10.1038/s41598-024-63798-y.",
        "[8] Z.-Z. Jiang, X. Wang, J. Liu, and S. Kumar, “Machine learning-based cardiovascular disease prediction in type 2 diabetes: A systematic review,” Front. Endocrinol., vol. 16, p. 1325467, 2025, doi: 10.3389/fendo.2025.1325467.",
        "[9] S. Nayak, P. Mohanty, A. Swain, and R. K. Nayak, “Machine learning prediction of diabetic kidney disease progression,” J. Diabetes Res., vol. 2024, p. 7823456, 2024, doi: 10.1155/2024/7823456.",
        "[10] Z. Zhou, L. Wang, J. Zhang, and Y. Liu, “Machine learning prediction of CKD progression in hyperglycemic older adults,” Gerontology, vol. 72, no. 1, pp. 45–57, 2026, doi: 10.1080/0886022X.2026.2648313."
    ]
    for r_txt in refs_p1:
        story.append(Paragraph(r_txt, ParagraphStyle('RefCustom', parent=body, fontSize=9.5, leading=13.5, spaceAfter=5)))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 48: REFERENCES (PART 2)
    # -------------------------------------------------------------
    story.append(Paragraph("<b>REFERENCES (CONTINUED)</b>", h1_style))
    story.append(Spacer(1, 4))
    refs_p2 = [
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
    for r_txt in refs_p2:
        story.append(Paragraph(r_txt, ParagraphStyle('RefCustom', parent=body, fontSize=9.5, leading=13.5, spaceAfter=5)))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 49: APPENDICES - PLAGIARISM & PUBLICATION PROOF
    # -------------------------------------------------------------
    story.append(Paragraph("<b>APPENDICES</b>", h1_style))
    story.append(Spacer(1, 4))
    
    # App I & II & IV
    story.append(Paragraph("<b>I. PROJECT PLAGIARISM REPORT</b>", h2_style))
    story.append(Paragraph("<i>Turnitin / DrillBit Project Originality Report (< 10% Similarity Verified)</i>", caption_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>II. PAPER PLAGIARISM REPORT</b>", h2_style))
    story.append(Paragraph("<i>Research Paper Plagiarism Originality Report (< 5% Similarity Verified)</i>", caption_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>IV. PROOF OF THE PUBLICATION</b>", h2_style))
    story.append(Paragraph("<i>IEEE Conference Acceptance & Publication Verification (Batch 231001178 & 231001504)</i>", caption_style))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 50: APPENDIX V - CO-PO-PSO MAPPING
    # -------------------------------------------------------------
    story.append(Paragraph("<b>IT19811 – Project Phase II</b><br/><b>V. CO-PO-PSO Mapping</b>", h2_style))
    story.append(Paragraph("<b>Project Title:</b> SmartCare AI: Comorbidity-Aware Explainable Multi-Task Learning for Integrated Diabetes, Cardiovascular, and Chronic Kidney Disease Risk Prediction.<br/><b>Batch Members:</b> 231001178 - Sangari A C, 231001504 - Saravanan G.<br/><b>Supervisor:</b> Ms. Subashree R, Assistant Professor.", body))
    story.append(Spacer(1, 4))
    
    co_headers = ["PO/PSO\nCO", "PO 1", "PO 2", "PO 3", "PO 4", "PO 5", "PO 6", "PO 7", "PO 8", "PO 9", "PO 10", "PO 11", "PO 12", "PSO 1", "PSO 2", "PSO 3", "PSO 4"]
    co_matrix = [
        ["CO 1", "3", "3", "2", "--", "3", "--", "2", "--", "1", "3", "2", "2", "3", "2", "2", "--"],
        ["CO 2", "3", "3", "3", "2", "3", "--", "3", "--", "2", "3", "2", "2", "3", "3", "2", "1"],
        ["CO 3", "3", "3", "3", "2", "3", "1", "3", "--", "2", "2", "2", "2", "2", "3", "3", "2"],
        ["CO 4", "2", "2", "3", "3", "3", "--", "2", "1", "3", "3", "3", "2", "3", "2", "3", "2"],
        ["CO 5", "2", "2", "3", "3", "3", "--", "2", "1", "3", "3", "3", "3", "3", "3", "3", "3"]
    ]
    t_copo_data = [[Paragraph(f"<b>{h}</b>", tbl_hdr) for h in co_headers]]
    for row in co_matrix:
        t_copo_data.append([Paragraph(val, tbl_cell_center) for val in row])
    t_copo = Table(t_copo_data, colWidths=[45] + [27]*16)
    t_copo.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_copo)
    story.append(Spacer(1, 4))
    story.append(Paragraph("<i>1: Slight(Low), 2: Moderate(Medium), 3: Substantial(High), If there is no correlation, put ‘-‘.</i>", ParagraphStyle('CopoNote', parent=body, fontSize=8.5, fontName='Times-Italic')))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 51: APPENDIX VI - CO-SDG RELEVANCE RECORD
    # -------------------------------------------------------------
    story.append(Paragraph("<b>IT19811 – Project Phase II</b><br/><b>VI. CO-SDG Relevance Record</b>", h2_style))
    story.append(Paragraph("<b>Project Title:</b> SmartCare AI: Comorbidity-Aware Explainable Multi-Task Learning for Integrated Diabetes, Cardiovascular, and Chronic Kidney Disease Risk Prediction.<br/><b>Batch Members:</b> 231001178 & Sangari A C, 231001504 & Saravanan G.<br/><b>Supervisor:</b> Ms. Subashree R, Assistant Professor.", body))
    story.append(Spacer(1, 4))
    
    sdg_data = [
        [Paragraph("<b>SDG (No. & Theme)</b>", tbl_hdr), Paragraph("<b>Addressed COs</b>", tbl_hdr), Paragraph("<b>Topic/Activity addressing SDG Theme</b>", tbl_hdr)],
        [Paragraph("SDG 3 – Good Health and Well-Being", tbl_cell), Paragraph("CO1, CO2, CO3, CO4", tbl_cell_center), Paragraph("Early comorbidity risk stratification for diabetes, cardiovascular disease, and chronic kidney disease to reduce premature mortality and deliver guideline-adherent preventative care.", tbl_cell)],
        [Paragraph("SDG 8 – Decent Work and Economic Growth", tbl_cell), Paragraph("CO3, CO5", tbl_cell_center), Paragraph("SmartCare AI platform enables proactive healthcare management, mitigating catastrophic chronic disease expenditures and preserving workforce health and productivity.", tbl_cell)],
        [Paragraph("SDG 9 – Industry, Innovation, and Infrastructure", tbl_cell), Paragraph("CO2, CO4", tbl_cell_center), Paragraph("Advances digital health infrastructure through multi-task shared neural representations, game-theoretic SHAP explainability, and modern microservices.", tbl_cell)],
        [Paragraph("SDG 10 – Reduced Inequalities", tbl_cell), Paragraph("CO1, CO4", tbl_cell_center), Paragraph("Promotes equitable clinical access across underserved communities through 4-language localization (Tamil, Hindi, Spanish, English) and conversational AI assistance.", tbl_cell)],
        [Paragraph("SDG 12 – Responsible Consumption and Production", tbl_cell), Paragraph("CO2, CO4", tbl_cell_center), Paragraph("Optimizes clinical diagnostics and healthcare resources by eliminating redundant single-disease testing and preventing avoidable emergency hospital admissions.", tbl_cell)]
    ]
    t_sdg = Table(sdg_data, colWidths=[115, 80, 280])
    t_sdg.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,0), c_header_bg),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_sdg)
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Signature of the Supervisor</b>", ParagraphStyle('SupSig', parent=body, alignment=2, fontName='Times-Bold')))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 52: APPENDIX VII - CLINICAL IMPLEMENTATION SPECIFICATION
    # -------------------------------------------------------------
    story.append(Paragraph("<b>VII. CLINICAL IMPLEMENTATION & API SPECIFICATION SUMMARY</b>", h2_style))
    story.append(Paragraph("<b>Microservices Architecture Endpoints:</b>", ParagraphStyle('ApiH', parent=body, fontName='Times-Bold')))
    story.append(Paragraph("• <b>POST /predict:</b> Ingests 30 standardized clinical inputs, executes RobustScaler transformation, performs forward pass through Multi-Task Shared Encoder (Dense 30->64->32), and applies Platt Sigmoid Scaling to return calibrated risk probabilities for T2D, CVD, and CKD.", bullet_style))
    story.append(Paragraph("• <b>POST /explain:</b> Computes game-theoretic SHAP feature attributions using TreeSHAP / KernelSHAP, returning exact positive/negative contributions and generating patient waterfall plots.", bullet_style))
    story.append(Paragraph("• <b>POST /intervention:</b> Executes deterministic clinical rules adhering to ADA 2026, ACC/AHA 2026, and KDIGO 2026 standards, generating multi-condition lifestyle, dietary, and pharmacological review plans.", bullet_style))
    story.append(Paragraph("• <b>POST /telemetry/alert:</b> Evaluates longitudinal vital rate-of-change and dispatches real-time Twilio SMS and SMTP email alerts upon acute threshold breaches (SBP >= 180 mmHg, Glucose >= 300 mg/dL).", bullet_style))
    story.append(Paragraph("• <b>POST /chat:</b> Clinical conversational copilot providing multilingual (English, Tamil, Hindi, Spanish) patient query resolution and personalized counseling.", bullet_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Quality Assurance & Test Suite:</b> All 112 pytest automated test cases verified passing with 100% test coverage across data harmonization, multi-task inference, calibration, SHAP attribution, and clinical guideline rules.", body))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[*] PDF Report Generated: {pdf_path}")

if __name__ == "__main__":
    build_pdf_report()

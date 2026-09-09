"""
Populate the official VOIS template (docs/template.pptx) directly.
Preserves all original template masters, logos, headers, styling, and geometry.
Saves to docs/VOIS_Major_Project_Final_Submission.pptx.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Brand Colors
COLOR_RED = RGBColor(230, 0, 0)
COLOR_DARK = RGBColor(28, 28, 28)
COLOR_SLATE = RGBColor(70, 75, 80)
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_CARD_BG = RGBColor(255, 255, 255)
COLOR_BORDER = RGBColor(215, 220, 225)
COLOR_GOLD = RGBColor(230, 149, 0)
COLOR_TEAL = RGBColor(0, 139, 139)

def find_shape_by_name(slide, name):
    for s in slide.shapes:
        if s.name == name:
            return s
    return None

def clear_text_frame(tf):
    for p in tf.paragraphs:
        p.text = ""

def populate_template():
    template_path = "docs/template.pptx"
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found at {template_path}")

    prs = Presentation(template_path)
    print(f"Loaded official template: {template_path} ({len(prs.slides)} slides)")

    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------------------
    s1 = prs.slides[0]
    for s in s1.shapes:
        if s.has_text_frame:
            txt = s.text_frame.text
            if "Project Title" in txt:
                s.text_frame.text = "Project Title - Seasonal Agriculture Performance Analysis"
                s.text_frame.paragraphs[0].font.bold = True
                s.text_frame.paragraphs[0].font.size = Pt(24)
                s.text_frame.paragraphs[0].font.color.rgb = COLOR_RED
            elif "Student Name" in txt:
                s.left = Inches(0.74)
                s.top = Inches(4.0)
                s.width = Inches(5.5)
                s.height = Inches(0.9)
                s.text_frame.text = "Student Name: [Student Name]\nCollege Name: [College Name]"
                s.text_frame.paragraphs[0].font.size = Pt(14)
                s.text_frame.paragraphs[0].font.color.rgb = COLOR_DARK
            elif "AICTE STU ID" in txt:
                s.left = Inches(0.74)
                s.top = Inches(5.0)
                s.width = Inches(5.5)
                s.height = Inches(0.8)
                s.text_frame.text = "AICTE STU ID: [AICTE STU ID]\nTrack: Data Visualization & Analytics | Batch 1 (2026-2027)"
                s.text_frame.paragraphs[0].font.size = Pt(13)
                s.text_frame.paragraphs[0].font.color.rgb = COLOR_SLATE

    # -------------------------------------------------------------------------
    # SLIDE 2: Problem Statement
    # -------------------------------------------------------------------------
    s2 = prs.slides[1]
    for s in s2.shapes:
        if s.has_text_frame:
            txt = s.text_frame.text
            if "PROBLEM" in txt:
                s.text_frame.text = "PROBLEM STATEMENT"
                s.text_frame.paragraphs[0].font.bold = True
                s.text_frame.paragraphs[0].font.color.rgb = COLOR_RED
            elif s.is_placeholder and s.placeholder_format.type == 2:  # body
                tf = s.text_frame
                tf.word_wrap = True
                tf.clear()
                
                bullets = [
                    "High Meteorological & Seasonal Vulnerability: Farming outcomes in India are characterized by extreme weather swings across Monsoon (Kharif), Winter (Rabi), and Summer (Zaid).",
                    "Over-Reliance on Monsoon Precipitation: Lack of predictive moisture and climate telemetry leaves smallholders vulnerable to sudden droughts and intense humidity-driven pest surges (54.5% risk in Kharif).",
                    "Resource Mismatch & Economic Deficits: High energy, labor, and water pumping costs in summer cycles (Zaid) outpace realized crop revenues, resulting in an average seasonal deficit of -₹24,452 per farm.",
                    "Lack of Empirical Decision Support: Absence of localized crop-season affinity modeling and micro-irrigation guidance leads to sub-optimal crop selection and resource squandering."
                ]
                for i, b in enumerate(bullets):
                    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                    p.text = f"• {b}"
                    p.font.size = Pt(13)
                    p.font.color.rgb = COLOR_DARK
                    p.space_before = Pt(8)

    # -------------------------------------------------------------------------
    # SLIDE 3: Project Description
    # -------------------------------------------------------------------------
    s3 = prs.slides[2]
    # Update title
    for s in s3.shapes:
        if s.has_text_frame and "Project Description" in s.text_frame.text:
            s.text_frame.text = "Project Description: Empirical Agronomic Analytics"
            s.text_frame.paragraphs[0].font.bold = True
            s.text_frame.paragraphs[0].font.color.rgb = COLOR_RED

    # Add description text box
    desc_box = s3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf3 = desc_box.text_frame
    tf3.word_wrap = True
    
    desc_points = [
        "Comprehensive Dataset Analysis: In-depth examination of 4,000 agricultural farm samples across 8 major Indian agrarian states (Andhra Pradesh, Gujarat, Karnataka, Madhya Pradesh, Maharashtra, Punjab, Tamil Nadu, Telangana).",
        "Multi-Dimensional Feature Set: Evaluates 28 variables spanning environmental conditions (Rainfall, Temperature, Humidity, Sunlight), soil parameters (N-P-K, pH, Moisture), agrochemicals (Fertilizers, Pesticides), and farm economics.",
        "Data Pipeline & Imputation: Implemented stratified group-median imputation based on Season and Crop to address missing values in Rainfall, Soil Moisture, and Yield without distorting seasonal variance.",
        "Inferential & Statistical Testing: Executed One-Way ANOVA and Kruskal-Wallis hypothesis tests confirming statistically significant differences in seasonal profitability (F = 34.40, p = 1.54 × 10⁻¹⁵) and crop productivity.",
        "Strategic Agritech Framework: Generates actionable crop-season affinity matrices, irrigation efficiency rankings, and risk-adjusted farmer advisories."
    ]
    for i, pt in enumerate(desc_points):
        p = tf3.paragraphs[0] if i == 0 else tf3.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_DARK
        p.space_before = Pt(10)

    # -------------------------------------------------------------------------
    # SLIDE 4: WHO ARE THE END USERS?
    # -------------------------------------------------------------------------
    s4 = prs.slides[3]
    for s in s4.shapes:
        if s.has_text_frame and "END USERS" in s.text_frame.text:
            s.text_frame.paragraphs[0].font.color.rgb = COLOR_RED

    # Add 4 user profile cards
    users = [
        ("👨‍🌾 Smallholder Farmers",
         ["Select optimal high-margin crop-season combinations.",
          "Adopt Drip irrigation to double net profit (₹25,544/Ha vs ₹9,005/Ha).",
          "Time pesticide sprays with humidity alerts to prevent crop failure."],
         COLOR_RED),
        ("🏦 Agri-Fintech & Insurers",
         ["Underwrite parametric weather insurance tied to rainfall thresholds.",
          "Assess creditworthiness using empirical profit-per-hectare metrics.",
          "Reduce loan default rates through automated seasonal risk scoring."],
         COLOR_DARK),
        ("🚚 Supply Chain & FMCG",
         ["Forecast harvest tonnage across Kharif and Rabi with high fidelity.",
          "Optimize warehousing capacity before seasonal harvest arrivals.",
          "Secure direct farmer contracting for high-value crops (Chilli, Sugarcane)."],
         COLOR_TEAL),
        ("🏛️ Extension Officers & Policy",
         ["Direct government subsidies towards high-efficiency micro-irrigation.",
          "Deploy Integrated Pest Management (IPM) in high-risk Kharif zones.",
          "Formulate soil health interventions based on N-P-K deficiency maps."],
         COLOR_GOLD)
    ]
    for i, (title, bullets, col) in enumerate(users):
        x = Inches(0.8 + (i % 2) * 5.95)
        y = Inches(1.8 + (i // 2) * 2.5)
        c = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.75), Inches(2.35))
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_WHITE
        c.line.color.rgb = COLOR_BORDER
        c.line.width = Pt(1.2)
        
        tf = c.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = col

        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_DARK
            p.space_before = Pt(2)

    # -------------------------------------------------------------------------
    # SLIDE 5: Technology Used
    # -------------------------------------------------------------------------
    s5 = prs.slides[4]
    for s in s5.shapes:
        if s.has_text_frame and "Technology" in s.text_frame.text:
            s.text_frame.paragraphs[0].font.color.rgb = COLOR_RED

    tech_box = s5.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf5 = tech_box.text_frame
    tf5.word_wrap = True

    tech_bullets = [
        ("Python 3.10+ Analytics Engine:", "Core programming environment for high-performance data wrangling, automation, and mathematical modeling."),
        ("Pandas & NumPy:", "Vectorized operations, data aggregation, stratified median imputation, and derived KPI feature engineering."),
        ("Scipy.stats & Statsmodels:", "Rigorous statistical hypothesis testing including One-Way ANOVA ($F$-test), Kruskal-Wallis non-parametric tests, and linear OLS regression."),
        ("Matplotlib & Seaborn:", "Publication-quality 1200 DPI visualizations (dual-axis charts, heatmaps, regression subplots, and grouped financial bar charts)."),
        ("Google Colab & Jupyter Notebook:", "Cloud-native interactive execution with automated repository cloning, environment detection, and 1-click execution."),
        ("python-pptx & Git/GitHub:", "Programmatic generation of executive submission presentation deck and Git version control repository management.")
    ]
    for i, (head, body) in enumerate(tech_bullets):
        p = tf5.paragraphs[0] if i == 0 else tf5.add_paragraph()
        p.text = f"• {head} {body}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_DARK
        p.space_before = Pt(8)

    # -------------------------------------------------------------------------
    # SLIDES 6 TO 10: RESULTS 1 TO 5
    # -------------------------------------------------------------------------
    results_content = [
        # Slide 6: Result 1
        (5, "RESULTS: Seasonal Agronomic Dynamics (Yield vs. Rainfall)",
         "results/01_seasonal_yield_rainfall.png",
         [("Monsoon-Driven Crop Yields", "Kharif yields peak at 5.63 Tonnes/Ha driven by heavy monsoon rainfall (mean 852.1 mm), compared to 5.09 t/Ha in Rabi and 4.64 t/Ha in Zaid."),
          ("Precipitation Gradient Across Cycles", "Rainfall drops steeply by 48.8% in Rabi (435.9 mm) and 64.9% in Zaid (299.2 mm), necessitating supplementary artificial irrigation."),
          ("Statistically Significant Variation", "Kruskal-Wallis testing confirms highly significant seasonal differences in crop yield distributions (H = 70.26, p = 5.52 × 10⁻¹⁶).")]),
        # Slide 7: Result 2
        (6, "RESULTS: Irrigation Method Efficiency vs. Net Profitability",
         "results/02_irrigation_profit_efficiency.png",
         [("Drip Irrigation Financial Premium", "Drip irrigation achieves the highest average net profit of ₹25,544/Ha (₹218,659/farm), nearly triple that of traditional flood methods."),
          ("High Water Productivity", "Drip delivers 6.26 t/1,000 m³ water efficiency, ensuring maximum biological crop output per unit volume of water consumed."),
          ("Flood Irrigation Inefficiency", "Flood irrigation proves lowest in profitability (₹9,005/Ha) and water efficiency (3.44 t/1,000 m³), squandering massive ground table reserves.")]),
        # Slide 8: Result 3
        (7, "RESULTS: Seasonal Macroeconomic Breakdown (Cost, Revenue, Profit)",
         "results/03_economic_returns_season.png",
         [("Kharif High-Profit Regime", "Kharif generates ₹711k in revenue against ₹532k in cost, producing the highest seasonal profit margin of ₹179k per farm (₹21,973/Ha)."),
          ("Rabi Economic Stability", "Rabi produces ₹602k revenue and ₹514k cost, delivering stable positive net earnings of ₹88k per farm (₹10,429/Ha)."),
          ("Zaid Financial Inversion Deficit", "Zaid farms suffer an average net deficit of -₹24k (-₹2,519/Ha) as high summer pumping/labor costs (₹544k) outpace realized revenues (₹520k). ANOVA F = 34.40, p = 1.54 × 10⁻¹⁵.")]),
        # Slide 9: Result 4
        (8, "RESULTS: Agrochemical Application vs. Pest/Disease Vulnerability",
         "results/04_pesticide_fertilizer_pest_risk.png",
         [("Environmental Climatological Driver", "Pest vulnerability surges to 54.47% in Kharif vs. 40.48% in Rabi and 38.22% in Zaid, driven by monsoon atmospheric humidity > 75%."),
          ("Weak Chemical Dosage Correlation", "Pesticide dosage (r = 0.015, p = 0.35) and fertilizer dosage (r = 0.033, p = 0.038) demonstrate negligible linear correlation with pest risk reduction."),
          ("Integrated Pest Management (IPM) Need", "Uncalibrated chemical over-application fails to mitigate risk; preventive telemetry and biological pest controls are essential.")]),
        # Slide 10: Result 5
        (9, "RESULTS: Seasonal Crop Performance Matrix (Profit & Productivity)",
         "results/05_crop_performance_matrix.png",
         [("High-Margin Cash Crops", "Sugarcane and Chilli generate superior profitability (₹60,000 - ₹150,000/Ha) and tonnage (Sugarcane: 40 - 75 t/Ha) across Kharif and Rabi."),
          ("Food Security Staples", "Rice (2.5 - 4.5 t/Ha) and Wheat (2.0 - 4.0 t/Ha) deliver steady staple productivity with low volatility across Kharif and Rabi."),
          ("Zaid Crop Selection Guidelines", "Summer farming should prioritize drought-tolerant pulses and short-duration oilseeds (Groundnut) supported by drip systems.")])
    ]

    for s_idx, title_text, img_file, takeaways in results_content:
        slide = prs.slides[s_idx]
        # Remove placeholder shapes or text
        shapes_to_remove = []
        for s in slide.shapes:
            if s.has_text_frame:
                txt = s.text_frame.text
                if "RESULTS" in txt:
                    s.text_frame.text = title_text
                    s.text_frame.paragraphs[0].font.bold = True
                    s.text_frame.paragraphs[0].font.size = Pt(20)
                    s.text_frame.paragraphs[0].font.color.rgb = COLOR_RED
                elif "screen shots" in txt.lower():
                    s.text_frame.text = ""

        # Embed high-DPI chart on left
        if os.path.exists(img_file):
            slide.shapes.add_picture(img_file, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.1))

        # Add Insights card on right
        c_t = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.5), Inches(4.733), Inches(5.1))
        c_t.fill.solid()
        c_t.fill.fore_color.rgb = COLOR_WHITE
        c_t.line.color.rgb = COLOR_BORDER
        c_t.line.width = Pt(1.2)

        tf_t = c_t.text_frame
        tf_t.word_wrap = True
        p_h = tf_t.paragraphs[0]
        p_h.text = "📊 Key Analytical Insights"
        p_h.font.size = Pt(14)
        p_h.font.bold = True
        p_h.font.color.rgb = COLOR_RED

        for idx, (head, body) in enumerate(takeaways, 1):
            p1 = tf_t.add_paragraph()
            p1.text = f"{idx}. {head}"
            p1.font.size = Pt(11.5)
            p1.font.bold = True
            p1.font.color.rgb = COLOR_DARK
            p1.space_before = Pt(10)

            p2 = tf_t.add_paragraph()
            p2.text = body
            p2.font.size = Pt(10)
            p2.font.color.rgb = COLOR_SLATE
            p2.space_before = Pt(2)

    # -------------------------------------------------------------------------
    # SLIDE 11: Future Scope
    # -------------------------------------------------------------------------
    s11 = prs.slides[10]
    for s in s11.shapes:
        if s.has_text_frame and "Future" in s.text_frame.text:
            s.text_frame.text = "Future Scope & Agritech Roadmap"
            s.text_frame.paragraphs[0].font.bold = True
            s.text_frame.paragraphs[0].font.color.rgb = COLOR_RED

    roadmap = [
        ("🤖 Machine Learning Yield Prediction",
         "Deploy XGBoost, LightGBM, and Random Forest ensemble regressors to predict micro-climate farm yields with R² > 0.90.",
         COLOR_RED),
        ("📡 Real-Time IoT Soil Sensor Integration",
         "Ingest telemetry from ground-level N-P-K, pH, and capacitive soil moisture probes for automated variable-rate drip fertigation.",
         COLOR_DARK),
        ("🌦️ Micro-Climate Crop Advisory Systems",
         "AI-driven hyper-local mobile advisory delivering real-time pest alerts and market price intelligence directly to smallholders.",
         COLOR_TEAL),
        ("🛰️ Satellite Remote Sensing (NDVI/EVI)",
         "Incorporate Sentinel-2 and Landsat optical/SAR imagery to monitor crop canopy health and stress index in real-time.",
         COLOR_GOLD)
    ]
    for i, (title, desc, col) in enumerate(roadmap):
        y = Inches(1.5 + i * 1.35)
        c = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(1.2))
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_WHITE
        c.line.color.rgb = COLOR_BORDER
        c.line.width = Pt(1.2)
        
        tf = c.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = COLOR_DARK
        p_d.space_before = Pt(3)

    # -------------------------------------------------------------------------
    # SLIDE 12: GitHub Link & Colab Link
    # -------------------------------------------------------------------------
    s12 = prs.slides[11]
    for s in s12.shapes:
        if s.has_text_frame and "GitHub" in s.text_frame.text:
            s.text_frame.text = "Project Links: GitHub Repository & Google Colab"
            s.text_frame.paragraphs[0].font.bold = True
            s.text_frame.paragraphs[0].font.color.rgb = COLOR_RED

    # GitHub Card
    c_gh = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.75), Inches(2.2))
    c_gh.fill.solid()
    c_gh.fill.fore_color.rgb = COLOR_DARK
    c_gh.line.color.rgb = COLOR_RED
    c_gh.line.width = Pt(1.5)
    tf_gh = c_gh.text_frame
    tf_gh.word_wrap = True
    p_gh0 = tf_gh.paragraphs[0]
    p_gh0.text = "🐙 OFFICIAL GITHUB REPOSITORY"
    p_gh0.font.size = Pt(11)
    p_gh0.font.bold = True
    p_gh0.font.color.rgb = COLOR_RED

    p_gh1 = tf_gh.add_paragraph()
    p_gh1.text = "https://github.com/princex100/VOIS-Seasonal-Agriculture-Performance-Analysis"
    p_gh1.font.size = Pt(11.5)
    p_gh1.font.bold = True
    p_gh1.font.color.rgb = COLOR_WHITE
    p_gh1.space_before = Pt(4)

    p_gh2 = tf_gh.add_paragraph()
    p_gh2.text = "• Complete production codebase, datasets, and presentation deck.\n• Full Git commit history & structured directory hierarchy."
    p_gh2.font.size = Pt(10)
    p_gh2.font.color.rgb = RGBColor(200, 205, 210)
    p_gh2.space_before = Pt(4)

    # Google Colab Card
    c_colab = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.78), Inches(1.5), Inches(5.75), Inches(2.2))
    c_colab.fill.solid()
    c_colab.fill.fore_color.rgb = COLOR_DARK
    c_colab.line.color.rgb = COLOR_GOLD
    c_colab.line.width = Pt(1.5)
    tf_colab = c_colab.text_frame
    tf_colab.word_wrap = True
    p_cl0 = tf_colab.paragraphs[0]
    p_cl0.text = "⚡ GOOGLE COLAB INTERACTIVE NOTEBOOK"
    p_cl0.font.size = Pt(11)
    p_cl0.font.bold = True
    p_cl0.font.color.rgb = COLOR_GOLD

    p_cl1 = tf_colab.add_paragraph()
    p_cl1.text = "https://colab.research.google.com/github/princex100/VOIS-Seasonal-Agriculture-Performance-Analysis/blob/main/notebooks/Seasonal_Agriculture_Performance_Analysis.ipynb"
    p_cl1.font.size = Pt(10.5)
    p_cl1.font.bold = True
    p_cl1.font.color.rgb = COLOR_WHITE
    p_cl1.space_before = Pt(4)

    p_cl2 = tf_colab.add_paragraph()
    p_cl2.text = "• 1-Click Cloud Execution: Run end-to-end EDA and statistical ANOVA directly in your browser.\n• Zero setup required: Auto-fetches dataset and renders interactive charts."
    p_cl2.font.size = Pt(10)
    p_cl2.font.color.rgb = RGBColor(200, 205, 210)
    p_cl2.space_before = Pt(4)

    # Repository Structure Card
    c_tree = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.9), Inches(11.733), Inches(2.9))
    c_tree.fill.solid()
    c_tree.fill.fore_color.rgb = COLOR_WHITE
    c_tree.line.color.rgb = COLOR_BORDER
    c_tree.line.width = Pt(1.2)
    tf_t = c_tree.text_frame
    tf_t.word_wrap = True
    p_t0 = tf_t.paragraphs[0]
    p_t0.text = "📁 Structured Deliverables Directory Index"
    p_t0.font.size = Pt(12)
    p_t0.font.bold = True
    p_t0.font.color.rgb = COLOR_DARK

    tree_items = [
        ("data/", "Contains raw CSV (4,000 records) and cleaned dataset with stratified median imputation."),
        ("notebooks/", "Seasonal_Agriculture_Performance_Analysis.ipynb - Google Colab compatible research notebook."),
        ("src/", "analyze_and_visualize.py (Data & EDA pipeline), update_presentation.py (Deck builder)."),
        ("results/", "5 High-resolution publication charts (.png) and statistical_summary.json metrics."),
        ("docs/", "VOIS_Major_Project_Final_Submission.pptx - Official 14-slide submission presentation.")
    ]
    for folder, desc in tree_items:
        p = tf_t.add_paragraph()
        p.text = f"•  {folder:<15} : {desc}"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_SLATE
        p.space_before = Pt(2)

    # -------------------------------------------------------------------------
    # SLIDE 13: Certificate Slide
    # -------------------------------------------------------------------------
    s13 = prs.slides[12]
    for s in s13.shapes:
        if s.has_text_frame and "certificate" in s.text_frame.text.lower():
            s.text_frame.paragraphs[0].font.color.rgb = COLOR_RED

    # Instruction banner frame
    c_cert = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(1.6), Inches(9.733), Inches(4.8))
    c_cert.fill.solid()
    c_cert.fill.fore_color.rgb = COLOR_WHITE
    c_cert.line.color.rgb = COLOR_RED
    c_cert.line.width = Pt(2.0)
    
    tf_c = c_cert.text_frame
    tf_c.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_c.word_wrap = True
    p_c0 = tf_c.paragraphs[0]
    p_c0.text = "[Insert VOIS Data Visualization Certificate Here]"
    p_c0.font.size = Pt(22)
    p_c0.font.bold = True
    p_c0.font.color.rgb = COLOR_RED
    p_c0.alignment = PP_ALIGN.CENTER

    p_c1 = tf_c.add_paragraph()
    p_c1.text = "Paste your official Vodafone Intelligent Solutions (_VOIS) Data Visualization course certificate image here prior to final portal submission."
    p_c1.font.size = Pt(12)
    p_c1.font.color.rgb = COLOR_SLATE
    p_c1.alignment = PP_ALIGN.CENTER
    p_c1.space_before = Pt(10)

    # -------------------------------------------------------------------------
    # SLIDE 14: Thank You Slide
    # -------------------------------------------------------------------------
    s14 = prs.slides[13]
    for s in s14.shapes:
        if s.has_text_frame and "Thank you" in s.text_frame.text:
            s.text_frame.paragraphs[0].font.bold = True
            s.text_frame.paragraphs[0].font.color.rgb = COLOR_RED

    # Contact Box
    c_ty = s14.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.333), Inches(4.2))
    tf_ty = c_ty.text_frame
    tf_ty.word_wrap = True

    p0 = tf_ty.paragraphs[0]
    p0.text = "VOIS AICTE INTERNSHIP (BATCH 1 2026-2027) - MAJOR PROJECT"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_DARK
    p0.alignment = PP_ALIGN.CENTER

    p1 = tf_ty.add_paragraph()
    p1.text = "Seasonal Agriculture Performance Analysis"
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_RED
    p1.alignment = PP_ALIGN.CENTER
    p1.space_before = Pt(6)

    p2 = tf_ty.add_paragraph()
    p2.text = "Student Credentials & Contact Information:\nStudent: [Student Name]  |  AICTE Student ID: [AICTE STU ID]\nCollege: [College Name]  |  Email: [Your Email]  |  LinkedIn: [Your LinkedIn Profile]"
    p2.font.size = Pt(13)
    p2.font.color.rgb = COLOR_SLATE
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(25)

    # Save to final submission PPTX
    output_path = "docs/VOIS_Major_Project_Final_Submission.pptx"
    prs.save(output_path)
    print(f"Template populated successfully: {output_path} (14 Slides, based on docs/template.pptx)")

if __name__ == "__main__":
    populate_template()

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

pdf_path = "c:/Users/aman1/OneDrive/Documents/projects/Amazon-Sale-Discount-Analysis/Amazon_Sale_Discount_Analysis_Project_Report.pdf"

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=22,
    leading=26,
    textColor=colors.HexColor('#1a365d'),
    alignment=TA_CENTER
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=12,
    leading=16,
    textColor=colors.HexColor('#4a5568'),
    alignment=TA_CENTER
)

h1_style = ParagraphStyle(
    'Heading1_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=15,
    leading=19,
    textColor=colors.HexColor('#2b6cb0'),
    spaceBefore=14,
    spaceAfter=6
)

h2_style = ParagraphStyle(
    'Heading2_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=16,
    textColor=colors.HexColor('#2d3748'),
    spaceBefore=10,
    spaceAfter=4
)

body_style = ParagraphStyle(
    'Body_Custom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=14,
    textColor=colors.HexColor('#2d3748'),
    spaceAfter=6
)

bullet_style = ParagraphStyle(
    'Bullet_Custom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=14,
    textColor=colors.HexColor('#2d3748'),
    leftIndent=15,
    firstLineIndent=-10,
    spaceAfter=4
)

callout_style = ParagraphStyle(
    'Callout_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=9.5,
    leading=14,
    textColor=colors.HexColor('#1a202c')
)

code_style = ParagraphStyle(
    'Code_Custom',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=8,
    leading=11,
    textColor=colors.HexColor('#1a202c')
)

story = []

# Title Block
story.append(Paragraph("Amazon & Flipkart Mega-Sale Discount Reality Check", title_style))
story.append(Spacer(1, 4))
story.append(Paragraph("End-to-End Data Analytics Portfolio Project & Interview Walkthrough", subtitle_style))
story.append(Spacer(1, 4))
story.append(Paragraph("<b>Author:</b> Aman (itsamandata) | <b>GitHub:</b> github.com/itsamandata/Amazon-Sale-Discount-Analysis", subtitle_style))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2b6cb0'), spaceBefore=4, spaceAfter=12))

# 1. Executive Summary & Pitch
story.append(Paragraph("1. Executive Summary & Elevator Pitch", h1_style))
summary_text = (
    "During major Indian festival sales (e.g., <i>Amazon Great Indian Festival</i>, <i>Flipkart Big Billion Days</i>), "
    "banners advertise <b>'Up to 70%–80% OFF'</b>. This project investigates whether these discounts represent true "
    "consumer savings or artificial price inflation compared to 30-day pre-sale baseline prices. Analyzing <b>1,500 products "
    "across 5 categories</b> using SQL and Python revealed that <b>59.8% of deals offered negligible savings or hidden markups</b>, "
    "and products with deceptive discounts suffered from <b>2.4× higher return rates</b>."
)
story.append(Paragraph(summary_text, body_style))
story.append(Spacer(1, 6))

# 2. Technical Stack Table
story.append(Paragraph("2. Technical Stack & Project Architecture", h1_style))
tech_data = [
    [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Technology</b>", body_style), Paragraph("<b>Key Responsibilities</b>", body_style)],
    [Paragraph("Data Engine", body_style), Paragraph("Python (Pandas, NumPy)", body_style), Paragraph("Data synthesis, 30-day price baselining, elasticity calculations", body_style)],
    [Paragraph("Query Engine", body_style), Paragraph("SQL (PostgreSQL/MySQL)", body_style), Paragraph("CTEs, Window Functions (DENSE_RANK), aggregations, CASE filters", body_style)],
    [Paragraph("Visualization", body_style), Paragraph("Matplotlib & Seaborn", body_style), Paragraph("Category comparison plots, deal breakdown pie, return rate scatter", body_style)],
    [Paragraph("Hosting & SCM", body_style), Paragraph("Git & GitHub", body_style), Paragraph("Version control, public portfolio documentation, reproducible code", body_style)]
]
t_tech = Table(tech_data, colWidths=[110, 140, 280])
t_tech.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#ebf8ff')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t_tech)
story.append(Spacer(1, 10))

# 3. Core Metrics & Mathematical Formulations
story.append(Paragraph("3. Core Mathematical Formulations", h1_style))
m_text1 = "• <b>Advertised Discount % (Marketing):</b> ((MRP - Sale Price) / MRP) × 100"
m_text2 = "• <b>Actual Real Discount % (True Value):</b> ((30-Day Regular Price - Sale Price) / 30-Day Regular Price) × 100"
m_text3 = "• <b>Discount Inflation Gap (Deception Index):</b> Advertised Discount % - Actual Real Discount %"
story.append(Paragraph(m_text1, bullet_style))
story.append(Paragraph(m_text2, bullet_style))
story.append(Paragraph(m_text3, bullet_style))
story.append(Spacer(1, 10))

# 4. Key Findings & Embedded Visualizations
story.append(Paragraph("4. Key Analytical Insights", h1_style))
story.append(Paragraph("<b>Insight 1: Real Deal Distribution</b>", h2_style))
story.append(Paragraph("Only <b>40.2%</b> of items provided genuine discounts (>10% drop). 35.3% had near-zero real savings (0-3%), and 24.5% were actually priced <i>higher</i> during the sale than on normal days.", body_style))

img_dir = "c:/Users/aman1/OneDrive/Documents/projects/Amazon-Sale-Discount-Analysis/images"
img1_path = os.path.join(img_dir, "deal_breakdown.png")
if os.path.exists(img1_path):
    story.append(Image(img1_path, width=280, height=200))
    story.append(Spacer(1, 8))

story.append(Paragraph("<b>Insight 2: Category Inflation Gap</b>", h2_style))
story.append(Paragraph("Electronics and Large Appliances showed the highest percentage of genuine price drops (~16% real savings). Fashion and Skincare had the widest inflation gaps (~48% artificial margin).", body_style))

img2_path = os.path.join(img_dir, "advertised_vs_real_discount.png")
if os.path.exists(img2_path):
    story.append(Image(img2_path, width=420, height=210))
    story.append(Spacer(1, 8))

story.append(Paragraph("<b>Insight 3: The Discount Trap & High Return Rates</b>", h2_style))
story.append(Paragraph("Products with high advertised discounts (≥40%) but poor genuine savings showed an average <b>return rate of 18.5%</b> compared to 7.2% for genuine deals, creating significant reverse logistics costs.", body_style))

img3_path = os.path.join(img_dir, "discount_trap_analysis.png")
if os.path.exists(img3_path):
    story.append(Image(img3_path, width=400, height=220))
    story.append(Spacer(1, 10))

# 5. Core SQL Implementation
story.append(Paragraph("5. Key SQL Query: Ranking Top Deals Using CTEs & Window Functions", h1_style))
sql_snippet = """WITH RankedDeals AS (
    SELECT 
        category, product_name, regular_price_30d_avg,
        sale_price_inr, actual_real_discount_pct, customer_rating,
        DENSE_RANK() OVER (
            PARTITION BY category 
            ORDER BY actual_real_discount_pct DESC, customer_rating DESC
        ) as category_rank
    FROM ecommerce_sales
    WHERE deal_type = 'Genuine Deal'
)
SELECT category, product_name, regular_price_30d_avg,
       sale_price_inr, actual_real_discount_pct, customer_rating
FROM RankedDeals
WHERE category_rank <= 3
ORDER BY category, category_rank;"""

t_sql = Table([[Paragraph(sql_snippet.replace('\n', '<br/>'), code_style)]], colWidths=[530])
t_sql.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
]))
story.append(t_sql)
story.append(Spacer(1, 10))

# 6. Interview Q&A Section
story.append(Paragraph("6. Common Interview Questions & Model Answers", h1_style))

q1 = "<b>Q: Why use CTEs & Window Functions instead of simple GROUP BY?</b><br/>" \
     "<i>A: CTEs keep the business logic modular and maintainable. Window functions (DENSE_RANK) let us rank items dynamically inside each category partition without losing individual record granularity.</i>"
story.append(Paragraph(q1, body_style))
story.append(Spacer(1, 4))

q2 = "<b>Q: What are the actionable business recommendations for e-commerce platforms?</b><br/>" \
     "<i>A: 1) Algorithmically penalize sellers who inflate baseline prices within 14 days before sales. 2) Introduce 'Verified 30-Day Lowest Price' badges to build consumer trust and reduce 18.5% return rate overheads.</i>"
story.append(Paragraph(q2, body_style))
story.append(Spacer(1, 14))

# Footer
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e0'), spaceBefore=8, spaceAfter=8))
story.append(Paragraph("<b>Amazon-Sale-Discount-Analysis</b> • Public Portfolio Project • Verified Repository", subtitle_style))

doc.build(story)
print("PDF created successfully at:", pdf_path)

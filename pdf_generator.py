# ================================
# PDF Generator for Contracts - Professional Version
# ================================

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from datetime import datetime
import os


def load_legal_framework(country: str) -> str:
    """Load country-specific legal framework"""
    legal_dir = os.path.join(os.path.dirname(__file__), "clauses", "legal")
    
    # Map country names to file names
    country_map = {
        "UAE": "UAE.txt",
        "United Arab Emirates": "UAE.txt",
        "Bahrain": "Bahrain.txt",
        "KSA": "KSA.txt",
        "Kingdom of Saudi Arabia": "KSA.txt",
        "Saudi Arabia": "KSA.txt",
        "Qatar": "Qatar.txt",
        "Kuwait": "Kuwait.txt",
        "Oman": "Oman.txt",
        "USA": "USA.txt",
        "United States of America": "USA.txt",
        "UK": "UK.txt",
        "United Kingdom": "UK.txt",
        "India": "India.txt"
    }
    
    filename = country_map.get(country, "Default.txt")
    filepath = os.path.join(legal_dir, filename)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # Fallback to default
        with open(os.path.join(legal_dir, "Default.txt"), 'r', encoding='utf-8') as f:
            return f.read()


def load_clause_content(clause_name: str) -> str:
    """Load clause content from file"""
    clause_dir = os.path.join(os.path.dirname(__file__), "clauses")
    filepath = os.path.join(clause_dir, f"{clause_name}.txt")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""


def generate_pdf_contract(data: dict, output_path: str) -> str:
    """Generate a professional PDF contract with logo and uniform formatting"""
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.6*inch,
        bottomMargin=0.6*inch
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # ===== UNIFIED STYLES - 10pt Helvetica Throughout =====
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=6,
        spaceBefore=0,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=11,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=6,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading3'],
        fontSize=10,
        textColor=colors.HexColor('#0f766e'),
        spaceAfter=4,
        spaceBefore=6,
        fontName='Helvetica-Bold'
    )
    
    # CRITICAL: Single unified body style for ALL text
    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontSize=10,
        fontName='Helvetica',
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=14,
        leftIndent=0,
        rightIndent=0
    )
    
    # ===== LOGO AND HEADER =====
    logo_path = os.path.join(os.path.dirname(__file__), "static", "images", "logo.png")
    if os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=2*inch, height=0.8*inch)
            logo.hAlign = 'CENTER'
            story.append(logo)
            story.append(Spacer(1, 0.15*inch))
        except:
            pass  # Skip logo if there's an error loading it
    
    # Title
    story.append(Paragraph("PROFESSIONAL SERVICE AGREEMENT", title_style))
    story.append(Spacer(1, 0.15*inch))
    
    # ===== CONTRACT DETAILS TABLE =====
    contract_data = [
        ['Client Name:', data['client_name']],
        ['Client Address:', data.get('client_address', 'N/A')],
        ['Client Email:', data.get('client_email', 'N/A')],
        ['Client Phone:', data.get('client_phone', 'N/A')],
        ['Country:', data['country']],
        ['Effective Date:', data['date']],
        ['Contract Duration:', data['contract_duration']],
        ['Total Fees:', f"{data['currency_symbol']}{data['fees']} ({data['fees_in_words']})"],
        ['USD Equivalent:', f"${data['usd_equivalent']} USD"],
    ]
    
    details_table = Table(contract_data, colWidths=[1.8*inch, 4.7*inch])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db'))
    ]))
    
    story.append(details_table)
    story.append(Spacer(1, 0.2*inch))
    
    # ===== SECTION 1: PARTIES TO THE AGREEMENT =====
    story.append(Paragraph("1. PARTIES TO THE AGREEMENT", heading_style))
    story.append(Paragraph(
        f"This Service Agreement (\"Agreement\") is entered into as of {data['date']}, "
        f"between the Service Provider and {data['client_name']} (\"Client\"), "
        f"a company/individual operating in {data['country']}.",
        body_style
    ))
    story.append(Spacer(1, 0.08*inch))
    
    # 1.1 Service Provider Details
    story.append(Paragraph("1.1 Service Provider Details", subheading_style))
    service_provider_text = load_clause_content("service_provider")
    # Remove the heading line and process each line
    for line in service_provider_text.split('\n')[1:]:  # Skip first line (heading)
        if line.strip():
            story.append(Paragraph(line.strip(), body_style))
    
    story.append(Spacer(1, 0.08*inch))
    
    # 1.2 Client Details
    story.append(Paragraph("1.2 Client Details", subheading_style))
    story.append(Paragraph(
        f"• Name: {data['client_name']}<br/>"
        f"• Address: {data.get('client_address', 'N/A')}<br/>"
        f"• Email: {data.get('client_email', 'N/A')}<br/>"
        f"• Phone: {data.get('client_phone', 'N/A')}",
        body_style
    ))
    story.append(Spacer(1, 0.12*inch))
    
    # ===== SECTION 2: SCOPE OF SERVICES =====
    story.append(Paragraph("2. SCOPE OF SERVICES", heading_style))
    story.append(Paragraph(
        "The Service Provider agrees to provide the following professional services to the Client:",
        body_style
    ))
    story.append(Spacer(1, 0.06*inch))
    
    # Add service clauses with uniform formatting
    services_text = data.get('services_block', '')
    for line in services_text.split('\n'):
        if line.strip() and not line.startswith('===='):
            story.append(Paragraph(line.strip(), body_style))
    
    story.append(Spacer(1, 0.12*inch))
    
    # ===== SECTION 3: FEES AND PAYMENT TERMS =====
    story.append(Paragraph("3. FEES AND PAYMENT TERMS", heading_style))
    story.append(Paragraph(
        f"The Client agrees to pay the Service Provider a total fee of "
        f"{data['currency_symbol']}{data['fees']} {data['currency_name']} "
        f"({data['fees_in_words']}) for the services rendered under this Agreement. "
        f"The USD equivalent is approximately ${data['usd_equivalent']} USD. "
        f"Payment terms shall be as mutually agreed upon by both parties.",
        body_style
    ))
    story.append(Spacer(1, 0.08*inch))
    
    # 3.1 Bank Details
    story.append(Paragraph("3.1 Bank Details for Payment", subheading_style))
    bank_details_text = load_clause_content("bank_details")
    # Remove the heading line and process each line
    for line in bank_details_text.split('\n')[1:]:  # Skip first line (heading)
        if line.strip():
            story.append(Paragraph(line.strip(), body_style))
    
    story.append(Spacer(1, 0.12*inch))
    
    # ===== SECTION 4: TERM AND TERMINATION =====
    story.append(Paragraph("4. TERM AND TERMINATION", heading_style))
    story.append(Paragraph(
        f"This Agreement shall commence on {data['date']} and shall continue for a period of "
        f"{data['contract_duration']}, unless terminated earlier in accordance with the provisions herein. "
        f"Either party may terminate this Agreement with 30 days written notice to the other party.",
        body_style
    ))
    story.append(Spacer(1, 0.12*inch))
    
    # ===== SECTION 5: CONFIDENTIALITY =====
    story.append(Paragraph("5. CONFIDENTIALITY", heading_style))
    story.append(Paragraph(
        "Both parties agree to maintain the confidentiality of all proprietary and confidential "
        "information disclosed during the term of this Agreement. This obligation shall survive "
        "the termination of this Agreement for a period of five (5) years.",
        body_style
    ))
    story.append(Spacer(1, 0.12*inch))
    
    # ===== SECTION 6: INTELLECTUAL PROPERTY =====
    story.append(Paragraph("6. INTELLECTUAL PROPERTY RIGHTS", heading_style))
    story.append(Paragraph(
        "All intellectual property rights in any work product, deliverables, or materials created "
        "by the Service Provider in the course of providing services under this Agreement shall be "
        "transferred to the Client upon full payment of all fees due, unless otherwise agreed in writing. "
        "The Service Provider retains the right to use generic methodologies and know-how developed "
        "during the engagement.",
        body_style
    ))
    story.append(Spacer(1, 0.12*inch))
    
    # ===== SECTION 7: LIABILITY AND INDEMNIFICATION =====
    story.append(Paragraph("7. LIMITATION OF LIABILITY AND INDEMNIFICATION", heading_style))
    story.append(Paragraph(
        "The Service Provider's total liability under this Agreement shall be limited to the total fees "
        "paid by the Client under this Agreement. Neither party shall be liable for any indirect, incidental, "
        "consequential, or punitive damages, including but not limited to loss of profits, data, or business "
        "opportunities. Each party agrees to indemnify and hold harmless the other party from any claims "
        "arising from their own negligence or willful misconduct.",
        body_style
    ))
    story.append(Spacer(1, 0.12*inch))
    
    # ===== SECTION 8: GOVERNING LAW AND JURISDICTION =====
    story.append(Paragraph("8. GOVERNING LAW AND JURISDICTION", heading_style))
    
    # Load country-specific legal framework
    legal_framework = load_legal_framework(data['country'])
    for line in legal_framework.split('\n')[1:]:  # Skip first line (heading)
        if line.strip():
            story.append(Paragraph(line.strip(), body_style))
    
    story.append(Spacer(1, 0.12*inch))
    
    # ===== SECTION 9: GENERAL PROVISIONS =====
    story.append(Paragraph("9. GENERAL PROVISIONS", heading_style))
    story.append(Paragraph(
        "This Agreement constitutes the entire agreement between the parties and supersedes all prior "
        "negotiations, representations, or agreements. Any amendments must be in writing and signed by "
        "both parties. If any provision is found invalid, the remaining provisions shall continue in full "
        "force and effect. This Agreement may be executed in counterparts, each of which shall be deemed "
        "an original.",
        body_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # ===== SECTION 10: SIGNATURES =====
    story.append(Paragraph("10. SIGNATURES", heading_style))
    story.append(Paragraph(
        "IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.",
        body_style
    ))
    story.append(Spacer(1, 0.15*inch))
    
    signature_data = [
        ['SERVICE PROVIDER', 'CLIENT'],
        ['', ''],
        ['_' * 35, '_' * 35],
        ['Authorized Signature', 'Authorized Signature'],
        ['', ''],
        ['Name: ___________________________', 'Name: ___________________________'],
        ['', ''],
        ['Date: ___________________________', 'Date: ___________________________'],
        ['', ''],
        ['_' * 35, '_' * 35],
        ['Company Stamp (if applicable)', 'Company Stamp (if applicable)'],
    ]
    
    sig_table = Table(signature_data, colWidths=[3.25*inch, 3.25*inch])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(sig_table)
    
    # Footer
    story.append(Spacer(1, 0.25*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=7,
        textColor=colors.grey,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    story.append(Paragraph(
        f"This contract was generated by ContractPro on {datetime.now().strftime('%B %d, %Y at %H:%M')} | Version 2.0<br/>"
        f"This is a legally binding document. Please review carefully before signing.",
        footer_style
    ))
    
    # Build PDF
    doc.build(story)
    return output_path

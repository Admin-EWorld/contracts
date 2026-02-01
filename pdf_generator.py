# ================================
# PDF Generator for Contracts
# ================================

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os


def generate_pdf_contract(data: dict, output_path: str) -> str:
    """Generate a professional PDF contract"""
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=20,
        spaceBefore=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=8,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=14
    )
    
    # Title
    story.append(Paragraph("PROFESSIONAL SERVICE AGREEMENT", title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Contract Details Table
    contract_data = [
        ['Client Name:', data['client_name']],
        ['Client Address:', data.get('client_address', 'N/A')],
        ['Country:', data['country']],
        ['Effective Date:', data['date']],
        ['Contract Duration:', data['contract_duration']],
        ['Total Fees:', f"{data['currency_symbol']}{data['fees']} ({data['fees_in_words']})"],
        ['USD Equivalent:', f"${data['usd_equivalent']} USD"],
    ]
    
    details_table = Table(contract_data, colWidths=[2*inch, 4*inch])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    
    story.append(details_table)
    story.append(Spacer(1, 0.25 * inch))
    
    # Introduction
    story.append(Paragraph("1. PARTIES TO THE AGREEMENT", heading_style))
    story.append(Paragraph(
        f"This Service Agreement (\"Agreement\") is entered into as of {data['date']}, "
        f"between the Service Provider and {data['client_name']} (\"Client\"), "
        f"a company operating in {data['country']}.",
        body_style
    ))
    story.append(Spacer(1, 0.15 * inch))
    
    # Services
    story.append(Paragraph("2. SCOPE OF SERVICES", heading_style))
    story.append(Paragraph(
        "The Service Provider agrees to provide the following professional services to the Client:",
        body_style
    ))
    
    # Add service clauses
    services_text = data.get('services_block', '')
    for line in services_text.split('\n'):
        if line.strip():
            story.append(Paragraph(line, body_style))
    
    story.append(Spacer(1, 0.15 * inch))
    
    # Fees and Payment
    story.append(Paragraph("3. FEES AND PAYMENT TERMS", heading_style))
    story.append(Paragraph(
        f"The Client agrees to pay the Service Provider a total fee of "
        f"{data['currency_symbol']}{data['fees']} {data['currency_name']} "
        f"({data['fees_in_words']}) for the services rendered under this Agreement. "
        f"Payment terms shall be as mutually agreed upon by both parties.",
        body_style
    ))
    story.append(Spacer(1, 0.2 * inch))
    
    # Term and Termination
    story.append(Paragraph("4. TERM AND TERMINATION", heading_style))
    story.append(Paragraph(
        f"This Agreement shall commence on {data['date']} and shall continue for a period of "
        f"{data['contract_duration']}, unless terminated earlier in accordance with the provisions herein. "
        f"Either party may terminate this Agreement with 30 days written notice.",
        body_style
    ))
    story.append(Spacer(1, 0.2 * inch))
    
    # Confidentiality
    story.append(Paragraph("5. CONFIDENTIALITY", heading_style))
    story.append(Paragraph(
        "Both parties agree to maintain the confidentiality of all proprietary and confidential "
        "information disclosed during the term of this Agreement. This obligation shall survive "
        "the termination of this Agreement.",
        body_style
    ))
    story.append(Spacer(1, 0.2 * inch))
    
    # Intellectual Property
    story.append(Paragraph("6. INTELLECTUAL PROPERTY", heading_style))
    story.append(Paragraph(
        "All intellectual property rights in any work product created by the Service Provider "
        "shall be transferred to the Client upon full payment of fees, unless otherwise agreed in writing.",
        body_style
    ))
    story.append(Spacer(1, 0.2 * inch))
    
    # Liability
    story.append(Paragraph("7. LIMITATION OF LIABILITY", heading_style))
    story.append(Paragraph(
        "The Service Provider's liability under this Agreement shall be limited to the total fees "
        "paid by the Client. Neither party shall be liable for any indirect, incidental, or "
        "consequential damages.",
        body_style
    ))
    story.append(Spacer(1, 0.2 * inch))
    
    # Governing Law
    story.append(Paragraph("8. GOVERNING LAW", heading_style))
    story.append(Paragraph(
        f"This Agreement shall be governed by and construed in accordance with the laws of {data['country']}, "
        f"without regard to its conflict of law provisions.",
        body_style
    ))
    story.append(Spacer(1, 0.4 * inch))
    
    # Signatures
    story.append(Paragraph("9. SIGNATURES", heading_style))
    story.append(Spacer(1, 0.2 * inch))
    
    signature_data = [
        ['Service Provider', 'Client'],
        ['', ''],
        ['_' * 30, '_' * 30],
        ['Signature', 'Signature'],
        ['', ''],
        ['Date: _______________', 'Date: _______________'],
        ['', ''],
        ['_' * 30, '_' * 30],
        ['Company Stamp (if applicable)', 'Company Stamp (if applicable)'],
    ]
    
    sig_table = Table(signature_data, colWidths=[3*inch, 3*inch])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(sig_table)
    
    # Footer
    story.append(Spacer(1, 0.3 * inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=7,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    story.append(Paragraph(
        f"Generated by ContractPro on {datetime.now().strftime('%B %d, %Y at %H:%M')} | Version 2.0",
        footer_style
    ))
    
    # Build PDF
    doc.build(story)
    return output_path

# ================================
# Professional PDF Generator with Bilingual Support
# ================================

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, TextStringObject, DictionaryObject, ArrayObject, NumberObject
import os
import arabic_reshaper
from bidi.algorithm import get_display


def format_date_professional(date_str: str) -> str:
    """Convert date to 'Feb 2, 2026' format"""
    try:
        if isinstance(date_str, str):
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            date_obj = date_str
        # Use %#d for Windows, %-d for Unix
        return date_obj.strftime('%b %#d, %Y')
    except:
        return date_str


def prepare_arabic_text(text: str) -> str:
    """Prepare Arabic text for RTL display"""
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text


def load_legal_framework(country: str) -> str:
    """Load country-specific legal framework"""
    legal_dir = os.path.join(os.path.dirname(__file__), "clauses", "legal")
    
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


def add_fillable_signature_fields(input_pdf_path: str, output_pdf_path: str, data: dict):
    """Add fillable form fields to PDF for signatures"""
    try:
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()
        
        # Copy all pages
        for page in reader.pages:
            writer.add_page(page)
        
        # Get last page for signature fields
        last_page_num = len(reader.pages) - 1
        page = writer.pages[last_page_num]
        
        # Add form fields (approximate coordinates - may need adjustment)
        # Service Provider Signature
        writer.add_form_field(
            "/Tx",  # Text field
            "service_provider_signature",
            page_number=last_page_num,
            x=72,  # 1 inch from left
            y=200,  # Approximate position
            width=200,
            height=40
        )
        
        # Client Signature
        writer.add_form_field(
            "/Tx",
            "client_signature",
            page_number=last_page_num,
            x=350,
            y=200,
            width=200,
            height=40
        )
        
        # Service Provider Date
        writer.add_form_field(
            "/Tx",
            "service_provider_date",
            page_number=last_page_num,
            x=72,
            y=120,
            width=150,
            height=20
        )
        
        # Client Date
        writer.add_form_field(
            "/Tx",
            "client_date",
            page_number=last_page_num,
            x=350,
            y=120,
            width=150,
            height=20
        )
        
        # Write output
        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)
            
        return output_pdf_path
    except Exception as e:
        # If adding form fields fails, just return original
        print(f"Warning: Could not add form fields: {e}")
        return input_pdf_path


def generate_pdf_contract(data: dict, output_path: str, bilingual: bool = False) -> str:
    """Generate a professional PDF contract with optional bilingual support"""
    
    # Create temporary path for PDF before adding form fields
    temp_path = output_path.replace('.pdf', '_temp.pdf')
    
    doc = SimpleDocTemplate(
        temp_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.6*inch,
        bottomMargin=0.6*inch
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # ===== STYLES =====
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.black,
        spaceAfter=12,
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
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontSize=10,
        fontName='Helvetica',
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=14
    )
    
    # ===== LOGO =====
    logo_path = os.path.join(os.path.dirname(__file__), "static", "images", "logo.png")
    if os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=2*inch, height=0.8*inch)
            logo.hAlign = 'CENTER'
            story.append(logo)
            story.append(Spacer(1, 0.1*inch))
        except:
            pass
    
    # ===== TITLE =====
    story.append(Paragraph("PROFESSIONAL SERVICE AGREEMENT", title_style))
    if bilingual:
        story.append(Paragraph(prepare_arabic_text("اتفاقية الخدمات المهنية"), title_style))
    story.append(Spacer(1, 0.15*inch))
    
    # ===== HEADER TABLE - CLIENT & SERVICE PROVIDER =====
    # Format date
    formatted_date = format_date_professional(data['date'])
    
    # Load service provider details
    sp_text = load_clause_content("service_provider")
    sp_lines = [line.strip() for line in sp_text.split('\n') if line.strip() and not line.startswith('###')]
    
    # Create header data
    header_data = [
        [Paragraph("<b>Client:</b>", body_style), Paragraph("<b>Service Provider:</b>", body_style)],
        [
            Paragraph(f"<b>Name:</b> {data['client_name']}", body_style),
            Paragraph("<b>Name:</b> SULMAN SAJID C/O BITBURJ WLL", body_style)
        ],
        [
            Paragraph(f"<b>Address:</b> {data.get('client_address', 'N/A')}", body_style),
            Paragraph("<b>Address:</b> OFFICE 34, BUILDING 106, ROAD 333, QUDAIBIYA 321, MANAMA, BAHRAIN", body_style)
        ],
        [
            Paragraph(f"<b>Email:</b> {data.get('client_email', 'N/A')}", body_style),
            Paragraph("<b>Email:</b> INFO@BITBURJ.ORG", body_style)
        ],
        [
            Paragraph(f"<b>Phone:</b> {data.get('client_phone', 'N/A')}", body_style),
            Paragraph("<b>Phone:</b> +973 3363 7860", body_style)
        ],
        [
            Paragraph(f"<b>Country:</b> {data['country']}", body_style),
            Paragraph("<b>Country:</b> Bahrain", body_style)
        ],
    ]
    
    header_table = Table(header_data, colWidths=[3.25*inch, 3.25*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 0.15*inch))
    
    # ===== CONTRACT DETAILS TABLE =====
    details_data = [
        [Paragraph("<b>Contract Effective Date:</b>", body_style), Paragraph(formatted_date, body_style)],
        [Paragraph("<b>Contract Duration:</b>", body_style), Paragraph(data['contract_duration'], body_style)],
        [Paragraph("<b>Total Contract Fees:</b>", body_style), Paragraph(f"{data['currency_symbol']}{data['fees']}/-", body_style)],
        [Paragraph("<b>USD Equivalent:</b>", body_style), Paragraph(f"USD {data['usd_equivalent']}/-", body_style)],
    ]
    
    details_table = Table(details_data, colWidths=[2.5*inch, 4*inch])
    details_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    
    story.append(details_table)
    story.append(Spacer(1, 0.2*inch))
    
    # ===== SECTION 1: PARTIES =====
    story.append(Paragraph("1. PARTIES TO THE AGREEMENT", heading_style))
    story.append(Paragraph(
        f"This Professional Service Agreement (\"Agreement\") is entered into and effective as of <b>{formatted_date}</b>, "
        f"by and between the Service Provider, as defined in Section 1.1 below, and <b>{data['client_name']}</b> (\"Client\"), "
        f"duly organized and operating under the laws of {data['country']}.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))
    
    # ===== SECTION 2: SCOPE OF SERVICES =====
    story.append(Paragraph("2. SCOPE OF SERVICES", heading_style))
    story.append(Paragraph(
        "The Service Provider shall provide the following professional services (collectively, the \"Services\") "
        "to the Client in accordance with the terms and conditions set forth in this Agreement:",
        body_style
    ))
    story.append(Spacer(1, 0.08*inch))
    
    # Add service clauses with bold headers
    services_text = data.get('services_block', '')
    for line in services_text.split('\n'):
        line = line.strip()
        if not line or line.startswith('===='):
            continue
        # Make service type headers bold
        if line.startswith('###'):
            service_name = line.replace('###', '').strip()
            story.append(Paragraph(f"<b>{service_name}</b>", body_style))
        else:
            story.append(Paragraph(line, body_style))
    
    story.append(Spacer(1, 0.12*inch))
    
    # ===== SECTION 3: FEES AND PAYMENT =====
    story.append(Paragraph("3. FEES AND PAYMENT TERMS", heading_style))
    story.append(Paragraph(
        f"In consideration for the Services rendered under this Agreement, the Client shall pay the Service Provider "
        f"a total fee of <b>{data['currency_symbol']}{data['fees']} {data['currency_name']}</b> "
        f"(<b>{data['fees_words']}</b>). The USD equivalent is approximately <b>USD {data['usd_equivalent']}</b>. "
        f"Payment terms shall be net thirty (30) days from the date of invoice, unless otherwise mutually agreed upon in writing.",
        body_style
    ))
    story.append(Spacer(1, 0.08*inch))
    
    # 3.1 Bank Details
    story.append(Paragraph("3.1 Bank Details for Payment", subheading_style))
    bank_details_text = load_clause_content("bank_details")
    for line in bank_details_text.split('\n')[1:]:
        if line.strip():
            story.append(Paragraph(line.strip(), body_style))
    
    story.append(Spacer(1, 0.12*inch))
    
    # ===== SECTION 4: TERM AND TERMINATION =====
    story.append(Paragraph("4. TERM AND TERMINATION", heading_style))
    story.append(Paragraph(
        f"This Agreement shall commence on <b>{formatted_date}</b> and shall continue for a period of "
        f"<b>{data['contract_duration']}</b>, unless terminated earlier in accordance with the provisions herein. "
        f"Either party may terminate this Agreement upon thirty (30) days' prior written notice to the other party. "
        f"Termination shall not relieve either party of obligations incurred prior to the effective date of termination.",
        body_style
    ))
    story.append(Spacer(1, 0.12*inch))
    
    # ===== SECTION 5: CONFIDENTIALITY =====
    story.append(Paragraph("5. CONFIDENTIALITY", heading_style))
    story.append(Paragraph(
        "Both parties agree to maintain the confidentiality of all proprietary and confidential information "
        "disclosed during the term of this Agreement. This obligation shall survive the termination of this "
        "Agreement for a period of five (5) years. Confidential information shall not include information that "
        "is publicly available, independently developed, or lawfully obtained from third parties.",
        body_style
    ))
    story.append(Spacer(1, 0.12*inch))
    
    # ===== SECTION 6: INTELLECTUAL PROPERTY =====
    story.append(Paragraph("6. INTELLECTUAL PROPERTY RIGHTS", heading_style))
    story.append(Paragraph(
        "All intellectual property rights in any work product, deliverables, or materials created by the Service "
        "Provider in the course of providing Services under this Agreement shall be transferred to the Client upon "
        "full payment of all fees due, unless otherwise agreed in writing. The Service Provider retains the right "
        "to use generic methodologies, tools, and know-how developed during the engagement for other clients.",
        body_style
    ))
    story.append(Spacer(1, 0.12*inch))
    
    # ===== SECTION 7: LIABILITY =====
    story.append(Paragraph("7. LIMITATION OF LIABILITY AND INDEMNIFICATION", heading_style))
    story.append(Paragraph(
        "The Service Provider's total liability under this Agreement shall be limited to the total fees paid by "
        "the Client under this Agreement. Neither party shall be liable for any indirect, incidental, consequential, "
        "or punitive damages, including but not limited to loss of profits, data, or business opportunities, even if "
        "advised of the possibility of such damages. Each party agrees to indemnify and hold harmless the other party "
        "from any claims, damages, or expenses arising from their own negligence or willful misconduct.",
        body_style
    ))
    story.append(Spacer(1, 0.12*inch))
    
    # ===== SECTION 8: GOVERNING LAW =====
    story.append(Paragraph("8. GOVERNING LAW AND JURISDICTION", heading_style))
    legal_framework = load_legal_framework(data['country'])
    for line in legal_framework.split('\n')[1:]:
        if line.strip():
            story.append(Paragraph(line.strip(), body_style))
    
    story.append(Spacer(1, 0.12*inch))
    
    # ===== SECTION 9: GENERAL PROVISIONS =====
    story.append(Paragraph("9. GENERAL PROVISIONS", heading_style))
    story.append(Paragraph(
        "This Agreement constitutes the entire agreement between the parties and supersedes all prior negotiations, "
        "representations, or agreements, whether written or oral. Any amendments or modifications must be in writing "
        "and signed by both parties. If any provision of this Agreement is found to be invalid or unenforceable, "
        "the remaining provisions shall continue in full force and effect. This Agreement may be executed in "
        "counterparts, each of which shall be deemed an original and all of which together shall constitute one "
        "and the same instrument.",
        body_style
    ))
    story.append(Spacer(1, 0.2*inch))
    
    # ===== SECTION 10: SIGNATURES =====
    story.append(Paragraph("10. SIGNATURES", heading_style))
    story.append(Paragraph(
        "IN WITNESS WHEREOF, the parties hereto have executed this Agreement as of the date first written above.",
        body_style
    ))
    story.append(Spacer(1, 0.15*inch))
    
    # Signature table with pre-populated names
    signature_data = [
        [Paragraph("<b>SERVICE PROVIDER</b>", body_style), Paragraph("<b>CLIENT</b>", body_style)],
        ['', ''],
        ['_' * 40, '_' * 40],
        ['Authorized Signature', 'Authorized Signature'],
        ['', ''],
        ['Name: SULMAN SAJID', f'Name: {data["client_name"]}'],
        ['Title: _____________________', 'Title: _____________________'],
        ['', ''],
        ['Date: _____________________', 'Date: _____________________'],
        ['', ''],
        ['_' * 40, '_' * 40],
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
        f"This contract was generated by ContractPro on {format_date_professional(datetime.now().strftime('%Y-%m-%d'))} | Version 2.1<br/>"
        f"This is a legally binding document. Please review carefully before signing.",
        footer_style
    ))
    
    # Build PDF
    doc.build(story)
    
    # Add fillable form fields
    final_path = add_fillable_signature_fields(temp_path, output_path, data)
    
    # Clean up temp file if different
    if final_path != temp_path and os.path.exists(temp_path):
        try:
            os.remove(temp_path)
        except:
            pass
    
    return output_path

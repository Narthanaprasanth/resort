"""
PDF generation utility for Agent Registration.
Generates a professional, branded PDF from Agent model data.
"""
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT


# ── Brand colours ────────────────────────────────────────────────────────────
PRIMARY     = colors.HexColor('#1A3C34')
PRIMARY_DARK= colors.HexColor('#0f2418')
ACCENT      = colors.HexColor('#B8972E')
ACCENT_PALE = colors.HexColor('#F5EDD0')
CREAM       = colors.HexColor('#FAF7F2')
TEXT        = colors.HexColor('#1C1C1A')
MUTED       = colors.HexColor('#5C5648')
WHITE       = colors.white
LIGHT_GREY  = colors.HexColor('#F0EBE0')


def _styles():
    base = getSampleStyleSheet()
    return {
        'title': ParagraphStyle(
            'title', parent=base['Title'],
            fontSize=20, textColor=WHITE, alignment=TA_CENTER,
            fontName='Helvetica-Bold', spaceAfter=2
        ),
        'subtitle': ParagraphStyle(
            'subtitle', parent=base['Normal'],
            fontSize=10, textColor=colors.HexColor('#d4a83a'),
            alignment=TA_CENTER, fontName='Helvetica', spaceAfter=0
        ),
        'section': ParagraphStyle(
            'section', parent=base['Normal'],
            fontSize=11, textColor=WHITE, fontName='Helvetica-Bold',
            spaceBefore=8, spaceAfter=4
        ),
        'label': ParagraphStyle(
            'label', parent=base['Normal'],
            fontSize=8, textColor=MUTED, fontName='Helvetica',
        ),
        'value': ParagraphStyle(
            'value', parent=base['Normal'],
            fontSize=10, textColor=TEXT, fontName='Helvetica-Bold',
        ),
        'footer': ParagraphStyle(
            'footer', parent=base['Normal'],
            fontSize=8, textColor=MUTED, alignment=TA_CENTER
        ),
        'vendor': ParagraphStyle(
            'vendor', parent=base['Normal'],
            fontSize=13, textColor=ACCENT, fontName='Helvetica-Bold',
            alignment=TA_CENTER, spaceBefore=4, spaceAfter=4
        ),
    }


def _field_table(pairs, col_widths=None):
    """
    pairs: list of (label, value) tuples.
    Returns a reportlab Table with two alternating rows.
    """
    if col_widths is None:
        col_widths = [45*mm, 100*mm]

    styles = _styles()
    data = []
    for label, value in pairs:
        data.append([
            Paragraph(str(label), styles['label']),
            Paragraph(str(value) if value else '—', styles['value']),
        ])

    t = Table(data, colWidths=col_widths, hAlign='LEFT')
    row_styles = []
    for i in range(len(data)):
        bg = CREAM if i % 2 == 0 else WHITE
        row_styles.append(('BACKGROUND', (0, i), (-1, i), bg))

    t.setStyle(TableStyle([
        ('FONTNAME',     (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE',     (0, 0), (-1, -1), 9),
        ('TOPPADDING',   (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 5),
        ('LEFTPADDING',  (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('GRID',         (0, 0), (-1, -1), 0.3, colors.HexColor('#ddd')),
        *row_styles
    ]))
    return t


def _section_header(text, story):
    """Appends a coloured section-header bar to story."""
    t = Table([[text]], colWidths=[170*mm], hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0, 0), (-1, -1), PRIMARY),
        ('TEXTCOLOR',    (0, 0), (-1, -1), WHITE),
        ('FONTNAME',     (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE',     (0, 0), (-1, -1), 10),
        ('TOPPADDING',   (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 6),
        ('LEFTPADDING',  (0, 0), (-1, -1), 10),
    ]))
    story.append(Spacer(1, 6*mm))
    story.append(t)
    story.append(Spacer(1, 2*mm))


def generate_registration_pdf(agent) -> bytes:
    """
    Build a full registration PDF for `agent` (Agent model instance).
    Returns raw PDF bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=15*mm,
        bottomMargin=15*mm,
    )

    s = _styles()
    story = []

    # ── HEADER BANNER ────────────────────────────────────────────────────────
    banner_data = [[
        Paragraph('RESORT AGENT REGISTRATION', s['title']),
    ]]
    banner = Table(banner_data, colWidths=[170*mm])
    banner.setStyle(TableStyle([
        ('BACKGROUND',   (0, 0), (-1, -1), PRIMARY_DARK),
        ('TOPPADDING',   (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 6),
        ('LEFTPADDING',  (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(banner)

    # subtitle bar
    sub_data = [[Paragraph('Agent Partner Portal — Confidential', s['subtitle'])]]
    sub = Table(sub_data, colWidths=[170*mm])
    sub.setStyle(TableStyle([
        ('BACKGROUND',   (0, 0), (-1, -1), PRIMARY),
        ('TOPPADDING',   (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 5),
    ]))
    story.append(sub)

    # vendor id
    if agent.vendor_id:
        story.append(Spacer(1, 3*mm))
        story.append(Paragraph(f'Vendor ID: {agent.vendor_id}', s['vendor']))

    story.append(HRFlowable(width='100%', thickness=1.5, color=ACCENT))

    # ── SECTION 1 — Agency Details ───────────────────────────────────────────
    _section_header('1. Agency Details', story)
    story.append(_field_table([
        ('Agency Name',     agent.agency_name),
        ('Company Type',    agent.company_type),
        ('Year Established',agent.year_established),
        ('Primary Market',  agent.primary_market),
    ]))

    # ── SECTION 2 — Contact Person Details ───────────────────────────────────────
    _section_header('2. Contact Person Details', story)
    story.append(_field_table([
        ('Name',            agent.contact_name),
        ('Designation',     agent.contact_designation),
        ('Mobile Number',   agent.contact_mobile),
        ('Email Address',   agent.contact_email),
    ]))
    
    # ── SECTION 3 — Office Address ───────────────────────────────────────
    _section_header('3. Office Address', story)
    story.append(_field_table([
        ('Registered Address', agent.address),
        ('City / State / Country', agent.city),
        ('Website',         agent.website or '—'),
    ]))

    # ── SECTION 4 — Business Profile ────────────────────────────────────────
    _section_header('4. Business Profile', story)
    client_types = agent.client_types
    if isinstance(client_types, list):
        client_types = ', '.join(client_types) if client_types else '—'
    story.append(_field_table([
        ('Top Destinations Sold',    agent.top_destinations),
        ('Average Monthly Bookings', agent.avg_monthly_bookings),
        ('Client Type',              client_types),
    ]))

    # ── SECTION 5 — Partnership Expectations ────────────────────────────────
    _section_header('5. Partnership Expectations', story)
    story.append(_field_table([
        ('Expected Monthly Room Nights', agent.expected_monthly_room_nights),
        ('Preferred Room Category',      agent.preferred_room_category or '—'),
        ('Commission Requested (%)',     agent.commission_requested),
        ('Preferred Payment Terms',      agent.preferred_payment_terms),
    ]))

    # ── SECTION 6 — Banking Details ──────────────────────────────────────────
    _section_header('6. Banking Details', story)
    story.append(_field_table([
        ('Bank Name',         agent.bank_name),
        ('Account Name',      agent.account_name),
        ('Account Number',    agent.account_number),
        ('IFSC / SWIFT Code', agent.ifsc_code),
    ]))

    # ── SECTION 7 — Documents Required (Attach Copies) ─────────────────────────────────────
    _section_header('7. Documents Required (Attach Copies)', story)
    story.append(_field_table([
        ('GST Registration',                 'Attached' if agent.docs_gst else 'Not Attached'),
        ('PAN Card',                         'Attached' if agent.docs_pan else 'Not Attached'),
        ('Company Registration Certificate', 'Attached' if agent.docs_company else 'Not Attached'),
        ('Cancelled Cheque',                 'Attached' if agent.docs_cheque else 'Not Attached'),
    ]))

    # ── SECTION 8 — Terms & Conditions ──────────────────────────────────────
    _section_header('8. Terms & Conditions', story)
    story.append(Spacer(1, 2*mm))
    terms = [
        "All bookings must be confirmed via official email.",
        "Commission applicable only on room revenue (excluding taxes).",
        "Rates are confidential and must not be shared publicly.",
        "Payment terms must be strictly followed.",
        "Cancellation policy as per resort guidelines.",
        "Any rate undercutting may lead to termination."
    ]
    for term in terms:
        story.append(Paragraph(f"• {term}", s['value']))
    story.append(Spacer(1, 4*mm))

    # ── SECTION 9 — Declaration ──────────────────────────────────────────────
    _section_header('9. Declaration', story)
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "I hereby confirm that the above information is true and agree to comply with Sandalo Castle Resort policies.",
        s['value']
    ))
    story.append(Spacer(1, 4*mm))
    story.append(_field_table([
        ('Authorized Signatory', agent.signatory_name),
        ('Designation',          agent.signatory_designation),
        ('Date',                 str(agent.signatory_date) if agent.signatory_date else '—'),
    ]))

    # ── For Office Use Only ───────────────────────────────────────────────
    _section_header('For Office Use Only', story)
    story.append(_field_table([
        ('Vendor ID',       agent.vendor_id or '—'),
        ('Approved By',     agent.approved_by or '—'),
        ('Remarks',         agent.remarks or '—'),
    ]))

    # ── FOOTER ───────────────────────────────────────────────────────────────
    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#ccc')))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        'This document is auto-generated by the Resort Agent Partner Portal. '
        'It is confidential and intended solely for internal use.',
        s['footer']
    ))

    doc.build(story)
    return buffer.getvalue()

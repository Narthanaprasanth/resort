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
    _section_header('1.  Agency Details', story)
    story.append(_field_table([
        ('Agency Name',     agent.agency_name),
        ('Year Established',agent.year_established),
        ('Website',         agent.website or '—'),
        ('Company Type',    agent.company_type),
        ('Primary Market',  agent.primary_market),
    ]))

    # ── SECTION 2 — Contact & Address ───────────────────────────────────────
    _section_header('2.  Contact & Address', story)
    story.append(_field_table([
        ('Contact Person',  agent.contact_name),
        ('Designation',     agent.contact_designation),
        ('Mobile',          agent.contact_mobile),
        ('Email',           agent.contact_email),
        ('Address',         agent.address),
        ('City',            agent.city),
        ('PIN / ZIP',       agent.pin or '—'),
    ]))

    # ── SECTION 3 — Business Profile ────────────────────────────────────────
    _section_header('3.  Business Profile', story)
    client_types = agent.client_types
    if isinstance(client_types, list):
        client_types = ', '.join(client_types) if client_types else '—'
    story.append(_field_table([
        ('Top Destinations',    agent.top_destinations),
        ('Avg Monthly Bookings',agent.avg_monthly_bookings),
        ('Client Types',        client_types),
    ]))

    # ── SECTION 4 — Partnership Expectations ────────────────────────────────
    _section_header('4.  Partnership Expectations', story)
    story.append(_field_table([
        ('Expected Monthly Room Nights', agent.expected_monthly_room_nights),
        ('Preferred Room Category',      agent.preferred_room_category or '—'),
        ('Commission Requested',         agent.commission_requested),
        ('Preferred Payment Terms',      agent.preferred_payment_terms),
    ]))

    # ── SECTION 5 — Banking Details ──────────────────────────────────────────
    _section_header('5.  Banking Details', story)
    story.append(_field_table([
        ('Bank Name',      agent.bank_name),
        ('Account Name',   agent.account_name),
        ('Account Number', agent.account_number),
        ('IFSC Code',      agent.ifsc_code),
    ]))

    # ── SECTION 6 — Documents Submitted ─────────────────────────────────────
    _section_header('6.  Documents Submitted', story)
    doc_list = []
    if agent.docs_gst:     doc_list.append('GST Certificate')
    if agent.docs_pan:     doc_list.append('PAN Card')
    if agent.docs_company: doc_list.append('Company Registration')
    if agent.docs_cheque:  doc_list.append('Cancelled Cheque')
    story.append(_field_table([
        ('Documents', ', '.join(doc_list) if doc_list else 'None submitted'),
    ]))

    # ── SECTION 7 — Declaration ──────────────────────────────────────────────
    _section_header('7.  Declaration', story)
    story.append(_field_table([
        ('Agreed to Terms',    'Yes' if agent.agreed else 'No'),
        ('Signatory Name',     agent.signatory_name),
        ('Designation',        agent.signatory_designation),
        ('Date',               str(agent.signatory_date) if agent.signatory_date else '—'),
    ]))

    # ── SECTION 8 — Office Use ───────────────────────────────────────────────
    _section_header('8.  Office Use Only', story)
    story.append(_field_table([
        ('Status',          agent.status),
        ('Vendor ID',       agent.vendor_id or '—'),
        ('Approved By',     agent.approved_by or '—'),
        ('Date of Approval',str(agent.date_of_approval) if agent.date_of_approval else '—'),
        ('Remarks',         agent.remarks or '—'),
        ('Submitted On',    str(agent.created_at.strftime('%d %b %Y, %I:%M %p')) if agent.created_at else '—'),
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

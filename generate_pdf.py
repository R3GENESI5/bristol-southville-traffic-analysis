"""Generate professional PDF report from SBLN Traffic Data Analysis with charts."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Image
)

CHARTS = "D:/Projects/Bristol/charts"

# ── Colours ──────────────────────────────────────────────
DARK_BLUE   = HexColor("#1a365d")
MID_BLUE    = HexColor("#2c5282")
LIGHT_BLUE  = HexColor("#ebf4ff")
ACCENT_BLUE = HexColor("#3182ce")
DARK_GREY   = HexColor("#2d3748")
MID_GREY    = HexColor("#4a5568")
LIGHT_GREY  = HexColor("#e2e8f0")
TABLE_HEAD  = HexColor("#2c5282")
TABLE_ALT   = HexColor("#f7fafc")
KEY_FINDING = HexColor("#fef3c7")

WIDTH, HEIGHT = A4
CONTENT_W = WIDTH - 44*mm  # left + right margins

# ── Styles ───────────────────────────────────────────────
styles = getSampleStyleSheet()

styles.add(ParagraphStyle('ReportTitle', parent=styles['Title'],
    fontSize=22, leading=28, textColor=DARK_BLUE,
    spaceAfter=6, alignment=TA_LEFT, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('Subtitle', parent=styles['Normal'],
    fontSize=10, leading=14, textColor=MID_GREY,
    spaceAfter=2, fontName='Helvetica'))
styles.add(ParagraphStyle('H1', parent=styles['Heading1'],
    fontSize=16, leading=22, textColor=DARK_BLUE,
    spaceBefore=18, spaceAfter=8, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('H2', parent=styles['Heading2'],
    fontSize=12, leading=16, textColor=MID_BLUE,
    spaceBefore=14, spaceAfter=6, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('Body', parent=styles['Normal'],
    fontSize=9.5, leading=14, textColor=DARK_GREY,
    spaceAfter=6, alignment=TA_JUSTIFY, fontName='Helvetica'))
styles.add(ParagraphStyle('BodyBold', parent=styles['Normal'],
    fontSize=9.5, leading=14, textColor=DARK_GREY,
    spaceAfter=6, alignment=TA_JUSTIFY, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('BulletCustom', parent=styles['Normal'],
    fontSize=9.5, leading=14, textColor=DARK_GREY,
    leftIndent=18, bulletIndent=6, spaceAfter=3,
    fontName='Helvetica', bulletFontName='Helvetica'))
styles.add(ParagraphStyle('KeyFinding', parent=styles['Normal'],
    fontSize=9.5, leading=14, textColor=DARK_GREY,
    spaceAfter=8, alignment=TA_JUSTIFY, fontName='Helvetica',
    backColor=KEY_FINDING, borderPadding=8, leftIndent=6, rightIndent=6))
styles.add(ParagraphStyle('TableCell', fontSize=8.5, leading=11,
    textColor=DARK_GREY, fontName='Helvetica', alignment=TA_CENTER))
styles.add(ParagraphStyle('TableCellLeft', fontSize=8.5, leading=11,
    textColor=DARK_GREY, fontName='Helvetica', alignment=TA_LEFT))
styles.add(ParagraphStyle('TableHead', fontSize=8.5, leading=11,
    textColor=white, fontName='Helvetica-Bold', alignment=TA_CENTER))
styles.add(ParagraphStyle('TableHeadLeft', fontSize=8.5, leading=11,
    textColor=white, fontName='Helvetica-Bold', alignment=TA_LEFT))
styles.add(ParagraphStyle('Footer', fontSize=7.5, leading=10, textColor=MID_GREY,
    fontName='Helvetica-Oblique', alignment=TA_CENTER))
styles.add(ParagraphStyle('NumberedItem', parent=styles['Normal'],
    fontSize=9.5, leading=14, textColor=DARK_GREY,
    leftIndent=18, spaceAfter=6, fontName='Helvetica', alignment=TA_JUSTIFY))
styles.add(ParagraphStyle('FigCaption', parent=styles['Normal'],
    fontSize=8, leading=11, textColor=MID_GREY,
    fontName='Helvetica-Oblique', alignment=TA_CENTER,
    spaceBefore=2, spaceAfter=10))


# ── Helper functions ─────────────────────────────────────
def hr():
    return HRFlowable(width="100%", thickness=0.5, color=LIGHT_GREY, spaceAfter=6, spaceBefore=6)

def chart_img(filename, width_pct=0.95):
    """Insert a chart image scaled to page width."""
    w = CONTENT_W * width_pct
    return Image(f'{CHARTS}/{filename}', width=w, height=w * 0.53,
                 kind='proportional')

def make_table(headers, rows, col_widths=None):
    header_cells = [Paragraph(h, styles['TableHead'] if i > 0 else styles['TableHeadLeft'])
                    for i, h in enumerate(headers)]
    data = [header_cells]
    for row in rows:
        cells = []
        for j, cell in enumerate(row):
            st = styles['TableCell'] if j > 0 else styles['TableCellLeft']
            cells.append(Paragraph(str(cell), st))
        data.append(cells)
    if col_widths is None:
        col_widths = [None] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEAD),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.4, LIGHT_GREY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), TABLE_ALT))
    t.setStyle(TableStyle(style_cmds))
    return t

def add_page_number(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFont('Helvetica', 7.5)
    canvas_obj.setFillColor(MID_GREY)
    canvas_obj.drawCentredString(WIDTH / 2, 15 * mm,
        f"SBLN Traffic Data Analysis  |  Page {doc.page}")
    canvas_obj.restoreState()


# ── Build document ───────────────────────────────────────
import sys
HEADLINE_ONLY = '--headline' in sys.argv
suffix = '_HEADLINE' if HEADLINE_ONLY else '_FULL'
output_path = f"D:/Projects/Bristol/SBLN_Traffic_Data_Analysis_Report{suffix}_v5.pdf"
doc = SimpleDocTemplate(output_path, pagesize=A4,
    leftMargin=22*mm, rightMargin=22*mm,
    topMargin=20*mm, bottomMargin=22*mm)

story = []

# ═══════════════════════════════════════════════════════════
# TITLE PAGE
# ═══════════════════════════════════════════════════════════
story.append(Spacer(1, 40*mm))
story.append(Paragraph(
    "Independent Analysis of the<br/>South Bristol Liveable Neighbourhoods<br/>Traffic Survey Data",
    styles['ReportTitle']))
story.append(Spacer(1, 8*mm))
story.append(HRFlowable(width="60%", thickness=2, color=ACCENT_BLUE, spaceAfter=8))
story.append(Spacer(1, 6*mm))
story.append(Paragraph("Author: Ali Bin Shahid", styles['Subtitle']))
story.append(Paragraph("Volunteer Data Analyst &amp; Systems Engineer", styles['Subtitle']))
story.append(Spacer(1, 3*mm))
story.append(Paragraph("Date: April 2026", styles['Subtitle']))
story.append(Paragraph("Data Source: SBLN 2024 Traffic Survey Results (June 2024)", styles['Subtitle']))
story.append(Paragraph("Survey Contractor: Intelligent Data Collection Ltd (Project ID-0524-0183)", styles['Subtitle']))
story.append(Spacer(1, 20*mm))
story.append(Paragraph(
    "<b>Key Finding:</b> The survey data does not contain evidence sufficient to demonstrate "
    "that vehicles are using Southville's residential streets as a cut-through between "
    "Coronation Road and North Street. The ANPR camera network had no cameras placed within "
    "the Southville zone. The two nearest cameras recorded only <b>10-11 vehicles per day</b> "
    "appearing at both locations, representing approximately <b>0.07-0.14%</b> of the traffic "
    "at those cameras.", styles['KeyFinding']))
story.append(Spacer(1, 30*mm))
story.append(Paragraph(
    "<i>This analysis is based solely on the publicly available traffic survey dataset. "
    "No additional data sources were consulted. All calculations are reproducible from "
    "the original spreadsheets.</i>", styles['Footer']))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# 1. EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("1. Executive Summary", styles['H1']))
story.append(hr())
story.append(Paragraph(
    "This report presents an independent analysis of the 94 spreadsheets contained in the "
    "publicly available \"SBLN Traffic Survey Results 2024\" dataset. The analysis was conducted "
    "to assess whether this data supports or refutes claims that significant volumes of "
    "\"cut-through\" traffic use residential streets in the Southville area.", styles['Body']))
story.append(Paragraph(
    "The survey data does not contain evidence sufficient to demonstrate that vehicles are "
    "using Southville's residential streets as a cut-through between Coronation Road and North "
    "Street. The ANPR (Automatic Number Plate Recognition) camera network, which is the only "
    "survey type capable of tracking vehicle routes, had no cameras placed within the Southville "
    "zone. The two nearest cameras recorded only <b>10-11 vehicles per day</b> appearing at both "
    "locations -- representing approximately <b>0.07-0.14%</b> of the traffic at those cameras.",
    styles['KeyFinding']))

# ═══════════════════════════════════════════════════════════
# 2. DATASET OVERVIEW
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("2. Dataset Overview", styles['H1']))
story.append(hr())
story.append(Paragraph(
    "These surveys were commissioned by Bristol City Council as part of the South Bristol "
    "Liveable Neighbourhoods programme. The survey data comprises five distinct types of traffic "
    "data collection, covering the period from 7-27 June 2024:", styles['Body']))
story.append(make_table(
    ["Survey Type", "Files", "Description"],
    [["ANPR (Origin-Destination)", "6", "Vehicle tracking via number plate recognition across 25 cameras"],
     ["ATC (Automatic Traffic Count)", "22", "Volume and speed counts at 22 locations"],
     ["Bus Stop Boarding/Alighting", "19", "Passenger activity at bus stops"],
     ["Junction Turning Counts", "22", "Vehicle turning movements at 11 junctions"],
     ["Queue Length Surveys", "22", "Queue observations at 11 junctions"],
     ["Manual Classified Counts", "4", "Cycle, scooter, and link counts"]],
    col_widths=[55*mm, 15*mm, 96*mm]))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "The ANPR data was collected on 11-12 June 2024 (06:00-19:00). The ATC data was collected "
    "continuously over approximately three weeks (7-27 June 2024).", styles['Body']))

# ═══════════════════════════════════════════════════════════
# 3. ANPR CAMERA COVERAGE
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("3. ANPR Camera Coverage", styles['H1']))
story.append(hr())

story.append(Paragraph("3.1 Camera Placement", styles['H2']))
story.append(Paragraph(
    "The ANPR survey deployed 25 cameras across South Bristol. Of these, only <b>two</b> cameras "
    "were located on roads bordering the Southville residential area:", styles['Body']))
story.append(Paragraph("<b>Camera 14:</b> Coronation Road (northern boundary of Southville)",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("<b>Camera 16:</b> North Street (southern boundary of Southville)",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "<b>No ANPR cameras were placed on any street within the Southville zone.</b> "
    "Without sensors inside the zone, it is impossible to determine whether a vehicle "
    "detected at both Camera 14 and Camera 16 drove <i>through</i> the residential streets or "
    "travelled <i>around</i> them via perimeter roads.", styles['BodyBold']))

# ── MAP: ANPR camera locations (Matt's map) ─────────────
story.append(Image('D:/Projects/Bristol/maps/ANPR Cameras Map.png',
    width=CONTENT_W * 0.95, height=CONTENT_W * 0.95 * 0.7, kind='proportional'))
story.append(Paragraph("Figure 1: Locations of all 25 ANPR cameras relative to the "
    "Southville Zone and the wider SBLN area perimeter. No ANPR cameras were placed within "
    "the Southville Zone.",
    styles['FigCaption']))

story.append(Paragraph("3.2 Cross-Zone Vehicle Movements", styles['H2']))
story.append(Paragraph(
    "The ANPR Origin-Destination (OD) matrix records the number of vehicles detected at two "
    "different cameras within specified time windows. The following tables show all vehicles "
    "detected at both Camera 14 and Camera 16:", styles['Body']))

story.append(Paragraph("<b>11 June 2024:</b>", styles['Body']))
story.append(make_table(
    ["Direction", "Within 15 min", "Over 15 min", "Total"],
    [["Camera 14 \u2192 Camera 16", "2", "4", "6"],
     ["Camera 16 \u2192 Camera 14", "4", "1", "5"],
     ["Total", "6", "5", "11"]],
    col_widths=[50*mm, 35*mm, 35*mm, 25*mm]))
story.append(Spacer(1, 6))

story.append(Paragraph("<b>12 June 2024:</b>", styles['Body']))
story.append(make_table(
    ["Direction", "Within 15 min", "Over 15 min", "Total"],
    [["Camera 14 \u2192 Camera 16", "1", "4", "5"],
     ["Camera 16 \u2192 Camera 14", "2", "3", "5"],
     ["Total", "3", "7", "10"]],
    col_widths=[50*mm, 35*mm, 35*mm, 25*mm]))
story.append(Spacer(1, 4))

story.append(Paragraph(
    "For context, Camera 14 recorded <b>15,092</b> total vehicle detections on 11 June "
    "(sum of all origin-destination pairs in the OD matrix), and Camera 16 recorded <b>7,642</b>. "
    "The cross-zone detections represent <b>0.07%</b> of Camera 14 traffic "
    "and <b>0.14%</b> of Camera 16 traffic.", styles['Body']))

# ── CHART: Cross-zone in context (pie charts) ──────────
story.append(chart_img('chart2_context.png'))
story.append(Paragraph("Figure 2: Cross-zone detections (red) as a fraction of total traffic at each camera. "
    "The red slices representing cross-zone vehicles are so small they are barely visible.",
    styles['FigCaption']))

story.append(Paragraph("3.3 Trip Chain Analysis", styles['H2']))
story.append(Paragraph(
    "The Trip Chain report traces the full sequence of cameras each matched vehicle passed. "
    "On 11 June, the trip chains show:", styles['Body']))
story.append(Paragraph("<b>15 journeys</b> originating at Camera 14 that also passed Camera 16",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("<b>19 journeys</b> originating at Camera 16 that also passed Camera 14",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Many of these involved extended multi-stop routes (e.g., Camera 14 \u2192 19 \u2192 16 or "
    "Camera 16 \u2192 14 \u2192 01), with travel times ranging from 3.7 minutes to over 38 minutes, "
    "indicating the vehicles were not making simple direct crossings of the area. The majority "
    "of Camera 16 \u2192 Camera 14 trips continued onward to Camera 01 (Clift House Road), consistent "
    "with travel along the perimeter rather than through the zone.", styles['Body']))

story.append(Paragraph("3.4 Where Camera 14 Traffic Actually Goes", styles['H2']))
story.append(Paragraph(
    "Analysis of the OD matrix reveals that the overwhelming majority of vehicles detected at "
    "Camera 14 (Coronation Road) were next detected at Camera 01 (Clift House Road area), "
    "indicating travel <i>along</i> Coronation Road rather than <i>through</i> the Southville zone.",
    styles['Body']))

# ── CHART: Camera 14 destinations ────────────────────────
story.append(chart_img('chart3_cam14_destinations.png'))
story.append(Paragraph("Figure 3: Destination cameras for vehicles detected at Camera 14 (Coronation Road). "
    "Only 2 of 1,028 matched vehicles were next seen at Camera 16 (North Street).",
    styles['FigCaption']))

story.append(Paragraph("3.5 Where Camera 16 Traffic Actually Goes", styles['H2']))
story.append(Paragraph(
    "Conversely, analysis of Camera 16 (North Street) destinations reveals that 45% of matched "
    "vehicles were next detected at Camera 1 (Clift House Road), consistent with travel <i>along "
    "the perimeter</i> via Coronation Road. The remaining traffic disperses to cameras well away "
    "from the Southville Zone. Only 2 vehicles were next seen at Camera 14.",
    styles['Body']))
story.append(chart_img('chart3b_cam16_destinations.png'))
story.append(Paragraph("Figure 4: Destination cameras for vehicles detected at Camera 16 (North Street). "
    "45% were next seen at Camera 1 (Clift House Road), indicating perimeter travel, not cut-through.",
    styles['FigCaption']))

story.append(Paragraph("3.6 Dominant ANPR Traffic Flows", styles['H2']))
# Section numbering: 3.1 Placement, 3.2 Cross-Zone, 3.3 Trip Chain, 3.4 Cam14, 3.5 Cam16, 3.6 Flows, 3.7 Flow Map
story.append(Paragraph(
    "The top ANPR origin-destination flows on 11 June (within 15 minutes) demonstrate that "
    "the Southville cross-zone flow is negligible relative to the actual traffic patterns in "
    "the network:", styles['Body']))

# ── CHART: ANPR flows comparison ─────────────────────────
story.append(chart_img('chart5_flows.png'))
story.append(Paragraph("Figure 5: The Southville cross-zone flow (red) compared to the top network flows. "
    "The 6 cross-zone vehicles are three orders of magnitude smaller than the dominant flows.",
    styles['FigCaption']))

story.append(PageBreak())
story.append(Paragraph("3.7 ANPR Flow Map", styles['H2']))
story.append(Paragraph(
    "The following map visualises the dominant ANPR traffic flows across the survey area. Arrow "
    "thickness is proportional to the number of matched vehicles. The cross-zone flow between "
    "Camera 14 and Camera 16 (red) is so small as to be barely visible against the major corridor "
    "flows (blue). The Southville Zone is shaded for reference.", styles['Body']))
story.append(Image(f'{CHARTS}/chart12_flow_map.png',
    width=CONTENT_W, height=CONTENT_W * 0.78, kind='proportional'))
story.append(Paragraph("Figure 6: ANPR traffic flows on 11 June 2024 (within 15 min). The dominant flows "
    "run along the major road corridors. The cross-zone flow (red, 6 vehicles) is negligible.",
    styles['FigCaption']))

story.append(Paragraph("3.8 Comprehensive Survey Map", styles['H2']))
story.append(Paragraph(
    "The following map combines all survey data layers: all 25 ANPR cameras, all 22 ATC sensors "
    "(with daily traffic volumes for key sites), and the road-routed ANPR flow arrows. This view "
    "makes clear that the entire survey infrastructure surrounds the Southville Zone without "
    "measuring any traffic within it.", styles['Body']))
story.append(PageBreak())
story.append(Image(f'{CHARTS}/chart_analysis_map.png',
    width=CONTENT_W, height=CONTENT_W * 0.78, kind='proportional'))
story.append(Paragraph("Figure 7: Comprehensive analysis map showing all 25 ANPR cameras, 22 ATC sensors "
    "(purple squares with daily volumes), and road-routed ANPR flows. No sensors of any type were "
    "placed within the Southville Zone.",
    styles['FigCaption']))

# ═══════════════════════════════════════════════════════════
# 4. TRAFFIC VOLUMES ON SURROUNDING RESIDENTIAL ROADS
# ═══════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph("4. Traffic Volumes on Nearby Residential Roads", styles['H1']))
story.append(hr())

# ── MAP: ATC sensor locations (Matt's map) ──────────────
story.append(Image('D:/Projects/Bristol/maps/ATC Sensors Map.png',
    width=CONTENT_W * 0.95, height=CONTENT_W * 0.95 * 0.7, kind='proportional'))
story.append(Paragraph("Figure 8: Locations of all ATC (Automatic Traffic Count) sensors relative to the "
    "Southville Zone and the wider SBLN area. No ATC sensors were placed within the Southville Zone.",
    styles['FigCaption']))

story.append(Paragraph(
    "While ANPR could not track routes through Southville, Automatic Traffic Counters (ATC) "
    "were deployed at 22 locations across the wider South Bristol area, providing volume and "
    "speed data. As shown above, <b>no ATC sensors were placed within the Southville Zone</b>, "
    "so no claims can be made about traffic levels on roads inside the zone. "
    "As there is no ATC data available for the Southville Zone, the following analysis relates "
    "to nearby roads outside the zone.", styles['Body']))

story.append(Paragraph("4.1 Daily Traffic Volumes (Tuesday-Thursday Average)", styles['H2']))
story.append(make_table(
    ["Location", "ATC Site", "Daily Volume\n(2-way)", "AM Peak\n(07-09)", "PM Peak\n(16-18)"],
    [["Main Roads", "", "", "", ""],
     ["Winterstoke Road (A3029)", "12", "28,602", "-", "2,161"],
     ["Coronation Road (east)", "8", "23,826", "2,956", "3,318"],
     ["Coronation Road (west)", "9", "18,894", "2,101", "2,593"],
     ["North Street (B3120)", "11", "9,688", "1,363", "1,594"],
     ["Bedminster Parade (A38)", "7", "9,424", "-", "615"],
     ["Residential Roads (outside zone)", "", "", "", ""],
     ["Luckwell Road (W\u2194E)", "10", "6,425", "1,074", "1,119"],
     ["Luckwell Road (S\u2194N)", "15", "5,405", "763", "944"],
     ["Palmyra Road", "14", "1,958", "426", "349"]],
    col_widths=[48*mm, 20*mm, 30*mm, 28*mm, 28*mm]))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Luckwell Road carries <b>6,425 vehicles per day</b>, which is 66% of North Street's volume "
    "(9,688/day). This is a notable volume for a residential street. However, the ATC data cannot "
    "distinguish between local residents, visitors, deliveries, and potential cut-through traffic.",
    styles['Body']))

# ── CHART: Volume comparison ─────────────────────────────
story.append(chart_img('chart1_volumes.png'))
story.append(Paragraph("Figure 9: Daily traffic volumes on nearby residential roads (blue) "
    "compared to main roads (grey). Tuesday-Thursday average.",
    styles['FigCaption']))

story.append(Paragraph("4.2 Hourly Traffic Profiles", styles['H2']))
story.append(Paragraph(
    "The hourly traffic profile of Luckwell Road follows a typical commuter pattern with "
    "AM and PM peaks, broadly mirroring the shape of Coronation Road's profile at a smaller scale. "
    "This pattern is consistent with both residential access and potential commuter usage, "
    "but does not by itself indicate cut-through behaviour.", styles['Body']))

# ── CHART: Hourly profile ────────────────────────────────
story.append(chart_img('chart6_hourly.png'))
story.append(Paragraph("Figure 10: Hourly traffic profile comparison. Luckwell Road's commuter-style "
    "peaks mirror Coronation Road's pattern at approximately 27% of the volume.",
    styles['FigCaption']))

story.append(Paragraph("4.3 Weekday vs Weekend Traffic Patterns", styles['H2']))
story.append(Paragraph(
    "The ATC data spans three weeks (7-26 June 2024), enabling comparison between weekday and "
    "weekend volumes. All three residential road sites show lower traffic on weekends:", styles['Body']))
story.append(make_table(
    ["Location", "Weekday Avg", "Weekend Avg", "Difference"],
    [["Luckwell Road (W\u2194E)", "6,252", "5,253", "\u221216%"],
     ["Luckwell Road (S\u2194N)", "5,377", "4,916", "\u22129%"],
     ["Palmyra Road", "1,847", "1,448", "\u221222%"]],
    col_widths=[42*mm, 30*mm, 30*mm, 30*mm]))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "The consistent weekend reduction across all sites is characteristic of residential and "
    "commuter traffic patterns. Palmyra Road shows the steepest weekend drop (\u221222%), while "
    "Luckwell Road (S\u2194N) shows the smallest (\u22129%), suggesting the latter also serves "
    "shopping and leisure traffic along North Street.", styles['Body']))

story.append(chart_img('chart10_weekly.png'))
story.append(Paragraph("Figure 11: Three-week daily traffic profile. Weekend dips (orange shading) are "
    "consistent across all sites. Sunday volumes are the lowest throughout.",
    styles['FigCaption']))

story.append(chart_img('chart11_weekday_weekend.png'))
story.append(Paragraph("Figure 12: Weekday vs weekend averages. Percentage drops are consistent with "
    "residential commuter patterns rather than through-traffic, which would show less weekend variation.",
    styles['FigCaption']))

story.append(Paragraph("4.4 Directional Analysis", styles['H2']))
story.append(Paragraph(
    "Luckwell Road (Site 10) shows a directional imbalance: approximately 2,716 vehicles travel "
    "westbound versus 3,709 eastbound on average. A strong directional imbalance could theoretically "
    "suggest commuter cut-through patterns, though it could equally reflect the asymmetric geography "
    "of the local road network and the locations of amenities, schools, and parking.", styles['Body']))

story.append(Paragraph("4.5 Junction Turning Movements", styles['H2']))
story.append(Paragraph(
    "Junction Turning Count (JTC) surveys were conducted at 11 junctions across the SBLN area. "
    "As with the other survey types, no JTC monitors were placed within the Southville Zone, and "
    "only two were on its perimeter roads. We examine these two junctions below.", styles['Body']))

# ── JTC Surveys Map (Matt's map) ────────────────────────
story.append(Image('D:/Projects/Bristol/maps/JTC Surveys Map.png',
    width=CONTENT_W * 0.85, height=CONTENT_W * 0.85 * 0.7, kind='proportional'))
story.append(Paragraph("Figure 13: Locations of all JTC (Junction Turning Count) survey sites. Only Sites 6 "
    "and 11 are on the perimeter of the Southville Zone.",
    styles['FigCaption']))

story.append(Paragraph(
    "<b>Site 6 (Dean Lane / Cannon Street / North Street):</b> This 3-arm roundabout sits on "
    "North Street approximately 200m east of Luckwell Road. North Street and Dean Lane both "
    "form part of the perimeter of the Southville Zone, but none of the three roads at this "
    "junction actually enters it. This data therefore demonstrates vehicles using the perimeter "
    "roads, consistent with the council's desire for traffic to remain on boundary roads.",
    styles['Body']))

story.append(Image('D:/Projects/Bristol/maps/JTC 6.png',
    width=CONTENT_W * 0.4, height=CONTENT_W * 0.4, kind='proportional'))
story.append(Paragraph("Site 6: Dean Lane / Cannon St / North St roundabout.",
    styles['FigCaption']))

story.append(Paragraph(
    "Cannon Street is a major feeder from the south (~6,700 approaches/day), with traffic "
    "dispersing primarily into Dean Lane (~3,844) and westbound on North Street (~2,700). "
    "The tidal pattern (strong northbound AM, southbound PM) is consistent with residential "
    "commuter behaviour.", styles['Body']))

story.append(Paragraph(
    "<b>Site 11 (Raleigh Road / North Street):</b> This crossroads is at the western end of "
    "the Southville Zone. Unlike Site 6, the north-east-bound stretch of Raleigh Road does "
    "enter the Southville Zone, making this a potential entry point for through-traffic.",
    styles['Body']))

story.append(Image('D:/Projects/Bristol/maps/JTC 11.png',
    width=CONTENT_W * 0.4, height=CONTENT_W * 0.4, kind='proportional'))
story.append(Paragraph("Site 11: Raleigh Rd / North St crossroads.",
    styles['FigCaption']))

story.append(Paragraph(
    "North Street through-traffic dominates at ~3,400 vehicles in each direction over 12 hours. "
    "Approximately 880 vehicles/day turn between North Street and Raleigh Road, representing "
    "less than 10% of the junction's total 10,361 movements. While 880 vehicles entering the "
    "Southville Zone is a notable number, there is no way of determining how many of these are "
    "genuine through-traffic versus vehicles travelling to local destinations within the zone, "
    "due to the absence of any monitoring within the zone itself.", styles['Body']))

story.append(chart_img('chart13_jtc.png'))
story.append(Paragraph("Figure 14: Junction turning movements at two North Street junctions. Through-traffic "
    "on North Street dominates; turns onto residential streets are secondary flows.",
    styles['FigCaption']))

story.append(Paragraph("4.6 Speed Data on Residential Roads", styles['H2']))
story.append(make_table(
    ["Location", "Speed Limit", "Mean Speed", "85th Percentile", "Exceeding Limit"],
    [["Luckwell Road (W\u2194E)", "30 mph", "20.7 mph", "~22 mph", "1.8%"],
     ["Palmyra Road", "20 mph", "17.1 mph", "~22 mph", "21.4%"],
     ["Luckwell Road (S\u2194N)", "30 mph", "16.6 mph", "~22 mph", "0.4%"]],
    col_widths=[42*mm, 25*mm, 25*mm, 30*mm, 30*mm]))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Speeds on these nearby residential roads are generally well below posted limits, which is "
    "inconsistent with a pattern of vehicles using these roads as high-speed cut-throughs. Palmyra "
    "Road has a 20 mph limit and shows 21.4% of vehicles exceeding it, though the mean speed "
    "remains at 17.1 mph. As with all other data in this section, no speed data is available for "
    "roads within the Southville Zone itself.", styles['Body']))

# ── CHART: Speed distributions ───────────────────────────
story.append(chart_img('chart4_speeds.png', width_pct=1.0))
story.append(Paragraph("Figure 15: Speed distribution on nearby residential roads. "
    "Blue bars show vehicles within the speed limit; red bars show those exceeding it.",
    styles['FigCaption']))

# ═══════════════════════════════════════════════════════════
# 5. METHODOLOGICAL LIMITATIONS
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("5. Methodological Limitations", styles['H1']))
story.append(hr())

story.append(Paragraph("5.1 The Cut-Through Evidence Gap", styles['H2']))
story.append(Paragraph(
    "To demonstrate that vehicles are using residential streets as a \"cut-through,\" a survey "
    "would need to show that a vehicle:", styles['Body']))
story.append(Paragraph("<b>Enters</b> the area from one side (e.g., Coronation Road)",
    styles['BulletCustom'], bulletText='1.'))
story.append(Paragraph("<b>Travels through</b> the residential streets",
    styles['BulletCustom'], bulletText='2.'))
story.append(Paragraph("<b>Exits</b> from the other side (e.g., North Street)",
    styles['BulletCustom'], bulletText='3.'))
story.append(Paragraph("<b>Does not stop</b> at a destination within the area",
    styles['BulletCustom'], bulletText='4.'))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Requirements 1 and 3 could be captured by perimeter ANPR cameras (which exist). Requirements "
    "2 and 4 require <b>ANPR cameras within the Southville Zone</b> (which do not exist in this "
    "dataset). Without cameras inside the zone, a vehicle detected at both Camera 14 and Camera "
    "16 may have:", styles['Body']))
story.append(Paragraph("Driven along Coronation Road westward, then south on a perimeter road to North Street",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("Stopped at a destination within Southville (making it local traffic, not cut-through)",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("Taken any number of routes that do not constitute a \"cut-through\"",
    styles['BulletCustom'], bulletText='\u2022'))

story.append(Paragraph("5.2 Volume Data is Not Route Data", styles['H2']))
story.append(Paragraph(
    "The ATC counters on Luckwell Road and Palmyra Road show that vehicles <i>use</i> these streets, "
    "but cannot determine <i>why</i>. Possible explanations for the observed volumes include:",
    styles['Body']))
story.append(Paragraph("Residents of the area driving to/from their homes",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("Visitors to local businesses, pubs, shops, and services",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("Deliveries and servicing",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("School-related trips",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("Genuine cut-through traffic",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Without ANPR or equivalent tracking on these roads, it is not possible to determine "
    "what proportion of the 6,425 daily vehicles on Luckwell Road (for example) represent "
    "cut-through traffic. Furthermore, no ATC volume data exists for any road within the "
    "Southville Zone itself, so no traffic volume claims can be made about those streets.",
    styles['Body']))

story.append(Paragraph("5.3 Sample Size", styles['H2']))
story.append(Paragraph(
    "The ANPR data covers only two days (11-12 June 2024, a Tuesday and Wednesday). While the ATC "
    "data covers approximately three weeks, providing more robust volume estimates, the critical "
    "origin-destination data relies on just two days of observation.", styles['Body']))

story.append(Paragraph("5.4 Camera Position Discrepancy", styles['H2']))
story.append(Paragraph(
    "The council's published ArcGIS map of camera locations does not fully agree with the survey "
    "contractor's spreadsheet regarding the position of the North Street ANPR camera (Camera 16). "
    "One source places it near the junction with Luckwell Road; the other indicates a position "
    "slightly further east, near Upper Sydney Street. While this is a minor discrepancy, it "
    "introduces additional uncertainty into any analysis that depends on Camera 16's precise "
    "location relative to the Southville Zone boundary.", styles['Body']))

story.append(Paragraph("5.5 Subsequent 2025 Surveys", styles['H2']))
story.append(Paragraph(
    "Additional traffic surveys were carried out in November/December 2025 with a significantly "
    "larger number of sensors placed within the Southville Zone. However, these appear to consist "
    "of ATC and JTC (junction turning count) sensors only \u2014 not ANPR cameras. While the "
    "results have not yet been published at the time of writing, the absence of ANPR within the "
    "zone means that even the 2025 surveys cannot track vehicle routes or demonstrate cut-through "
    "behaviour. <b>Volume data remains fundamentally different from route data</b>, regardless of "
    "how many volume sensors are deployed.", styles['Body']))

# ═══════════════════════════════════════════════════════════
# 6. RESIDENTIAL TRIP GENERATION ANALYSIS (full version only)
# ═══════════════════════════════════════════════════════════
SEC_OFFSET = 0  # section number offset for headline version
if HEADLINE_ONLY:
    SEC_OFFSET = -1  # skip section 6, so 7->6, 8->7

if not HEADLINE_ONLY:
    story.append(PageBreak())
    story.append(Paragraph("6. Residential Trip Generation Analysis", styles['H1']))
    story.append(hr())
    story.append(Paragraph(
        "To test whether the observed traffic volumes on surrounding residential roads can be "
        "explained by local residential demand alone, a trip generation model was constructed using "
        "Census 2021 population data and standard UK trip generation rates from the TRICS database.",
        styles['Body']))

    story.append(Paragraph("6.1 Local Demographics (Census 2021)", styles['H2']))
    story.append(Paragraph(
        "Luckwell Road straddles the boundary between Southville Ward and Bedminster Ward. The "
        "analysis therefore draws on data from <b>both wards</b> to ensure accuracy. Both wards "
        "have similar demographics and household characteristics.", styles['Body']))
    story.append(make_table(
        ["Metric", "Southville Ward", "Bedminster Ward", "Combined"],
        [["Population", "12,882", "12,916", "25,798"],
         ["Total households", "5,774", "5,780", "11,554"],
         ["Avg household size", "2.2", "2.2", "2.2"],
         ["Home ownership", "48.6%", "60.2%", "~54%"],
         ["Private rented", "34.8%", "27.1%", "~31%"],
         ["Households with no car*", "32.2%", "~28% (est.)", "~30%"],
         ["Car-owning households*", "67.8%", "~72% (est.)", "~70%"]],
        col_widths=[38*mm, 35*mm, 35*mm, 35*mm]))
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "<i>* Bedminster Ward car ownership estimated from tenure profile and Bristol averages. "
        "Higher home ownership typically correlates with higher car ownership.</i>",
        styles['Footer']))
    story.append(Spacer(1, 4))

    story.append(chart_img('chart8_car_ownership.png'))
    story.append(Paragraph("Figure 16: Combined ward car ownership estimate (left) and the household "
        "funnel from combined ward total to the estimated Luckwell Road catchment (right).",
        styles['FigCaption']))

    story.append(Paragraph("6.2 Luckwell Road Catchment Area", styles['H2']))
    story.append(Paragraph(
        "Luckwell Road serves as a primary access route for a significant number of residential "
        "streets in the area south of the Southville Zone. The catchment includes Luckwell Road "
        "itself (~201 properties) plus all streets that feed into it: Aubrey Road, Stackpool Road, "
        "Merrywood Road, Palmyra Road, Greenway Bush Lane, and numerous side streets. Luckwell "
        "Primary School is located 300 metres from the road, generating parent traffic.", styles['Body']))
    story.append(Paragraph(
        "The estimated catchment is approximately <b>1,800 dwellings</b>. Applying the combined "
        "ward car ownership rate of ~70%, approximately <b>1,260</b> are car-owning households.",
        styles['Body']))

    story.append(Paragraph("6.3 Trip Generation Model", styles['H2']))
    story.append(Paragraph(
        "Using the UK standard TRICS (Trip Rate Information Computer System) database, typical "
        "residential trip generation rates for urban, mixed-tenure housing are approximately "
        "<b>5.0-5.7 vehicle trips per dwelling per day</b> over a 12-hour weekday period. Applying "
        "these rates to the estimated catchment, and assuming 70% of generated trips route via "
        "Luckwell Road:", styles['Body']))
    story.append(make_table(
        ["Scenario", "Trip Rate", "Total Generated", "Via Luckwell Rd (70%)"],
        [["Conservative", "4.0/dwelling/day", "5,040", "3,480"],
         ["Mid-range", "5.0/dwelling/day", "6,300", "4,350"],
         ["Standard TRICS", "5.7/dwelling/day", "7,182", "4,980"],
         ["High estimate", "6.5/dwelling/day", "8,190", "5,655"]],
        col_widths=[35*mm, 38*mm, 38*mm, 42*mm]))
    story.append(Spacer(1, 4))

    story.append(chart_img('chart7_trip_generation.png'))
    story.append(Paragraph("Figure 17: Residential trip generation estimates compared to observed "
        "Luckwell Road traffic (red dashed line at 6,425 vehicles/day). Even mid-range estimates, "
        "combined with schools, deliveries, and visitors, approach or exceed the observed volume.",
        styles['FigCaption']))

    story.append(Paragraph("6.4 Accounting for Remaining Traffic", styles['H2']))
    story.append(Paragraph(
        "The mid-range residential estimate of ~4,350 vehicles/day accounts for 68% of the observed "
        "6,425. The remaining ~2,075 vehicles can be attributed to non-residential local sources:",
        styles['Body']))
    story.append(Paragraph("<b>Luckwell Primary School:</b> parent drop-off/pick-up generates an estimated 300-500 vehicle movements/day",
        styles['BulletCustom'], bulletText='\u2022'))
    story.append(Paragraph("<b>North Street businesses:</b> shops, pubs, cafes, and services generate customer traffic routed via Luckwell Road",
        styles['BulletCustom'], bulletText='\u2022'))
    story.append(Paragraph("<b>Deliveries and services:</b> Royal Mail, couriers, tradespeople, waste collection",
        styles['BulletCustom'], bulletText='\u2022'))
    story.append(Paragraph("<b>Visitors:</b> friends, family, healthcare workers visiting residents",
        styles['BulletCustom'], bulletText='\u2022'))
    story.append(Spacer(1, 4))

    story.append(chart_img('chart9_waterfall.png'))
    story.append(Paragraph("Figure 18: Estimated breakdown of Luckwell Road traffic by source. "
        "Local demand and identifiable services can plausibly account for 94% or more of the "
        "observed volume. The remaining gap (~6%) falls within estimation uncertainty.",
        styles['FigCaption']))

    story.append(Paragraph(
        "This analysis demonstrates that <b>the observed traffic on Luckwell Road is broadly "
        "consistent with what would be expected from local residential demand and associated "
        "services alone</b>. There is no statistical need to invoke \"cut-through\" traffic to "
        "explain the volumes observed.",
        styles['KeyFinding']))

# ═══════════════════════════════════════════════════════════
# 7. WHAT THE DATA DOES AND DOES NOT SUPPORT
# ═══════════════════════════════════════════════════════════
story.append(Paragraph(f"{7 + SEC_OFFSET}. What the Data Does and Does Not Support", styles['H1']))
story.append(hr())

story.append(Paragraph(f"{7 + SEC_OFFSET}.1 Statements Supported by the Data", styles['H2']))
story.append(Paragraph("Coronation Road and Winterstoke Road carry significant traffic volumes (19,000-29,000 vehicles/day)",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("North Street carries approximately 9,700 vehicles/day",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("Luckwell Road carries approximately 6,400 vehicles/day, a notable volume for a residential street",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("Speeds on surrounding residential roads are generally moderate (mean 17-21 mph)",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("The vast majority of vehicles at Camera 14 (Coronation Road) travelled along the Coronation Road corridor, not through Southville",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("On both survey days, approximately <b>10-11 vehicles</b> were detected at both Camera 14 and Camera 16",
    styles['BulletCustom'], bulletText='\u2022'))

story.append(Paragraph(f"{7 + SEC_OFFSET}.2 Statements NOT Supported by the Data", styles['H2']))
story.append(Paragraph("That \"high numbers of vehicles from outside the area use residential streets as a cut-through\"",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("That any specific number or proportion of vehicles on residential roads are cut-through traffic",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("That vehicles detected at both Camera 14 and Camera 16 drove through Southville rather than around it",
    styles['BulletCustom'], bulletText='\u2022'))
story.append(Paragraph("That the traffic volumes on nearby residential roads are primarily caused by non-local drivers",
    styles['BulletCustom'], bulletText='\u2022'))

# ═══════════════════════════════════════════════════════════
# 8. CONCLUSIONS
# ═══════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph(f"{8 + SEC_OFFSET}. Conclusions", styles['H1']))
story.append(hr())

conclusions = [
    "<b>The ANPR data does not demonstrate the existence of significant cut-through traffic "
    "in Southville.</b> The 10-11 vehicles per day detected at both boundary cameras represent "
    "a negligible fraction of traffic (0.07-0.14%), and even these cannot be confirmed as having "
    "driven through the residential area.",

    "<b>There are meaningful traffic volumes on nearby residential roads</b>, particularly "
    "Luckwell Road (~6,400/day). However, the data does not indicate what proportion of this "
    "traffic is local versus non-local, or whether any of it constitutes cut-through behaviour.",

    "<b>The survey methodology is not designed to answer the cut-through question.</b> Proving "
    "or disproving cut-through traffic would require ANPR cameras within the Southville Zone, "
    "which were not part of either the 2024 or the 2025 surveys. The absence of evidence is not "
    "necessarily evidence of absence, but claims of cut-through cannot be substantiated from "
    "this dataset.",

    "<b>The dominant traffic patterns</b> revealed by the ANPR data show vehicles moving along "
    "the major road corridors (Coronation Road, North Street, Winterstoke Road) rather than "
    "between them through residential streets.",

    "<b>Speed compliance</b> on nearby residential roads is generally good, with mean "
    "speeds well below posted limits, which does not support a characterisation of aggressive "
    "or opportunistic cut-through driving behaviour.",
]
if not HEADLINE_ONLY:
    conclusions.append(
        "<b>Residential trip generation modelling</b> using Census 2021 household data from "
        "both Bedminster and Southville wards, combined with standard UK TRICS rates, demonstrates "
        "that local residential demand, school traffic, deliveries, and commercial visitors can "
        "plausibly account for the observed volumes on nearby residential roads without "
        "invoking any cut-through traffic."
    )

for i, c in enumerate(conclusions, 1):
    story.append(Paragraph(f"{i}. {c}", styles['NumberedItem']))
    story.append(Spacer(1, 4))

story.append(Spacer(1, 12))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_BLUE, spaceAfter=8))
if HEADLINE_ONLY:
    story.append(Paragraph(
        "<i>This analysis is based on the publicly available \"SBLN Traffic Survey Results 2024\" dataset. "
        "All calculations are reproducible from the original data sources.<br/>"
        "Analysis code: github.com/R3GENESI5/bristol-southville-traffic-analysis</i>", styles['Footer']))
else:
    story.append(Paragraph(
        "<i>This analysis is based on the publicly available \"SBLN Traffic Survey Results 2024\" dataset "
        "and Census 2021 ward-level data from the Office for National Statistics. Trip generation rates "
        "are derived from published TRICS research. All calculations are reproducible from the original "
        "data sources.<br/>Analysis code: github.com/R3GENESI5/bristol-southville-traffic-analysis</i>", styles['Footer']))

# ── Build ────────────────────────────────────────────────
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(f"PDF generated: {output_path}")

"""Generate Executive Summary PDF report for Bristol City Council / WECA."""

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

# -- Colours (same as main report) ----------------------------
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

# -- Styles (same as main report) -----------------------------
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


# -- Helper functions -----------------------------------------
def hr():
    return HRFlowable(width="100%", thickness=0.5, color=LIGHT_GREY, spaceAfter=6, spaceBefore=6)

def chart_img(filename, width_pct=0.95):
    """Insert a chart image scaled to page width."""
    w = CONTENT_W * width_pct
    return Image(f'{CHARTS}/{filename}', width=w, height=w * 0.53,
                 kind='proportional')

def full_page_img(filename):
    """Insert a chart image at maximum page size."""
    max_w = CONTENT_W
    max_h = HEIGHT - 60*mm  # top + bottom margins + title space
    return Image(f'{CHARTS}/{filename}', width=max_w, height=max_h,
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
        f"SBLN Executive Summary  |  Page {doc.page}")
    canvas_obj.restoreState()


# -- Build document -------------------------------------------
output_path = "D:/Projects/Bristol/SBLN_Executive_Report.pdf"
doc = SimpleDocTemplate(output_path, pagesize=A4,
    leftMargin=22*mm, rightMargin=22*mm,
    topMargin=20*mm, bottomMargin=22*mm)

story = []

# =============================================================
# PAGE 1 -- TITLE PAGE
# =============================================================
story.append(Spacer(1, 40*mm))
story.append(Paragraph(
    "Independent Analysis of the<br/>SBLN 2024 Traffic Survey Data",
    styles['ReportTitle']))
story.append(Spacer(1, 4*mm))
story.append(Paragraph("Executive Summary Report", ParagraphStyle(
    'SubTitle2', parent=styles['ReportTitle'],
    fontSize=14, leading=18, textColor=MID_BLUE, fontName='Helvetica')))
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


# =============================================================
# PAGE 2 -- EXECUTIVE SUMMARY
# =============================================================
story.append(Paragraph("1. Executive Summary", styles['H1']))
story.append(hr())

bullets = [
    "The SBLN 2024 Traffic Survey dataset comprises <b>94 spreadsheets</b> across six survey "
    "types, commissioned by Bristol City Council and conducted in June 2024.",

    "The ANPR origin-destination data -- the only survey type capable of tracking vehicle "
    "routes -- shows that just <b>10-11 vehicles per day</b> were detected at both Camera 14 "
    "(Coronation Road) and Camera 16 (North Street), the two cameras nearest to the Southville zone.",

    "This cross-zone figure represents <b>0.07-0.14%</b> of total traffic at those cameras. "
    "Even these vehicles cannot be confirmed as having driven through the zone, as they may "
    "have used perimeter roads.",

    "Over <b>90% of Camera 14 traffic</b> travelled to Camera 1 (Clift House Road), indicating "
    "movement along the Coronation Road corridor rather than through residential streets.",

    "Automatic Traffic Counter (ATC) speed data from nearby residential roads shows mean speeds "
    "of 16.6-20.7 mph in 20-30 mph zones, with speed limit exceedance rates between "
    "<b>0.4% and 21.4%</b> depending on the site.",
]

for b in bullets:
    story.append(Paragraph(b, styles['BulletCustom'], bulletText='\u2022'))
    story.append(Spacer(1, 2*mm))

story.append(PageBreak())


# =============================================================
# PAGE 3 -- SURVEY OVERVIEW
# =============================================================
story.append(Paragraph("2. Survey Overview", styles['H1']))
story.append(hr())
story.append(Paragraph(
    "The SBLN 2024 Traffic Survey was commissioned by Bristol City Council as part of the "
    "South Bristol Liveable Neighbourhoods programme. The survey was conducted by Intelligent "
    "Data Collection Ltd (Project ID-0524-0183) during June 2024.", styles['Body']))
story.append(Paragraph(
    "The dataset comprises <b>94 spreadsheets</b> across six distinct survey types:",
    styles['Body']))
story.append(Spacer(1, 3*mm))

survey_table = make_table(
    ['Survey Type', 'Files', 'Period', 'Coverage'],
    [
        ['ANPR (Origin-Destination)', '6', '11-12 June 2024', '25 cameras across South Bristol'],
        ['ATC (Automatic Traffic Count)', '22', '7-27 June 2024', '22 locations, volume + speed'],
        ['Junction Turning Counts', '22', '11-12 June 2024', '11 junctions'],
        ['Bus Stop Boarding/Alighting', '19', '11-12 June 2024', 'Bus passenger counts'],
        ['Queue Length Surveys', '22', '11-12 June 2024', '11 junctions'],
        ['Manual Classified Counts', '4', '8-21 June 2024', 'Vehicle classification + cycles'],
    ],
    col_widths=[55*mm, 15*mm, 35*mm, 55*mm]
)
story.append(survey_table)
story.append(Spacer(1, 6*mm))

story.append(Paragraph(
    "<b>Note:</b> None of the 25 ANPR cameras were located within the Southville residential zone. "
    "Cameras 14 (Coronation Road) and 16 (North Street) are the nearest, positioned on the zone's "
    "perimeter roads. Without cameras inside the zone, it is not possible to determine from this "
    "data whether any vehicle travelled through the residential streets.", styles['Body']))

story.append(Spacer(1, 4*mm))
story.append(Paragraph(
    "<b>Note:</b> None of the 22 ATC sites were located within the Southville residential zone either. "
    "The nearest ATC sites monitor perimeter and arterial roads.", styles['Body']))

story.append(PageBreak())


# =============================================================
# PAGE 4 -- ANPR FINDINGS
# =============================================================
story.append(Paragraph("3. ANPR Findings", styles['H1']))
story.append(hr())

story.append(Paragraph("3.1 Camera Placement", styles['H2']))
story.append(Paragraph(
    "The ANPR survey deployed 25 cameras across South Bristol. Cameras 14 and 16 are the only "
    "cameras adjacent to the Southville zone. No ANPR cameras were placed within the zone itself. "
    "This means the data can show vehicles arriving at the zone boundary but cannot confirm whether "
    "they entered or traversed residential streets.", styles['Body']))

# Matt's ANPR map showing SBLN perimeter + Southville Zone
story.append(Image('D:/Projects/Bristol/maps/ANPR Cameras Map.png',
    width=CONTENT_W * 0.95, height=CONTENT_W * 0.95 * 0.7, kind='proportional'))
story.append(Paragraph("Locations of all 25 ANPR cameras relative to the Southville Zone "
    "and the SBLN area perimeter. No cameras were placed within the Southville Zone.",
    styles['FigCaption']))

story.append(Paragraph("3.2 Cross-Zone Detections", styles['H2']))
story.append(Paragraph(
    "Vehicles detected at both Camera 14 (Coronation Road) and Camera 16 (North Street):",
    styles['Body']))
story.append(Spacer(1, 2*mm))

cross_table_1 = make_table(
    ['Date', '14\u219216 (<15m)', '14\u219216 (>15m)', '16\u219214 (<15m)', '16\u219214 (>15m)', 'Total'],
    [
        ['11 June 2024', '2', '4', '4', '1', '11'],
        ['12 June 2024', '1', '4', '2', '3', '10'],
    ],
    col_widths=[28*mm, 26*mm, 26*mm, 26*mm, 26*mm, 18*mm]
)
story.append(cross_table_1)
story.append(Spacer(1, 4*mm))

story.append(Paragraph("3.3 Context", styles['H2']))
story.append(Paragraph(
    "On 11 June 2024, Camera 14 recorded 15,092 total detections and Camera 16 recorded 7,642. "
    "The 10-11 cross-zone vehicles represent <b>0.07%</b> of Camera 14 traffic and <b>0.14%</b> "
    "of Camera 16 traffic.", styles['Body']))
story.append(Spacer(1, 2*mm))

story.append(chart_img('chart2_context.png', 0.85))
story.append(Paragraph(
    "Figure 1: Cross-zone detections in context of total camera traffic",
    styles['FigCaption']))

story.append(PageBreak())


# =============================================================
# PAGE 5 -- WHERE TRAFFIC ACTUALLY GOES
# =============================================================
story.append(Paragraph("4. Where Traffic Actually Goes", styles['H1']))
story.append(hr())

story.append(Paragraph(
    "The ANPR data reveals where vehicles detected at Cameras 14 and 16 actually travelled. "
    "The dominant pattern is travel along perimeter corridors, not through residential streets.",
    styles['Body']))

story.append(Paragraph("4.1 Camera 14 Destinations (within 15 minutes)", styles['H2']))
story.append(Paragraph(
    "Over 90% of vehicles detected at Camera 14 (Coronation Road) next appeared at Camera 1 "
    "(Clift House Road), indicating travel along the Coronation Road corridor.",
    styles['Body']))
story.append(chart_img('chart3_cam14_destinations.png', 0.85))
story.append(Paragraph(
    "Figure 2: Camera 14 -- next camera detected within 15 minutes",
    styles['FigCaption']))

story.append(Spacer(1, 4*mm))

story.append(Paragraph("4.2 Camera 16 Destinations (within 15 minutes)", styles['H2']))
story.append(Paragraph(
    "45% of Camera 16 (North Street) traffic also went to Camera 1, consistent with perimeter "
    "travel. Only 4 vehicles (of 7,642) were next detected at Camera 14.",
    styles['Body']))
story.append(chart_img('chart3b_cam16_destinations.png', 0.85))
story.append(Paragraph(
    "Figure 3: Camera 16 -- next camera detected within 15 minutes",
    styles['FigCaption']))

story.append(PageBreak())


# =============================================================
# PAGE 6 -- FLOW MAP (FULL PAGE)
# =============================================================
story.append(Paragraph("5. Vehicle Flow Map", styles['H1']))
story.append(hr())
story.append(Paragraph(
    "The flow map below illustrates the origin-destination patterns from the ANPR data. "
    "Line thickness is proportional to the number of vehicles detected travelling between "
    "each camera pair within 15 minutes.", styles['Body']))
story.append(Spacer(1, 4*mm))
story.append(full_page_img('chart12_flow_map.png'))
story.append(Paragraph(
    "Figure 4: ANPR vehicle flow map -- line thickness proportional to vehicle count",
    styles['FigCaption']))

story.append(PageBreak())


# =============================================================
# PAGE 7 -- ATC DATA SUMMARY
# =============================================================
story.append(Paragraph("6. ATC Data Summary", styles['H1']))
story.append(hr())

story.append(Paragraph("6.1 Daily Traffic Volumes (Key Sites)", styles['H2']))
story.append(Paragraph(
    "Automatic Traffic Counters recorded continuous volume and speed data at 22 sites across "
    "South Bristol from 7-27 June 2024. Key sites near the Southville zone:",
    styles['Body']))
story.append(Spacer(1, 2*mm))

vol_table = make_table(
    ['Site', 'Road', 'Daily Volume', 'AM Peak', 'PM Peak'],
    [
        ['12', 'Winterstoke Rd (A3029)', '28,602', '-', '2,161'],
        ['8', 'Coronation Rd (east)', '23,826', '2,956', '3,318'],
        ['9', 'Coronation Rd (west)', '18,894', '2,101', '2,593'],
        ['11', 'North St (B3120)', '9,688', '1,363', '1,594'],
        ['7', 'Bedminster Parade (A38)', '9,424', '-', '615'],
        ['10', 'Luckwell Rd (W-E)', '6,425', '1,074', '1,119'],
        ['15', 'Luckwell Rd (S-N)', '5,405', '763', '944'],
        ['14', 'Palmyra Rd', '1,958', '426', '349'],
    ],
    col_widths=[14*mm, 40*mm, 28*mm, 22*mm, 22*mm]
)
story.append(vol_table)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("6.2 Speed Compliance", styles['H2']))
story.append(Paragraph(
    "Speed data from residential roads near the zone shows generally low speeds and high "
    "compliance with posted limits:", styles['Body']))
story.append(Spacer(1, 2*mm))

speed_table = make_table(
    ['Road', 'Limit', 'Mean Speed', '85th Percentile', 'Exceeding'],
    [
        ['Luckwell Rd (W-E)', '30 mph', '20.7 mph', '~22 mph', '1.8%'],
        ['Palmyra Rd', '20 mph', '17.1 mph', '~22 mph', '21.4%'],
        ['Luckwell Rd (S-N)', '30 mph', '16.6 mph', '~22 mph', '0.4%'],
    ],
    col_widths=[35*mm, 18*mm, 25*mm, 30*mm, 22*mm]
)
story.append(speed_table)
story.append(Spacer(1, 6*mm))

story.append(Paragraph("6.3 Weekend Variation", styles['H2']))
story.append(Paragraph(
    "Traffic volumes on residential roads drop at weekends, consistent with commuter and "
    "school-run patterns rather than persistent cut-through:", styles['Body']))
story.append(Spacer(1, 2*mm))

weekend_table = make_table(
    ['Road', 'Weekend Drop'],
    [
        ['Luckwell Rd (W-E)', '-16%'],
        ['Luckwell Rd (S-N)', '-9%'],
        ['Palmyra Rd', '-22%'],
    ],
    col_widths=[55*mm, 30*mm]
)
story.append(weekend_table)

story.append(PageBreak())


# =============================================================
# PAGE 8 -- ALL SURVEY SENSORS MAP (FULL PAGE)
# =============================================================
story.append(Paragraph("7. All Survey Sensor Locations", styles['H1']))
story.append(hr())
story.append(Paragraph(
    "The maps below show the locations of all survey sensors deployed during the June 2024 "
    "data collection period, relative to both the Southville Zone and the wider SBLN perimeter. "
    "No sensors of any type were placed within the Southville Zone.", styles['Body']))

# Matt's ATC map showing SBLN perimeter
story.append(Image('D:/Projects/Bristol/maps/ATC Sensors Map.png',
    width=CONTENT_W * 0.85, height=CONTENT_W * 0.85 * 0.7, kind='proportional'))
story.append(Paragraph("ATC sensor locations relative to the Southville Zone and SBLN perimeter. "
    "No ATC sensors were placed within the Southville Zone.",
    styles['FigCaption']))

# Matt's JTC map
story.append(Image('D:/Projects/Bristol/maps/JTC Surveys Map.png',
    width=CONTENT_W * 0.85, height=CONTENT_W * 0.85 * 0.7, kind='proportional'))
story.append(Paragraph("JTC survey site locations. Only Sites 6 and 11 are on the perimeter "
    "of the Southville Zone.",
    styles['FigCaption']))

story.append(PageBreak())


# =============================================================
# PAGE 9 -- METHODOLOGY NOTES
# =============================================================
story.append(Paragraph("8. Methodology Notes", styles['H1']))
story.append(hr())

story.append(Paragraph("8.1 What the Data Can Show", styles['H2']))
method_can = [
    "Total traffic volumes on specific roads at specific times (ATC data).",
    "Speed distributions and compliance rates on monitored roads (ATC data).",
    "The next camera at which a vehicle was detected after passing a given camera (ANPR data).",
    "Junction turning movements at 11 surveyed junctions (JTC data).",
    "Bus passenger boarding and alighting volumes (bus stop surveys).",
    "Cyclist and e-scooter counts at selected locations (MCC data).",
]
for item in method_can:
    story.append(Paragraph(item, styles['BulletCustom'], bulletText='\u2022'))

story.append(Spacer(1, 4*mm))
story.append(Paragraph("8.2 What the Data Cannot Show", styles['H2']))
method_cannot = [
    "Whether a vehicle drove through the Southville residential zone (no ANPR cameras inside the zone).",
    "The specific route taken by any vehicle between two camera locations.",
    "Whether a vehicle detected at two cameras used a perimeter road or an internal residential street.",
    "The purpose of any journey (commuting, deliveries, local access, etc.).",
    "Whether traffic volumes have changed since June 2024.",
]
for item in method_cannot:
    story.append(Paragraph(item, styles['BulletCustom'], bulletText='\u2022'))

story.append(Spacer(1, 6*mm))
story.append(Paragraph("8.3 Volume Data Is Not Route Data", styles['H2']))
story.append(Paragraph(
    "ATC counters record the total number of vehicles passing a fixed point. A high volume on a "
    "residential road does not, by itself, indicate cut-through traffic. Local residents, their "
    "visitors, delivery vehicles, and service providers all contribute to the count. TRICS trip "
    "generation rates suggest that local demand from approximately 1,800 dwellings in the Luckwell "
    "Road catchment could account for around 94% of the observed daily volume on that road.",
    styles['Body']))

story.append(Spacer(1, 6*mm))
story.append(Paragraph("8.4 Note on 2025 Surveys", styles['H2']))
story.append(Paragraph(
    "This analysis is based entirely on the June 2024 dataset. Any subsequent surveys conducted "
    "in 2025 or later are not included in this analysis. Should additional data become available, "
    "the methodology used here can be applied to those datasets for comparison.",
    styles['Body']))

story.append(PageBreak())


# =============================================================
# PAGE 10 -- CONCLUSIONS
# =============================================================
story.append(Paragraph("9. Conclusions", styles['H1']))
story.append(hr())

conclusions = [
    ("1.", "The ANPR camera network deployed for the SBLN 2024 survey had <b>no cameras within "
     "the Southville residential zone</b>. The survey design therefore cannot determine whether "
     "vehicles travel through the zone's residential streets."),

    ("2.", "The two nearest ANPR cameras (14 and 16) recorded only <b>10-11 vehicles per day</b> "
     "appearing at both locations, representing 0.07-0.14% of total traffic. Even these vehicles "
     "cannot be confirmed as having used residential streets, as perimeter routes exist between "
     "the two camera locations."),

    ("3.", "The dominant traffic pattern at Camera 14 is travel along the <b>Coronation Road "
     "corridor</b> (90%+ to Camera 1), not diversion into residential streets."),

    ("4.", "ATC volume data on residential roads is <b>largely consistent with local demand</b> "
     "from the approximately 1,800 dwellings in the catchment area, based on standard TRICS trip "
     "generation rates."),

    ("5.", "Speed compliance on monitored roads is generally high, with mean speeds well below "
     "posted limits. The exception is Palmyra Road (20 mph zone) where 21.4% of vehicles exceed "
     "the limit, though the mean speed remains 17.1 mph."),

    ("6.", "The weekend traffic reduction of 9-22% on residential roads is consistent with "
     "weekday commuter and school-run patterns, which would be expected from local residents "
     "rather than from persistent external cut-through traffic."),
]

for num, text in conclusions:
    story.append(Paragraph(
        f"<b>{num}</b> {text}", styles['NumberedItem']))
    story.append(Spacer(1, 2*mm))

story.append(Spacer(1, 10*mm))
story.append(hr())
story.append(Spacer(1, 4*mm))

story.append(Paragraph("Data Sources", styles['H2']))
story.append(Paragraph(
    "SBLN 2024 Traffic Survey Results (94 spreadsheets), published by Bristol City Council. "
    "Survey conducted by Intelligent Data Collection Ltd, Project ID-0524-0183, June 2024.",
    styles['Body']))
story.append(Paragraph(
    "Census 2021 ward-level data (ONS) for Southville and Bedminster wards. "
    "TRICS trip generation rates for urban residential areas.",
    styles['Body']))

story.append(Spacer(1, 6*mm))
story.append(Paragraph("Credits", styles['H2']))
story.append(Paragraph(
    "<b>Ali Bin Shahid</b> -- Volunteer Data Analyst &amp; Systems Engineer (independent analysis)",
    styles['Body']))
story.append(Paragraph(
    "<b>Matt Sanders</b> -- Community advocate, art director (WECA statement, data verification, "
    "map production)", styles['Body']))

story.append(Spacer(1, 10*mm))
story.append(Paragraph(
    "<i>This report presents factual analysis of publicly available data. It does not make "
    "policy recommendations. All calculations are reproducible from the original spreadsheets.</i>",
    styles['Footer']))


# -- Generate PDF ---------------------------------------------
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(f"Executive report generated: {output_path}")

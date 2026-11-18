import os
from PIL import Image, ImageDraw, ImageFont

def create_newspaper():
    width, height = 1024, 1024
    image = Image.new("RGB", (width, height), color="#FBFBFA")
    draw = ImageDraw.Draw(image)

    # Fonts
    font_path_serif = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
    font_path_serif_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    font_path_sans = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font_path_sans_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    try:
        f_masthead = ImageFont.truetype(font_path_serif_bold, 42)
        f_subhead = ImageFont.truetype(font_path_sans_bold, 13)
        f_lead_title = ImageFont.truetype(font_path_serif_bold, 20)
        f_lead_body = ImageFont.truetype(font_path_serif, 12)
        f_med_title = ImageFont.truetype(font_path_serif_bold, 15)
        f_med_body = ImageFont.truetype(font_path_serif, 11)
        f_small_title = ImageFont.truetype(font_path_serif_bold, 12)
        f_small_body = ImageFont.truetype(font_path_serif, 10)
        f_footer = ImageFont.truetype(font_path_sans, 10)
    except IOError:
        f_masthead = f_subhead = f_lead_title = f_lead_body = f_med_title = f_med_body = f_small_title = f_small_body = f_footer = ImageFont.load_default()

    # Colors
    c_red = "#8B0000"     # Deep red accent
    c_navy = "#1B365D"    # Navy accent
    c_black = "#111111"   # Dark text
    c_gray = "#666666"    # Gray text
    c_line = "#CCCCCC"    # Divider lines

    # --- MASTHEAD ---
    draw.rectangle([30, 20, 994, 90], fill=c_red)
    draw.text((512, 55), "THE WORLD IN ONE PAGE", fill="#FFFFFF", font=f_masthead, anchor="mm")
    
    # Sub-masthead bar
    draw.rectangle([30, 93, 994, 118], fill="#FFFFFF")
    draw.rectangle([30, 93, 994, 95], fill=c_navy)
    draw.rectangle([30, 116, 994, 118], fill=c_navy)
    
    subtext = "VOL. III NO. 322  •  WEDNESDAY, 18 NOVEMBER 2026  •  GLOBAL DAILY INTELLIGENCE"
    draw.text((512, 105), subtext, fill=c_navy, font=f_subhead, anchor="mm")

    # Layout grid setup
    # Margins: 30 to 994 (width 964px)
    # Y range: 130 to 990
    
    # --- LEAD STORY (Top span: x=30 to 994, y=130 to 330) ---
    draw.rectangle([30, 130, 994, 335], outline=c_line, width=1)
    draw.rectangle([30, 130, 994, 148], fill="#F0F2F5")
    draw.text((40, 134), "LEAD STORY • GLOBAL DIPLOMACY", fill=c_red, font=f_subhead)
    
    # Lead title & body (title wrapped to the text column, clear of the pictogram)
    lead_title = "XI & TRUMP MEET IN SHENZHEN AS APEC OPENS; TRILATERAL SUMMIT SET FOR THURSDAY"
    n_lead = draw_wrapped(draw, 40, 156, lead_title, f_lead_title, c_black, 680, 26)

    lead_text = (
        "Xi Jinping greets Donald Trump on the tarmac in Shenzhen for a rare personal airport greeting as APEC opens. "
        "Xi and Vladimir Putin meet in Shenzhen the same day ahead of Thursday's first-ever three-way Xi-Trump-Putin summit. "
        "Meanwhile, the US-China tariff truce remains in effect, running through 10 January 2027."
    )
    # Simple word wrap simulation for lead body (two columns inside lead box)
    # Left text column: x=40 to 680, Right pictogram: x=700 to 984
    y = 156 + n_lead * 26 + 8
    for line in wrap_text(lead_text, 85):
        draw.text((40, y), line, fill=c_black, font=f_lead_body)
        y += 16

    # Lead Pictogram (Summit podium / 3 flags) at x=740, y=160
    draw.rectangle([730, 155, 970, 315], fill="#F4F6F9", outline=c_navy, width=1)
    draw.rectangle([760, 280, 940, 288], fill=c_navy) # podium base
    # 3 flags
    for fx in [780, 850, 920]:
        draw.line([fx, 280, fx, 180], fill=c_black, width=3)
    draw.polygon([(780, 180), (815, 195), (780, 210)], fill=c_red)
    draw.polygon([(850, 180), (885, 195), (850, 210)], fill=c_navy)
    draw.polygon([(920, 180), (955, 195), (920, 210)], fill="#D97706")
    draw.text((850, 295), "APEC / TRILATERAL SUMMIT", fill=c_navy, font=f_subhead, anchor="mm")

    # --- TWO MEDIUM BLOCKS (Row 2: y=345 to 545) ---
    # Medium Block 1 (Left: x=30 to 504)
    draw.rectangle([30, 345, 504, 545], outline=c_line, width=1)
    draw.rectangle([30, 345, 504, 363], fill="#F0F2F5")
    draw.text((40, 349), "MIDDLE EAST CONFLICT • STRAIT OF HORMUZ", fill=c_navy, font=f_subhead)
    n_m1 = draw_wrapped(draw, 40, 372, "US JETS STRIKE QESHM ISLAND MISSILE SITE", f_med_title, c_black, 464, 19)

    m1_text = (
        "US fighter jets strike an Iranian Revolutionary Guard missile launch site "
        "on Qeshm Island in the Strait of Hormuz in response to attacks on US personnel. "
        "Iran says it targeted US drone and missile sites in Kuwait overnight—its first attack "
        "on Kuwait since September—and fired at a US site in Bahrain; a UAE ship is hit."
    )
    y = 372 + n_m1 * 19 + 8
    for line in wrap_text(m1_text, 55):
        draw.text((40, y), line, fill=c_black, font=f_med_body)
        y += 15

    # Medium Block 2 (Right: x=520 to 994)
    draw.rectangle([520, 345, 994, 545], outline=c_line, width=1)
    draw.rectangle([520, 345, 994, 363], fill="#F0F2F5")
    draw.text((530, 349), "EASTERN EUROPE • UKRAINE CONFLICT", fill=c_navy, font=f_subhead)
    n_m2 = draw_wrapped(draw, 530, 372, "KERCH BRIDGE HIT FOR SECOND DAY; SPAN COLLAPSES", f_med_title, c_black, 464, 19)

    m2_text = (
        "Ukraine hits the Kerch Bridge to Crimea for a second consecutive day in a major operation. "
        "Part of the road span collapses following precision drone and missile strikes. "
        "All cross-strait vehicular and rail traffic is suspended indefinitely as structural assessments begin."
    )
    y = 372 + n_m2 * 19 + 8
    for line in wrap_text(m2_text, 55):
        draw.text((530, y), line, fill=c_black, font=f_med_body)
        y += 15


    # --- SMALL BLOCKS GRID (Rows 3 & 4: y=555 to 975) ---
    # 7 small blocks arranged in a 3-column or mixed grid
    # Column X coords: c1=30, c2=358, c3=686 (Widths ~308 each)
    
    blocks = [
        ("US SENATE • ALASKA", "PELTOLA WINS ALASKA SENATE SEAT", 
         "Democrat Mary Peltola defeats two-term Republican incumbent Dan Sullivan, giving Democrats a 56-44 majority in the incoming US Senate."),
        ("TECH MARKETS • NVIDIA", "NVIDIA Q3 REVENUE HITS $115.8B", 
         "First earnings since Jensen Huang's exit: revenue up 103% YoY, adjusted EPS $2.68 above forecasts. Board rejects Huang's return as CEO."),
        ("PUBLIC HEALTH • US", "US LOSES MEASLES ELIMINATION STATUS", 
         "United States loses measles elimination status after 26 years following a 12-month transmission chain, 5,400+ cases and 10 deaths."),
        ("WEATHER • BAY OF BENGAL", "CYCLONE AKVAN THREATENS INDIA COAST", 
         "Cyclone Akvan strengthens, forecast to make landfall on Andhra Pradesh coast Friday as very severe storm with winds up to 145 km/h."),
        ("PUBLIC HEALTH • DR CONGO", "EBOLA OUTBREAK PASSES 11,000 CASES", 
         "DR Congo outbreak surpasses 11,000 recorded cases; nearly three-quarters of infected children under the age of five do not survive."),
        ("TRADE • ASIA-PACIFIC", "US-PHILIPPINES TRADE UNDERSTANDING", 
         "Trump announces a 'very big trade deal' with the Philippines at a Manila state lunch; Manila describes the pact as an economic understanding."),
        ("ARTIFICIAL INTELLIGENCE", "OPENAI LAUNCHES GPT-6.2 ASTRA & SOL", 
         "OpenAI officially launches next-generation GPT-6.2 Astra and Sol models accompanied by significantly lower API pricing structures.")
    ]

    # Grid positions (cols, rows)
    # Row 1 of small blocks: y=555 to 755 (3 cols)
    # Row 2 of small blocks: y=765 to 965 (4 cols or 3 cols + footer note)
    
    grid_coords = [
        (30, 555, 338, 755),   # Box 1
        (358, 555, 666, 755),  # Box 2
        (686, 555, 994, 755),  # Box 3
        (30, 765, 260, 975),   # Box 4 (narrower)
        (270, 765, 500, 975),  # Box 5 (narrower)
        (510, 765, 740, 975),  # Box 6 (narrower)
        (750, 765, 994, 975),  # Box 7 (narrower)
    ]

    for idx, (cat, title, body) in enumerate(blocks):
        x1, y1, x2, y2 = grid_coords[idx]
        draw.rectangle([x1, y1, x2, y2], outline=c_line, width=1)
        draw.rectangle([x1, y1, x2, y1+18], fill="#F0F2F5")
        draw.text((x1+6, y1+3), cat, fill=c_navy, font=f_subhead)
        
        # Title (wrapped to the box width, never overflowing into the next box)
        n_title = draw_wrapped(draw, x1+6, y1+24, title, f_small_title, c_black, x2-x1-12, 15)

        # Body text wrap
        bw = int((x2 - x1 - 12) / 6.5) # approximate chars per line
        y_text = y1+24+n_title*15+6
        for line in wrap_text(body, max(25, int(bw))):
            if y_text < y2 - 12:
                draw.text((x1+6, y_text), line, fill=c_black, font=f_small_body)
                y_text += 13

    # --- FOOTER ---
    draw.line([30, 982, 994, 982], fill=c_navy, width=2)
    draw.text((512, 994), "COMPILED FOR MAKE.FUN NEWS-IMAGE-20261118 BOUNTY • VERIFIED WORLD NEWS ARCHIVE", fill=c_gray, font=f_footer, anchor="mm")

    # Save output
    image.save("entry.png", "PNG")
    print("Successfully generated entry.png (1024x1024)")

def wrap_to_width(draw, text, font, max_width):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(draw, x, y, text, font, fill, max_width, line_height):
    lines = wrap_to_width(draw, text, font, max_width)
    for ln in lines:
        draw.text((x, y), ln, fill=fill, font=font)
        y += line_height
    return len(lines)

def wrap_text(text, width_chars):
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    for word in words:
        if current_length + len(word) + len(current_line) <= width_chars:
            current_line.append(word)
            current_length += len(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
    if current_line:
        lines.append(" ".join(current_line))
    return lines

if __name__ == "__main__":
    create_newspaper()

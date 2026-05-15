"""
PHB-style formatting constants and styles for Google Docs.
"""

# Fonts (Google Fonts names)
BODY_FONT = "EB Garamond"
HEADING_1_FONT = "Cinzel Decorative"
HEADING_2_FONT = "Cinzel"
HEADING_3_FONT = "Libre Baskerville"
HEADING_4_FONT = "Libre Baskerville"
FONT_NAME = BODY_FONT  # backward-compat alias

# Font sizes (pt)
BODY_FONT_SIZE = 11.5
HEADING_1_SIZE = 28
HEADING_2_SIZE = 17
HEADING_3_SIZE = 12
HEADING_4_SIZE = 10
RULE_FONT_SIZE = 7

# Colors — parchment / ink palette
# #2C241C = very dark warm brown for body text
BLACK_COLOR = {"red": 0.173, "green": 0.141, "blue": 0.110}
# #6B2E1A = dark red-brown accent (rules, ornaments)
ACCENT_COLOR = {"red": 0.420, "green": 0.180, "blue": 0.102}
# Heading colors
HEADING_1_COLOR = {"red": 0.420, "green": 0.180, "blue": 0.102}  # dark red-brown  (#6B2E1A)
HEADING_2_COLOR = {"red": 0.220, "green": 0.120, "blue": 0.060}  # very dark brown
HEADING_3_COLOR = {"red": 0.173, "green": 0.141, "blue": 0.110}  # near-black warm (#2C241C)
HEADING_4_COLOR = {"red": 0.173, "green": 0.141, "blue": 0.110}
HEADING_COLOR = HEADING_1_COLOR  # backward-compat alias

# Layout — tighter print-book margins
COLUMN_GAP = 36         # points between columns
MARGIN_TOP = 43.2       # 0.60 in
MARGIN_BOTTOM = 46.8    # 0.65 in
MARGIN_LEFT = 54.0      # 0.75 in
MARGIN_RIGHT = 54.0     # 0.75 in

# Body typography
BODY_LINE_SPACING = 112       # 1.12 × 100 (percentage)
BODY_SPACE_BELOW = 3          # pt
BODY_INDENT_FIRST_LINE = 14.4 # 0.2 inches in pt

# Heading spacing (pt)
HEADING_1_SPACE_ABOVE = 18
HEADING_1_SPACE_BELOW = 8
HEADING_2_SPACE_ABOVE = 12
HEADING_2_SPACE_BELOW = 4
HEADING_3_SPACE_ABOVE = 8
HEADING_3_SPACE_BELOW = 4
HEADING_4_SPACE_ABOVE = 8
HEADING_4_SPACE_BELOW = 3

# Ornamental rule spacing
RULE_SPACE_ABOVE = 5
RULE_SPACE_BELOW = 5

# Named styles (Google Docs API)
HEADING_1 = "HEADING_1"
HEADING_2 = "HEADING_2"
HEADING_3 = "HEADING_3"
HEADING_4 = "HEADING_4"
NORMAL_TEXT = "NORMAL_TEXT"
TITLE = "TITLE"
SUBTITLE = "SUBTITLE"

# Cover page
COVER_TAGLINE_FONT_SIZE = 9
COVER_TITLE_FONT_SIZE = 52
COVER_SUBTITLE_FONT_SIZE = 34
COVER_TAGLINE_COLOR = {"red": 0.8, "green": 0.0, "blue": 0.0}
COVER_TITLE_COLOR = {"red": 0.58, "green": 0.0, "blue": 0.0}
COVER_SUBTITLE_COLOR = {"red": 0.2, "green": 0.05, "blue": 0.05}
COVER_IMAGE_HEIGHT_PT = 430
COVER_IMAGE_WIDTH_PT = 468
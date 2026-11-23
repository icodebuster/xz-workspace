import sys

src, dst = sys.argv[1], sys.argv[2]
html = open(src, encoding="utf-8").read()

# Order matters: specific (context) replacements first, then plain colour swaps.
pairs = [
    # Fonts: Inter (Axis), falling back to Arial where web fonts don't load.
    ("<title>", '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">\n<title>'),
    ("font-family:Georgia, 'Times New Roman', serif;", "font-family:Inter, Arial, Helvetica, sans-serif;"),
    ("font-family:Georgia, serif;", "font-family:Inter, Arial, Helvetica, sans-serif;"),
    ("font-family:Arial, Helvetica, sans-serif;", "font-family:Inter, Arial, Helvetica, sans-serif;"),

    # Corners: Axis v2 radii (xl 12px, lg 8px, md 6px).
    ("max-width:600px; background-color:#FFFFFF; border-radius:16px;", "max-width:600px; background-color:#FFFFFF; border-radius:12px; border:1px solid #E5E7EB;"),
    ("border-radius:12px 0 0 12px;", "border-radius:8px 0 0 8px;"),
    ("border-radius:0 12px 12px 0;", "border-radius:0 8px 8px 0;"),
    ("border:2px solid #E3B65B; border-radius:14px;", "border:1px solid #E5E7EB; border-radius:12px;"),
    ("border-radius:999px;", "border-radius:6px;"),
    ("border-radius:12px; padding:14px 18px;", "border-radius:8px; padding:14px 18px;"),

    # Step circles: teal with white figures.
    ("background-color:#E3B65B; text-align:center; font-family:Inter, Arial, Helvetica, sans-serif; font-size:17px; font-weight:bold; color:#0F2A1F;",
     "background-color:#10A37F; text-align:center; font-family:Inter, Arial, Helvetica, sans-serif; font-size:16px; font-weight:600; color:#FFFFFF;"),

    # Stripe under the header: teal then deeper teal.
    ("font-size:0; background-color:#E3B65B;", "font-size:0; background-color:#3DDCAB;"),
    ("font-size:0; background-color:#C8372D;", "font-size:0; background-color:#10A37F;"),

    # Headline on the navy header.
    ("font-weight:bold; color:#F7F1E3;", "font-weight:700; letter-spacing:-0.5px; color:#F2F5F8;"),
    # Date cards.
    ("background-color:#F7F1E3;", "background-color:#ECFAF5;"),
    ("background-color:#C8372D;", "background-color:#10A37F;"),
    ("border-left:2px dashed #E7DCC4;", "border-left:1px dashed #D0D5DD;"),

    # Primary button: Axis teal, like the app's Sign in button.
    ('bgcolor="#0F2A1F"', 'bgcolor="#10A37F"'),

    # Snowflakes keep their original gold (placeholder protects them from the swap below).
    ("letter-spacing:6px; color:#E3B65B;", "letter-spacing:6px; color:@@GOLD@@;"),
    ('<span style="color:#E3B65B;">&#10052;</span>', '<span style="color:@@GOLD@@;">&#10052;</span>'),

    # Plain colour swaps (Axis tokens).
    ("#F3EEE2", "#F5F6F8"),  # page background -> canvas
    ("#0F2A1F", "#0B1A28"),  # dark green -> nav navy
    ("#E3B65B", "#3DDCAB"),  # gold -> brand-300 (on navy)
    ("#D9E4DC", "#A7B4C2"),  # header subtitle -> nav-text
    ("#8A2620", "#08705A"),  # dark red labels -> brand-700
    ("#FBE3DF", "#D1F2E6"),  # pale red label -> brand-100
    ("#1E2E25", "#344054"),  # body text -> ink-2
    ("#4A5A50", "#667085"),  # muted text -> ink-3
    ("#1F5C3F", "#0B8A6A"),  # link -> brand-600
    ("#EEF4EF", "#F2F4F7"),  # reminder box -> surface-3
    ("#1F3B2C", "#344054"),  # reminder text -> ink-2
    ("#C9D7CD", "#A7B4C2"),  # footer text -> nav-text
    ("@@GOLD@@", "#E3B65B"),  # restore original snowflake gold
    # Festive sign-off in place of the placeholder.
    ("<strong>[Your name]</strong>", "<strong>Santa's little Axis builders &#127876;&#65039;</strong>"),
    # Force the colour-emoji snowflake (light blue) in every client, as in the original's look.
    ("&#10052;", "&#10052;&#65039;"),
    # Reindeer and Santa either side of the star, a little larger than the snowflakes.
    ("&#9733;",
     '<span style="font-size:26px; line-height:26px; letter-spacing:0; vertical-align:middle;">&#129420;</span> &nbsp; &#9733; &nbsp; '
     '<span style="font-size:26px; line-height:26px; letter-spacing:0; vertical-align:middle;">&#127877;</span>'),
]

# Header snowflake/star row exists only in the first draft; the new draft has a banner image instead.
OPTIONAL = {"letter-spacing:6px; color:#E3B65B;", "&#9733;"}

# Banner: swap in the copy recoloured to Axis navy (argv[3]), if given.
if len(sys.argv) > 3:
    import base64, re
    navy = base64.b64encode(open(sys.argv[3], "rb").read()).decode()
    html, n = re.subn(r'(<!-- Santa and reindeer banner -->.*?src="data:image/png;base64,)[A-Za-z0-9+/=]+',
                      lambda m: m.group(1) + navy, html, count=1, flags=re.S)
    if n != 1:
        sys.exit("banner image not found")

for old, new in pairs:
    if old not in html:
        if old in OPTIONAL:
            continue
        sys.exit(f"not found: {old}")
    html = html.replace(old, new)

# Training date only: drop the "Rolling out" card and let the training card fill the row.
import re
html, n = re.subn(r'\n<td width="50%" valign="top" style="background-color:#10A37F;.*?</td>', "", html, count=1, flags=re.S)
if n != 1:
    sys.exit("rolling-out card not found")
for old, new in [
    ('<td width="50%" valign="top" style="background-color:#ECFAF5; padding:16px 18px; border-radius:8px 0 0 8px;',
     '<td width="100%" align="center" valign="top" style="background-color:#ECFAF5; padding:16px 18px; border-radius:8px; text-align:center;'),
    ('<p style="margin:0;">Training on our new system, <strong>Axis</strong>, starts today. That gives us <strong>14 sleeps</strong> to get comfortable with it before it rolls out, so please jump in and have a look around.',
     '<p style="margin:0;">Training on our new system, <strong>Axis</strong>, starts today. Jump in, unwrap it and get comfortable with it before it goes live.'),
    ("Santa's delivered our new system early this year.",
     "Santa, Mrs Claus and the elves are working hard to deliver a New System for Christmas this year!"),
    ("Training starts today, Axis rolls out Mon 7 Dec. Click or scan to sign in.",
     "Axis training starts today. Click or scan to sign in."),
]:
    if old not in html:
        sys.exit(f"not found: {old}")
    html = html.replace(old, new)

open(dst, "w", encoding="utf-8").write(html)
print("written", dst)

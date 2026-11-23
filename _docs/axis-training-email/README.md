# Axis training email (Christmas, Nov 2026)

HTML email announcing Axis training to the Xzibit team, styled with the Axis system theme (colours, font and corners from `Axis-ERP/app/assets/tailwind/application.css`).

## Files

| File | What it is |
|---|---|
| `Axis-Training-Email-Axis-Theme.html` | **The final email.** Generated: do not hand-edit, change `tools/retheme.py` and rebuild |
| `source/Axis-Training-Email-New.html` | Source draft the final email is built from (Christmas green/gold/red look, Santa banner) |
| `source/Axis-Training-Email.html` | First draft (snowflake row instead of the banner) |
| `source/Axis.html` | Identical copy of the first draft |
| `source/Axis Training - Christmas QR Poster-project.zip` | The matching Christmas QR poster project |
| `tools/retheme.py` | Turns the source draft into the final email: Axis colours, Inter font, corners, navy banner, and the content changes below |
| `tools/recolour.py` | Recolours the banner's green sky to Axis navy `#0B1A28` (needs Pillow) |
| `tools/banner.png`, `tools/banner-navy.png` | Banner as extracted from the source draft, and the navy version used in the final email |

## Changes made on top of the source draft (all in `retheme.py`)

- Axis theme: navy `#0B1A28` header and footer, teal `#10A37F` button, step circles and accents, Axis greys, Inter font (Arial fallback), corners 6 to 12px.
- Santa banner recoloured to navy.
- Snowflakes in the footer forced to colour emoji (light blue), gold kept in the code.
- "Rolling out Mon 7 December" card removed; the training card is full width and centred. Preview text no longer mentions 7 Dec.
- Header subtitle: "Santa, Mrs Claus and the elves are working hard to deliver a New System for Christmas this year!"
- Intro: "Training on our new system, **Axis**, starts today. Jump in, unwrap it and get comfortable with it before it goes live."
- Sign-off: "Santa's little Axis builders 🎄".

## Rebuild

From this folder:

```sh
python3 -I tools/retheme.py source/Axis-Training-Email-New.html Axis-Training-Email-Axis-Theme.html tools/banner-navy.png
```

To regenerate the navy banner (only if the source banner changes), use a throwaway venv with Pillow:

```sh
python3 -m venv /tmp/venv && /tmp/venv/bin/pip install -q pillow
/tmp/venv/bin/python -I tools/recolour.py tools/banner.png tools/banner-navy.png
```

Preview in Chrome headless:

```sh
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --hide-scrollbars --window-size=700,1500 --screenshot=/tmp/email.png "file://$PWD/Axis-Training-Email-Axis-Theme.html"
```

## Before sending

- The banner and the QR code are embedded as `data:` images. Gmail on the web often hides these: send a test to yourself first, and if they are missing, host the images and link them instead.
- The button, link and QR code point to `https://axis-staging.xzibit.com.au/`.

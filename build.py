"""Wrap the artifact fragment in _work/landing-redesign.html into a standalone page.

The fragment is authored for the artifact host, which supplies <!doctype>, <head>
and <body> itself. Here we split it at the end of the stylesheet: everything up to
and including </style> belongs in <head>, the rest is the document body.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT.parent / "_work" / "landing-redesign.html"
OUT = ROOT / "index.html"

HEAD_EXTRA = """<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#15181e">
<meta property="og:type" content="website">
<meta property="og:title" content="הוזלת ביטוח חיים למשכנתא | בדיקה חינם">
<meta property="og:description" content="בכל חודש, בשקט בשקט, יורד לכם מהחשבון כסף מיותר. בדיקה חינם להוזלת ביטוח החיים למשכנתא — אותם כיסויים בדיוק.">
<meta property="og:locale" content="he_IL">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#127968;</text></svg>">
"""

src = SRC.read_text(encoding="utf-8")

marker = "</style>"
cut = src.rindex(marker) + len(marker)
head, body = src[:cut], src[cut:]

if "<title>" not in head or "<style>" not in head:
    sys.exit("unexpected fragment layout — refusing to build a broken page")

page = (
    "<!doctype html>\n<html lang=\"he\" dir=\"rtl\">\n<head>\n"
    + HEAD_EXTRA
    + head.strip()
    + "\n</head>\n<body>\n"
    + body.strip()
    + "\n</body>\n</html>\n"
)

OUT.write_text(page, encoding="utf-8")
print(f"wrote {OUT} ({len(page):,} chars)")

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

<script async src="https://www.googletagmanager.com/gtag/js?id=G-1QG5097HFX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-1QG5097HFX');
</script>
"""

# Ported verbatim from the old site so both pages feed the same `visits` table.
# It lives here rather than in the artifact fragment because the artifact host
# blocks every external request — there it would only produce console errors.
# Visits from this page arrive with path "/", the old site's with "/my-site/".
TRACKING = """
<!-- ---- Visitor tracking (Supabase) ---- -->
<script>
(function(){
  var SUPA_URL = "https://ktcabahjyjmtfavlsdks.supabase.co";
  var SUPA_KEY = "sb_publishable_jYj0az-JCWUc3ga1fRYcew_La1y7qVw";
  function device(){
    var ua = navigator.userAgent;
    if(/Tablet|iPad/i.test(ua)) return 'טאבלט';
    if(/Mobi|Android/i.test(ua)) return 'מובייל';
    return 'מחשב';
  }
  var startTime = Date.now();
  var converted = false;
  var sent = false;

  function sendVisit(){
    if(sent) return; sent = true;
    var duration = Math.round((Date.now()-startTime)/1000);
    try{
      fetch(SUPA_URL + '/rest/v1/visits', {
        method:'POST', keepalive:true,
        headers:{'Content-Type':'application/json','apikey':SUPA_KEY,'Prefer':'return=minimal'},
        body: JSON.stringify({
          path: location.pathname,
          referrer: document.referrer || null,
          user_agent: navigator.userAgent,
          device: device(),
          duration: duration,
          converted: converted
        })
      });
    }catch(e){}
  }
  /* Hold the record while a form is being filled, so switching apps mid-form
     is not written down as a non-conversion. */
  var touched = false;
  document.addEventListener('input', function(e){
    if(e.target && e.target.form) touched = true;
  }, true);

  document.addEventListener('visibilitychange', function(){
    if(document.visibilityState === 'hidden' && !touched) sendVisit();
  });
  window.addEventListener('pagehide', sendVisit);

  var forms = document.querySelectorAll('form');
  for(var i=0;i<forms.length;i++){
    forms[i].addEventListener('submit', function(){ converted = true; sendVisit(); });
  }
})();
</script>
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
    + "\n"
    + TRACKING
    + "\n</body>\n</html>\n"
)

OUT.write_text(page, encoding="utf-8")
print(f"wrote {OUT} ({len(page):,} chars)")

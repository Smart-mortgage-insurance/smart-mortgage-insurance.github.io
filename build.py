"""Wrap the artifact fragment in _work/landing-redesign.html into a standalone page.

The fragment is authored for the artifact host, which supplies <!doctype>, <head>
and <body> itself. Here we split it at the end of the stylesheet: everything up to
and including </style> belongs in <head>, the rest is the document body.

  ⚠️  DIVERGED — READ BEFORE RUNNING
  The live index.html was hand-edited directly (native-POST form fix, insurance-
  type selector, theme toggle removed) and no longer matches this fragment.
  To avoid destroying that work, this script writes a PREVIEW file
  (index.generated.html), NOT index.html. index.html is now maintained by hand.
  If you want to go back to fragment-as-source, first port those live edits into
  _work/landing-redesign.html, then point OUT back at index.html.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT.parent / "_work" / "landing-redesign.html"
OUT = ROOT / "index.generated.html"

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
  var ua = navigator.userAgent;

  function device(){
    if(/Tablet|iPad/i.test(ua)) return 'טאבלט';
    if(/Mobi|Android/i.test(ua)) return 'מובייל';
    return 'מחשב';
  }
  function osName(){
    if(/Windows/i.test(ua)) return 'Windows';
    if(/Android/i.test(ua)) return 'Android';
    if(/iPhone|iPad|iPod/i.test(ua)) return 'iOS';
    if(/Mac OS X/i.test(ua)) return 'macOS';
    if(/Linux/i.test(ua)) return 'Linux';
    return 'אחר';
  }
  function browserName(){
    if(/Edg\\//i.test(ua)) return 'Edge';
    if(/OPR\\/|Opera/i.test(ua)) return 'Opera';
    if(/SamsungBrowser/i.test(ua)) return 'Samsung';
    if(/Chrome\\//i.test(ua)) return 'Chrome';
    if(/Firefox\\//i.test(ua)) return 'Firefox';
    if(/Safari\\//i.test(ua)) return 'Safari';
    return 'אחר';
  }

  /* returning visitor — a flag we set the first time and read on later visits */
  var returningVisitor = false;
  try{
    returningVisitor = localStorage.getItem('v_seen') === '1';
    localStorage.setItem('v_seen', '1');
  }catch(e){}

  var screenSize = (screen.width||0) + 'x' + (screen.height||0) +
                   (window.devicePixelRatio > 1 ? ' @' + window.devicePixelRatio + 'x' : '');

  /* which ad/link brought them here */
  var qp = new URLSearchParams(location.search);
  function utm(k){ var v = qp.get(k); return (v && v.length < 120) ? v : null; }
  var utmSource = utm('utm_source'), utmMedium = utm('utm_medium'), utmCampaign = utm('utm_campaign');

  /* approximate city from the IP — best effort, may be the ISP's routing city
     (poor on mobile) and may be blocked on filtered networks. Never blocks the
     visit: if it hasn't resolved by send time the city columns stay empty. */
  var geo = {};
  function geoFrom(url, map){
    return fetch(url).then(function(r){ return r.json(); }).then(function(d){
      if(d) map(d);
    });
  }
  geoFrom('https://ipwho.is/', function(d){
    if(d.success === false) throw 0;
    geo.city = d.city || null; geo.region = d.region || null;
    geo.country = d.country || null;
    geo.isp = (d.connection && d.connection.isp) || null;
  }).catch(function(){
    return geoFrom('https://ipapi.co/json/', function(d){
      geo.city = d.city || null; geo.region = d.region || null;
      geo.country = d.country_name || null; geo.isp = d.org || null;
    });
  }).catch(function(){});

  /* engagement signals */
  var maxScroll = 0, reachedForm = false, viewedTestimonials = false;
  function scrollPct(){
    var h = document.documentElement.scrollHeight - innerHeight;
    return h > 0 ? Math.min(100, Math.round(scrollY / h * 100)) : 100;
  }
  var forms = document.querySelectorAll('form');
  function checkForm(){
    if(reachedForm) return;
    for(var i=0;i<forms.length;i++){
      var r = forms[i].getBoundingClientRect();
      if(r.top < innerHeight * 0.9 && r.bottom > 0){ reachedForm = true; return; }
    }
  }
  addEventListener('scroll', function(){
    var p = scrollPct(); if(p > maxScroll) maxScroll = p;
    checkForm();
  }, {passive:true});
  checkForm();
  var tstBtn = document.getElementById('tstToggle');
  if(tstBtn) tstBtn.addEventListener('click', function(){ viewedTestimonials = true; });

  var startTime = Date.now();
  var converted = false;
  var sent = false;

  function base(){
    return {
      path: location.pathname,
      referrer: document.referrer || null,
      user_agent: ua,
      device: device(),
      duration: Math.round((Date.now() - startTime) / 1000),
      converted: converted
    };
  }
  function full(){
    var p = base();
    p.city = geo.city || null; p.region = geo.region || null;
    p.country = geo.country || null; p.isp = geo.isp || null;
    p.utm_source = utmSource; p.utm_medium = utmMedium; p.utm_campaign = utmCampaign;
    p.scroll_depth = maxScroll; p.reached_form = reachedForm;
    p.viewed_testimonials = viewedTestimonials; p.returning_visitor = returningVisitor;
    p.browser = browserName(); p.os = osName(); p.screen_size = screenSize;
    return p;
  }
  function post(body, onFail){
    try{
      fetch(SUPA_URL + '/rest/v1/visits', {
        method:'POST', keepalive:true,
        headers:{'Content-Type':'application/json','apikey':SUPA_KEY,'Prefer':'return=minimal'},
        body: JSON.stringify(body)
      }).then(function(r){ if(!r.ok && onFail) onFail(); })
        .catch(function(){ if(onFail) onFail(); });
    }catch(e){ if(onFail) onFail(); }
  }
  function sendVisit(){
    if(sent) return; sent = true;
    /* Try the rich record; if the new columns aren't in the table yet, fall
       back to the original six fields so a visit is never lost. */
    post(full(), function(){ post(base()); });
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

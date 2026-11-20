"""Builds site/index.html and site/demo.html from their sources, applying the shared header and theme.

  python3 -I tools/site/make-site.py

Sources: archive/1120-page-pairing/a-download.html (the download page) and
tools/demo-build/out/index.html (the demo page, from tools/demo-build/build.py).
"""
import os, re, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = os.path.join(ROOT, 'site')

SHARED_CSS = '''
  /* Shared across the site: page switcher, header, footer */
  .pairbar { width: min(1120px, 100%); margin: 0 auto; padding-top: 1rem; display: flex; justify-content: flex-end; }
  nav.pair { display: flex; gap: .35rem; font: 700 .8rem Verdana, Geneva, sans-serif; }
  nav.pair a, nav.pair span { padding: .28rem .8rem; border-radius: 999px; border: 1px solid rgba(47,115,64,.35); text-decoration: none; }
  nav.pair a { color: #2f7340; background: rgba(255,255,255,.55); }
  nav.pair a:hover { background: #fff; }
  nav.pair span { color: #fff; background: #1a672c; border-color: #1a672c; }
  .sitehead { text-align: center; margin-top: 1.5rem; }
  .sitehead img { width: 110px; height: 110px; }
  .sitehead h1 { font-size: 2.4rem; line-height: 1.2; margin: 1rem 0 0; }
  footer.sitefoot { margin-top: 3rem; padding-top: 2rem; text-align: center; font-size: .85rem; color: #43524a; }
  footer.sitefoot a { color: inherit; }
  footer.sitefoot div + div { margin-top: .4rem; }
'''
FOOTER = '''  <footer class="sitefoot">
    <div>Created by <a href="https://github.com/jaymoran103">Jay Moran</a> &middot; Questions welcome: <a href="mailto:jaymorandev@gmail.com">jaymorandev@gmail.com</a></div>
    <div>
      <a href="https://github.com/jaymoran103/happycamper-heart">Source &amp; documentation</a> &middot;
      <a href="https://github.com/jaymoran103/happycamper-heart/releases">All releases</a>
    </div>
  </footer>
'''
def nav(here):
    pages = [('Download', 'index.html'), ('Demo', 'demo.html')]
    items = ''.join('<span aria-current="page">%s</span>' % n if n == here else '<a href="%s">%s</a>' % (h, n) for n, h in pages)
    return '<div class="pairbar"><nav class="pair" aria-label="HappyCamper pages">%s</nav></div>\n' % items

def sub(text, old, new, count=1):
    assert text.count(old) == count, (text.count(old), old[:70])
    return text.replace(old, new)

def download():
    h = open(os.path.join(ROOT, 'archive/1120-page-pairing/a-download.html'), encoding='utf-8').read()
    h = re.sub(r'\n  /\* Page pair switcher \*/.*?  body \{ position: relative; \}\n', '\n', h, flags=re.S)
    h = sub(h, '--paper: #f4f9f4;', '--paper: #cfe3c9;')
    h = sub(h, 'min-height: 100vh; padding: 3rem 1.25rem; text-align: center;', 'min-height: 100vh; padding: 0 1.25rem 3rem; text-align: center;')
    h = sub(h, 'color: #5c6a5e; }', 'color: #43524a; }')
    h = sub(h, '</style>', SHARED_CSS + '  @media (max-width: 760px) { .buttons { flex-wrap: wrap; } .dl { flex: 1 1 100%; } .dl.demo { width: 100%; } }\n</style>')
    h = re.sub(r'<nav class="pair"[^\n]*</nav>\n', nav('Download') + '  <header class="sitehead">\n', h, count=1)
    h = sub(h, '  <img class="logo" src="icon.png" alt="HappyCamper logo">\n  <h1>HappyCamper</h1>\n', '  <img class="logo" src="icon.png" alt="HappyCamper logo">\n  <h1>HappyCamper</h1>\n  </header>\n')
    h = re.sub(r'  <footer>.*?</footer>\n', FOOTER, h, count=1, flags=re.S)
    return h

def demo():
    h = open(os.path.join(ROOT, 'tools/demo-build/out/index.html'), encoding='utf-8').read()
    h = sub(h, 'padding: 3rem 1.25rem 2rem; }', 'padding: 0 1.25rem 2rem; }')
    h = sub(h, '</style>', SHARED_CSS + '  @media (max-width: 820px) { .page { padding-top: 0; } }\n</style>')
    h = sub(h, '<div class="page">\n', '<div class="page">\n' + nav('Demo'))
    h = sub(h, '<header class="top">', '<header class="top sitehead">')
    # The headline introduces the overview, so it sits left-aligned above it.
    h = sub(h, '    <p class="headline">Catch schedule problems before your campers do</p>\n  </header>', '  </header>')
    h = sub(h, '    <div class="intro">\n', '    <div class="intro">\n      <h2 class="headline">Catch schedule problems before your campers do</h2>\n')
    h = sub(h, '</style>', '  .intro .headline { margin: 0 0 .75rem; }\n</style>')
    h = sub(h, '      <a class="dl" href="https://jaymoran103.github.io/happycamper-heart/docs/">Downloads and sample rosters</a>\n', '')
    h = re.sub(r'  <footer>\n    <div>Created by.*?</footer>\n', FOOTER, h, count=1, flags=re.S)
    return h

os.makedirs(SITE, exist_ok=True)
open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8').write(download())
open(os.path.join(SITE, 'demo.html'), 'w', encoding='utf-8').write(demo())
for f in ('icon.png', 'whatsnew.json'):
    shutil.copy(os.path.join(ROOT, 'archive/1120-page-pairing', f), os.path.join(SITE, f))
print('site/index.html and site/demo.html written')

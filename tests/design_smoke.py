"""Check original restored gradient, 102px height and dark-theme fallback in Chromium."""
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'tests/browser.html').read_text().replace('<script src="../dist/central-overview-card.js"></script>', '<script>'+ (root/'dist/central-overview-card.js').read_text() +'</script>')
with sync_playwright() as p:
  b=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
  page=b.new_page(viewport={'width':1120,'height':1100},device_scale_factor=1)
  page.set_content(html)
  page.wait_for_function('window.card && window.card.shadowRoot.querySelectorAll("button.tile").length===16')
  heights=page.evaluate('''() => [...card.shadowRoot.querySelectorAll('button.tile')].map(x=>x.getBoundingClientRect().height)''')
  assert len(heights)==16
  assert all(h==102 for h in heights),heights
  assert page.evaluate('''() => card.shadowRoot.querySelector('.grid').getBoundingClientRect().height''')==872
  assert page.evaluate('''() => card.shadowRoot.querySelector('button.tile ha-icon').getAttribute('icon').startsWith('mdi:')''')
  assert page.evaluate('''() => getComputedStyle(card.shadowRoot.querySelector('button.tile.colored')).backgroundImage.includes('linear-gradient(135deg')''')
  page.add_style_tag(content=':root { --ha-card-background:#1c222c; --card-background-color:#1c222c; --primary-text-color:#ecf0f5; --secondary-text-color:#aab7c7; --divider-color:#384456; --ha-card-border-color:#394559; --success-color:#66bb6a; --error-color:#ef5350; --warning-color:#ffca28; --info-color:#64b5f6; --orange-color:#ffb74d; --cyan-color:#4dd0e1; --purple-color:#ba9cf6; --pink-color:#f48fb1; } body{background:#10151d;}section>h2{color:#e7eef8;}')
  page.locator('#dashboard').screenshot(path=str(root/'images/preview-dark.png'))
  assert 'rgb(28, 34, 44)' in page.evaluate('''() => getComputedStyle(card.shadowRoot.querySelector('button.tile')).backgroundColor''')
  b.close()
print('PASS: 16 tiles each 102px, restored 135-degree gradient, 872px overall, MDI icons and dark theme.')

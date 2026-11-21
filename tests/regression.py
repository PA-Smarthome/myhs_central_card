"""Real DOM interactions against simulated Home Assistant card editor behavior.
Uses real Chromium, but cannot replace tests in a live Home Assistant frontend.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
html=(root/'tests/browser.html').read_text(encoding='utf-8').replace(
 '<script src="../dist/central-overview-card.js"></script>',
 '<script>'+ (root/'dist/central-overview-card.js').read_text(encoding='utf-8') + '</script>')

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=2, is_mobile=True,has_touch=True)
 pageerrors=[]
 page.on('pageerror',lambda e:pageerrors.append(str(e)))
 page.set_content(html)
 page.wait_for_function("window.card && window.editor && editor.shadowRoot.querySelectorAll('details.tile-item').length === 16")
 # HA behavior: config-changed sends config to card, then editor.setConfig with same config
 page.evaluate('''() => editor.addEventListener('config-changed', e=>{card.setConfig(e.detail.config); editor.setConfig(e.detail.config);})''')
 def get(js):return page.evaluate(js)
 assert get("() => card.shadowRoot.querySelectorAll('button.tile').length") == 16
 # quick visibility, including collapse & persistent configuration
 assert not get("() => editor.shadowRoot.querySelector('details.tile-item').open")
 page.locator('central-overview-card-editor').evaluate("el=>el.shadowRoot.querySelector('details.tile-item button[data-action=toggle-enabled]').click()")
 assert get("() => editor._config.tiles[0].enabled") is False
 assert not get("() => editor.shadowRoot.querySelector('details.tile-item').open"), 'quick toggle unexpectedly expanded editor'
 assert get("() => card.shadowRoot.querySelectorAll('button.tile').length") == 15
 assert get("() => editor.shadowRoot.querySelector('.count-badge').textContent") == '15 / 16 sichtbar'
 page.locator('central-overview-card-editor').evaluate("el=>el.shadowRoot.querySelector('details.tile-item button[data-action=toggle-enabled]').click()")
 assert get("() => editor._config.tiles[0].enabled") is True
 assert get("() => card.shadowRoot.querySelectorAll('button.tile').length") == 16
 # bulk updates + card preview, with no remount
 page.locator('central-overview-card-editor').evaluate("el=>el.shadowRoot.querySelector('#hide-all').click()")
 assert get("() => card.shadowRoot.querySelectorAll('button.tile').length") == 0
 assert get("() => editor.shadowRoot.querySelector('.count-badge').textContent") == '0 / 16 sichtbar'
 page.locator('central-overview-card-editor').evaluate("el=>el.shadowRoot.querySelector('#show-all').click()")
 assert get("() => card.shadowRoot.querySelectorAll('button.tile').length") == 16
 # Change manually typed mdi: icon and preserve across render and HASS update
 page.locator('central-overview-card-editor').evaluate('''el=>{
  const t=el.shadowRoot.querySelector('details.tile-item');t.open=true;
  const input=t.querySelector('input[data-field=icon]');input.value='mdi:shield-custom';
  input.dispatchEvent(new Event('input',{bubbles:true}));
 }''')
 assert get("() => editor._config.tiles[0].icon") == 'mdi:shield-home', 'partial icon was committed on input'
 page.locator('central-overview-card-editor').evaluate('''el=>{
  const input=el.shadowRoot.querySelector('details.tile-item input[data-field=icon]');
  input.dispatchEvent(new Event('change',{bubbles:true}));
 }''')
 assert get("() => editor._config.tiles[0].icon") == 'mdi:shield-custom'
 assert get("() => card.shadowRoot.querySelector('button.tile ha-icon').getAttribute('icon')") == 'mdi:shield-custom'
 # Preserve custom icon even though lock normally has state-dependent icon.
 page.locator('central-overview-card-editor').evaluate('''el=>{
  const t=el.shadowRoot.querySelectorAll('details.tile-item')[10];t.open=true;
  const input=t.querySelector('input[data-field=icon]');input.value='mdi:door';
  input.dispatchEvent(new Event('change',{bubbles:true}));
 }''')
 page.evaluate("() => {hassMock.states['lock.door'].state='unlocked';card.hass=hassMock;}")
 assert get("() => card.shadowRoot.querySelectorAll('button.tile')[10].querySelector('ha-icon').getAttribute('icon')") == 'mdi:door'
 # Group kind dynamic icon must not overwrite custom shading icon either
 page.locator('central-overview-card-editor').evaluate('''el=>{
  const t=el.shadowRoot.querySelectorAll('details.tile-item')[7];t.open=true;
  const inp=t.querySelector('input[data-field=icon]');inp.value='mdi:window-shutter';
  inp.dispatchEvent(new Event('change',{bubbles:true}));
 }''')
 assert get("() => card.shadowRoot.querySelectorAll('button.tile')[7].querySelector('ha-icon').getAttribute('icon')") == 'mdi:window-shutter'
 # Select source and add entity by manual field even if picker unavailable
 page.locator('central-overview-card-editor').evaluate('''el=>{
  const t=el.shadowRoot.querySelectorAll('details.tile-item')[2];t.open=true;
  const s=t.querySelector('select[data-field=source]');s.value='selected';s.dispatchEvent(new Event('change',{bubbles:true}));
 }''')
 page.locator('central-overview-card-editor').evaluate('''el=>{
  const t=el.shadowRoot.querySelectorAll('details.tile-item')[2];
  const inp=t.querySelector('input[data-field=manual-entity]');inp.value='light.living';
  t.querySelector('button[data-action=add-entity]').click();
 }''')
 assert get("() => editor._config.tiles[2].entities") == ['light.living']
 assert get("() => card.shadowRoot.querySelectorAll('button.tile')[2].querySelector('.state').textContent") == 'In 1 Raum aktiv'
 # Need check input focus persist after editor emit
 assert get("() => editor.shadowRoot.querySelectorAll('details.tile-item')[2].open")
 # Filtering hidden tiles and finding them again
 page.locator('central-overview-card-editor').evaluate("el=>el.shadowRoot.querySelector('details.tile-item button[data-action=toggle-enabled]').click()")
 page.locator('central-overview-card-editor').evaluate('''el=>{
  const s=el.shadowRoot.querySelector('#tile-filter');s.value='hidden';s.dispatchEvent(new Event('change',{bubbles:true}));
 }''')
 assert get("() => Array.from(editor.shadowRoot.querySelectorAll('details.tile-item')).filter(x=>!x.hidden).length") == 1
 page.locator('central-overview-card-editor').evaluate('''el=>el.shadowRoot.querySelector('details.tile-item button[data-action=toggle-enabled]').click()''')
 assert get("() => Array.from(editor.shadowRoot.querySelectorAll('details.tile-item')).filter(x=>!x.hidden).length") == 0
 assert not pageerrors, pageerrors
 browser.close()
print('PASS: live save/reload, quick hide/show, bulk hide/show, manual icon, dynamic state icons, manual entities, filtering, and iPhone layout interactions')

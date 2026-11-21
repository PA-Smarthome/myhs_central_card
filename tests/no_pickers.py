"""Editor remains usable when optional native picker elements are not registered."""
from pathlib import Path
import re
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'tests/browser.html').read_text()
html=html.replace('<script src="../dist/central-overview-card.js"></script>', '<script>'+(root/'dist/central-overview-card.js').read_text()+'</script>')
html=re.sub(r"customElements\.define\('ha-icon-picker',[^\n]*\n",'',html)
html=re.sub(r"customElements\.define\('ha-entity-picker',[^\n]*\n",'',html)
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':420,'height':800})
 errs=[]
 page.on('pageerror', lambda e:errs.append(str(e)))
 page.set_content(html)
 page.wait_for_function('window.editor && editor.shadowRoot.querySelectorAll(".tile-item").length===16')
 page.evaluate("() => editor.addEventListener('config-changed',e=>card.setConfig(e.detail.config))")
 page.evaluate('''() => {
   const panel=editor.shadowRoot.querySelector('.tile-item');panel.querySelector('[data-action=expand-tile]').click();
   const icon=editor.shadowRoot.querySelector('.tile-item input[data-field=icon]');icon.value='mdi:shield-star';icon.dispatchEvent(new Event('change',{bubbles:true}));
 }''')
 assert page.evaluate("() => editor._config.tiles[0].icon")=='mdi:shield-star'
 assert page.evaluate("() => card.shadowRoot.querySelector('button.tile ha-icon').getAttribute('icon')")=='mdi:shield-star'
 page.evaluate('''() => {
   const panel=editor.shadowRoot.querySelectorAll('.tile-item')[2];panel.querySelector('[data-action=expand-tile]').click();
   const sel=editor.shadowRoot.querySelectorAll('.tile-item')[2].querySelector('select[data-field=source]');sel.value='selected';sel.dispatchEvent(new Event('change',{bubbles:true}));
   const input=editor.shadowRoot.querySelectorAll('.tile-item')[2].querySelector('input[data-field=manual-entity]');
   input.value='light.living';input.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true}));
 }''')
 assert page.evaluate("() => editor._config.tiles[2].entities") == ['light.living']
 # Group selection without native picker
 page.evaluate('''() => {
   const panel=editor.shadowRoot.querySelectorAll('.tile-item')[1];panel.querySelector('[data-action=expand-tile]').click();
   const sel=editor.shadowRoot.querySelectorAll('.tile-item')[1].querySelector('select[data-field=source]');sel.value='group';sel.dispatchEvent(new Event('change',{bubbles:true}));
   const manual=editor.shadowRoot.querySelectorAll('.tile-item')[1].querySelector('input[data-field=entity]');
   manual.value='group.windows';manual.dispatchEvent(new Event('change',{bubbles:true}));
 }''')
 assert page.evaluate("() => editor._config.tiles[1].entity") == 'group.windows'
 assert page.evaluate("() => card.shadowRoot.querySelectorAll('button.tile')[1].querySelector('.state').textContent") == 'Nicht verfügbar'
 assert not errs,errs
 b.close()
print('PASS: manual icon, multi-entity selection, and group picker fallbacks work without native selectors')

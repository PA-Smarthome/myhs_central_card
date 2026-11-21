"""Simulates Home Assistant native icon selector to check end-to-end persistence."""
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'tests/browser.html').read_text()
selector_stub='''<script>
 customElements.define('ha-selector', class extends HTMLElement {
   set selector(value){this._selector=value;}
   get selector(){return this._selector;}
   set value(value){this._value=value;}
   get value(){return this._value;}
 });
 </script>'''
html=html.replace('<script src="../dist/central-overview-card.js"></script>',selector_stub+'<script>'+(root/'dist/central-overview-card.js').read_text()+'</script>')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':390,'height':812})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(html)
 page.wait_for_function('window.editor && editor._config?.tiles?.length===16')
 page.evaluate('''() => {
    const row=editor.shadowRoot.querySelector('details.tile-item');row.open=true;
    const sel=row.querySelector('ha-selector[data-field=icon]');
    if(!sel || !sel.selector || !sel.selector.icon)throw Error('native HA icon selector missing');
    sel.dispatchEvent(new CustomEvent('value-changed',{detail:{value:'mdi:home-circle'},bubbles:true,composed:true}));
 }''')
 assert page.evaluate('editor._config.tiles[0].icon')=='mdi:home-circle'
 assert page.evaluate("editor.shadowRoot.querySelector('ha-selector').value")=='mdi:home-circle'
 page.evaluate('''() => editor.shadowRoot.querySelector('ha-selector').dispatchEvent(
    new CustomEvent('value-changed',{detail:{value:'phu:wallbox'},bubbles:true,composed:true}))''')
 assert page.evaluate('editor._config.tiles[0].icon')=='phu:wallbox'
 assert page.evaluate("editor.shadowRoot.querySelector('ha-selector').value")=='phu:wallbox'
 assert page.evaluate("editor.shadowRoot.querySelector('input[data-field=icon]').value")=='phu:wallbox'
 assert not errors,errors
 b.close()
print('OK: selector event and persistence for native and installed icon prefixes')

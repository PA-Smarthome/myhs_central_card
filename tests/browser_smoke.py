"""Editor visuals and essential UI interactions in Chromium (mock Home Assistant)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'tests/browser.html').read_text().replace('<script src="../dist/central-overview-card.js"></script>',
    '<script>'+(root/'dist/central-overview-card.js').read_text()+'</script>')
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':420,'height':900},device_scale_factor=1)
    errors=[]
    page.on('pageerror', lambda e:errors.append(str(e)))
    page.set_content(html)
    page.wait_for_function('window.editor && editor.shadowRoot.querySelectorAll(".tile-item").length===16')
    page.evaluate("()=>editor.addEventListener('config-changed',e=>card.setConfig(e.detail.config))")
    get=lambda js:page.evaluate(js)
    assert get('()=>card.shadowRoot.querySelectorAll("button.tile").length')==16
    assert get('()=>editor.shadowRoot.textContent.includes("Version 1.0.7")')
    assert get('()=>editor.shadowRoot.querySelectorAll("button[data-action=toggle-enabled]").length')==16
    assert get('()=>editor.shadowRoot.querySelectorAll("button[data-action=expand-tile]").length')==16
    assert get('()=>editor.shadowRoot.querySelector("#hide-all, #show-all, #tile-filter")===null')
    (root/'images').mkdir(exist_ok=True)
    page.locator('#visual-editor').screenshot(path=str(root/'images/editor-overview.png'))
    page.evaluate('()=>editor.shadowRoot.querySelector(".tile-item button[data-action=expand-tile]").click()')
    assert get('()=>editor.shadowRoot.querySelector(".tile-item button[data-action=expand-tile]").getAttribute("aria-expanded")')=='true'
    page.locator('#visual-editor').screenshot(path=str(root/'images/editor.png'))
    page.locator('#dashboard').screenshot(path=str(root/'images/preview.png'))
    page.evaluate('''()=>{const input=editor.shadowRoot.querySelector('.tile-item input[data-field="icon"]');
       input.value='mdi:shield-star';input.dispatchEvent(new Event('change',{bubbles:true}));}''')
    assert get('()=>editor._config.tiles[0].icon')=='mdi:shield-star'
    assert get('()=>editor.shadowRoot.querySelector(".tile-item button[data-action=expand-tile]").getAttribute("aria-expanded")')=='true'
    page.evaluate('()=>editor.shadowRoot.querySelector(".tile-item button[data-action=toggle-enabled]").click()')
    assert get('()=>editor._config.tiles[0].enabled') is False
    assert get('()=>card.shadowRoot.querySelectorAll("button.tile").length')==15
    page.evaluate('()=>editor.shadowRoot.querySelector(".tile-item button[data-action=toggle-enabled]").click()')
    assert get('()=>editor._config.tiles[0].enabled') is True
    assert get('()=>card.shadowRoot.querySelectorAll("button.tile").length')==16
    page.evaluate('()=>editor.shadowRoot.querySelector(".tile-item button[data-action=expand-tile]").click()')
    assert get('()=>editor.shadowRoot.querySelector(".tile-item button[data-action=expand-tile]").getAttribute("aria-expanded")')=='false'
    assert not errors,errors
    browser.close()
print('PASS: separate edit/eye controls, reversible visibility, icon change, collapse, 16 tiles, screenshots')

"""Runs a real Chromium UI smoke test using Playwright; screenshot uses synthetic demo entities."""
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1120,'height':1150},device_scale_factor=1)
    html=(root/'tests/browser.html').read_text().replace('<script src="../dist/central-overview-card.js"></script>', '<script>'+ (root/'dist/central-overview-card.js').read_text() +'</script>')
    page.goto('about:blank')
    page.set_content(html)
    page.wait_for_function('window.card && window.editor && window.card.shadowRoot.querySelectorAll("button.tile").length === 16')
    assert page.evaluate('window.card.shadowRoot.querySelectorAll("button.tile").length')==16
    assert page.evaluate('window.card.constructor.getStubConfig().type') is None
    assert page.evaluate('typeof window.editor.shadowRoot.querySelector("select[data-global=columns]")')=='object'
    # Capture before modifications, using generated demonstration data.
    (root/'images').mkdir(exist_ok=True)
    page.locator('#dashboard').screenshot(path=str(root/'images/preview.png'))
    page.locator('#visual-editor').screenshot(path=str(root/'images/editor.png'))
    # The icon is chosen via Home Assistant's native icon picker and persisted to the config.
    assert page.evaluate('window.editor.shadowRoot.querySelectorAll("ha-icon-picker").length')==16
    page.locator('central-overview-card-editor').evaluate('el=>{const d=el.shadowRoot.querySelectorAll("details")[0];const picker=d.querySelector("ha-icon-picker");picker.value="mdi:shield-check";picker.dispatchEvent(new CustomEvent("value-changed",{detail:{value:"mdi:shield-check"}}));}')
    assert page.evaluate('window.changes.at(-1).tiles[0].icon')=='mdi:shield-check'
    # A third-party icon is rejected to retain dependency-free MDI behaviour.
    page.locator('central-overview-card-editor').evaluate('el=>{const d=el.shadowRoot.querySelectorAll("details")[0];const picker=d.querySelector("ha-icon-picker");picker.value="local:external";picker.dispatchEvent(new CustomEvent("value-changed",{detail:{value:"local:external"}}));}')
    assert page.evaluate('window.changes.at(-1).tiles[0].icon')=='mdi:shield-home'
    # Visual editor: modify the number of columns, emit a complete config.
    page.locator('central-overview-card-editor').evaluate('el=>{const f=el.shadowRoot.querySelector("[data-global=columns]");f.value="3";f.dispatchEvent(new Event("change",{bubbles:true}));}')
    assert page.evaluate('window.changes.at(-1).columns')==3
    # Visual editor: tile colors are editable, too.
    page.locator('central-overview-card-editor').evaluate('el=>{const f=el.shadowRoot.querySelectorAll("details")[2].querySelector("select[data-field=tone]");f.value="purple";f.dispatchEvent(new Event("change",{bubbles:true}));}')
    assert page.evaluate('window.changes.at(-1).tiles[2].tone')=='purple'
    # Manually assigned entities via UI, with Home Assistant value-changed event.
    page.locator('central-overview-card-editor').evaluate('el=>{const d=el.shadowRoot.querySelectorAll("details")[1];d.querySelector("select[data-field=source]").value="selected";d.querySelector("select[data-field=source]").dispatchEvent(new Event("change",{bubbles:true}));}')
    page.locator('central-overview-card-editor').evaluate('el=>{const d=el.shadowRoot.querySelectorAll("details")[1];const picker=d.querySelector("ha-entity-picker[data-field=new-entity]");picker.value="binary_sensor.windows_a";picker.dispatchEvent(new CustomEvent("value-changed",{bubbles:true,detail:{value:"binary_sensor.windows_a"}}));d.querySelector("button[data-action=add-entity]").click();}')
    assert 'binary_sensor.windows_a' in page.evaluate('window.changes.at(-1).tiles[1].entities')
    browser.close()
print('PASS: Chromium rendered 16 tiles. Visual menu edits columns, palette and entity list; config-changed emitted; screenshots created.')

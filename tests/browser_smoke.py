"""Browser checks for MYHS Central Card and its Home Assistant visual editor.
Uses synthetic entities only; no real Home Assistant installation required.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1120, 'height': 1250}, device_scale_factor=1)
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    html = (root / 'tests/browser.html').read_text().replace(
        '<script src="../dist/central-overview-card.js"></script>',
        '<script>' + (root / 'dist/central-overview-card.js').read_text() + '</script>'
    )
    page.goto('about:blank')
    page.set_content(html)
    page.wait_for_function('window.card && window.editor && editor.shadowRoot.querySelectorAll("details.tile-item").length === 16')
    assert page.evaluate('card.shadowRoot.querySelectorAll("button.tile").length') == 16
    assert page.evaluate('editor.shadowRoot.querySelectorAll("ha-icon-picker").length') == 16
    assert page.evaluate('editor.shadowRoot.textContent.includes("Version 1.1.2")')

    (root / 'images').mkdir(exist_ok=True)
    page.locator('#dashboard').screenshot(path=str(root / 'images/preview.png'))
    page.locator('#visual-editor').screenshot(path=str(root / 'images/editor-overview.png'))
    page.locator('central-overview-card-editor').evaluate(
        'el => el.shadowRoot.querySelectorAll("details.tile-item")[0].open=true'
    )
    page.wait_for_timeout(100)
    page.locator('#visual-editor').screenshot(path=str(root / 'images/editor.png'))

    # Opening a tile is preserved when its data-source selection changes.
    page.locator('central-overview-card-editor').evaluate('''el => {
      const sel=el.shadowRoot.querySelector('details.tile-item select[data-field="source"]');
      sel.value='selected';sel.dispatchEvent(new Event('change',{bubbles:true}));
    }''')
    assert page.evaluate('window.changes.at(-1).tiles[0].source') == 'selected'
    assert page.evaluate('editor.shadowRoot.querySelector("details.tile-item").open')

    # Native picker events and multi-entity addition.
    page.locator('central-overview-card-editor').evaluate('''el => {
      const d=el.shadowRoot.querySelector('details.tile-item');
      d.querySelector('ha-icon-picker').dispatchEvent(new CustomEvent('value-changed',{
        detail:{value:'mdi:shield-check'}}));
      const picker=d.querySelector('ha-entity-picker[data-field="new-entity"]');
      picker.value='binary_sensor.new_window';
      picker.dispatchEvent(new CustomEvent('value-changed',{detail:{value:'binary_sensor.new_window'}}));
      d.querySelector('button[data-action="add-entity"]').click();
    }''')
    assert page.evaluate('window.changes.at(-1).tiles[0].icon') == 'mdi:shield-check'
    assert 'binary_sensor.new_window' in page.evaluate('window.changes.at(-1).tiles[0].entities')

    # Appearance settings in collapsed global panel.
    page.locator('central-overview-card-editor').evaluate('''el => {
      const x=el.shadowRoot.querySelector('select[data-global="columns"]');
      x.value='3';x.dispatchEvent(new Event('change',{bubbles:true}));
    }''')
    assert page.evaluate('window.changes.at(-1).columns') == 3

    # Local UI search must not change persisted card config.
    previous = page.evaluate('window.changes.length')
    page.locator('central-overview-card-editor').evaluate('''el => {
      const x=el.shadowRoot.querySelector('#tile-search');
      x.value='fenster';x.dispatchEvent(new Event('input',{bubbles:true}));
    }''')
    assert page.evaluate('Array.from(editor.shadowRoot.querySelectorAll("details.tile-item")).filter(x=>!x.hidden).length') == 1
    assert page.evaluate('window.changes.length') == previous

    # Duplicate/reorder/edit visibility, and adding a tile.
    page.locator('central-overview-card-editor').evaluate('''el => {
      const search=el.shadowRoot.querySelector('#tile-search');
      search.value='';search.dispatchEvent(new Event('input',{bubbles:true}));
      el.shadowRoot.querySelector('details.tile-item button[data-action="duplicate"]').click();
    }''')
    assert len(page.evaluate('window.changes.at(-1).tiles')) == 17
    assert page.evaluate('editor.shadowRoot.querySelectorAll("details.tile-item")[1].open')
    page.locator('central-overview-card-editor').evaluate('''el => {
      const newType=el.shadowRoot.querySelector('#new-kind');newType.value='windows';
      el.shadowRoot.querySelector('#add-tile').click();
      const last=el.shadowRoot.querySelectorAll('details.tile-item')[17];
      last.querySelector('button[data-action="up"]').click();
    }''')
    assert len(page.evaluate('window.changes.at(-1).tiles')) == 18
    assert page.evaluate('window.changes.at(-1).tiles[16].kind') == 'windows'
    page.locator('central-overview-card-editor').evaluate('''el => {
      const el16=el.shadowRoot.querySelectorAll('details.tile-item')[16];
      const toggle=el16.querySelector('input[data-field="enabled"]');
      toggle.checked=false;toggle.dispatchEvent(new Event('change',{bubbles:true}));
    }''')
    assert page.evaluate('window.changes.at(-1).tiles[16].enabled') is False
    assert page.evaluate('card.shadowRoot.querySelectorAll("button.tile").length') == 16
    assert not errors, errors
    browser.close()
print('PASS: 16 tiles, editor visuals, source selection, persistent open tile, entity/icon pickers, search, duplication, reorder, visibility, and global settings.')

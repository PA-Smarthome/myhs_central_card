"""Full editor lifecycle: repeated edits, hide/show, undo/redo, search, source selection."""
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'tests/browser.html').read_text().replace('<script src="../dist/central-overview-card.js"></script>',
    '<script>'+(root/'dist/central-overview-card.js').read_text()+'</script>')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(html)
 page.wait_for_function("editor && editor.shadowRoot.querySelectorAll('.tile-item').length===16")
 page.evaluate("()=>editor.addEventListener('config-changed',e=>{card.setConfig(e.detail.config);editor.setConfig(e.detail.config)})")
 get=lambda expr:page.evaluate(expr)
 fire=lambda expr:page.evaluate(expr)
 expand=lambda idx:fire(f"()=>editor.shadowRoot.querySelectorAll('.tile-item')[{idx}].querySelector('[data-action=expand-tile]').click()")
 eye=lambda idx:fire(f"()=>editor.shadowRoot.querySelectorAll('.tile-item')[{idx}].querySelector('[data-action=toggle-enabled]').click()")
 assert get("()=>card.shadowRoot.querySelectorAll('button.tile').length")==16
 # independent eye and open: never toggle accordion accidentally
 eye(0);assert get('()=>editor._config.tiles[0].enabled') is False
 assert get('()=>editor._openTile') is None
 eye(0);assert get('()=>editor._config.tiles[0].enabled') is True
 expand(0);assert get('()=>editor._openTile')==0
 eye(0);assert get('()=>editor._openTile')==0
 eye(0)
 assert get('()=>editor._config.tiles[0].enabled') is True
 # icon/source and navigation survive repeated rerenders
 fire('''()=>{const x=editor.shadowRoot.querySelector('.tile-item input[data-field=icon]');
 x.value='mdi:star';x.dispatchEvent(new Event('change',{bubbles:true}));}''')
 fire('''()=>{const x=editor.shadowRoot.querySelector('.tile-item input[data-field=label]');
 x.value='Testbereich';x.dispatchEvent(new Event('change',{bubbles:true}));}''')
 assert get('()=>editor._config.tiles[0].icon')=='mdi:star'
 assert get('()=>editor._config.tiles[0].label')=='Testbereich'
 assert get('()=>editor._openTile')==0
 fire('()=>editor.shadowRoot.querySelector("#undo").click()')
 assert get('()=>editor._config.tiles[0].label')!='Testbereich'
 fire('()=>editor.shadowRoot.querySelector("#redo").click()')
 assert get('()=>editor._config.tiles[0].label')=='Testbereich'
 expand(1)
 fire('''()=>{const x=editor.shadowRoot.querySelectorAll('.tile-item')[1].querySelector('select[data-field=source]');
 x.value='selected';x.dispatchEvent(new Event('change',{bubbles:true}));}''')
 assert get('()=>editor._openTile')==1
 assert get('()=>editor._config.tiles[1].source')=='selected'
 fire('''()=>{const x=editor.shadowRoot.querySelectorAll('.tile-item')[1].querySelector('input[data-field=manual-entity]');
 x.value='binary_sensor.window';editor.shadowRoot.querySelectorAll('.tile-item')[1].querySelector('[data-action=add-entity]').click();}''')
 assert get('()=>editor._config.tiles[1].entities')==['binary_sensor.window']
 # search is local and clearing it restores all tiles
 previous=get('()=>window.changes.length')
 fire('''()=>{const x=editor.shadowRoot.querySelector('#tile-search');x.value='fenster';x.dispatchEvent(new Event('input',{bubbles:true}));}''')
 assert get("()=>[...editor.shadowRoot.querySelectorAll('.tile-item')].filter(x=>!x.hidden).length")==1
 assert get('()=>window.changes.length')==previous
 fire('''()=>{const x=editor.shadowRoot.querySelector('#tile-search');x.value='';x.dispatchEvent(new Event('input',{bubbles:true}));}''')
 assert get("()=>[...editor.shadowRoot.querySelectorAll('.tile-item')].filter(x=>!x.hidden).length")==16
 # after save and recreate, eye can always restore
 saved=get('()=>structuredClone(editor._config)')
 page.evaluate('''(saved)=>{editor.remove();const fresh=document.createElement('central-overview-card-editor');
 document.getElementById('visual-editor').appendChild(fresh);window.editor=fresh;fresh.setConfig(saved);fresh.hass=hassMock;}''',saved)
 eye(0);eye(0)
 assert get('()=>editor._config.tiles[0].enabled') is True
 assert not errors,errors
 b.close()
print('PASS: iPhone editor, open/close, eye independent, undo/redo, icon, source, manual entity, search, reload')

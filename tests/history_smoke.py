"""Edit/undo/redo lifecycle with HA-style configuration echoes."""
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'tests/browser.html').read_text().replace(
 '<script src="../dist/central-overview-card.js"></script>',
 '<script>'+ (root/'dist/central-overview-card.js').read_text() +'</script>')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':390,'height':812},is_mobile=True,has_touch=True)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(html)
 page.wait_for_function('window.card && window.editor && editor._config?.tiles.length === 16')
 page.evaluate("() => editor.addEventListener('config-changed',e=>{card.setConfig(e.detail.config); editor.setConfig(e.detail.config);})")
 def val(expr):return page.evaluate(expr)
 def fire(js): page.evaluate(js)
 assert val('()=>card.shadowRoot.querySelectorAll("button.tile").length')==16
 # quick hide and unhide while editing before save
 fire('()=>editor.shadowRoot.querySelector("details.tile-item button[data-action=toggle-enabled]").click()')
 assert val('()=>editor._config.tiles[0].enabled')==False
 fire('()=>editor.shadowRoot.querySelector("details.tile-item button[data-action=toggle-enabled]").click()')
 assert val('()=>editor._config.tiles[0].enabled')==True
 # multiple distinct changes
 fire('''()=>{let row=editor.shadowRoot.querySelector('details.tile-item');row.open=true;
 let icon=row.querySelector('input[data-field="icon"]');icon.value='mdi:home-alert';icon.dispatchEvent(new Event('change',{bubbles:true}));}''')
 assert val('()=>editor._config.tiles[0].icon')=='mdi:home-alert'
 fire('''()=>{let row=editor.shadowRoot.querySelector('details.tile-item');
 let title=row.querySelector('input[data-field="label"]');title.value='Neuer Titel';title.dispatchEvent(new Event('change',{bubbles:true}));}''')
 assert val('()=>editor._config.tiles[0].label')=='Neuer Titel'
 assert val('()=>editor._undoStack.length')>=4
 # undo title then icon and redo icon then title
 fire('()=>editor.shadowRoot.querySelector("#undo").click()')
 assert val('()=>editor._config.tiles[0].label')!='Neuer Titel'
 assert val('()=>editor._config.tiles[0].icon')=='mdi:home-alert'
 fire('()=>editor.shadowRoot.querySelector("#undo").click()')
 assert val('()=>editor._config.tiles[0].icon')!='mdi:home-alert'
 fire('()=>editor.shadowRoot.querySelector("#redo").click()')
 assert val('()=>editor._config.tiles[0].icon')=='mdi:home-alert'
 fire('()=>editor.shadowRoot.querySelector("#redo").click()')
 assert val('()=>editor._config.tiles[0].label')=='Neuer Titel'
 # Edit a tile, reset it, undo reset
 fire('()=>editor.shadowRoot.querySelector("details.tile-item button[data-action=reset-tile]").click()')
 assert val('()=>editor._config.tiles[0].label')!='Neuer Titel'
 fire('()=>editor.shadowRoot.querySelector("#undo").click()')
 assert val('()=>editor._config.tiles[0].label')=='Neuer Titel'
 # all hidden can be recovered in a single click without filter trap
 fire('()=>editor.shadowRoot.querySelector("#hide-all").click()')
 assert val('()=>card.shadowRoot.querySelectorAll("button.tile").length')==0
 fire('()=>editor.shadowRoot.querySelector("#show-all").click()')
 assert val('()=>card.shadowRoot.querySelectorAll("button.tile").length')==16
 # restoration after editor was closed and recreated from saved JSON
 saved=val('()=>JSON.parse(JSON.stringify(editor._config))')
 fire('''(saved)=>{let old=window.editor;old.remove();let next=document.createElement('central-overview-card-editor');document.querySelector('#visual-editor').appendChild(next);window.editor=next;next.setConfig(saved);next.hass=hassMock;}'''.replace('(saved)=>','(saved)=>')) if False else None
 page.evaluate('''(saved)=>{editor.remove();const fresh=document.createElement('central-overview-card-editor');document.getElementById('visual-editor').appendChild(fresh);window.editor=fresh;fresh.setConfig(saved);fresh.hass=hassMock;}''',saved)
 assert val('()=>editor._config.tiles[0].label')=='Neuer Titel'
 fire('()=>editor.shadowRoot.querySelector("details.tile-item button[data-action=toggle-enabled]").click()')
 assert val('()=>editor._config.tiles[0].enabled')==False
 fire('()=>editor.shadowRoot.querySelector("details.tile-item button[data-action=toggle-enabled]").click()')
 assert val('()=>editor._config.tiles[0].enabled')==True
 assert not errors, errors
 b.close()
print('PASS: multiple edits, native config echo, undo/redo, reset, all visible/hidden, reopen saved editor')

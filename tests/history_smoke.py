"""History and reversibility of hide/show actions."""
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'tests/browser.html').read_text().replace('<script src="../dist/central-overview-card.js"></script>',
 '<script>'+(root/'dist/central-overview-card.js').read_text()+'</script>')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':390,'height':812})
 page.set_content(html)
 page.wait_for_function('editor && editor._config?.tiles.length===16')
 page.evaluate("()=>editor.addEventListener('config-changed',e=>editor.setConfig(e.detail.config))")
 cmd=lambda s:page.evaluate(s)
 cmd('()=>editor.shadowRoot.querySelector(".tile-item [data-action=toggle-enabled]").click()')
 assert cmd('()=>editor._config.tiles[0].enabled') is False
 cmd('()=>editor.shadowRoot.querySelector("#undo").click()')
 assert cmd('()=>editor._config.tiles[0].enabled') is True
 cmd('()=>editor.shadowRoot.querySelector("#redo").click()')
 assert cmd('()=>editor._config.tiles[0].enabled') is False
 cmd('()=>editor.shadowRoot.querySelector(".tile-item [data-action=toggle-enabled]").click()')
 assert cmd('()=>editor._config.tiles[0].enabled') is True
 b.close()
print('PASS: undo/redo reverses visibility changes')

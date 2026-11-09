import json
import subprocess
from pathlib import Path

root = Path(__file__).parent
session = 'modulo-controls-update'
checks = []

def cli(*args):
    result = subprocess.run(['agent-browser', '--session', session, *args], text=True, capture_output=True, check=True)
    return result.stdout

def evaluate(script):
    result = json.loads(cli('eval', '--json', script))
    assert result['success'], result
    return result['data']['result']

def check(name, script):
    result = evaluate(script)
    assert result, (name, result)
    checks.append(name)

def open_page(slug, controller):
    cli('open', f'http://modulo.localhost:1355/components/{slug}')
    cli('wait', '--fn', f'window.{controller} !== undefined')

def click(name):
    cli('find', 'role', 'button', 'click', '--name', name, '--exact')

def switch(name):
    cli('find', 'role', 'switch', 'click', '--name', name, '--exact')

def capture(name):
    cli('screenshot', str(root / name))

cli('set', 'viewport', '1440', '1000')
open_page('elastic-slider', 'elasticSlider')
cli('focus', '[role=combobox]')
cli('press', 'ArrowDown')
cli('press', 'End')
cli('press', 'Enter')
cli('wait', '--fn', 'window.elasticSlider.snapshot().orientation === "vertical"')
check('Dropdown keyboard selection reaches vertical slider', 'window.elasticSlider.snapshot().orientation === "vertical"')
cli('focus', 'input[aria-label=Value]')
cli('press', 'ArrowRight')
check('Custom range updates the bounded preview value', 'window.elasticSlider.snapshot().value === 70')
click('More preview actions')
cli('wait', '[role="menu"]')
cli('find', 'role', 'menuitemcheckbox', 'click', '--name', 'Reduce motion', '--exact')
check('Action menu preference updates runtime', 'window.elasticSlider.snapshot().reducedMotion')
cli('press', 'Escape')
cli('wait', '--fn', 'document.activeElement.getAttribute("aria-label") === "More preview actions"')
check('Escape returns focus to action trigger', 'document.activeElement.getAttribute("aria-label") === "More preview actions"')
switch('Disable control')
check('Disable switch disables preview and value input', 'document.querySelector("[role=slider][aria-label=Level]").getAttribute("aria-disabled") === "true" && document.querySelector("input[aria-label=Value]").disabled')
switch('Disable control')
capture('controls-desktop.png')

open_page('liquid-cluster', 'liquidCluster')
cli('wait', '--fn', '!window.liquidCluster.snapshot().framePending')
check('Notification starts joined in canvas renderer', 'window.liquidCluster.snapshot().separation === 0 && window.liquidCluster.snapshot().renderer === "canvas"')
capture('liquid-joined-desktop.png')
click('Open notification actions')
cli('wait', '--fn', '!window.liquidCluster.snapshot().framePending')
check('Notification activation separates card and Clear', 'window.liquidCluster.snapshot().separation === 1 && document.querySelector("[data-item-id=clear]").getBoundingClientRect().left > document.querySelector("[data-item-id=notification]").getBoundingClientRect().right')
capture('liquid-separated-desktop.png')

row_segments = '''(() => {
  const canvas = document.querySelector('.liquid-cluster__canvas');
  const row = canvas.getContext('2d').getImageData(0, Math.floor(canvas.height / 2), canvas.width, 1).data;
  let segments = 0, inside = false;
  for(let x = 0; x < canvas.width; x++) { const next = row[x * 4 + 3] > 100; if(next && !inside) segments++; inside = next; }
  return segments;
})()'''
assert evaluate(row_segments) == 2
switch('Reduce motion')
evaluate('window.liquidCluster.setSeparation(.35)')
cli('wait', '--fn', 'window.liquidCluster.snapshot().renderedSeparation === .35')
assert evaluate(row_segments) == 1
checks.append('Intermediate geometry has one connecting bridge; separated geometry has two silhouettes')
capture('liquid-bridge-desktop.png')
switch('Reduce motion')
click('Separate')
click('Join')
cli('wait', '--fn', '!window.liquidCluster.snapshot().framePending')
check('Rapid reversal settles back to one joined rectangle', 'window.liquidCluster.snapshot().renderedSeparation === 0')

bounds = evaluate('(() => {const r = document.querySelector("[aria-label=\\"Liquid cluster preview\\"]").getBoundingClientRect(); return {x:r.left+60,y:r.top+60};})()')
cli('mouse', 'move', str(round(bounds['x'])), str(round(bounds['y'])))
cli('mouse', 'down', 'right')
cli('mouse', 'up', 'right')
cli('wait', '[role=menu]')
check('Real right-click opens custom context menu', 'document.querySelector("[role=menu]").textContent.includes("Reveal Clear")')
capture('context-menu.png')
cli('find', 'role', 'menuitem', 'click', '--name', 'Reveal Clear', '--exact')
cli('wait', '--fn', 'window.liquidCluster.snapshot().separation === 1 && !window.liquidCluster.snapshot().framePending')
cli('focus', '[data-item-id=clear]')
cli('press', 'Enter')
check('Keyboard Clear dismisses notification and removes its targets', 'document.body.textContent.includes("No notifications") && document.querySelector(".liquid-cluster").closest("[inert]") !== null')
click('Reset')
check('Reset restores notification', 'document.querySelector(".liquid-cluster").closest("[inert]") === null')
switch('Disable actions')
check('Disabled notification targets stay inert', 'Array.from(document.querySelectorAll(".liquid-cluster__button")).every(button => button.disabled)')
switch('Disable actions')
click('More preview actions')
capture('actions-menu.png')
cli('press', 'Escape')

for width in [390, 320]:
    cli('set', 'viewport', str(width), '1000')
    click('Separate')
    cli('wait', '--fn', '!window.liquidCluster.snapshot().framePending')
    check(f'Notification fits at {width}px', 'document.documentElement.scrollWidth <= innerWidth && Array.from(document.querySelectorAll(".liquid-cluster__button")).every(button => {const r=button.getBoundingClientRect(); return r.left >= 0 && r.right <= innerWidth;})')
    check(f'Notification text stays inside card at {width}px', '(() => {const card=document.querySelector("[data-item-id=notification]").getBoundingClientRect(); return Array.from(document.querySelectorAll("[data-item-id=notification] span,strong")).filter(element => getComputedStyle(element).display !== "none").every(element => {const r=element.getBoundingClientRect(); return r.left >= card.left && r.right <= card.right && r.top >= card.top && r.bottom <= card.bottom;});})()')
    check(f'Notification mask aligns with targets at {width}px', '(() => {if(window.liquidCluster.snapshot().renderer !== "canvas") return false; const canvas=document.querySelector(".liquid-cluster__canvas"), row=canvas.getContext("2d").getImageData(0,canvas.height/2,canvas.width,1).data, origin=canvas.getBoundingClientRect().left; const edges=[]; let inside=false; for(let x=0;x<canvas.width;x++){const next=row[x*4+3]>100;if(next!==inside)edges.push(origin+x);inside=next;} const targets=Array.from(document.querySelectorAll(".liquid-cluster__button")).flatMap(button=>{const r=button.getBoundingClientRect();return [r.left,r.right];}); return edges.length===4 && edges.every((edge,i)=>Math.abs(edge-targets[i])<=1);})()')
    evaluate('scrollTo(0,document.querySelector("#preview").getBoundingClientRect().top+scrollY-15)')
    capture(f'liquid-{width}.png')
    click('Reset')

for slug, controller in [('elastic-slider', 'elasticSlider'), ('snap-rail', 'snapRail')]:
    cli('set', 'viewport', '390', '1000')
    open_page(slug, controller)
    check(f'{slug} narrow controls fit', 'document.documentElement.scrollWidth <= innerWidth')
    capture(f'{slug}-390.png')
    cli('set', 'viewport', '1440', '1000')
    capture(f'{slug}-desktop.png')

open_page('liquid-cluster', 'liquidCluster')
click('Separate')
cli('set', 'media', 'dark', 'reduced-motion')
check('Hot system reduced motion stops the liquid spring', 'window.liquidCluster.snapshot().reducedMotion && !window.liquidCluster.snapshot().framePending')
check('System reduced motion also disables notification dismissal travel', 'getComputedStyle(document.querySelector("[data-reduced-motion]")).transitionDuration === "0s"')
click('Join')
check('Reduced motion applies joined geometry immediately', 'window.liquidCluster.snapshot().renderedSeparation === 0')
errors = json.loads(cli('errors', '--json'))
(root / 'browser-errors.json').write_text(json.dumps(errors, indent=2) + '\n')
(root / 'checks.json').write_text(json.dumps({'passed': checks, 'count': len(checks)}, indent=2) + '\n')
print(f'Passed {len(checks)} focused browser checks.')

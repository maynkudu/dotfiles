import json
import subprocess
from pathlib import Path

folder = Path(__file__).parent
evidence = []

def browser(*args):
    arguments = [str(round(arg)) if isinstance(arg, float) else str(arg) for arg in args]
    result = subprocess.run(['agent-browser', '--session', 'apple-motion-review', '--json', *arguments], text=True, capture_output=True, check=True)
    data = json.loads(result.stdout)
    if not data.get('success'):
        raise RuntimeError(data)
    return data.get('data', {})

def evaluate(expression):
    return browser('eval', expression).get('result')

def record(name):
    state = evaluate('window.motionLab.inspect()')
    evidence.append({'scenario': name, 'state': state})
    return state

def rect(selector):
    return evaluate(f'document.querySelector({json.dumps(selector)}).getBoundingClientRect().toJSON()')

def settled():
    browser('wait', '--fn', '!window.motionLab.inspect().lifecycle.rafPending')

evaluate('window.qaPointerIds = {}; document.querySelectorAll("[role=slider]").forEach(el => el.addEventListener("pointerdown", event => { window.qaPointerIds[el.id] = event.pointerId; }))')
browser('focus', '#brightness')
browser('press', 'End')
r = rect('#brightness')
x, y = r['x'] + r['width']/2, r['y'] + r['height']/2
browser('mouse', 'move', x, y)
browser('mouse', 'down')
browser('mouse', 'move', x, y - 110)
state = record('upper endpoint while dragging')
assert state['brightness']['value'] == 100
assert -48 < state['brightness']['renderedOvershoot'] < 0
browser('screenshot', str(folder / 'upper-stretch.png'))
evaluate('window.qaHoldAt = performance.now()')
browser('wait', '--fn', 'performance.now() - window.qaHoldAt > 140')
browser('mouse', 'up')
state = record('release after stationary hold')
assert state['brightness']['releaseVelocity'] == 0
settled()

browser('focus', '#brightness')
browser('press', 'Home')
browser('mouse', 'move', x, y)
browser('mouse', 'down')
browser('mouse', 'move', x, y + 120)
state = record('lower endpoint while dragging')
assert state['brightness']['value'] == 0
assert 0 < state['brightness']['renderedOvershoot'] < 48
browser('mouse', 'up')
settled()

browser('drag', '#snap', '[data-detent="2"]')
state = record('snap flick release')
assert state['snap']['destination'] == 'Right'
assert state['snap']['releaseVelocity'] > 0
r = rect('#snap-item')
browser('mouse', 'move', r['x'] + r['width']/2, r['y'] + r['height']/2)
before = record('before snap regrab')
browser('mouse', 'down')
after = record('snap regrab')
assert after['snap']['dragging']
browser('mouse', 'move', r['x'] + r['width']/2 - 65, r['y'] + r['height']/2)
evaluate('document.querySelector("#snap").releasePointerCapture(window.qaPointerIds.snap)')
browser('mouse', 'move', r['x'] + r['width']/2 - 66, r['y'] + r['height']/2)
state = record('lost pointer capture')
assert not state['snap']['dragging']
assert state['snap']['releaseVelocity'] == 0
browser('mouse', 'up')
settled()

browser('find', 'role', 'button', 'click', '--name', 'Merge', '--exact')
settled()
state = record('merged circles')
assert state['union']['gap'] == 38
browser('screenshot', str(folder / 'merged.png'))
browser('find', 'role', 'button', 'click', '--name', 'Separate', '--exact')
settled()
assert record('separated circles')['union']['gap'] == 148

browser('find', 'role', 'button', 'click', '--name', 'Play sequence', '--exact')
browser('find', 'role', 'checkbox', 'check', '--name', 'Reduce motion', '--exact')
state = record('reduced motion interrupts replay')
assert state['lifecycle']['reduced']
assert not state['lifecycle']['rafPending']
assert state['brightness']['renderedOvershoot'] == 0
browser('focus', '#brightness')
browser('press', 'Home')
assert record('reduced motion keyboard')['brightness']['value'] == 0
browser('set', 'media', 'light', 'reduced-motion')
state = record('hot system reduced motion')
assert state['lifecycle']['systemReduced']
browser('set', 'viewport', 390, 1200)
browser('screenshot', str(folder / 'mobile.png'))
assert evaluate('document.documentElement.scrollWidth <= innerWidth')
record('390 pixel layout')

(folder / 'browser-evidence.json').write_text(json.dumps(evidence, indent=2))
print(f'Passed {len(evidence)} focused browser observations. Evidence: {folder / "browser-evidence.json"}')

"""Focused browser checks for the prototype's evolving and elastic scene."""
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
BASE = ['agent-browser', '--session', 'interactive-art-23249c62a0f7']
results = {}


def browser(*args, source=None):
    result = subprocess.run([*BASE, *args], input=source, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr or result.stdout)
    return result.stdout


def evaluate(source):
    isolated = '(() => eval(' + json.dumps(source) + '))()'
    return json.loads(browser('eval', '--stdin', source=isolated))


def wait_for(expression):
    browser('wait', '--fn', expression)


browser('reload')
wait_for('Boolean(window.garden)')
browser('set', 'viewport', '1000', '820')
browser('mouse', 'move', '10', '10')
evaluate('garden.setTimeScale(0); garden.seek(150); garden.snapshot()')
before = evaluate('garden.snapshot().plants[3]')
browser('mouse', 'move', str(round(before['screen']['x'] + 25)), str(round(before['screen']['y'])))
wait_for('Math.abs(garden.snapshot().plants[3].tip.x - garden.snapshot().plants[3].rest.x) > 4')
hover = evaluate('garden.snapshot().plants[3]')
results['hover'] = {'displacement': abs(hover['tip']['x'] - hover['rest']['x']), 'root': hover['root']}
assert hover['root'] == before['root']

browser('mouse', 'move', '10', '10')
wait_for('Math.abs(garden.snapshot().plants[3].tip.x - garden.snapshot().plants[3].rest.x) < 2')
before_drag = evaluate('garden.snapshot().plants[3]')
browser('mouse', 'move', str(round(before_drag['screen']['x'])), str(round(before_drag['screen']['y'])))
browser('mouse', 'down')
browser('mouse', 'move', '940', '430')
wait_for('garden.snapshot().plants[3].tip.x - garden.snapshot().plants[3].rest.x > 40')
results['drag_samples'] = evaluate('''new Promise(resolve => {
  const samples = []; const start = performance.now();
  function sample() {
    const p = garden.snapshot().plants[3];
    samples.push({distance: Math.hypot(p.tip.x - p.rest.x, p.tip.y - p.rest.y), limit: p.maxPull,
      error: p.maxSegmentError, root: p.root});
    if (performance.now() - start < 1200) requestAnimationFrame(sample);
    else resolve({maxDistance: Math.max(...samples.map(p => p.distance)), limit: samples[0].limit,
      maxSegmentError: Math.max(...samples.map(p => p.error)), rootMoved: samples.some(p => p.root.x !== 578 || p.root.y !== 612)});
  } sample();
})''')
drag = results['drag_samples']
assert drag['maxDistance'] <= drag['limit'] + .001, drag
assert drag['maxSegmentError'] < .01, drag
assert not drag['rootMoved'], drag
browser('screenshot', str(ROOT / 'drag.png'))
browser('mouse', 'up')
browser('mouse', 'move', '10', '10')
wait_for('Math.hypot(garden.snapshot().plants[3].tip.x - garden.snapshot().plants[3].rest.x, garden.snapshot().plants[3].tip.y - garden.snapshot().plants[3].rest.y) < 2')
results['release'] = evaluate('''new Promise((resolve, reject) => {
  const samples = []; const deadline = performance.now() + 8000;
  function sample() {
    const state = garden.snapshot(), p = state.plants[3];
    samples.push(Math.hypot(p.tip.x-p.rest.x,p.tip.y-p.rest.y));
    if (samples.length > 45) samples.shift();
    if (samples.length === 45 && Math.max(...samples) < 2) resolve({drag: state.drag, settledMaxDistance: Math.max(...samples)});
    else if (performance.now() > deadline) reject(new Error('The flower did not settle after release'));
    else requestAnimationFrame(sample);
  } sample();
})''')
assert results['release']['drag'] is None

browser('snapshot', '-i')
browser('focus', '#bend')
browser('press', 'Enter')
wait_for('garden.snapshot().plants[3].tip.x - garden.snapshot().plants[3].rest.x > 8')
results['keyboard_bend'] = True
evaluate('garden.pause(); garden.seek(0); garden.snapshot()')
early = evaluate('garden.snapshot()')
evaluate('garden.seek(150); garden.snapshot()')
late = evaluate('garden.snapshot()')
assert early['plants'][2]['bloom'] == 0 and late['plants'][2]['bloom'] == 1
results['growth'] = {'early': early['plants'][2]['bloom'], 'late': late['plants'][2]['bloom']}
assert late['name'] == 'Day'
browser('screenshot', str(ROOT / 'day.png'))
night = evaluate('garden.seek(210); garden.snapshot()')
assert night['name'] == 'Night'
browser('screenshot', str(ROOT / 'night.png'))
repeat = evaluate('garden.seek(270); garden.snapshot()')
assert abs(repeat['daylight'] - late['daylight']) < 1e-10
results['cycle'] = {'day': late['daylight'], 'night': night['daylight'], 'repeat': repeat['daylight']}

results['pause'] = evaluate('''new Promise(resolve => {
  const start = garden.snapshot(); let frames = 0;
  function sample() { if (++frames < 12) requestAnimationFrame(sample);
    else { const end = garden.snapshot(); resolve({elapsed: end.elapsed-start.elapsed, renders: end.renderedFrames-start.renderedFrames}); } }
  sample();
})''')
assert results['pause'] == {'elapsed': 0, 'renders': 0}, results['pause']

evaluate('garden.resume(); garden.setTimeScale(1); garden.snapshot()')
browser('set', 'media', 'dark', 'reduced-motion')
wait_for('garden.snapshot().reducedMotion && !garden.snapshot().running')
results['reduced_motion'] = evaluate('''new Promise(resolve => {
  const start = garden.snapshot(); let frames = 0;
  function sample() { if (++frames < 12) requestAnimationFrame(sample);
    else { const end = garden.snapshot(); resolve({elapsed: end.elapsed-start.elapsed, renders: end.renderedFrames-start.renderedFrames, reduced: end.reducedMotion}); } }
  sample();
})''')
assert results['reduced_motion'] == {'elapsed': 0, 'renders': 0, 'reduced': True}
browser('set', 'media', 'dark')
wait_for('!garden.snapshot().reducedMotion && garden.snapshot().running')
results['preference_resumed'] = True

browser('set', 'viewport', '390', '720', '2')
evaluate('garden.pause(); garden.seek(150); garden.snapshot()')
results['phone_viewport'] = evaluate('({overflow: document.documentElement.scrollWidth > innerWidth, width: garden.snapshot().width, height: garden.snapshot().height, bitmap: [document.querySelector("canvas").width,document.querySelector("canvas").height]})')
assert not results['phone_viewport']['overflow']
browser('screenshot', str(ROOT / 'phone.png'))

evaluate('garden.resume(); garden.destroy(); garden.destroy(); garden.snapshot()')
results['cleanup'] = evaluate('''new Promise(resolve => {
  const start = garden.snapshot(); let frames = 0;
  function sample() { if (++frames < 12) requestAnimationFrame(sample);
    else { const end = garden.snapshot(); resolve({destroyed: end.destroyed, running: end.running, renders: end.renderedFrames-start.renderedFrames}); } }
  sample();
})''')
assert results['cleanup'] == {'destroyed': True, 'running': False, 'renders': 0}
results['browser_errors'] = browser('errors').strip()
results['browser_console'] = browser('console').strip()
(ROOT / 'verification.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))

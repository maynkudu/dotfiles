"""Focused checks for the actual local garden, using the task's Agent Browser session."""
import base64
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
BROWSER = ['agent-browser', '--session', 'interactive-art-page-2a9456764711']
results = {}


def browser(*args, source=None):
    run = subprocess.run([*BROWSER, *args], input=source, capture_output=True, text=True, timeout=45)
    if run.returncode:
        raise RuntimeError(run.stderr or run.stdout)
    return run.stdout


def evaluate(source):
    return json.loads(browser('eval', '--stdin', source='(() => eval(' + json.dumps(source) + '))()'))


def wait_for(expression):
    browser('wait', '--fn', expression)


def point():
    return evaluate("(() => { const r = document.querySelector('canvas').getBoundingClientRect(); const p = garden.snapshot().targets[3].screen; return { x:r.left+p.x, y:r.top+p.y }; })()")


def move(p):
    browser('mouse', 'move', str(round(p['x'])), str(round(p['y'])))


browser('reload')
wait_for('Boolean(window.garden) && garden.snapshot().inView')
browser('set', 'viewport', '1200', '1100')
browser('mouse', 'move', '5', '5')
evaluate('garden.setTimeScale(0); garden.seek(150); garden.resume(); true')
wait_for('garden.snapshot().running')
p = point()
move({'x': p['x'] + 25, 'y': p['y']})
wait_for('Math.abs(garden.snapshot().details.plants[3].tip.x - garden.snapshot().details.plants[3].rest.x) > 4')
results['hover'] = evaluate('garden.snapshot().details.plants[3]')
assert results['hover']['root'] == {'x': 578, 'y': 612}

browser('mouse', 'move', '5', '5')
wait_for('Math.abs(garden.snapshot().details.plants[3].tip.x - garden.snapshot().details.plants[3].rest.x) < 2')
evaluate('garden.seek(150); true')
p = point()
move(p)
browser('mouse', 'down')
wait_for("garden.snapshot().drag === 'flower-4'")
move({'x': 1140, 'y': p['y'] + 180})
wait_for('garden.snapshot().details.plants[3].tip.x - garden.snapshot().details.plants[3].rest.x > 40')
results['extreme_pull'] = evaluate('''new Promise(resolve => {
  const samples = [], start = performance.now();
  function sample() {
    const p = garden.snapshot().details.plants[3];
    samples.push({ distance: Math.hypot(p.tip.x-p.rest.x,p.tip.y-p.rest.y), error: p.maxSegmentError, root: p.root, limit: p.maxPull });
    if (performance.now()-start < 1200) requestAnimationFrame(sample);
    else resolve({ maxDistance: Math.max(...samples.map(p=>p.distance)), limit: samples[0].limit,
      maxSegmentError: Math.max(...samples.map(p=>p.error)), rootMoved: samples.some(p=>p.root.x!==578||p.root.y!==612) });
  } sample();
})''')
pull = results['extreme_pull']
assert pull['maxDistance'] <= pull['limit'] + .001, pull
assert pull['maxSegmentError'] < .01, pull
assert not pull['rootMoved'], pull
browser('screenshot', str(ROOT / 'page-pull.png'), '--full')
browser('mouse', 'up')
browser('mouse', 'move', '5', '5')
results['release'] = evaluate('''new Promise((resolve, reject) => {
  const samples = [], deadline = performance.now()+8000;
  function sample() {
    const s = garden.snapshot(), p = s.details.plants[3];
    samples.push(Math.hypot(p.tip.x-p.rest.x,p.tip.y-p.rest.y));
    if (samples.length > 30) samples.shift();
    if (samples.length === 30 && Math.max(...samples)<2) resolve({drag:s.drag, settledMaxDistance:Math.max(...samples)});
    else if (performance.now()>deadline) reject(new Error('Flower did not settle'));
    else requestAnimationFrame(sample);
  } sample();
})''')
assert results['release']['drag'] is None
assert evaluate('garden.snapshot().elapsed') == 150
results['time_scale_does_not_stop_physics'] = True

browser('snapshot', '-i')
browser('focus', '[data-scene-object="flower-4"]')
browser('press', 'Enter')
wait_for('garden.snapshot().details.plants[3].tip.x - garden.snapshot().details.plants[3].rest.x > 8')
results['keyboard'] = True
browser('press', 'Tab')
evaluate('garden.seek(150); true')
move(point())
browser('mouse', 'down')
wait_for("garden.snapshot().drag === 'flower-4'")
evaluate('garden.pause(); true')
assert evaluate('garden.snapshot().drag') is None
browser('mouse', 'up')
results['pause_releases_drag'] = True

evaluate('garden.seek(0); true')
early = evaluate('garden.snapshot().details.plants[2].bloom')
evaluate('garden.seek(150); true')
late = evaluate('garden.snapshot().details.plants[2].bloom')
assert early == 0 and late == 1
results['growth'] = {'early_bloom': early, 'late_bloom': late}
browser('mouse', 'move', '5', '5')
browser('screenshot', str(ROOT / 'page-day.png'), '--full')
evaluate('garden.seek(210); true')
assert evaluate('document.querySelector(".time").textContent.startsWith("Night")')
browser('screenshot', str(ROOT / 'page-night.png'), '--full')
evaluate('garden.seek(270); true')
assert evaluate('document.querySelector(".time").textContent.startsWith("Day")')
results['repeated_day_night'] = True

results['pause'] = evaluate('''new Promise(resolve => {
  const start = garden.snapshot(); let frames = 0;
  function sample() { if (++frames<12) requestAnimationFrame(sample); else { const end=garden.snapshot(); resolve({elapsed:end.elapsed-start.elapsed,renders:end.renderedFrames-start.renderedFrames}); } }
  sample();
})''')
assert results['pause'] == {'elapsed': 0, 'renders': 0}
evaluate('garden.resume(); garden.setTimeScale(3); true')
browser('set', 'media', 'light', 'reduced-motion')
wait_for('garden.snapshot().reducedMotion && !garden.snapshot().running')
results['reduced_motion'] = evaluate('''new Promise(resolve => {
  const start=garden.snapshot(); let frames=0;
  function sample() { if (++frames<12) requestAnimationFrame(sample); else { const end=garden.snapshot(); resolve({elapsed:end.elapsed-start.elapsed,renders:end.renderedFrames-start.renderedFrames, disabled:[...document.querySelectorAll('.interactive-art-target')].every(b=>b.disabled)}); } }
  sample();
})''')
assert results['reduced_motion'] == {'elapsed': 0, 'renders': 0, 'disabled': True}
before_advance = evaluate('garden.snapshot().elapsed')
browser('snapshot', '-i')
browser('find', 'role', 'button', 'click', '--name', 'Advance 20 seconds')
assert evaluate('garden.snapshot().elapsed') == before_advance + 20
results['reduced_motion_time_control'] = True
browser('set', 'media', 'light')
wait_for('!garden.snapshot().reducedMotion && garden.snapshot().running')

evaluate("(() => { const spacer=document.createElement('div'); spacer.id='verification-spacer'; spacer.style.height='2200px'; document.body.append(spacer); window.scrollTo(0,document.body.scrollHeight); return true; })()")
wait_for('!garden.snapshot().inView && !garden.snapshot().running')
before = evaluate('garden.snapshot().elapsed')
evaluate('new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(()=>resolve(true))))')
assert evaluate('garden.snapshot().elapsed') == before
results['offscreen_pause'] = True
evaluate("document.getElementById('verification-spacer').remove(); window.scrollTo(0,0); true")
wait_for('garden.snapshot().inView && garden.snapshot().running')

browser('set', 'viewport', '390', '844', '2')
evaluate('garden.pause(); garden.seek(150); true')
results['mobile_layout'] = evaluate("({overflow:document.documentElement.scrollWidth>innerWidth,canvasTouch:getComputedStyle(document.querySelector('canvas')).touchAction,targetTouch:getComputedStyle(document.querySelector('.interactive-art-target')).touchAction, targets:document.querySelectorAll('.interactive-art-target').length})")
assert results['mobile_layout'] == {'overflow': False, 'canvasTouch': 'pan-y', 'targetTouch': 'none', 'targets': 6}
browser('screenshot', str(ROOT / 'page-mobile.png'), '--full')

(ROOT / 'page-checks.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps({key: value for key, value in results.items() if key != 'hover'}, indent=2))

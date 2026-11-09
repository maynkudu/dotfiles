"""Verify independent mounts, suspension, exports, and cleanup in the local page."""
import base64
import json
from pathlib import Path
import subprocess
from PIL import Image, ImageChops

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


browser('reload')
wait_for('Boolean(window.garden) && garden.snapshot().inView')
browser('set', 'viewport', '390', '844', '2')
evaluate('garden.setTimeScale(0); garden.seek(150); true')
results['mobile_focus_targets'] = evaluate("[...document.querySelectorAll('.interactive-art-target')].filter(b=>!b.hidden).map(b=>b.dataset.sceneObject)")
assert results['mobile_focus_targets'] == ['flower-2', 'flower-3', 'flower-4', 'flower-5']
browser('focus', '[data-scene-object="flower-4"]')
browser('press', 'Enter')
wait_for('garden.snapshot().details.plants[3].tip.x - garden.snapshot().details.plants[3].rest.x > 8')
results['mobile_keyboard'] = True

browser('set', 'viewport', '1200', '1100')
evaluate('garden.pause(); garden.seek(150); true')
evaluate('''(async () => {
  const module = await import('/src/interactive-art/scenes/garden.ts');
  window.gardenModule = module;
  window.mountFixture = (key, options={}) => {
    const host=document.createElement('div'); host.className='interactive-art-scene'; host.dataset.fixture=key;
    Object.assign(host.style,{position:'fixed',top:'0',left:key==='a'?'0':'220px',width:'200px',height:'136px'});
    const canvas=document.createElement('canvas'); host.append(canvas); document.body.append(host);
    return {host, garden:module.createGarden(canvas, options)};
  };
  window.fixtureA=mountFixture('a'); window.fixtureB=mountFixture('b',{seed:731});
  return true;
})()''')
wait_for('fixtureA.garden.snapshot().inView && fixtureB.garden.snapshot().inView')
evaluate('fixtureA.garden.pause(); window.aBefore=fixtureA.garden.snapshot(); window.bBefore=fixtureB.garden.snapshot(); true')
wait_for('fixtureB.garden.snapshot().renderedFrames > bBefore.renderedFrames + 5')
assert evaluate('fixtureA.garden.snapshot().elapsed === aBefore.elapsed')
results['independent_instances'] = True
evaluate('fixtureA.garden.destroy(); fixtureA.garden.destroy(); window.aBefore=fixtureA.garden.snapshot(); window.bBefore=fixtureB.garden.snapshot(); true')
wait_for('fixtureB.garden.snapshot().renderedFrames > bBefore.renderedFrames + 5')
results['local_cleanup'] = evaluate("({stopped:fixtureA.garden.snapshot().renderedFrames===aBefore.renderedFrames, targets:fixtureA.host.querySelectorAll('.interactive-art-target').length, siblingRunning:fixtureB.garden.snapshot().running})")
assert results['local_cleanup'] == {'stopped': True, 'targets': 0, 'siblingRunning': True}

results['saved_progress'] = evaluate('''(() => {
  const saved=JSON.parse(JSON.stringify(garden.saveState()));
  const restored=mountFixture('saved',{...gardenModule.readGardenState(saved),paused:true});
  const same=JSON.stringify(restored.garden.snapshot().details)===JSON.stringify(garden.snapshot().details);
  let invalidRejected=false;
  try { gardenModule.readGardenState({version:1,seed:0,elapsed:Infinity}); } catch { invalidRejected=true; }
  restored.garden.destroy(); restored.host.remove();
  return {same, invalidRejected};
})()''')
assert results['saved_progress'] == {'same': True, 'invalidRejected': True}
results['repeated_mount_cleanup'] = evaluate('''(() => {
  const destroyed=[];
  for(let i=0;i<4;i++) {
    const fixture=mountFixture('repeat'); fixture.garden.destroy();
    destroyed.push(fixture.garden.snapshot().destroyed && fixture.host.children.length===1);
    fixture.host.remove();
  }
  fixtureA.host.remove(); fixtureB.garden.destroy(); fixtureB.host.remove();
  return {allDestroyed:destroyed.every(Boolean),remainingTargets:document.querySelectorAll('.interactive-art-target').length};
})()''')
assert results['repeated_mount_cleanup'] == {'allDestroyed': True, 'remainingTargets': 6}

# Read the background scene through its same-origin popup, excluding visibility transitions.
evaluate("garden.setTimeScale(1); garden.resume(); window.open('about:blank','garden-visibility-check'); true")
tabs = json.loads(browser('--json', 'tab', 'list'))['data']['tabs']
popup = next(tab for tab in tabs if tab['url'] == 'about:blank')
browser('tab', popup['tabId'])
results['hidden_tab'] = evaluate("""new Promise(resolve => {
  const start=opener.garden.snapshot(); let frames=0;
  function sample() {
    if(++frames<12) requestAnimationFrame(sample);
    else { const end=opener.garden.snapshot(); resolve({hiddenBefore:start.hidden,hiddenAfter:end.hidden,elapsed:end.elapsed-start.elapsed,renders:end.renderedFrames-start.renderedFrames}); }
  } sample();
})""")
browser('tab', 'close')
assert results['hidden_tab'] == {'hiddenBefore': True, 'hiddenAfter': True, 'elapsed': 0, 'renders': 0}

evaluate('garden.pause(); garden.seek(150); true')
output_dir = ROOT / 'exports'
output_dir.mkdir(exist_ok=True)
layers = evaluate('gardenModule.GARDEN_LAYERS')
for name in ['whole', 'plants', *layers]:
    selected = None if name == 'whole' else ['stems', 'leaves', 'blossoms'] if name == 'plants' else [name]
    settings = {} if selected is None else {'layers': selected}
    data = evaluate('''(async () => {
      const blob = await garden.exportPNG(SETTINGS);
      return new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result);reader.onerror=reject;reader.readAsDataURL(blob);});
    })()'''.replace('SETTINGS', json.dumps(settings)))
    (output_dir / f'{name}.png').write_bytes(base64.b64decode(data.split(',', 1)[1]))

whole = Image.open(output_dir / 'whole.png').convert('RGBA')
plants = Image.open(output_dir / 'plants.png').convert('RGBA')
assert whole.size == plants.size == (1000, 680)
assert whole.getextrema()[3] == (255, 255)
assert plants.getextrema()[3] == (0, 255)
composite = Image.new('RGBA', whole.size)
for name in layers:
    layer = Image.open(output_dir / f'{name}.png').convert('RGBA')
    assert layer.size == whole.size
    composite = Image.alpha_composite(composite, layer)
composite.save(output_dir / 'reconstructed.png')
difference = ImageChops.difference(whole, composite)
maximum = max(high for low, high in difference.getextrema())
difference.convert('RGB').save(output_dir / 'difference.png')
results['layer_exports'] = {'size': list(whole.size), 'layers': layers, 'plants_alpha': list(plants.getextrema()[3]), 'maximum_channel_difference': maximum}
(ROOT / 'integration-checks.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
assert maximum <= 3, results['layer_exports']

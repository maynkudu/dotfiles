from pathlib import Path
import hashlib
import json
import os
import subprocess
import tempfile
import time

root = Path('/home/maynkudu/Code/Projects/modulo')
evidence = root / '.plannotator/controls-notification'
environment = os.environ.copy()
secrets = []
for line in (root / '.env.production').read_text().splitlines():
    if not line or line.startswith('#') or '=' not in line:
        continue
    key, value = line.split('=', 1)
    value = value.strip().strip('"\'')
    environment[key] = value
    if value:
        secrets.append(value)

def scrub(text):
    for value in secrets:
        text = text.replace(value, '[redacted]')
    return text

results = {'steps': [], 'completed': False}
with tempfile.TemporaryDirectory(prefix='modulo-publication-') as temporary:
    checkout = Path(temporary) / 'checkout'

    def run(arguments, cwd):
        started = time.monotonic()
        print('Running', ' '.join(arguments), flush=True)
        process = subprocess.run(arguments, cwd=cwd, env=environment, capture_output=True, text=True)
        record = {'command': arguments, 'exitCode': process.returncode,
                  'seconds': round(time.monotonic() - started, 2),
                  'output': scrub(process.stdout + process.stderr)}
        results['steps'].append(record)
        (evidence / 'publication-check.json').write_text(json.dumps(results, indent=2) + '\n')
        print('Exit', process.returncode, 'after', record['seconds'], 'seconds', flush=True)
        if process.returncode:
            print(record['output'][-6000:], flush=True)
            raise SystemExit(process.returncode)

    run(['git', 'clone', '--no-local', str(root), str(checkout)], temporary)
    results['revision'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=checkout, text=True).strip()
    lock = json.loads((checkout / 'components.lock.json').read_text())
    assert all(not (checkout / 'src/registry' / item['name']).exists() for item in lock['components'])
    results['startedWithoutSourceCopies'] = True
    run(['bun', 'install', '--frozen-lockfile'], checkout)
    run(['bun', 'run', 'components:sync'], checkout)
    results['sourceFilesVerified'] = sum(len(item['files']) for item in lock['components'])
    for item in lock['components']:
        for file in item['files']:
            path = checkout / 'src/registry' / item['name'] / file['path']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == file['sha256']
    run(['bun', 'run', 'typecheck'], checkout)
    run(['bun', 'run', 'build'], checkout)
    run(['git', 'status', '--short'], checkout)
    assert not results['steps'][-1]['output'].strip()
    results['completed'] = True
    results['temporaryCheckoutRemoved'] = True

(evidence / 'publication-check.json').write_text(json.dumps(results, indent=2) + '\n')
print('Fresh checkout passed. Temporary checkout removed.', flush=True)

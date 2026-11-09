from pathlib import Path

root = Path(__file__).resolve().parent
template = (root / 'preview-template.html').read_text()
engine = (root / 'garden.js').read_text()
assert template.count('/* GARDEN_ENGINE */') == 1
(root / 'preview.html').write_text(template.replace(
    '/* GARDEN_ENGINE */', engine.replace('export function createGarden', 'function createGarden')))

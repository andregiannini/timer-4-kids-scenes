#!/usr/bin/env python3
"""Package approved scene data for GitHub Releases; no app source is copied."""
import argparse
import hashlib
import json
import pathlib
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('scene', type=pathlib.Path, help='Directory containing scene.json and referenced images')
parser.add_argument('--out', type=pathlib.Path, required=True)
args = parser.parse_args()
manifest = json.loads((args.scene / 'scene.json').read_text())
scene_id = manifest['id']
revision = manifest['revision']
assert scene_id and len(scene_id) <= 60 and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in scene_id)
assert isinstance(revision, int) and revision > 0
assert manifest['schemaVersion'] == 1
assert not args.out.exists(), 'Output directory must be new (published revisions are immutable).'
args.out.mkdir(parents=True)
assets = []
for asset in manifest['assets']:
    name = asset['file']
    assert pathlib.Path(name).name == name and not name.startswith('.')
    assert pathlib.Path(name).suffix.lower() in ('.png', '.jpg', '.jpeg')
    data = (args.scene / name).read_bytes()
    assert 0 < len(data) <= 20_000_000
    assets.append(dict(file=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
    shutil.copyfile(args.scene / name, args.out / name)
assert len({a['file'] for a in assets}) == len(assets) and len(assets) <= 80
assert sum(a['bytes'] for a in assets) <= 80_000_000
manifest['assets'] = assets
# Non-optional opacity is explicit in the wire format.
for layer in manifest['layers'] + manifest['finale']:
    layer.setdefault('opacity', 1)
data = (json.dumps(manifest, indent=2) + '\n').encode()
(args.out / 'scene.json').write_bytes(data)
entry = dict(id=scene_id, revision=revision, manifest=f'{scene_id}-r{revision}/scene.json', sha256=hashlib.sha256(data).hexdigest())
print(json.dumps(entry, indent=2))

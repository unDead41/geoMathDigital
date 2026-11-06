import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath, pathToFileURL} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const digest = (algorithm, bytes) => createHash(algorithm).update(bytes).digest('hex');
const blob = bytes => digest('sha1', Buffer.concat([Buffer.from(`blob ${bytes.length}\0`), bytes]));

export function verifySourceAssets({directory = root} = {}) {
  const manifest = JSON.parse(fs.readFileSync(path.join(directory, 'assets/manifest.json'), 'utf8'));
  const seen = new Set();
  for (const asset of manifest.assets) {
    assert.ok(!seen.has(asset.source), `Duplicate source asset: ${asset.source}`);
    seen.add(asset.source);
    const bytes = fs.readFileSync(path.join(directory, asset.source));
    assert.equal(bytes.length, asset.bytes, `${asset.source}: original byte length changed`);
    assert.equal(digest('sha256', bytes), asset.sha256, `${asset.source}: content changed`);
    assert.equal(blob(bytes), asset.original_git_blob, `${asset.source}: source provenance changed`);
    for (const relative of [...(asset.development_outputs ?? []), ...(asset.publication_outputs ?? [])]) {
      assert.deepEqual(fs.readFileSync(path.join(directory, relative)), bytes,
        `${relative}: generated media differs from its canonical source`);
    }
  }
  const media = fs.readdirSync(path.join(directory, 'assets'), {recursive: true})
    .filter(name => /\.(?:mp3|svg|png|jpe?g|webp|woff2?|ttf)$/i.test(name))
    .map(name => `assets/${name.replaceAll(path.sep, '/')}`);
  assert.deepEqual([...seen].sort(), media.sort(), 'Every original runtime media file must have one manifest entry');
  const pin = JSON.parse(fs.readFileSync(path.join(directory, 'vendor/module-release.json'), 'utf8'));
  const module = fs.readFileSync(path.join(directory, 'vendor', pin.path));
  assert.equal(blob(module), pin.blob, 'Reviewed learning module pin changed');
  return {assets: manifest.assets.length, module_version: pin.version};
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const result = verifySourceAssets();
  console.log(`PASS: ${result.assets} original media assets, development/PWA byte parity, module ${result.module_version} pin.`);
}

import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {verifySourceAssets} from '../tools/check-assets.mjs';
import {copyRuntimeMedia} from '../tools/assets.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

test('original media and generated PWA/development copies preserve the reviewed byte fingerprints', () => {
  assert.deepEqual(verifySourceAssets(), {assets: 3, module_version: '1.6.2'});
});

test('a changed generated audio file is rejected, rather than silently becoming a new source', () => {
  const scratch = fs.mkdtempSync(path.join(os.tmpdir(), 'geomath-assets-'));
  try {
    const manifest = JSON.parse(fs.readFileSync(path.join(root, 'assets/manifest.json'), 'utf8'));
    fs.mkdirSync(path.join(scratch, 'assets/audio'), {recursive: true});
    fs.mkdirSync(path.join(scratch, 'assets/icons'), {recursive: true});
    for (const asset of manifest.assets) fs.copyFileSync(path.join(root, asset.source), path.join(scratch, asset.source));
    fs.writeFileSync(path.join(scratch, 'assets/manifest.json'), JSON.stringify(manifest));
    copyRuntimeMedia({root: scratch});
    for (const item of manifest.assets) {
      for (const relative of item.publication_outputs ?? []) {
        const destination = path.join(scratch, relative);
        fs.mkdirSync(path.dirname(destination), {recursive: true});
        fs.copyFileSync(path.join(scratch, item.source), destination);
      }
    }
    fs.mkdirSync(path.join(scratch, 'vendor'), {recursive: true});
    const pin = JSON.parse(fs.readFileSync(path.join(root, 'vendor/module-release.json'), 'utf8'));
    fs.copyFileSync(path.join(root, 'vendor/module-release.json'), path.join(scratch, 'vendor/module-release.json'));
    fs.copyFileSync(path.join(root, 'vendor', pin.path), path.join(scratch, 'vendor', pin.path));
    assert.doesNotThrow(() => verifySourceAssets({directory: scratch}));
    const asset = manifest.assets.find(item => item.source === 'assets/audio/menu.mp3');
    const output = path.join(scratch, asset.development_outputs[0]);
    assert.deepEqual(fs.readFileSync(output), fs.readFileSync(path.join(scratch, asset.source)));
    fs.appendFileSync(output, 'corrupt');
    assert.throws(() => verifySourceAssets({directory: scratch}), /generated media differs/);
  } finally {
    fs.rmSync(scratch, {recursive: true, force: true});
  }
});

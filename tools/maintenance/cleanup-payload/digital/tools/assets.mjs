import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

export const digitalRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

/** Source media lives only in assets; dist copies are disposable development output. */
export function copyRuntimeMedia({root = digitalRoot} = {}) {
  const manifest = JSON.parse(fs.readFileSync(path.join(root, 'assets/manifest.json'), 'utf8'));
  for (const asset of manifest.assets) {
    const source = path.join(root, asset.source);
    for (const relative of asset.development_outputs ?? []) {
      const destination = path.join(root, relative);
      fs.mkdirSync(path.dirname(destination), {recursive: true});
      fs.copyFileSync(source, destination);
    }
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  copyRuntimeMedia();
  console.log('Prepared development media from the canonical asset manifest.');
}

import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
// Regenerate the standalone learning module and token adapters before bundling
// the portal. The released vendor pin remains the reviewed runtime dependency.
for (const relative of ['module/tools/build.mjs', 'tools/standalone.mjs']) {
  execFileSync(process.execPath, [path.join(root, relative)], {cwd: root, stdio: 'inherit'});
}

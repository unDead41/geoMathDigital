#!/usr/bin/env python3
"""Consolidate Digital source and retire exact branch snapshots after verification."""
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = '6313d2281b7bf621ca380c3beb78bbc94bef63f6'
REPOSITORY = 'unDead41/geoMathDigital'
URL = 'https://github.com/' + REPOSITORY + '.git'
PAGES = 'main-digitalized'
PAGES_SHA = '287155b5414a38e57d722446616228569b1ede68'
CONCEPT = '4074dffc29cbd5a0922049c2ebb056ca3c293b31'
TAG = 'archive/digital-before-cleanup-20261106'
SOURCE = ROOT.parent / 'digital-cleanup-source'
CONFIG = json.loads((ROOT / 'tools/maintenance/branch-snapshot.json').read_text())


def command(*args, cwd=SOURCE, capture=False, env=None):
    p = subprocess.run(args, cwd=cwd, check=True, env=env, text=True,
                       stdout=subprocess.PIPE if capture else None)
    return p.stdout.strip() if capture else None


def git(*args, cwd=SOURCE, capture=False, env=None):
    return command('git', *args, cwd=cwd, capture=capture, env=env)


def refs():
    return {ref.removeprefix('refs/heads/'): sha for sha, ref in
            (line.split() for line in git('ls-remote', '--heads', URL, cwd=ROOT, capture=True).splitlines())}


def auth():
    value = base64.b64encode(('x-access-token:' + os.environ['GH_TOKEN']).encode()).decode()
    env = os.environ.copy()
    env.update(GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='http.https://github.com/.extraheader',
               GIT_CONFIG_VALUE_0='AUTHORIZATION: basic ' + value, GIT_TERMINAL_PROMPT='0')
    return env


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def replace(relative, before, after, expected=1):
    path = SOURCE / relative
    text = path.read_text()
    if text.count(before) != expected:
        raise RuntimeError('Changed source anchor: ' + relative + ': ' + before)
    path.write_text(text.replace(before, after))


def snapshot(ref=BASE):
    result = {}
    for record in git('ls-tree', '-r', '-l', ref, capture=True).splitlines():
        metadata, path = record.split('\t', 1)
        mode, kind, digest, size = metadata.split()
        if kind == 'blob':
            result[path] = {'blob': digest, 'bytes': int(size)}
    return result


def write(relative, text):
    path = SOURCE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def prepare():
    if os.environ.get('GITHUB_REPOSITORY') != REPOSITORY:
        raise RuntimeError('Wrong repository.')
    current = refs()
    for row in CONFIG:
        if current.get(row['name']) != row['sha']:
            raise RuntimeError('A source branch advanced: ' + row['name'])
    if SOURCE.exists():
        raise RuntimeError('Refusing to overwrite an existing worktree.')
    git('config', 'user.name', 'GeoMath maintenance', cwd=ROOT)
    git('config', 'user.email', '121752339+unDead41@users.noreply.github.com', cwd=ROOT)
    git('worktree', 'add', str(SOURCE), '-b', 'cleanup/verified-20261106', BASE, cwd=ROOT)
    before = snapshot()
    # One unique concept commit; all other source feature heads are ancestors
    # of BASE. Publication branches are historical generated snapshots.
    git('merge', '--no-ff', '--no-commit', CONCEPT)
    overlay = ROOT / 'tools/maintenance/cleanup-payload'
    for source in overlay.rglob('*'):
        if source.is_file():
            destination = SOURCE / source.relative_to(overlay)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)

    media = []
    for name in ('menu', 'map'):
        old = 'digital/dist/assets/audio/' + name + '.mp3'
        new = 'digital/assets/audio/' + name + '.mp3'
        data = (SOURCE / old).read_bytes()
        assert blob(data) == before[old]['blob']
        (SOURCE / new).parent.mkdir(parents=True, exist_ok=True)
        (SOURCE / old).rename(SOURCE / new)
        media.append({'source': 'assets/audio/' + name + '.mp3', 'bytes': len(data),
                      'sha256': sha256(data), 'original_git_blob': blob(data),
                      'original_path': old,
                      'development_outputs': ['dist/assets/audio/' + name + '.mp3'],
                      'publication_outputs': ['artifacts/pwa/assets/audio/' + name + '.mp3']})
    old = 'digital/pwa/icon.svg'
    data = (SOURCE / old).read_bytes()
    (SOURCE / 'digital/assets/icons').mkdir(parents=True, exist_ok=True)
    (SOURCE / old).rename(SOURCE / 'digital/assets/icons/icon.svg')
    media.append({'source': 'assets/icons/icon.svg', 'bytes': len(data),
                  'sha256': sha256(data), 'original_git_blob': blob(data),
                  'original_path': old, 'development_outputs': [],
                  'publication_outputs': ['artifacts/pwa/icons/icon.svg']})
    write('digital/assets/manifest.json', json.dumps({'schema_version': 1,
          'reviewed_base': BASE, 'assets': media}, indent=2) + '\n')

    replace('digital/tools/standalone.mjs', "import {buildOfflinePackage} from './offline-package.mjs';",
            "import {buildOfflinePackage} from './offline-package.mjs';\nimport {copyRuntimeMedia} from './assets.mjs';")
    replace('digital/tools/standalone.mjs', "const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');",
            "const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');\ncopyRuntimeMedia({root});")
    replace('digital/tools/standalone.mjs', 'dist/assets/audio/${name}.mp3', 'assets/audio/${name}.mp3')
    replace('digital/tools/offline-package.mjs', 'dist/assets/audio/${name}.mp3', 'assets/audio/${name}.mp3')
    replace('digital/tools/offline-package.mjs', "path.join(source,'icon.svg')", "path.join(source,'../assets/icons/icon.svg')")
    # Its temporary fixture supplies audio; the worker/icon remain reviewed
    # inputs owned by the real builder module, as in the existing test.
    replace('digital/tests/offline-package.test.mjs', 'dist/assets/audio', 'assets/audio', expected=3)

    package_path = SOURCE / 'digital/package.json'
    package = json.loads(package_path.read_text())
    assert package['version'] == '2.10.0'
    package['version'] = '2.10.1'
    package['scripts'].update({'build': 'node tools/build.mjs',
        'standalone': 'node tools/build.mjs', 'pretest': 'npm run build',
        'test:module': 'npm --prefix module test',
        'check': 'node tools/check.mjs && node tools/check-assets.mjs',
        'verify': 'npm test && npm run test:module && npm run prepare:pages && npm run check',
        'release:check': 'npm run verify'})
    package_path.write_text(json.dumps(package, indent=2) + '\n')
    lock_path = SOURCE / 'digital/package-lock.json'
    lock = json.loads(lock_path.read_text())
    lock['version'] = '2.10.1'
    lock['packages']['']['version'] = '2.10.1'
    lock_path.write_text(json.dumps(lock, indent=2) + '\n')
    module_path = SOURCE / 'digital/module/package.json'
    module_package = json.loads(module_path.read_text())
    module_package['scripts']['pretest'] = 'npm run build'
    module_path.write_text(json.dumps(module_package, indent=2) + '\n')

    generated = [p for p in before if p.startswith('digital/artifacts/')]
    generated += ['index.html', '.nojekyll', 'digital/GeoDecoder_Digital_V1.html',
        'digital/GeoDecoder_Digital_V2.html', 'digital/dist/GeoDecoder_Digital_V1.html',
        'digital/dist/GeoDecoder_Digital_V2.html', 'digital/dist/app.bundle.js',
        'digital/module/GeoDecoder_Modul_V1.html', 'digital/dist/design-tokens.css',
        'digital/dist/module-design.mjs', 'digital/module/src/central-tokens.mjs',
        'digital/module/src/design-tokens.css',
        'digital/docs/design-system-evidence/GeoDecoder_Design_System.html',
        'digital/backend/security/qa/GeoDecoder_Session_QA.html']
    old_modules = ['digital/vendor/module-v1.5.0.html', 'digital/vendor/module-v1.6.0.html',
                   'digital/vendor/module-v1.6.1.html']
    obsolete = []
    removed = []
    for name in dict.fromkeys(generated + old_modules + obsolete):
        path = SOURCE / name
        if path.exists():
            path.unlink()
            removed.append({'path': name, **before[name],
                            'reason': 'generated output' if name in generated else
                                      'archived superseded vendor snapshot' if name in old_modules else
                                      'obsolete monorepo branch maintenance'})
    for name in ('sources.json', 'receipt.json', 'PLAN.md'):
        old_path = SOURCE / 'migration' / name
        destination = SOURCE / 'docs/archive/repository-split-20261106' / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        old_path.rename(destination)
    shutil.rmtree(SOURCE / 'migration')
    replace('docs/REPOSITORY_SPLIT.md', '`migration/receipt.json`',
            '`docs/archive/repository-split-20261106/receipt.json`')
    gitignore = SOURCE / 'digital/.gitignore'
    gitignore.write_text(gitignore.read_text() + '\n# Reproducible build outputs\n'
        'GeoDecoder_Digital_V*.html\ndist/GeoDecoder_Digital_V*.html\ndist/app.bundle.js\n'
        'dist/assets/\nmodule/GeoDecoder_Modul_V1.html\ndist/design-tokens.css\n'
        'dist/module-design.mjs\nmodule/src/central-tokens.mjs\nmodule/src/design-tokens.css\n'
        'docs/design-system-evidence/GeoDecoder_Design_System.html\n'
        'backend/security/qa/GeoDecoder_Session_QA.html\n')
    root_ignore = SOURCE / '.gitignore'
    root_ignore.write_text(root_ignore.read_text() + '\n# Source branch is separate from the Pages snapshot\n/index.html\n/.nojekyll\n')
    pin_path = SOURCE / 'digital/vendor/module-release.json'
    pin = json.loads(pin_path.read_text())
    pin['historicalReleasesArchive'] = f'https://github.com/{REPOSITORY}/tree/{TAG}/digital/vendor'
    pin_path.write_text(json.dumps(pin, indent=2) + '\n')
    # The existing rename utility and its concurrency/credential tests remain
    # useful, but they must be scoped to this repository and an empty reviewed
    # plan, rather than the former Physical/monorepo branch registry.
    legacy = "['main-digitalized', 'main', 'sharing', 'codex/game-flow-rgb', 'codex/question-audio-elevenlabs', 'codex/question-bank-harmonised-lcd', 'codex/serial-unassign', 'testing/components']"
    replace('digital/tools/organize-branches.mjs', "const repository = 'unDead41/geodecoder';", "const repository = 'unDead41/geoMathDigital';")
    replace('digital/tools/organize-branches.mjs', legacy, "['main-digitalized', 'main']")
    replace('digital/tools/organize-branches.mjs', "!Array.isArray(input.renames) || !input.renames.length", "!Array.isArray(input.renames)")
    replace('digital/tools/organize-branches.mjs', 'only the private GeoDecoder source repository is allowed.', 'only the GeoMath Digital source repository is allowed.')
    branch_tests = SOURCE / 'digital/tests/branch-organization.test.mjs'
    text = branch_tests.read_text().replace('unDead41/geodecoder', 'unDead41/geoMathDigital').replace(legacy, "['main-digitalized', 'main']")
    text = text.replace('assert.equal(result.pending, 11);', 'assert.equal(result.pending, 0);').replace('assert.equal(mock.calls.length, 22);', 'assert.equal(mock.calls.length, 0);')
    branch_tests.write_text(text)
    write('digital/docs/branch-registry.json', json.dumps({'schemaVersion': 1,
        'repository': REPOSITORY, 'publicationBranch': PAGES,
        'protectedBranches': [PAGES, 'main'], 'renames': [],
        'historyArchive': 'https://github.com/' + REPOSITORY + '/tree/' + TAG}, indent=2) + '\n')
    write('digital/vendor/README.md', '# Reviewed learning module\n\n'
        'Only the current release named in `module-release.json` is kept here. '
        'Its original Git blob is verified by the build checks. Source geometry '
        'and learning UI live in `../module/`. Older snapshots and the '
        '`previousRelease` provenance field refer to the history archive: '
        f'[{TAG}](https://github.com/{REPOSITORY}/tree/{TAG}/digital/vendor).\n')
    changelog = SOURCE / 'digital/CHANGELOG.md'
    text = changelog.read_text()
    entry = ('## v2.10.1 — 6 November 2026\n\n'
        '- Consolidate the remaining UI/UX concept reference into main.\n'
        '- Keep one original copy of each audio/icon asset with byte fingerprints.\n'
        '- Generate offline aliases, PWA files, bundles and module/token adapters during build.\n'
        '- Archive retired branch snapshots and remove superseded vendor/build files.\n'
        '- Add clean-checkout builds and asset parity checks; preserve the reviewed runtime module.\n\n')
    changelog.write_text(text.replace('# GeoDecoder Digital changelog\n\n', '# GeoDecoder Digital changelog\n\n' + entry, 1))
    agents = SOURCE / 'AGENTS.md'
    agents.write_text(agents.read_text() + '\n## Clean source policy\n\n'
        '- Branches: `main` owns source; `main-digitalized` is the existing Pages snapshot.\n'
        '- Original runtime media is owned by `digital/assets/manifest.json`. Preserve fingerprints unless an asset change is intended.\n'
        '- Build outputs and compatibility HTML aliases are ignored, regenerated files. Never commit them to main.\n'
        '- Use `cd digital && npm ci && npm run verify` for a fresh checkout. Run the root scope checker before publishing.\n'
        '- Historical repository split records live at `docs/archive/repository-split-20261106/`.\n'
        '- Read `digital/docs/maintenance/CLEANUP.md` before restoring an archived branch.\n')
    concept_readme = SOURCE / 'digital/docs/uiux-redesign-concept/README.md'
    concept_readme.write_text('> Consolidated into `geoMathDigital/main` on 6 November 2026. '
        'This is design reference history. Use the current repository README/AGENTS for source ownership and branch instructions.\n\n'
        + concept_readme.read_text())
    module_readme = SOURCE / 'digital/module/README.md'
    module_readme.write_text('> `GeoDecoder_Modul_V1.html` ialah hasil build. Jalankan `npm run build` '
        'atau `npm test` dari folder ini untuk menjananya. Fail sumber, 11 model dan '
        'ujian kekal dalam repository; salinan HTML lama berada dalam tag arkib pembersihan.\n\n'
        + module_readme.read_text())

    protected = {}
    for name, item in before.items():
        if name in generated:
            continue
        if ((name.startswith('digital/dist/') and Path(name).suffix in ('.mjs', '.css', '.html'))
            or name.startswith('digital/module/src/') or name.startswith('supabase/')
            or name.startswith('digital/backend/') or name == 'digital/vendor/module-v1.6.2.html'
            or name == 'digital/docs/question_bank.reference.h'):
            protected[name] = item['blob']
    report = {'schema_version': 1, 'base': BASE, 'version': '2.10.1', 'status': 'awaiting verification',
        'pages': {'branch': PAGES, 'sha': PAGES_SHA, 'changed': False},
        'archive_tag': TAG, 'original_branches': CONFIG, 'concept_commit': CONCEPT,
        'removed_files': removed, 'protected_runtime_and_backend_blobs': protected,
        'baseline': {'files': len(before), 'bytes': sum(x['bytes'] for x in before.values())},
        'kept_duplicates': 'Historical evidence/fixtures and migration history retain their original context; deployment email templates and the current reviewed module pin remain versioned.'}
    write('digital/docs/maintenance/CLEANUP.json', json.dumps(report, indent=2) + '\n')
    write('digital/docs/maintenance/CLEANUP.md',
        '# Digital consolidation and cleanup\n\n'
        'The 6 November 2026 cleanup consolidates the remaining UI/UX concept reference, '
        'moves original media to `digital/assets/`, and regenerates build output from source.\n\n'
        'The active source is `main`. The existing `main-digitalized` Pages snapshot is retained. '
        'Other original branches are mapped in `CLEANUP.json` and preserved by '
        f'[`{TAG}`](https://github.com/{REPOSITORY}/tree/{TAG}).\n\n'
        'Source JavaScript, CSS, geometry, backend SQL, email templates and the current '
        'reviewed module preserve their original bytes. Historical evidence remains attached '
        'to its original report; equal bytes in those records do not imply an unused runtime asset.\n\n'
        'Run `npm ci` and `npm run verify` from `digital/`. The build creates the portal, '
        'module, media copies, PWA and compatibility HTML aliases. Those outputs are ignored '
        'on main; the current module pin and deployment email templates remain reviewed source inputs.\n\n'
        'To restore an old branch, fetch the archive tag and create a new review branch '
        'from its recorded SHA. Rebase or port only the needed source change onto current main. '
        'Original branch names are historical; they do not become active again automatically.\n')
    git('add', '-A')
    command('python3', 'tools/check_repository_scope.py')
    print('Prepared cleanup over the exact audited baseline.', flush=True)


def publish():
    report_path = SOURCE / 'digital/docs/maintenance/CLEANUP.json'
    report = json.loads(report_path.read_text())
    current = refs()
    for row in CONFIG:
        if current.get(row['name']) != row['sha']:
            raise RuntimeError('A branch changed while checks ran: ' + row['name'])
    for name, expected in report['protected_runtime_and_backend_blobs'].items():
        if blob((SOURCE / name).read_bytes()) != expected:
            raise RuntimeError('Protected source changed: ' + name)
    # Create the historical archive with all audited heads as parents. Its tree
    # is the original source tree, so old paths and exact branch commits survive.
    tree = git('rev-parse', BASE + '^{tree}', capture=True)
    parents = list(dict.fromkeys([row['sha'] for row in CONFIG] + [os.environ['GITHUB_SHA']]))
    args = ['commit-tree', tree]
    for parent in parents:
        args += ['-p', parent]
    args += ['-m', 'Archive Digital branches before source and asset cleanup']
    archive = git(*args, capture=True)
    existing = git('ls-remote', URL, 'refs/tags/' + TAG, capture=True)
    if existing:
        archive = existing.split()[0]
        git('fetch', 'origin', 'refs/tags/' + TAG)
        for row in CONFIG:
            git('merge-base', '--is-ancestor', row['sha'], archive)
    else:
        git('push', URL, archive + ':refs/tags/' + TAG, env=auth())
    report['archive_commit'] = archive
    log = (ROOT / 'cleanup-verification.log').read_text()
    failures = [int(x) for x in re.findall(r'# fail (\d+)', log)]
    assert failures and all(x == 0 for x in failures)
    report['status'] = 'verified'
    report['verification'] = {'node_tests': [int(x) for x in re.findall(r'# tests (\d+)', log)],
        'node_pass': [int(x) for x in re.findall(r'# pass (\d+)', log)],
        'node_fail': failures, 'scope': 'passed', 'asset_parity': 'passed',
        'build': 'passed', 'publication_preparation': 'passed'}
    git('add', '-A')
    current_files = git('ls-files', '-z', capture=True).split('\0')
    current_files = [p for p in current_files if p and (SOURCE / p).is_file()]
    report['clean_source'] = {'files_before_report_refresh': len(current_files),
        'bytes_before_report_refresh': sum((SOURCE / p).stat().st_size for p in current_files)}
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    git('add', '-A')
    command('python3', 'tools/check_repository_scope.py')
    git('diff', '--cached', '--check')
    git('commit', '-m', 'Consolidate Digital branches and canonical assets for v2.10.1')
    candidate = git('rev-parse', 'HEAD', capture=True)
    git('push', URL, candidate + ':refs/heads/cleanup/verified-20261106', env=auth())
    print(json.dumps({'candidate': candidate, 'archive': archive, 'report': report}, indent=2), flush=True)


def retire():
    if os.environ.get('GITHUB_REPOSITORY') != REPOSITORY:
        raise RuntimeError('Wrong repository.')
    git('config', 'user.name', 'GeoMath maintenance', cwd=ROOT)
    git('config', 'user.email', '121752339+unDead41@users.noreply.github.com', cwd=ROOT)
    current = refs()
    assert current[PAGES] == PAGES_SHA
    main = current['main']
    trigger = json.loads((ROOT / 'tools/maintenance/retire-trigger.json').read_text())
    assert trigger['verified_main_sha'] == main, 'Main advanced after final verification.'
    git('fetch', 'origin', '+refs/heads/*:refs/remotes/origin/*', cwd=ROOT)
    archived = git('ls-remote', URL, 'refs/tags/' + TAG, cwd=ROOT, capture=True).split()[0]
    git('fetch', 'origin', 'refs/tags/' + TAG, cwd=ROOT)
    for row in CONFIG:
        git('merge-base', '--is-ancestor', row['sha'], archived, cwd=ROOT)
        if row['name'] not in ('main', PAGES):
            assert current.get(row['name']) == row['sha'], row['name']
    # Verify main actually contains the merged concept and checked candidate.
    candidate = current['cleanup/verified-20261106']
    git('merge-base', '--is-ancestor', candidate, main, cwd=ROOT)
    git('merge-base', '--is-ancestor', CONCEPT, main, cwd=ROOT)
    allowed = {row['name'] for row in CONFIG} | {'chore/digital-cleanup', 'cleanup/audit-20261106', 'cleanup/verified-20261106'}
    unexpected = set(current) - allowed
    if unexpected:
        raise RuntimeError('New branches need review: ' + ', '.join(sorted(unexpected)))
    retired = {name: sha for name, sha in current.items() if name not in ('main', PAGES)}
    # Preserve temporary preparation/audit heads as well, before their refs go.
    tree = git('rev-parse', main + '^{tree}', cwd=ROOT, capture=True)
    args = ['commit-tree', tree]
    for parent in dict.fromkeys([main] + list(retired.values())):
        args += ['-p', parent]
    args += ['-m', 'Keep cleanup preparation history before retiring temporary refs']
    final_archive = git(*args, cwd=ROOT, capture=True)
    git('push', URL, final_archive + ':refs/tags/archive/digital-cleanup-preparation-20261106', cwd=ROOT, env=auth())
    args = ['push', '--atomic']
    for name, sha in retired.items():
        args.append('--force-with-lease=refs/heads/' + name + ':' + sha)
    args += [URL] + [':refs/heads/' + name for name in retired]
    git(*args, cwd=ROOT, env=auth())
    remaining = refs()
    assert remaining == {'main': main, PAGES: PAGES_SHA}
    print(json.dumps({'retired': retired, 'remaining': remaining,
                     'history_archive': archived, 'preparation_archive': final_archive}, indent=2))


if __name__ == '__main__':
    if sys.argv[1:] not in (['prepare'], ['publish'], ['retire']):
        raise SystemExit('Expected prepare, publish or retire.')
    {'prepare': prepare, 'publish': publish, 'retire': retire}[sys.argv[1]]()

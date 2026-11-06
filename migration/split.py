#!/usr/bin/env python3
"""Export platform-only history, validate it, and publish with fast-forward refs."""
import base64
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.migration-work'
CONFIG = json.loads((ROOT / 'migration/sources.json').read_text())
SOURCE = WORK / 'source'
OWNER = 'unDead41'
PLATFORMS = {
    'app': {
        'repository': 'geoMathApp',
        'paths': ['apps/geomath_flutter/', 'docs/geomath-app/',
                  'docs/geomath-app-prompts/', 'APP.md'],
        'base': 'app-uiux-refinement',
    },
    'digital': {
        'repository': 'geoMathDigital',
        'paths': ['digital/', 'supabase/', 'docs/DIGITAL_PUBLISHING.md',
                  'index.html', '.nojekyll', '.gitattributes'],
        'base': 'main-digitalized',
    },
}


def run(*args, cwd=ROOT, capture=False, env=None):
    result = subprocess.run(args, cwd=cwd, env=env, check=True,
                            stdout=subprocess.PIPE if capture else None,
                            text=True)
    return result.stdout.strip() if capture else None


def git(*args, cwd=SOURCE, capture=False, env=None):
    return run('git', *args, cwd=cwd, capture=capture, env=env)


def selected(platform):
    def owns(name):
        if platform == 'app':
            return name == 'app' or name.startswith('app-')
        return name.startswith(('digitalized-', 'digitalize/')) or name in (
            'main-digitalized', 'ui/ux-redesign-concept')
    return [x for x in CONFIG['branches'] if owns(x['name'])]


def auth_env():
    token = os.environ.get('GH_TOKEN')
    if not token:
        raise RuntimeError('A repository-scoped Actions token is required.')
    value = base64.b64encode(('x-access-token:' + token).encode()).decode()
    env = os.environ.copy()
    env.update(GIT_CONFIG_COUNT='1',
               GIT_CONFIG_KEY_0='http.https://github.com/.extraheader',
               GIT_CONFIG_VALUE_0='AUTHORIZATION: basic ' + value,
               GIT_TERMINAL_PROMPT='0')
    return env


def copy_bootstrap():
    for name in ('migration', '.github'):
        source = ROOT / name
        if source.exists():
            shutil.copytree(source, SOURCE / name, dirs_exist_ok=True)


def write_guidance(platform):
    app = platform == 'app'
    repo = PLATFORMS[platform]['repository']
    ownership = ('Flutter Android app, native UI, learning modules, classroom, '
                 'Duel, adaptive AI and bundled offline assets' if app else
                 'web portal, browser game, 3D learning modules, PWA assets '
                 'and Supabase backend source')
    entry = 'apps/geomath_flutter' if app else 'digital'
    checks = ('flutter pub get\nflutter analyze\nflutter test' if app else
              'npm ci\nnpm test\nnpm run build\nnpm run prepare:pages\nnpm run check')
    (SOURCE / 'README.md').write_text(
        f'# {repo}\n\nGeoMath: {ownership}.\n\n'
        '| Repository | Scope |\n| --- | --- |\n'
        '| [geoMathPhysical](https://github.com/unDead41/geoMathPhysical) | ESP32, RFID, LCD, wiring, printable resources |\n'
        '| [geoMathDigital](https://github.com/unDead41/geoMathDigital) | Web portal, browser game, learning and backend |\n'
        '| [geoMathApp](https://github.com/unDead41/geoMathApp) | Flutter app, Android, AI and offline assets |\n\n'
        f'## Run locally\n\n```powershell\ngit clone https://github.com/{OWNER}/{repo}.git\n'
        f'Set-Location {repo}/{entry}\n{checks}\n```\n\n'
        + ('Use the SDK version recorded in `apps/geomath_flutter/docs/TOOLCHAIN.md`. '
           'Android package identity remains `com.geomath.dev`. The App includes '
           'both the latest UI/UX refinement and bounded Easy/Medium/Hard AI battles.\n\n'
           if app else
           'The root `index.html` is the generated standalone entry. '
           'The complete editable portal is in `digital/`; Supabase migrations '
           'remain at `supabase/`. Existing Pages branches are retained as '
           'deployment snapshots. No hosted backend or Pages deployment is '
           'performed by this source migration.\n\n')
        + '## Source ownership\n\n`main` is the development integration branch of '
        f'**{repo}**. Every feature branch in this repository must contain only '
        'this platform. Read `AGENTS.md` and `docs/REPOSITORY_SPLIT.md` before editing. '
        'The original source layout is retained so existing build/test paths work.\n\n'
        'Historical documents and canonical SHA locks describe their original '
        'snapshots; they do not authorize development in another repository. '
        'Filtered feature history and exact original-to-new branch mappings are '
        'recorded in `migration/receipt.json`.\n')
    (SOURCE / 'AGENTS.md').write_text(
        f'# {repo} contributor guidance\n\n'
        f'- This repository owns {ownership}. Its `main` branch is this platform.\n'
        '- Firmware, GPIO, RFID, LCD, UID/NVS, wiring and printable hardware '
        'resources belong only to `unDead41/geoMathPhysical`.\n'
        + ('- Editable browser portal and deployed Supabase backend source '
           'belong only to `unDead41/geoMathDigital`. App offline HTML/JS and '
           'contract reference files are intentional versioned App assets.\n'
           '- App source stays at `apps/geomath_flutter/`; app design contracts '
           'stay at `docs/geomath-app/`. Read pubspec/lock, source locks and '
           'feature contracts before modifying runtime code. Preserve 11 models, '
           'server-authoritative Duel, actor-isolated storage and bounded AI.\n'
           '- Canonical regeneration may consume an explicitly supplied '
           'read-only pinned Digital snapshot outside this repository. Normal '
           'build, tests and offline use require only this repository.\n'
           '- Keep package identity, callback scheme and signing setup. Do '
           'not commit keystores, local SDK configuration or credentials.\n'
           '- For Dart changes run formatter, analyzer and relevant Flutter '
           'tests; for bundle changes run existing Node contract tests. '
           'Distinguish host checks, Android compilation, emulator and phone.\n'
           if app else
           '- Flutter/Dart source and Android projects belong only to '
           '`unDead41/geoMathApp`. Do not copy its application into this repo.\n'
           '- Portal source stays under `digital/`. The source tree includes '
           'its existing dist modules, build tools and assets. Preserve 11 '
           'learning models, formulas, card roles, Duel protocol and offline sync.\n'
           '- This repository owns shared Supabase schema, migrations and Edge '
           'Function source. App consumes its public versioned API. Never '
           'duplicate schema ownership in the App repository.\n'
           '- Run existing Node tests, build, publication preparation and '
           'static checks. Source pushes do not imply backend deployment or '
           'Pages publication. Obtain authorization for those operations.\n')
        + '- Check working tree and remote branch before editing. Preserve '
        'unrelated work; use explicit refs and do not force-push.\n'
        '- Run `python3 tools/check_repository_scope.py` before publication. '
        'Never import the mixed repository tree or merge another platform.\n'
        '- These instructions supersede historical monorepo branch/path '
        'assumptions in archived planning/handoff documents. New work must '
        'use the repository named above and its current `main`.\n')
    docs = SOURCE / 'docs'
    docs.mkdir(exist_ok=True)
    (docs / 'REPOSITORY_SPLIT.md').write_text(
        '# GeoMath repository ownership\n\nEffective 6 November 2026.\n\n'
        '- `geoMathPhysical`: firmware and physical learning hardware.\n'
        '- `geoMathDigital`: portal, browser game, web modules, PWA and backend.\n'
        '- `geoMathApp`: Flutter application and its bundled offline modules.\n\n'
        'Each repository is independently editable and buildable. Sharing a '
        'public backend API does not require sharing a source checkout. '
        'App bundle provenance and historical source locks retain their original '
        'hashes. Rebuilding an exported bundle is an explicit pinned-source '
        'maintenance operation, separate from normal Flutter build/test.\n\n'
        'Paths inside filtered history are intentionally retained. Original '
        'and filtered branch hashes appear in `migration/receipt.json`. Only '
        'platform-owned paths survive history filtering. Original mixed refs '
        'must be archived before their active Physical branches are retired. '
        'No source history on the original server is force-rewritten.\n\n'
        'Do not follow historical prompts that identify firmware `main`, '
        '`geodecoder` or a Pages mirror as the current source owner. Use the '
        'ownership list above. Production deployment is unchanged.\n')
    if app:
        # These are active instructions, not immutable evidence/provenance.
        app_instructions = SOURCE / 'docs/geomath-app/AGENTS.md'
        if app_instructions.exists():
            app_instructions.write_text((SOURCE / 'AGENTS.md').read_text())
        (SOURCE / 'APP.md').write_text(
            '# GeoMath App\n\nFlutter source: `apps/geomath_flutter/`. '
            'Build from this repository. Read the root README, AGENTS and '
            'repository separation map. The firmware and web source live in '
            'their own repositories.\n')
    (SOURCE / '.gitignore').write_text(
        '.migration-work/\n.worktrees/\n__pycache__/\n*.pyc\n'
        + ('**/.dart_tool/\n**/build/\n**/local.properties\n*.jks\n*.keystore\n'
           if app else '**/node_modules/\n.env\n.env.*\n!.env.example\n'
           'supabase/.temp/\n'))
    tools = SOURCE / 'tools'
    tools.mkdir(exist_ok=True)
    shutil.copyfile(ROOT / 'migration/check_repository_scope.py',
                    tools / 'check_repository_scope.py')
    (SOURCE / '.geomath-platform').write_text(platform + '\n')
    shutil.copyfile(ROOT / f'migration/{platform}-ci.yml',
                    SOURCE / '.github/workflows/validate.yml')


def assert_scope(platform, cwd=SOURCE, ref=None):
    files = (git('ls-tree', '-r', '--name-only', ref, cwd=cwd, capture=True)
             if ref else git('ls-files', cwd=cwd, capture=True)).splitlines()
    banned = ['main/', 'src/', 'print_labels/', 'tutorial/', 'platformio.ini',
              'platformio.local.ini.example', 'SAMBUNGAN.md', 'COMMANDS.md']
    banned += ['digital/', 'supabase/'] if platform == 'app' else ['apps/']
    bad = [p for p in files if any(p == x or p.startswith(x) for x in banned)]
    if bad:
        raise RuntimeError(f'Cross-platform files in {ref or platform}: {bad[:15]}')


def prepare(platform):
    settings = PLATFORMS[platform]
    expected_repo = f'{OWNER}/{settings["repository"]}'
    if os.environ.get('GITHUB_REPOSITORY') != expected_repo:
        raise RuntimeError('Workflow repository does not match destination.')
    if WORK.exists():
        raise RuntimeError('Migration workspace already exists; do not overwrite.')
    WORK.mkdir()
    bare = WORK / 'filtered.git'
    run('git', 'clone', '--mirror', CONFIG['source_url'], str(bare))
    rows = selected(platform)
    for row in rows:
        actual = git('rev-parse', f'refs/heads/{row["name"]}', cwd=bare, capture=True)
        if actual != row['sha']:
            raise RuntimeError(f'Source branch advanced: {row["name"]}; re-audit required.')
    args = ['git', 'filter-repo', '--force']
    for value in settings['paths']:
        args += ['--path', value]
    run(*args, cwd=bare)
    filtered = {}
    for row in rows:
        new_sha = git('rev-parse', f'refs/heads/{row["name"]}', cwd=bare, capture=True)
        assert_scope(platform, cwd=bare, ref=new_sha)
        filtered[row['name']] = new_sha
    run('git', 'clone', '--no-hardlinks', str(bare), str(SOURCE))
    git('config', 'user.name', 'GeoMath source migration')
    git('config', 'user.email', '121752339+unDead41@users.noreply.github.com')
    git('checkout', '-B', 'migration/assembled', filtered[settings['base']])
    if platform == 'app':
        git('merge', '--no-ff', '--no-commit', filtered['app-cloud-game'])
        git('commit', '-m', 'Merge adaptive AI into the latest GeoMath App UI/UX')
    assembled_parent = git('rev-parse', 'HEAD', capture=True)
    target = f'https://github.com/{expected_repo}.git'
    target_head = os.environ['GITHUB_SHA']
    git('fetch', target, 'refs/heads/main:refs/remotes/destination/main')
    if git('rev-parse', 'refs/remotes/destination/main', capture=True) != target_head:
        raise RuntimeError('Destination main advanced while preparing; re-run after review.')
    copy_bootstrap()
    write_guidance(platform)
    mapping = [{**row, 'filtered_sha': filtered[row['name']],
                'destination_branch': ('source/main-digitalized' if platform == 'digital'
                                       and row['name'] == 'main-digitalized' else row['name'])}
               for row in rows]
    receipt = {
        'schema_version': 1, 'platform': platform, 'date': CONFIG['date'],
        'source_repository': CONFIG['source_repository'],
        'destination_repository': expected_repo,
        'source_branches': mapping, 'assembled_parent': assembled_parent,
        'destination_parent': target_head,
        'verification': 'Existing platform checks must pass before publish phase.',
        'published': False,
    }
    (WORK / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    (SOURCE / 'migration/receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    git('add', '-A')
    assert_scope(platform)
    run('python3', 'tools/check_repository_scope.py', cwd=SOURCE)
    print(f'Prepared {expected_repo}: {len(mapping)} filtered feature branches.', flush=True)


def publish(platform):
    receipt = json.loads((WORK / 'receipt.json').read_text())
    if receipt['platform'] != platform:
        raise RuntimeError('Wrong receipt platform.')
    target = f'https://github.com/{receipt["destination_repository"]}.git'
    # Check source input leases again after the test/build interval.
    live = dict(line.split()[::-1] for line in
                run('git', 'ls-remote', '--heads', CONFIG['source_url'],
                    capture=True).splitlines())
    for row in receipt['source_branches']:
        if live.get('refs/heads/' + row['name']) != row['sha']:
            raise RuntimeError(f'Source branch advanced during verification: {row["name"]}')
    receipt['verification'] = 'All platform checks in separate-geomath.yml passed before publication.'
    receipt['published'] = True
    receipt['checks'] = (
        ['scope', 'dart-format', 'flutter-analyze', 'flutter-test',
         'node-canonical-adapter-tests', 'python-tooling-tests', 'android-debug-apk']
        if platform == 'app' else
        ['scope', 'npm-ci', 'npm-test', 'standalone-build', 'publication-prepare', 'static-check'])
    (SOURCE / 'migration/receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    git('add', '-A')
    assert_scope(platform)
    tree = git('write-tree', capture=True)
    commit = git('commit-tree', tree, '-p', receipt['destination_parent'],
                 '-p', receipt['assembled_parent'], '-m',
                 f'Separate verified GeoMath {platform} source and preserve platform history',
                 capture=True)
    git('update-ref', 'refs/heads/migration/published', commit)
    specs = [commit + ':refs/heads/main']
    for row in receipt['source_branches']:
        specs.append(row['filtered_sha'] + ':refs/heads/' + row['destination_branch'])
    # All destination feature refs are new; the main parent makes its update
    # a normal fast-forward. Never force any remote history.
    git('push', '--atomic', target, *specs, env=auth_env())
    receipt['published_main_sha'] = commit
    (WORK / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Published {receipt["destination_repository"]}@{commit}', flush=True)


if __name__ == '__main__':
    action, platform = sys.argv[1:]
    if platform not in PLATFORMS or action not in ('prepare', 'publish'):
        raise SystemExit('Usage: split.py prepare|publish app|digital')
    (prepare if action == 'prepare' else publish)(platform)

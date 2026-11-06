#!/usr/bin/env python3
"""Keep Digital source independent and prevent regenerated output being tracked."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
if (root / '.geomath-platform').read_text().strip() != 'digital':
    raise SystemExit('This checkout must identify the Digital platform.')
tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
banned = ('main/', 'src/', 'apps/', 'print_labels/', 'tutorial/',
          'platformio.ini', 'platformio.local.ini.example', 'SAMBUNGAN.md',
          'COMMANDS.md', 'migration/', 'index.html', '.nojekyll',
          'digital/artifacts/', 'digital/GeoDecoder_Digital_V',
          'digital/dist/GeoDecoder_Digital_V', 'digital/dist/app.bundle.js',
          'digital/dist/assets/', 'digital/module/GeoDecoder_Modul_V1.html',
          'digital/vendor/module-v1.5.0.html', 'digital/vendor/module-v1.6.0.html',
          'digital/vendor/module-v1.6.1.html',
          'digital/docs/design-system-evidence/GeoDecoder_Design_System.html')
bad = [p for p in tracked if p and any(p == value or p.startswith(value) for value in banned)]
required = ('digital/package.json', 'supabase/config.toml',
            'digital/assets/manifest.json', 'digital/assets/audio/menu.mp3',
            'digital/assets/audio/map.mp3', 'digital/assets/icons/icon.svg')
missing = [p for p in required if not (root / p).is_file()]
if bad or missing:
    print('Unexpected platform/generated files:', bad)
    print('Missing source:', missing)
    sys.exit(1)
print(f'PASS: Digital source ownership and generated-file boundaries ({sum(bool(x) for x in tracked)} tracked files).')

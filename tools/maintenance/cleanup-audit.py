#!/usr/bin/env python3
import json, subprocess, pathlib
root=pathlib.Path.cwd()
tracked=subprocess.check_output(['git','ls-files','-z']).decode().split('\0')
patterns=['dist/assets/audio/','pwa/icon.svg','module-v1.5.0.html','module-v1.6.0.html','module-v1.6.1.html','GeoDecoder_Digital_V1.html','GeoDecoder_Digital_V2.html','GeoDecoder_Modul_V1.html','GeoDecoder_Design_System.html','app.bundle.js']
refs={p:[] for p in patterns}
skip=('digital/docs/','digital/module/docs/','digital/module/evidence/','digital/artifacts/','migration/')
for name in tracked:
 p=root/name
 if not name or not p.is_file() or name.startswith(skip) or p.stat().st_size>600000: continue
 if p.suffix.lower() not in ('.mjs','.js','.cjs','.py','.ts','.json','.md','.html','.toml','.css','.yml'):continue
 try: lines=p.read_text().splitlines()
 except UnicodeError: continue
 for i,line in enumerate(lines,1):
  for pattern in patterns:
   if pattern in line:refs[pattern].append({'path':name,'line':i,'text':line[:500]})
report={'base':'6313d2281b7bf621ca380c3beb78bbc94bef63f6','references':refs}
path=root/'cleanup-audit.json'
path.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

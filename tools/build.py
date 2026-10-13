# Repack index.html with a new OBP3 renderer; every other byte of the bundle stays as it was.
import sys, re, json, base64, gzip
idx, js, out = sys.argv[1:4]
UUID = '6b70e3db-5a75-4c85-abde-de8fb700d791'
s = open(idx).read()
m = re.search(r'<script type="__bundler/manifest">', s); e = s.index('</script>', m.end())
man = json.loads(s[m.end():e])
old = man[UUID]['data']
new = base64.b64encode(gzip.compress(open(js, 'rb').read(), compresslevel=9, mtime=0)).decode()
assert s.count(old) == 1
s = s.replace(old, new)
json.loads(s[m.end():s.index('</script>', m.end())])  # still valid
open(out, 'w').write(s); print('built', len(s))

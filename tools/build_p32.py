# Repack index.html: new OBP3 renderer + new page template; drop the unused Crimson Pro font entries;
# point the outer head at the new favicon set. Every other byte of the bundle stays as it was.
import sys, re, json, base64, gzip
idx, js_path, tpl_path, out = sys.argv[1:5]
UUID = '6b70e3db-5a75-4c85-abde-de8fb700d791'
CRIMSON = ['6400765a-6c30-418c-8807-f74ac9430d74', 'c6e21aef-6219-4607-886d-7e06feb2dc1f', 'fb8ae7df-fa7b-436e-aea6-45ff60fb1036',
           '95fc27de-90cc-44bd-b5d9-54592d3a59c3', '738fb1a2-b4d7-4f10-82d1-f4ad10bb5dd5', 'b5f207ee-0fe2-4880-a5d7-3307ee10fa6c']
s = open(idx).read()

def enc_tpl(t):
    return json.dumps(t, ensure_ascii=False).replace('</', '<\\u002F')

# --- template ---
m = re.search(r'<script type="__bundler/template">\n', s); e = s.index('\n  </script>', m.end())
old_line = s[m.end():e]
assert enc_tpl(json.loads(old_line)) == old_line, 'template encoding round-trip'
tpl = open(tpl_path).read()
for u in CRIMSON: assert u not in tpl, u
s = s[:m.end()] + enc_tpl(tpl) + s[e:]

# --- manifest ---
m = re.search(r'<script type="__bundler/manifest">', s); e = s.index('</script>', m.end())
man = json.loads(s[m.end():e])
new_data = base64.b64encode(gzip.compress(open(js_path, 'rb').read(), compresslevel=9, mtime=0)).decode()
man[UUID]['data'] = new_data
for u in CRIMSON: del man[u]
s = s[:m.end()] + json.dumps(man, separators=(',', ':')) + s[e:]
for u in CRIMSON: assert u not in s, u

# --- outer head ---
icon_re = re.compile(r'  <link rel="icon" type="image/png" href="data:image/png;base64,[^"]+">')
assert len(icon_re.findall(s)) == 1
ICONS = ('  <link rel="icon" href="favicon.ico?v=2" sizes="48x48">\n'
         '  <link rel="icon" href="favicon.svg?v=2" type="image/svg+xml">\n'
         '  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png?v=2">\n'
         '  <link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png?v=2">\n'
         '  <link rel="preload" href="fonts/newsreader/Newsreader-VF.woff2" as="font" type="font/woff2" crossorigin>')
s = icon_re.sub(lambda _: ICONS, s)
old = '  <link rel="apple-touch-icon" href="https://squidbay.github.io/oyster-bar-preview/apple-touch-icon.png">'
assert s.count(old) == 1
s = s.replace(old, old.replace('.png"', '.png?v=2"'))
open(out, 'w').write(s); print('built', len(s))

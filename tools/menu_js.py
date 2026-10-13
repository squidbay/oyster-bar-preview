# Builds the site's MENU constant from the parsed fwoysterbar.com/menu JSON. Text is kept as published;
# only structure is mapped: "**" becomes a gluten-free flag, helper rows become group notes.
import json, sys
m = json.load(open(sys.argv[1]))
NAMES = {'STARTERS':'Starters','SALADS':'Salads','SANDWICHES & SUCH':'Sandwiches & Such','ENTREES':'Entrées','SOUPS':'Soups',
 'OYSTER BAR SIDES':'Oyster Bar Sides','RAW OYSTERS':'Raw Oysters','BAKED OYSTERS':'Baked Oysters','OYSTER BAR CLASSICS':'Oyster Bar Classics',
 'FROM THE BUTCHER':'From the Butcher','FRESH FISH MARKET':'Fresh Fish Market','SCRATCH KITCHEN':'Scratch Kitchen',
 'OYSTER BAR SIGNATURE COCKTAILS':'Signature Cocktails','Oyster Bar Old Fashioneds':'Old Fashioneds',"MARTINI'S":'Martinis'}
def items(sec):
    out, note = [], ''
    for it in sec['items']:
        t, d = it['title'], it['desc']
        gf = d.rstrip().endswith('**')
        d = d.rstrip().rstrip('*').rstrip()
        if t == 'All sandwiches include': note = 'All sandwiches include ' + d; continue
        if t == 'Sides Include:': out.append({'n': 'Sides include', 'd': d}); continue
        if t == '+ Burger Builders:':
            parts = [d] + [it['price']] + it['options']
            seen=[]; [seen.append(p.strip().rstrip(',')) for p in parts if p and p.strip().rstrip(',') not in seen]
            out.append({'n': 'Burger Builders', 'd': ', '.join(seen), 'sub': True}); continue
        o = {'n': t}
        if d: o['d'] = d
        if gf: o['gf'] = True
        out.append(o)
    return out, note
lunch, dinner, drinks = m
G = {}
for key, w in (('lunch', lunch), ('dinner', dinner)):
    G[key] = []
    for s in w['sections']:
        its, note = items(s)
        g = {'name': NAMES[s['title']], 'items': its}
        if note: g['note'] = note
        G[key].append(g)
ds = drinks['sections']
G['drinks'] = []
for s in ds[:3]:
    its, _ = items(s); G['drinks'].append({'name': NAMES[s['title']], 'items': its})
for (s, label) in zip(ds[3:], ['By the Glass · White','By the Glass · Red','Bottles · White','Bottles · Red']):
    G['drinks'].append({'name': label, 'list': True, 'items': [{'n': i['title']} for i in s['items']]})
print('const MENU = ' + json.dumps(G, ensure_ascii=False) + ';')
n = sum(len(g['items']) for k in G for g in G[k])
print('/* items:', n, '*/')

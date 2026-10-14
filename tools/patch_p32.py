# P3.2 editorial rebalance: patch the OBP3 renderer (obp3.js) and the page template (template.html).
# Every replacement asserts it matched exactly once, so a drifted source fails loudly.
import sys, re
src_js, src_tpl, out_js, out_tpl = sys.argv[1:5]
js = open(src_js).read()
tpl = open(src_tpl).read()

def rep(s, old, new, count=1):
    n = s.count(old)
    assert n == count, (n, old[:100])
    return s.replace(old, new)

def rep_between(s, start, end, new):
    i = s.index(start); j = s.index(end, i)
    assert s.count(start) == 1, start
    return s[:i] + new + s[j:]

# ---------- 1. typography: Newsreader (self-hosted, OFL) replaces Crimson Pro for display ----------
js = rep(js, """display:"'Crimson Pro','Minion 3 Display',Georgia,serif\"""", """display:"'Newsreader',Georgia,serif\"""")

# ---------- 2. shared links ----------
LINKS = r'''
const TEL = 'tel:2607449490';
const MAP_Q = 'The+Oyster+Bar,+1830+S+Calhoun+St,+Fort+Wayne,+IN+46802';
const DIRECTIONS_URL = 'https://www.google.com/maps/dir/?api=1&destination=The+Oyster+Bar%2C+1830+S+Calhoun+St%2C+Fort+Wayne%2C+IN+46802';
const MAPS_URL = 'https://www.google.com/maps/search/?api=1&query=' + MAP_Q;
const MAP_EMBED = 'https://maps.google.com/maps?q=' + MAP_Q + '&z=16&output=embed';
const ext = 'target="_blank" rel="noopener"';
'''
js = rep(js, "const NAV = [", LINKS + "const NAV = [")

# btn/link as real anchors when they have a destination
js = rep(js, "const link = (label, dark) =>", r'''const asLink = (html, href, extra='') => html.replace(/^<span /, `<a href="${href}" ${extra} `).replace(/<\/span>$/, '</a>');
const btnA = (label, kind, dark, h, href, extra) => asLink(btn(label, kind, dark, h), href, extra);
const link = (label, dark) =>''')

# ---------- 3. content: the P3.2 page set ----------
PAGES = r'''const GIFT = {t:'Gift Cards',s:'Give the gift of an evening at The Oyster Bar.',cta:'Call About Gift Cards',href:TEL};
const OYSTER_TEASER = {k:'strip',flowPrev:true,eyebrow:'Selections change daily',title:'Today’s Oysters',text:'The Oyster Board, raw oysters by the full or half dozen, and baked oysters: Parmesan, Rockefeller, Casino, Fried, Blue Crab or Picatta. Ask what’s on the board today.',cta:"Today's Oysters"};
const pages = [
  {id:'home',name:'Home',route:'/',blocks:[
    {k:'header'},
    {k:'hero',home:true,eyebrow:'Est. 1888 · 1830 S Calhoun St',title:'Lunch downtown. Oysters on the bar. Dinner in the back room.',sub:'Lunch Monday to Friday, dinner Monday to Saturday, and a board of today’s oysters that changes with the kitchen. Table requests are confirmed by our staff.',cta1:'Request a Table',cta2:'Lunch menu & hours',photo:PHOTO.sign},
    {k:'feature',title:'Today’s Oysters & Current Features',eyebrow:'Selections change daily',items:OYSTER_BOARD,cta:'Request a Table'},
    {k:'split',title:'Lunch, downtown, with our own lot',text:'A proper lunch a few blocks from the Grand Wayne and the courthouse. Order at the table, park in our lot on Calhoun, and be back at your desk on time.',items:['Quick lunch for downtown workers','Groups and convention lunches','Own lot, about 30 spots'],cta:'See the lunch menu',photo:PHOTO.barOysters},
    {k:'cards',items:[{t:'Dinner & Cocktails',s:'Oysters raw and baked, the kitchen’s classics and the craft cocktail list',l:'Dinner & Cocktails',photo:PHOTO.dinnerFish},{t:'Fresh Fish Market',s:'Choose your fish, choose one of four preparations',l:'How it works',photo:PHOTO.fishPlate},{t:'History since 1888',s:'Our story since 1888, year by year',l:'Read the history',photo:PHOTO.historyBar}]},
    {k:'band',anchor:'giftcards',items:[{t:'Events & Private Occasions',s:'Sunday dinners · private dining · off-site catering',cta:'Inquire'},GIFT]},
    {k:'infoStrip'},{k:'footer'}]},
  {id:'lunch',name:'Lunch',route:'/lunch',blocks:[
    {k:'header'},
    {k:'hero',short:true,eyebrow:'Lunch · Mon–Fri 11–3',title:'A real lunch, downtown, in our own lot.',sub:'Fish and chips, fish tacos, oysters on the half shell. Park on site and order at the table.',cta1:'Request a Table',cta2:'Call (260) 744-9490',photo:PHOTO.lunch},
    {k:'strip',lead:true,eyebrow:'Lunch at a glance',title:'Weekdays from eleven',text:'Our lot is on site, and groups can call ahead so the table is ready when you are. Own lot, about 30 spots · Groups and convention lunches.',cta:'Directions & parking'},
    {k:'rows',anchor:'menu',eyebrow:'Lunch',title:'The lunch menu',menu:MENU.lunch,raw:true,layout:[['Starters'],['Salads'],['Sandwiches & Such'],['Entrées'],['Soups','Oyster Bar Sides']],flowNext:true},
    OYSTER_TEASER,
    {k:'split',flip:true,title:'Feeding a group or a meeting',text:'Convention and downtown office groups are regulars. Tell us the headcount and the hour, and staff will arrange the tables.',items:['Grand Wayne and downtown convention traffic','Large parties handed to staff'],cta:'Send a group inquiry',photo:PHOTO.barRoom},
    {k:'infoStrip'},{k:'footer'}]},
  {id:'dinner',name:'Dinner & Cocktails',route:'/dinner',blocks:[
    {k:'header'},
    {k:'hero',short:true,eyebrow:'Dinner · Mon–Thu 5–9 · Fri–Sat 5–10',title:'Dinner at an 1888 oyster house.',sub:'Oysters raw and baked, the Fresh Fish Market, the butcher’s cuts and a craft cocktail list.',cta1:'Request a Table',cta2:'Jump to cocktails',photo:PHOTO.shrimp},
    {k:'rows',anchor:'menu',eyebrow:'Dinner',title:'The dinner menu',jump:[['Starters','starters'],['Oysters','oysters'],['Classics','classics'],['Fish Market','fish'],['Scratch Kitchen','scratch'],['Cocktails','cocktails'],['Wine','wine']],
      menu:MG('dinner','Starters','Raw Oysters','Baked Oysters','Oyster Bar Classics','From the Butcher'),layout:[['Starters'],['Raw Oysters'],['Baked Oysters'],['Oyster Bar Classics','From the Butcher']],flowNext:true},
    {k:'fish',anchor:'fish',inline:true,photo:PHOTO.fishPlate,flowPrev:true,flowNext:true},
    {k:'rows',menu:MG('dinner','Scratch Kitchen','Oyster Bar Sides'),gf:true,raw:true,layout:[['Scratch Kitchen'],['Oyster Bar Sides']],flowPrev:true,flowNext:true},
    {k:'rows',anchor:'cocktails',eyebrow:'Dinner · Cocktails, wine & bottles',title:'Cocktails, wine & bottles',menu:MENU.drinks,layout:[['Signature Cocktails','Old Fashioneds','Martinis'],['By the Glass · White','By the Glass · Red'],['Bottles · White','Bottles · Red']],flowPrev:true,flowNext:true},
    OYSTER_TEASER,
    {k:'band',anchor:'giftcards',stack:true,items:[{t:'Request a table for dinner',s:'Staff confirm by phone or text',cta:'Request a Table'},GIFT]},
    {k:'footer'}]},
  {id:'oysters',name:"Today's Oysters",route:'/oysters',blocks:[
    {k:'header'},
    {k:'hero',short:true,eyebrow:'Today',title:'Today’s oysters.',sub:'Our oyster board changes with what comes in from the East and West Coasts. Ask your server what’s on it today.',cta1:'Request a Table',cta2:'Call',photo:PHOTO.oysters},
    {k:'feature',title:'Today’s Oysters',eyebrow:'Selections change daily',items:OYSTER_BOARD,cta:'Request a Table'},
    {k:'rows',anchor:'menu',eyebrow:'On the menu',title:'Raw & baked oysters',menu:MG('dinner','Raw Oysters','Baked Oysters'),gf:true,raw:true,layout:[['Raw Oysters'],['Baked Oysters']],flowNext:true},
    {k:'fish',photo:PHOTO.fishZucchini,flowPrev:true},
    {k:'footer'}]},
  {id:'history',name:'History',route:'/history',blocks:[
    {k:'header'},
    {k:'hero',eyebrow:'Since 1888 · 1830 S Calhoun St',title:'Since 1888, at 1830 South Calhoun.',sub:'From an 1888 saloon to today’s oyster bar: the story of 1830 South Calhoun, year by year.',cta1:'Request a Table',cta2:'Jump to timeline',photo:PHOTO.diningRoom},
    {k:'timeline',anchor:'timeline'},
    {k:'split',title:'The restaurant today',text:'Chef-owner Tony West has cooked in this kitchen since he was a teenager. The rooms are as they are; the photographs are ours.',items:['Chef-owner Tony West'],cta:'Visit & parking',photo:PHOTO.owners},
    {k:'band',anchor:'giftcards',stack:true,items:[{t:'Dinner in the rooms where it happened',s:'Staff confirm by phone or text',cta:'Request a Table'},GIFT]},
    {k:'footer'}]},
  {id:'events',name:'Events & Private Dining',route:'/events',blocks:[
    {k:'header'},
    {k:'hero',short:true,eyebrow:'Sunday dinners · Private dining · Catering',title:'Sunday dinners, private rooms, catering.',sub:'Special Sunday dinners, private dining in the back room, and off-site catering. Ask us about upcoming dates.',cta1:'Send an inquiry',cta2:'Call',photo:PHOTO.toast},
    {k:'split',title:'Private dining',text:'The back room seats a private party for dinner, with the menu arranged ahead with the kitchen.',items:['Sunday buyouts','Tell us the date, headcount and occasion'],cta:'Private dining inquiry',photo:PHOTO.dinnerWine,flowNext:true},
    {k:'boxes',flowPrev:true,items:[{title:'Off-site catering',text:'Oysters, fish and dinner favorites, brought to your event.',items:['On-site or off-site','Tell us the headcount, date and service style'],cta:'Catering inquiry'}]},
    {k:'band',anchor:'giftcards',items:[GIFT]},
    {k:'footer'}]},
  {id:'visit',name:'Visit & Parking',route:'/visit',blocks:[
    {k:'header'},
    {k:'hero',short:true,eyebrow:'1830 S Calhoun St · Fort Wayne, IN 46802',title:'How to find us, and where to park.',sub:'Our own lot is on site. Directions, hours and how to reach us.',cta1:'Get directions',cta2:'Request a Table',photo:PHOTO.patio},
    {k:'visitInfo',anchor:'map',flowNext:true},
    {k:'boxes',flowPrev:true,items:[
      {title:'Before the show',text:'A few minutes from the Embassy Theatre, Parkview Field, the Grand Wayne and the Clyde. Request a table before curtain.',items:['Request a table before the show']},
      {title:'Contact & email sign-up',text:'Call us during service hours, or leave your email for the occasional note about Sunday dinners and market features.',items:['<a href="tel:2607449490" style="color:#5C2026;text-decoration:underline;text-underline-offset:3px">(260) 744-9490</a>','<a href="https://www.instagram.com/fwoysterbar/" target="_blank" rel="noopener" style="color:#5C2026;text-decoration:underline;text-underline-offset:3px">Instagram</a> · <a href="https://www.facebook.com/fwoysterbar" target="_blank" rel="noopener" style="color:#5C2026;text-decoration:underline;text-underline-offset:3px">Facebook</a>']}]},
    {k:'footer'}]},
  {id:'request',name:'Request a Table',route:'/request',blocks:[
    {k:'header'},
    {k:'form',state:'default'},
    {k:'infoStrip'},
    {k:'footer'}]}
];
'''
js = rep_between(js, "const pages = [\n", "const states = [", PAGES)
js = rep(js, "  {id:'large',name:'Large party / special request handoff',large:true}\n];",
              "  {id:'large',name:'Large party / special request handoff',large:true},\n  {id:'notsent',name:'Preview only · nothing was sent',notsent:true}\n];")

# ---------- 4. renderers ----------
def fn_replace(s, name, new):
    """Replace a top-level `function name(` ... up to the next top-level function or const."""
    i = s.index(f'\nfunction {name}(') + 1
    m = re.compile(r'\n(function |const )').search(s, i + 1)
    return s[:i] + new.strip('\n') + '\n' + s[m.start() + 1:]

# section padding helper: blocks that continue the previous section drop the seam
js = rep(js, "/* ---------- block renderers ---------- */", r'''/* ---------- block renderers ---------- */
const secPad = (b, v) => `${b && b.flowPrev ? Math.round(v.sec/2) : v.sec}px ${v.pad}px ${b && b.flowNext ? Math.round(v.sec/2) : v.sec}px`;''')

ROWS = r'''
function rows(b, v) {
  if (!(OPTS.site && b.menu)) return rowsBase(b, v);
  const dsk = v.id==='desktop', por = v.id==='portrait';
  const gap = dsk ? 48 : 28;
  const gfMark = sp(`display:inline-block;margin-left:8px;padding:1px 5px;border:1px solid ${T.brass};font:600 10px/1.3 ${T.body};letter-spacing:.08em;color:#6E5424;vertical-align:3px;white-space:nowrap`, 'GF').replace('<span', '<span title="'+GF_NOTE+'" aria-label="Gluten free or can be made gluten free"');
  const ANCHOR = {'Starters':'starters','Raw Oysters':'oysters','Oyster Bar Classics':'classics','Scratch Kitchen':'scratch','By the Glass · White':'wine'};
  // A sub-row (Burger Builders) belongs to the dish above it, so it travels in the same cell.
  const cells = g => { const out = []; g.items.forEach(i => { if (i.sub && out.length) out[out.length-1].sub = i; else out.push({...i}); }); return out; };
  const dish = i => d(`padding:14px 0;border-bottom:1px solid ${T.foxing};min-width:0`,
    d('', sp(`font:600 ${dsk?22:20}px/1.2 ${T.display};color:${T.ink}`, esc(i.n)) + (i.gf ? gfMark : '')) +
    (i.d ? small(esc(i.d), '#4A4842', 'margin-top:4px;font-size:14px') : '') +
    (i.sub ? d(`margin-top:12px;border:1px solid ${T.foxing};background:${T.ivory};padding:10px 12px`, d(`font:600 16px/1.2 ${T.display};color:${T.ink}`, esc(i.sub.n)) + small(esc(i.sub.d), '#4A4842', 'margin-top:4px;font-size:14px')) : ''));
  const wine = i => d(`padding:9px 0;border-bottom:1px solid ${T.foxing};font:600 ${dsk?18:17}px/1.3 ${T.display};color:${T.ink};min-width:0`, esc(i.n));
  const group = (g, cols) => d(`min-width:0`,
    d(`border-bottom:1px solid ${T.ink};padding-bottom:8px`, eyebrow(g.name, T.oxblood, 13)) +
    (g.note ? small(g.note, '#4A4842', 'margin-top:10px;font-style:italic;font-size:14px') : '') +
    d(`display:grid;grid-template-columns:repeat(${cols},minmax(0,1fr));column-gap:${gap}px`, cells(g).map(g.list ? wine : dish).join('')),
    ANCHOR[g.name] ? `data-anchor="${ANCHOR[g.name]}"` : '');
  const byName = Object.fromEntries(b.menu.map(g => [g.name, g]));
  const layout = (b.layout || b.menu.map(g => [g.name]));
  const placed = layout.flat();
  b.menu.forEach(g => { if (!placed.includes(g.name)) layout.push([g.name]); });
  const rowsHtml = layout.map(names => {
    const gs = names.map(n => byName[n]).filter(Boolean);
    if (gs.length === 1) return group(gs[0], por ? 1 : 2);
    if (por) return gs.map(g => group(g, 1)).join(`<div style="height:${gap}px"></div>`);
    return d(`display:grid;grid-template-columns:repeat(${gs.length},minmax(0,1fr));column-gap:${gap}px;align-items:start`, gs.map(g => group(g, 1)).join(''));
  }).join(`<div style="height:${dsk?36:28}px"></div>`);
  const jump = b.jump ? d(`display:flex;flex-wrap:wrap;gap:8px;margin:0 0 ${dsk?28:22}px`, b.jump.map(([label]) =>
    spA(`display:inline-flex;align-items:center;min-height:${por?44:40}px;padding:0 14px;border:1px solid ${T.foxing};background:${T.ivory};font:600 12px/1 ${T.body};letter-spacing:.1em;text-transform:uppercase;color:${T.ink};white-space:nowrap`, esc(label), act('Jump · ' + label))).join('')) : '';
  const head = b.title ? d(`margin-bottom:${dsk?20:16}px`, (b.eyebrow ? eyebrow(b.eyebrow, T.oxblood, 11) : '') + d(b.eyebrow?'margin-top:8px':'', h2(b.title, T.ink, dsk?36:26))) : '';
  const notes = (b.gf || b.raw) ? d(`margin-top:${dsk?28:22}px;display:grid;gap:6px;max-width:80ch`,
    (b.gf ? small(sp(`font-weight:600;color:#6E5424`, 'GF') + ' · ' + GF_NOTE + '.', '#2A2926', 'font-size:14px') : '') +
    (b.raw ? small(RAW_NOTE + '.', '#2A2926', 'font-size:14px') : '')) : '';
  return d(`background:${T.parchment};height:100%;padding:${secPad(b, v)};box-sizing:border-box`, head + jump + rowsHtml + notes);
}
'''
js = fn_replace(js, 'rows', ROWS)

FISH = r'''
function fish(b, v) {
  const dsk = v.id==='desktop', por = v.id==='portrait';
  const box = (step, inner) => d(`border:1px solid ${T.foxing};padding:16px;background:${T.ivory};min-width:0`, eyebrow(step, T.oxblood, 11) + d('margin-top:12px', inner));
  const opt = t => d(`border:1px solid ${T.foxing};padding:10px 12px;font:400 15px/1.3 ${T.body};color:${T.ink}`, t);
  const head = b.inline
    ? d(`border-bottom:1px solid ${T.ink};padding-bottom:8px`, eyebrow('Fresh Fish Market', T.oxblood, 13))
    : eyebrow('Dinner · Today’s Oysters', T.oxblood, 11) + d('margin-top:8px', h2('Fresh Fish Market', T.ink, dsk?36:26));
  return d(`background:${T.parchment};height:100%;padding:${secPad(b, v)};box-sizing:border-box`,
    head +
    d('margin-top:12px;max-width:60ch', body('Choose From One of Our Daily Fresh Fish Selections & Then Choose One of Our Preparations', '#2A2926', 16)) +
    d(`display:grid;grid-template-columns:${por?'1fr':'repeat(3,minmax(0,1fr))'};gap:${v.gap}px;margin-top:20px`,
      box('Step 1 · Today’s fish', body('Our fresh fish changes daily. Ask your server for today’s selections.', T.ink, 15)) +
      box('Step 2 · Choose your fish', img('Image 3:2 · owned photo', '3/2', false, '', b.photo)) +
      box('Step 3 · One of four preparations', d('display:grid;gap:8px', MENU.dinner.find(g => g.name === 'Fresh Fish Market').items.filter(i => i.n === '~').map(i => opt(i.d)).join('')))) +
    (b.inline ? '' : d('display:flex;gap:16px;align-items:center;margin-top:24px;flex-wrap:wrap', btn('Request a Table','primary',false,44))));
}
'''
js = fn_replace(js, 'fish', FISH)

FEATURE_CARDS = r'''
function feature(b, v) {
  const dsk = v.id==='desktop', por = v.id==='portrait';
  const cols = dsk ? Math.min(4,b.items.length) : v.id==='landscape' ? 3 : 1;
  const items = b.items.map(([n,s]) => d(`padding:${por?'14px 0 4px':'0'};${por?`border-top:1px solid ${T.foxing}`:''}`, d(`font:600 20px/1.2 ${T.display};color:${T.ink}`, n) + small(s, '#4A4842', 'margin-top:4px'))).join('');
  return d(`background:${T.parchment};height:100%;padding:${v.sec}px ${v.pad}px ${dsk?Math.round(v.sec/2):v.sec}px;box-sizing:border-box`,
    d(`background:${T.ivory};border:1px solid ${T.foxing};padding:${dsk?28:20}px;box-sizing:border-box`,
      eyebrow(b.eyebrow, T.oxblood, 11) + d('margin-top:8px', h2(b.title, T.ink, dsk?32:26)) +
      d(`display:grid;grid-template-columns:repeat(${cols},minmax(0,1fr));gap:${por?4:24}px;margin-top:${por?8:18}px;${por?'':`border-top:1px solid ${T.foxing};padding-top:16px`}`, items) +
      d('display:flex;gap:16px 20px;align-items:center;flex-wrap:wrap;margin-top:20px', btn(b.cta,'primary',false,44) + link('Call (260) 744-9490', false))));
}
function strip(b, v) {
  const dsk = v.id==='desktop', por = v.id==='portrait';
  const lead = d('min-width:0', eyebrow(b.eyebrow, T.oxblood, 11) + d('margin-top:6px', h3(b.title, T.ink, dsk?24:22)));
  const txt = small(b.text, '#4A4842', 'font-size:14px;line-height:1.55');
  const cta = btn(b.cta, 'secondary', false, 44);
  const inner = por
    ? lead + d('margin-top:10px', txt) + d('margin-top:16px', cta)
    : d(`display:grid;grid-template-columns:${dsk?'minmax(180px,auto) 1fr auto':'1fr auto'};gap:${dsk?24:16}px;align-items:center`,
        lead + (dsk ? txt : '') + cta) + (dsk ? '' : d('margin-top:10px', txt));
  return d(`background:${T.parchment};height:100%;padding:${b.flowPrev ? Math.round(v.sec/2) : v.sec}px ${v.pad}px ${b.lead ? 0 : v.sec}px;box-sizing:border-box`,
    d(`background:${T.ivory};border:1px solid ${T.foxing};padding:${dsk?'18px 24px':'18px 20px'};box-sizing:border-box`, inner));
}
'''
js = fn_replace(js, 'feature', FEATURE_CARDS)

CARDS = r'''
function cards(b, v) {
  const dsk = v.id==='desktop', por = v.id==='portrait';
  const cols = dsk ? 3 : v.id==='landscape' ? 3 : 1;
  const ratio = dsk ? '4/3' : '4/3';
  const cs = b.items.map(c => {
    const text = d(`padding:${por?'14px 14px 14px 16px':'18px 18px 20px'};display:flex;flex-direction:column;flex:1;min-width:0`, h3(c.t, T.ink, dsk?24:21) + small(c.s, '#4A4842', 'margin-top:6px;font-size:15px') + d('margin-top:auto;padding-top:14px', link(c.l+'\u00a0→', false).replace('white-space:nowrap;','')));
    if (por) return d(`background:${T.ivory};border:1px solid ${T.foxing};display:grid;grid-template-columns:40% 1fr;min-height:190px`, img('', ratio, false, `aspect-ratio:auto;height:100%;border:0;border-right:1px solid ${T.foxing}`, c.photo) + text);
    return d(`background:${T.ivory};border:1px solid ${T.foxing};display:flex;flex-direction:column`, img('', ratio, false, 'border:0;border-bottom:1px solid '+T.foxing, c.photo) + text);
  }).join('');
  return d(`background:${T.parchment};height:100%;padding:${v.sec/2}px ${v.pad}px ${v.sec}px;box-sizing:border-box`, d(`display:grid;grid-template-columns:repeat(${cols},minmax(0,1fr));gap:${v.gap}px`, cs));
}
'''
js = fn_replace(js, 'cards', CARDS)

BAND = r'''
function band(b, v) {
  const dsk = v.id==='desktop', por = v.id==='portrait';
  const cols = b.stack || por ? 1 : Math.min(2, b.items.length);
  const ctaFor = it => it.href ? btnA(it.cta, 'secondary', true, 44, it.href) : btn(it.cta, it.cta==='Request a Table'?'primary':'secondary', true, 44);
  return d(`background:${T.ink};height:100%;padding:${dsk?20:v.sec*0.75}px ${v.pad}px;box-sizing:border-box`, d(`display:grid;grid-template-columns:repeat(${cols},minmax(0,1fr));gap:${dsk?16:v.gap}px;width:100%`, b.items.map(it => d(`border:1px solid #3A312C;padding:${dsk?'18px 24px':'18px 20px'};display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:14px 20px`, d('min-width:0;flex:1 1 220px', h3(it.t, T.parchment, dsk?24:22) + small(it.s, T.foxing, 'margin-top:4px;font-size:14px')) + ctaFor(it))).join('')));
}
function boxes(b, v) {
  const dsk = v.id==='desktop', por = v.id==='portrait';
  const one = b.items.length === 1;
  const box = it => {
    const text = d('min-width:0', h3(it.title, T.ink, dsk?28:22) + d('margin-top:8px;max-width:60ch', body(it.text, '#4A4842', 16)) +
      (it.items ? `<ul style="font:400 15px/1.6 ${T.body};color:${T.ink};margin:10px 0 0;padding-left:18px">${it.items.map(i=>`<li>${i}</li>`).join('')}</ul>` : ''));
    const cta = it.cta ? btn(it.cta, 'secondary', false, 44) : '';
    return d(`background:#FBF8F1;border:1px solid ${T.foxing};padding:${dsk?'24px 28px':'20px'};box-sizing:border-box;${one && !por ? 'display:flex;justify-content:space-between;align-items:center;gap:24px' : ''}`,
      text + (cta ? (one && !por ? cta : d('margin-top:16px', cta)) : ''));
  };
  return d(`background:${T.ivory};height:100%;padding:${secPad(b, v)};box-sizing:border-box`,
    d(`display:grid;grid-template-columns:${por || one ? '1fr' : `repeat(${b.items.length},minmax(0,1fr))`};gap:${v.gap}px`, b.items.map(box).join('')));
}
'''
js = fn_replace(js, 'band', BAND)

INFO = r'''
function infoStrip(b, v) {
  const dsk = v.id==='desktop', por = v.id==='portrait';
  const lab = t => eyebrow(t, T.brass, 11);
  const tel = `<a href="${TEL}" style="color:${T.oxblood};text-decoration:underline;text-underline-offset:3px;white-space:nowrap">(260) 744-9490</a>`;
  const hours = d('min-width:0', lab('Hours') + body('Lunch Mon–Fri 11–3 · Dinner Mon–Thu 5–9 · Fri–Sat 5–10 · Sunday closed', T.ink, 15, 'margin-top:4px;line-height:1.5'));
  const loc = d('min-width:0', lab('Location') + body('1830 S Calhoun St, Fort Wayne, IN 46802 · ' + tel, T.ink, 15, 'margin-top:4px;line-height:1.5'));
  const links = d(`display:flex;gap:12px 24px;flex-wrap:wrap;${por?'':'justify-content:flex-end;'}margin-top:${por?16:12}px`,
    asLink(link('Directions →', false).replace(/ data-act="[^"]*"/, ''), DIRECTIONS_URL, ext) + link('Visit & Parking →', false));
  return d(`background:${T.ivory};height:100%;padding:${dsk?24:20}px ${v.pad}px;box-sizing:border-box;border-top:1px solid ${T.foxing}`,
    d(`display:grid;grid-template-columns:${por?'1fr':'1fr 1fr'};gap:${por?14:32}px`, hours + loc) + links);
}
function visitInfo(b, v) {
  const dsk = v.id==='desktop', por = v.id==='portrait';
  const lab = t => eyebrow(t, T.brass, 11);
  const tel = `<a href="${TEL}" style="color:${T.oxblood};text-decoration:underline;text-underline-offset:3px">(260) 744-9490</a>`;
  const col = d('min-width:0;display:grid;gap:18px;align-content:start',
    d('', lab('Hours') + body('Lunch Mon–Fri 11–3<br>Dinner Mon–Thu 5–9<br>Dinner Fri–Sat 5–10<br>Sunday closed · events only', T.ink, 16, 'margin-top:4px;line-height:1.55')) +
    d('', lab('Location') + body('1830 S Calhoun St<br>Fort Wayne, IN 46802<br>' + tel, T.ink, 16, 'margin-top:4px;line-height:1.55')) +
    d('', lab('Parking') + body('Our own lot is on site, about 30 spots. Pull into our lot off Calhoun. The entrance is at the front; staff can help with accessibility on arrival.', T.ink, 16, 'margin-top:4px;line-height:1.55')));
  // Live keyless Google Maps embed. The engraved poster sits underneath: it shows while the map loads,
  // and stays as the fallback (with a working maps link) if the frame is blocked.
  const poster = `<img src="${A.etch}" alt="" style="position:absolute;right:-14%;top:-22%;width:82%;height:auto;opacity:.22;pointer-events:none">` +
    `<a href="${MAPS_URL}" ${ext} style="position:absolute;left:14px;bottom:14px;background:${T.ivory};border:1px solid ${T.foxing};padding:10px 12px;font:500 13px/1.2 ${T.body};color:${T.oxblood};text-decoration:underline;text-underline-offset:3px">Open in Google Maps →</a>`;
  const map = d(`position:relative;overflow:hidden;width:100%;${por?'height:240px':'aspect-ratio:16/10'};background:#1C1714;border:1px solid ${T.foxing};box-sizing:border-box`,
    poster + `<iframe src="${MAP_EMBED}" title="Map: The Oyster Bar, 1830 S Calhoun St, Fort Wayne, Indiana" referrerpolicy="no-referrer-when-downgrade" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0;display:block"></iframe>`);
  const ctas = d('display:flex;gap:12px;flex-wrap:wrap;margin-top:14px', btnA('Directions', 'primary', false, 44, DIRECTIONS_URL, ext) + btn('Request a Table', 'secondary', false, 44));
  return d(`background:${T.ivory};height:100%;padding:${secPad(b, v)};box-sizing:border-box`,
    d(`display:grid;grid-template-columns:${por?'1fr':'1fr 1.25fr'};gap:${dsk?48:24}px;align-items:start`, col + d('min-width:0', map + ctas)));
}
'''
js = fn_replace(js, 'info', INFO)
js = rep(js, "const RENDER = {header,hero,feature,split,cards,rows,fish,timeline:timelineBlock,quote,band,info,text,form,footer};",
              "const RENDER = {header,hero,feature,strip,split,cards,rows,fish,timeline:timelineBlock,quote,band,boxes,infoStrip,visitInfo,text,form,footer};")

# split: honour flowNext so Events' catering card sits in the same section
js = rep(js, "return d(`background:${T.ivory};height:100%;padding:${v.sec}px ${v.pad}px;box-sizing:border-box;display:flex;align-items:center`, d(`display:grid;grid-template-columns:${por?'1fr':'1fr 1fr'};gap:${dsk?48:24}px;align-items:center;width:100%`, text + im));",
              "return d(`background:${T.ivory};height:100%;padding:${secPad(b, v)};box-sizing:border-box;display:flex;align-items:center`, d(`display:grid;grid-template-columns:${por?'1fr':'1fr 1fr'};gap:${dsk?48:24}px;align-items:center;width:100%`, text + im));")

# ---------- 5. Directions buttons in the hero are real external links ----------
js = rep(js, "const ctas = d(`display:flex;gap:${lnd?8:12}px;flex-wrap:wrap;margin-top:${lnd?14:24}px`, btn(b.cta1,'primary',true,lnd?44:48) + (b.cta2 ? btn(b.cta2,'secondary',true,lnd?44:48) : ''));",
              "const ctaEl = (label, kind) => label === 'Get directions' ? btnA(label, kind, true, lnd?44:48, DIRECTIONS_URL, ext) : btn(label, kind, true, lnd?44:48);\n  const ctas = d(`display:flex;gap:${lnd?8:12}px;flex-wrap:wrap;margin-top:${lnd?14:24}px`, ctaEl(b.cta1,'primary') + (b.cta2 ? ctaEl(b.cta2,'secondary') : ''));")

# ---------- 6. footer: compact phone nav, real (non-submitting) email field ----------
js = rep(js, "d(`display:flex;flex-direction:column;gap:10px;font:500 13px/1.3 ${T.body};letter-spacing:.06em;text-transform:uppercase;color:${T.parchment}`, NAV.concat(['Request a Table','Gift Cards']).map(n=>`<div ${act(n)}>${n}</div>`).join('')) +",
              "d(`display:${dsk?'flex;flex-direction:column':'grid;grid-template-columns:1fr 1fr'};gap:${dsk?'10px':'12px 16px'};font:500 13px/1.3 ${T.body};letter-spacing:.06em;text-transform:uppercase;color:${T.parchment}`, NAV.concat(['Request a Table','Gift Cards']).map(n=>`<div ${act(n)}>${n}</div>`).join('')) +")
js = rep(js, "d('display:flex;margin-top:8px', d(`flex:1;min-height:44px;border:1px solid ${T.foxing};display:flex;align-items:center;padding:0 12px;font:400 14px/1 ${T.body};color:${T.foxing}`, 'you@example.com') + btn('Join','inverse',true,44))",
              "d('display:flex;margin-top:8px', `<input type=\"email\" aria-label=\"Email address\" autocomplete=\"email\" style=\"flex:1;min-width:0;min-height:44px;box-sizing:border-box;border:1px solid ${T.brass};border-radius:0;background:transparent;padding:0 12px;font:400 16px/1 ${T.body};color:${T.parchment};-webkit-appearance:none;appearance:none\">` + btn('Join','inverse',true,44))")
js = rep(js, "const cols = dsk ? '1.2fr 1fr 1.2fr 1fr' : lnd ? '1fr 1fr' : '1fr';", "const cols = dsk ? '1.2fr 1fr 1.2fr 1fr' : lnd ? '1fr 1fr' : '1fr';\n  const por = v.id==='portrait';")
js = rep(js, "return d(`position:relative;overflow:hidden;background:${T.ink};height:100%;padding:${dsk?48:32}px ${v.pad}px;box-sizing:border-box`, etch(560, -160, -60, .22) +\n    d(`position:relative;display:grid;grid-template-columns:${cols};gap:${dsk?40:24}px`,",
              "return d(`position:relative;overflow:hidden;background:${T.ink};height:100%;padding:${dsk?48:28}px ${v.pad}px;box-sizing:border-box`, etch(560, -160, -60, .22) +\n    d(`position:relative;display:grid;grid-template-columns:${cols};gap:${dsk?40:por?22:24}px`,")

# ---------- 7. form: no dummy numbers; a submit says plainly that nothing was sent ----------
js = rep(js, "inputBox('Phone', val('phone', st.error?'':(OPTS.site?'':'(260) 555-0100')), {type:'tel', error: st.error ? 'Enter a phone number so staff can confirm your request.' : '', placeholder:'(260) 000-0000', helper: st.error?'':'Staff confirm by phone or text'})",
              "inputBox('Phone', val('phone', st.error?'':(OPTS.site?'':'(260) 555-0100')), {type:'tel', error: st.error ? 'Enter a phone number so staff can confirm your request.' : '', placeholder:'', helper: st.error?'':'Staff confirm by phone or text'})")
js = rep(js, "inputBox('Email', val('email',''), {optional:true,placeholder:'you@example.com',type:'email'})", "inputBox('Email', val('email',''), {optional:true,placeholder:'',type:'email'})")
js = rep(js, "inputBox('Name', val('name', OPTS.site?'':'Jane Doe'), {placeholder:'Your name'})", "inputBox('Name', val('name', OPTS.site?'':'Jane Doe'), {placeholder:''})")
js = rep(js, "  if (st.received) inner +=",
              "  if (st.notsent) inner += panel('Preview only · nothing was sent', 'Your request was not sent.', d('margin-top:10px', body('Online table requests are not connected yet, so nothing reached the restaurant. Please call us to request a table.', T.ink, 16) + d('display:flex;gap:12px;flex-wrap:wrap;margin-top:18px', btnA('Call (260) 744-9490','primary',false,44,TEL))));\n  if (st.received) inner +=")

open(out_js, 'w').write(js)

# ---------- template: fonts, controller ----------
# drop the Crimson Pro faces, add self-hosted Newsreader (variable wght + opsz)
faces = re.findall(r"/\* [a-z-]+ \*/\n@font-face \{\n  font-family: 'Crimson Pro';.*?\}\n", tpl, re.S)
assert len(faces) == 12, len(faces)
for f in faces: tpl = rep(tpl, f, '')
NEWS = """@font-face {
  font-family: 'Newsreader';
  font-style: normal;
  font-weight: 200 800;
  font-display: swap;
  src: url(fonts/newsreader/Newsreader-VF.woff2) format('woff2');
}
@font-face {
  font-family: 'Newsreader';
  font-style: italic;
  font-weight: 200 800;
  font-display: swap;
  src: url(fonts/newsreader/Newsreader-Italic-VF.woff2) format('woff2');
}
"""
tpl = rep(tpl, "<style>/* cyrillic-ext */\n", "<style>" + NEWS + "/* cyrillic-ext */\n")

# favicon: replace the data-URI icon in the template head
icon_re = re.compile(r'<link rel="icon" type="image/png" href="data:image/png;base64,[^"]+">')
assert len(icon_re.findall(tpl)) == 2, len(icon_re.findall(tpl))
ICONS = '<link rel="icon" href="favicon.ico?v=2" sizes="48x48"><link rel="icon" href="favicon.svg?v=2" type="image/svg+xml"><link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png?v=2"><link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png?v=2">'
tpl = icon_re.sub(ICONS, tpl)
tpl = rep(tpl, '<link rel="apple-touch-icon" href="https://squidbay.github.io/oyster-bar-preview/apple-touch-icon.png">', '<link rel="apple-touch-icon" href="https://squidbay.github.io/oyster-bar-preview/apple-touch-icon.png?v=2">')

# controller
tpl = rep(tpl, "'Lunch menu & hours':'/lunch','See the lunch menu':'/lunch','Directions & parking':'/visit','Visit & parking':'/visit',",
               "'Lunch menu & hours':'/lunch','See the lunch menu':'/lunch','Directions & parking':'/visit','Visit & parking':'/visit','Visit & Parking →':'/visit',")
tpl = rep(tpl, "      const el = e.target.closest('[data-act]'); if (!el) return;\n      const label = el.getAttribute('data-act');",
"""      const ios = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
      const a = e.target.closest('a[href]');
      if (a) {
        // Real links (tel:, maps, social) follow their href. Directions keep the iOS hand-off to Apple Maps.
        if (ios && /google\\.com\\/maps\\/dir\\//.test(a.href)) { e.preventDefault(); window.location.href = 'https://maps.apple.com/?q=The+Oyster+Bar&address=1830+S+Calhoun+St,+Fort+Wayne,+IN+46802'; }
        return;
      }
      const el = e.target.closest('[data-act]'); if (!el) return;
      const label = el.getAttribute('data-act');
      if (label.indexOf('Jump · ') === 0) { const J = {'Starters':'starters','Oysters':'oysters','Classics':'classics','Fish Market':'fish','Scratch Kitchen':'scratch','Cocktails':'cocktails','Wine':'wine'}; this.scrollToAnchor(J[label.slice(7)]); return; }
      if (label === 'Gift Cards' || label === 'Buy a gift card') { if (document.querySelector('[data-anchor="giftcards"]')) this.setState({ open:false }, () => this.scrollToAnchor('giftcards')); else this.go('/#giftcards'); return; }""")
tpl = rep(tpl, "      if (label === 'Gift Cards' || label === 'Buy a gift card') { this.say('Online gift cards are coming soon.'); return; }\n", "")
# Request a Table is a preview: any complete submit reports that nothing was sent.
tpl = rep(tpl, """    if (sunday) { this.setState({ values, formState:'unavailable' }); return; }
    if (large) { this.setState({ values, formState:'large' }); return; }
    this.setState({ values, formState:'submitting' });
    clearTimeout(this.timer);
    this.timer = setTimeout(() => this.setState({ formState:'received' }), 1400);""",
"""    this.setState({ values, formState:'notsent' });""")
tpl = rep(tpl, "  var RESULTS = ['Request received · pending staff confirmation',", "  var RESULTS = ['Preview only · nothing was sent', 'Request received · pending staff confirmation',")
tpl = rep(tpl, "var BUTTON = /^(MENU|CALL|Call\\b|Send request|Get directions|Open in maps|Gift Cards|Buy a gift card|Join|Pick another date|Change or cancel request)/;",
               "var BUTTON = /^(MENU|CALL|Call\\b|Send request|Get directions|Open in maps|Gift Cards|Buy a gift card|Join|Pick another date|Change or cancel request|Jump · )/;")
tpl = rep(tpl, '<link rel="preconnect" href="https://fonts.googleapis.com">\n', '')
open(out_tpl, 'w').write(tpl)
print('patched', len(js), len(tpl))

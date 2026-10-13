import sys
src, menu_js, out = sys.argv[1:4]
s = open(src).read()
menu = open(menu_js).read().split('\n')[0]
def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (n, old[:90])
    s = s.replace(old, new)

# ---- 1. data: photos, menu, oyster board, notices ----
DATA = r'''
/* ---------- owner content (website preview only) ---------- */
/* Menu transcribed from fwoysterbar.com/menu (retrieved 2026-10-13); see MENU-SOURCE.md. No prices are published there, so none are shown. */
''' + menu + r'''
const GF_NOTE = 'These items are or can be made gluten free';
const RAW_NOTE = 'Consuming raw or undercooked meats, poultry, seafood, shellfish or egg may increase your risk of food borne illness, especially if you have certain medical conditions';
const MG = (key, ...names) => MENU[key].filter(g => names.includes(g.name));
/* Oysters rotate daily, so the board describes how it works instead of listing today's selection. */
const OYSTER_BOARD = [['The Oyster Board','Our daily selection from the East and West Coasts, served with lemon and house mignonette. Ask what’s on the board today.'],
  ['Raw oysters','Chesapeake Bay oysters by the full or half dozen, with cocktail sauce, mignonette, fresh horseradish, saltines and lemon'],
  ['Baked oysters','Parmesan, Rockefeller, Casino, Fried, Blue Crab or Picatta']];
/* Photographs from fwoysterbar.com, stored locally; sources in PHOTOS.md. pos = object-position for the crop. */
const PHOTO = {
  sign:{src:'images/home-neon-sign.jpg',alt:'The Oyster Bar’s neon sign: The Oyster Bar, Steaks, Cocktails',pos:'50% 82%'},
  patio:{src:'images/patio-and-sign.jpg',alt:'The patio on Calhoun Street under The Oyster Bar sign',pos:'50% 24%'},
  barOysters:{src:'images/bar-oysters-and-beer.jpg',alt:'Oysters on the half shell with lemon and beers on the bar',pos:'50% 90%'},
  lunch:{src:'images/lunch-sandwich.jpg',alt:'A sandwich plated at the bar',pos:'45% 50%'},
  dinnerFish:{src:'images/dinner-plated-fish.jpg',alt:'A plated fish dinner with microgreens and sauce',pos:'50% 50%'},
  shrimp:{src:'images/dinner-shrimp.jpg',alt:'Two large shrimp, seasoned and roasted',pos:'50% 50%'},
  fishPlate:{src:'images/fish-market-plate.jpg',alt:'A fresh fish fillet plated over greens',pos:'50% 55%'},
  fishZucchini:{src:'images/fish-with-zucchini.jpg',alt:'Fresh fish with grilled zucchini and microgreens',pos:'50% 40%'},
  oysters:{src:'images/oysters-on-ice.jpg',alt:'Freshly shucked oysters on ice',pos:'50% 50%'},
  barRoom:{src:'images/bar-room-crowd.jpg',alt:'A full bar room in black and white',pos:'50% 55%'},
  historyBar:{src:'images/history-at-the-bar.jpg',alt:'Two men at the bar in black and white',pos:'50% 40%'},
  diningRoom:{src:'images/dining-room-photo-wall.jpg',alt:'The dining room in black and white, its wall hung with framed photographs',pos:'50% 35%'},
  owners:{src:'images/owners-at-the-bar.jpg',alt:'Kara and Tony West raising a glass at the bar',pos:'50% 50%'},
  toast:{src:'images/toast-at-the-bar.jpg',alt:'Guests raising their glasses at the bar, in black and white',pos:'50% 40%'},
  dinnerWine:{src:'images/dinner-and-wine-at-the-bar.jpg',alt:'A plated dinner and a glass of white wine on the bar',pos:'50% 75%'}
};
'''
rep("/* ---------- content ---------- */", DATA + "\n/* ---------- content ---------- */")

# ---- 2. photo slot: the existing panel frame, with a real photograph inside ----
rep("const img = (label, ratio, dark, extra='') => OPTS.site ? sitePanel(label, ratio, dark, extra) :",
    "const photoPanel = (ph, ratio, dark, extra='', eager) => d(`aspect-ratio:${ratio};width:100%;box-sizing:border-box;position:relative;overflow:hidden;background:${dark ? '#1C1714' : '#EFE4CC'};border:1px solid ${dark ? '#3A312C' : T.foxing};${extra}`,\n"
    "  `<img src=\"${ph.src}\" alt=\"${esc(ph.alt)}\" data-photo=\"${ph.src}\"${eager ? '' : ' loading=\"lazy\"'} decoding=\"async\" style=\"position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:${ph.pos};display:block\">` +\n"
    "  (dark ? '<div style=\"position:absolute;inset:0;pointer-events:none;box-shadow:inset 0 0 60px rgba(23,18,14,.55);background:linear-gradient(180deg,rgba(23,18,14,0) 55%,rgba(23,18,14,.35))\"></div>' : ''));\n"
    "const img = (label, ratio, dark, extra='', ph, eager) => OPTS.site ? (ph ? photoPanel(ph, ratio, dark, extra, eager) : sitePanel(label, ratio, dark, extra)) :")

# hero: photo in the designed image column; on phones it follows the text so the calls to action stay first
rep("const imgEl = d('position:relative', img(`Hero image ${ratio.replace('/',':')} · owned photo · alt required`, ratio, true, lnd?'aspect-ratio:auto;height:258px':''));\n  const grid = por ? d('display:grid;grid-template-columns:1fr;gap:24px', imgEl + textCol)",
    "const imgEl = d('position:relative', img(`Hero image ${ratio.replace('/',':')} · owned photo · alt required`, ratio, true, lnd?'aspect-ratio:auto;height:258px':'', OPTS.site && b.photo, true));\n  const grid = por ? d('display:grid;grid-template-columns:1fr;gap:24px', (OPTS.site && b.photo) ? textCol + imgEl : imgEl + textCol)")
# split / cards / fish
rep("img(`Image ${ratio.replace('/',':')} · owned photo`, ratio, false))", "img(`Image ${ratio.replace('/',':')} · owned photo`, ratio, false, '', OPTS.site && b.photo))")
rep("img(`Image ${ratio.replace('/',':')}`, ratio, false, 'border:0;border-bottom:1px solid '+T.foxing)", "img(`Image ${ratio.replace('/',':')}`, ratio, false, 'border:0;border-bottom:1px solid '+T.foxing, OPTS.site && c.photo)")

# feature: eyebrow can be set per block
rep("eyebrow(OPTS.site ? 'Posted by the kitchen' : 'Managed · updated [date]', T.oxblood, 11)", "eyebrow(OPTS.site ? (b.eyebrow || 'Posted by the kitchen') : 'Managed · updated [date]', T.oxblood, 11)")

# ---- 3. menu rows: real groups, notes, gluten-free marks, compact wine lists, notices ----
OLD_ROWS = s[s.index("function rows(b, v) {"):s.index("function fish(b, v) {")]
NEW_ROWS = OLD_ROWS.replace("function rows(b, v) {", "function rowsBase(b, v) {") + r'''function rows(b, v) {
  if (!(OPTS.site && b.menu)) return rowsBase(b, v);
  const dsk = v.id==='desktop', por = v.id==='portrait';
  const gfMark = sp(`display:inline-block;margin-left:8px;padding:1px 5px;border:1px solid ${T.brass};font:600 10px/1.3 ${T.body};letter-spacing:.08em;color:#6E5424;vertical-align:3px;white-space:nowrap`, 'GF') ;
  const group = g => d(`break-inside:avoid;margin-bottom:${dsk?36:28}px`,
    d(`border-bottom:1px solid ${T.ink};padding-bottom:8px`, eyebrow(g.name, T.oxblood, 13)) +
    (g.note ? small(g.note, '#4A4842', 'margin-top:10px;font-style:italic;font-size:14px') : '') +
    (g.list
      ? d(`display:grid;grid-template-columns:${por?'1fr':'1fr 1fr'};column-gap:24px`, g.items.map(i => d(`padding:10px 0;border-bottom:1px solid ${T.foxing};font:600 ${dsk?18:17}px/1.25 ${T.display};color:${T.ink}`, esc(i.n))).join(''))
      : g.items.map(i => d(`padding:${i.sub?'4px 0 14px 16px':'14px 0'};border-bottom:1px solid ${T.foxing}${i.sub?';margin-top:-1px':''}`,
          d('', sp(`font:600 ${i.sub?16:(dsk?22:20)}px/1.2 ${T.display};color:${T.ink}`, esc(i.n)) + (i.gf ? gfMark.replace('<span', '<span title="'+GF_NOTE+'" aria-label="Gluten free or can be made gluten free"') : '')) +
          (i.d ? small(esc(i.d), '#4A4842', 'margin-top:4px;font-size:14px') : ''))).join('')));
  const head = b.title ? d(`margin-bottom:${dsk?28:20}px`, (b.eyebrow ? eyebrow(b.eyebrow, T.oxblood, 11) : '') + d(b.eyebrow?'margin-top:8px':'', h2(b.title, T.ink, dsk?36:26))) : '';
  const notes = (b.gf || b.raw) ? d(`border-top:1px solid ${T.ink};padding-top:14px;display:grid;gap:8px;max-width:80ch`,
    (b.gf ? small(sp(`font-weight:600;color:#6E5424`, 'GF') + ' · ' + GF_NOTE + '.', '#2A2926', 'font-size:14px') : '') +
    (b.raw ? small(RAW_NOTE + '.', '#2A2926', 'font-size:14px') : '')) : '';
  return d(`background:${T.parchment};height:100%;padding:${v.sec}px ${v.pad}px;box-sizing:border-box`,
    head + d(dsk ? 'column-count:2;column-gap:64px' : '', b.menu.map(group).join('')) + notes);
}
'''
s = s.replace(OLD_ROWS, NEW_ROWS)

# ---- 4. Fresh Fish Market: the published wording and the four real preparations ----
rep("box('Step 2 · Choose your fish', img('Image 3:2 · owned photo', '3/2', false))", "box('Step 2 · Choose your fish', img('Image 3:2 · owned photo', '3/2', false, '', OPTS.site && b.photo))")
rep("d('margin-top:12px;max-width:60ch', body('See today’s fish, choose one, then choose one of four preparations. This is how it works; the order happens at the table.', '#2A2926', 16)) +",
    "d('margin-top:12px;max-width:60ch', body(OPTS.site ? 'Choose From One of Our Daily Fresh Fish Selections & Then Choose One of Our Preparations' : 'See today’s fish, choose one, then choose one of four preparations. This is how it works; the order happens at the table.', '#2A2926', 16)) +")
rep("box('Step 1 · Today’s fish', d('display:grid;gap:8px', opt('Walleye — VERIFY') + opt('Grouper — VERIFY') + opt('Salmon — VERIFY'))) +",
    "box('Step 1 · Today’s fish', OPTS.site ? body('Our fresh fish changes daily. Ask your server for today’s selections.', T.ink, 15) : d('display:grid;gap:8px', opt('Walleye — VERIFY') + opt('Grouper — VERIFY') + opt('Salmon — VERIFY'))) +")
rep("box('Step 3 · One of four preparations', d('display:grid;grid-template-columns:1fr 1fr;gap:8px', opt('Grilled') + opt('Blackened') + opt('Pan-fried') + opt('Broiled')))) +",
    "box('Step 3 · One of four preparations', OPTS.site ? d('display:grid;gap:8px', MENU.dinner.find(g => g.name === 'Fresh Fish Market').items.filter(i => i.n === '~').map(i => opt(i.d)).join('')) : d('display:grid;grid-template-columns:1fr 1fr;gap:8px', opt('Grilled') + opt('Blackened') + opt('Pan-fried') + opt('Broiled')))) +")
rep("btn('Request a Table','primary',false,44) + small(OPTS.site ? 'Market price' : 'Market price — wording VERIFY with owner', '#5E5B55')));",
    "btn('Request a Table','primary',false,44) + (OPTS.site ? '' : small('Market price — wording VERIFY with owner', '#5E5B55'))));")

# ---- 5. pages: wire in the content ----
P = [
 # home
 ("cta1:'Request a Table',cta2:'Lunch menu & hours',note:'Lunch + Request above the fold on all three viewports'}",
  "cta1:'Request a Table',cta2:'Lunch menu & hours',note:'Lunch + Request above the fold on all three viewports',photo:PHOTO.sign}"),
 ("{k:'feature',title:\"Today's Oysters & Current Features\",items:[['Blue Point','Long Island · briny, clean finish'],['Kumamoto','Pacific · small, sweet, cucumber'],['Wellfleet','Cape Cod · bright, mineral'],['Current feature','Kitchen note of the day']],cta:'Request a Table',note:'One owner update feeds this module first; social and email later'}",
  "{k:'feature',title:\"Today's Oysters & Current Features\",eyebrow:'Selections change daily',items:OYSTER_BOARD,cta:'Request a Table',note:'One owner update feeds this module first; social and email later'}"),
 ("items:['Quick lunch for downtown workers','Groups and convention lunches','Own lot, about 30 spots'],cta:'See the lunch menu'}",
  "items:['Quick lunch for downtown workers','Groups and convention lunches','Own lot, about 30 spots'],cta:'See the lunch menu',photo:PHOTO.barOysters}"),
 ("{t:'Dinner & Cocktails',s:'Raw bar, dinner movers, and the craft cocktail list',l:'Dinner & Cocktails'},{t:'Fresh Fish Market',s:'Choose your fish, choose one of four preparations',l:'How it works'},{t:'History since 1888',s:'Documented history and house legend, kept distinct',l:'Read the history'}",
  "{t:'Dinner & Cocktails',s:'Oysters raw and baked, the kitchen’s classics and the craft cocktail list',l:'Dinner & Cocktails',photo:PHOTO.dinnerFish},{t:'Fresh Fish Market',s:'Choose your fish, choose one of four preparations',l:'How it works',photo:PHOTO.fishPlate},{t:'History since 1888',s:'Documented history and house legend, kept distinct',l:'Read the history',photo:PHOTO.historyBar}"),
 # lunch
 ("chip:'Hours VERIFY',cta1:'Request a Table',cta2:'Call (260) 744-9490',note:'Hours, parking and Request visible on arrival'}",
  "chip:'Hours VERIFY',cta1:'Request a Table',cta2:'Call (260) 744-9490',note:'Hours, parking and Request visible on arrival',photo:PHOTO.lunch}"),
 ("{k:'rows',groups:[lunchRows,{name:'Lunch menu',tag:'APPROVED MENU PENDING',items:[['Category item','Short description line from the kitchen'],['Category item','Short description line from the kitchen'],['Category item','Short description line from the kitchen'],['Category item','Short description line from the kitchen']]}]},\n    {k:'feature',title:\"Today's Oysters\",items:[['Blue Point','Long Island · briny, clean finish'],['Kumamoto','Pacific · small, sweet, cucumber'],['Wellfleet','Cape Cod · bright, mineral']],cta:'Request a Table',note:'Same module as Home; one source'}",
  "{k:'rows',anchor:'menu',eyebrow:'Lunch',title:'The lunch menu',menu:MENU.lunch,raw:true,groups:[lunchRows,{name:'Lunch menu',tag:'APPROVED MENU PENDING',items:[['Category item','Short description line from the kitchen'],['Category item','Short description line from the kitchen'],['Category item','Short description line from the kitchen'],['Category item','Short description line from the kitchen']]}]},\n    {k:'feature',title:\"Today's Oysters\",eyebrow:'Selections change daily',items:OYSTER_BOARD,cta:'Request a Table',note:'Same module as Home; one source'}"),
 ("items:['Grand Wayne and downtown convention traffic','Large parties handed to staff'],cta:'Send a group inquiry'}",
  "items:['Grand Wayne and downtown convention traffic','Large parties handed to staff'],cta:'Send a group inquiry',photo:PHOTO.barRoom}"),
 # dinner
 ("sub:'Raw bar, dinner movers, the Fresh Fish Market and a craft cocktail list.',chip:'Hours VERIFY',cta1:'Request a Table',cta2:'Jump to cocktails'}",
  "sub:'Oysters raw and baked, the Fresh Fish Market, the butcher’s cuts and a craft cocktail list.',chip:'Hours VERIFY',cta1:'Request a Table',cta2:'Jump to cocktails',photo:PHOTO.shrimp}"),
 ("{k:'rows',groups:[{name:'Raw Bar',tag:\"LINKS TO TODAY'S OYSTERS\",items:[['Oysters on the Half Shell','Today’s selection, half or full dozen'],['Oysters Rockefeller','Spinach, herb butter, breadcrumb'],['Oysters Casino','Bacon, peppers, butter']]},{name:'Dinner movers',tag:'APPROVED MENU PENDING',items:[['Scallops','Seared, brown butter'],['Walleye','Pan-fried, lemon'],['Seafood Au Gratin','House classic'],['Filet','Eight ounces, char-grilled'],['Jambalaya','Shrimp, andouille, rice'],['Ribs','Slow-cooked, house sauce']]}]},\n    {k:'fish',anchor:'fish'},",
  "{k:'rows',anchor:'menu',eyebrow:'Dinner',title:'The dinner menu',menu:MG('dinner','Starters','Raw Oysters','Baked Oysters','Oyster Bar Classics','From the Butcher'),groups:[{name:'Raw Bar',tag:\"LINKS TO TODAY'S OYSTERS\",items:[['Oysters on the Half Shell','Today’s selection, half or full dozen'],['Oysters Rockefeller','Spinach, herb butter, breadcrumb'],['Oysters Casino','Bacon, peppers, butter']]},{name:'Dinner movers',tag:'APPROVED MENU PENDING',items:[['Scallops','Seared, brown butter'],['Walleye','Pan-fried, lemon'],['Seafood Au Gratin','House classic'],['Filet','Eight ounces, char-grilled'],['Jambalaya','Shrimp, andouille, rice'],['Ribs','Slow-cooked, house sauce']]}]},\n    {k:'fish',anchor:'fish',photo:PHOTO.fishPlate},\n    {k:'rows',siteOnly:true,menu:MG('dinner','Scratch Kitchen','Oyster Bar Sides'),gf:true,raw:true,groups:[]},"),
 ("{k:'rows',anchor:'cocktails',groups:[{name:'Cocktails',tag:'#cocktails · CRAFT LIST · JULY 2025 · PENDING'",
  "{k:'rows',anchor:'cocktails',eyebrow:'Drinks',title:'Cocktails, wine & bottles',menu:MENU.drinks,groups:[{name:'Cocktails',tag:'#cocktails · CRAFT LIST · JULY 2025 · PENDING'"),
 ("{k:'feature',title:\"Today's Oysters\",items:[['Blue Point','Long Island · briny, clean finish'],['Kumamoto','Pacific · small, sweet, cucumber'],['Wellfleet','Cape Cod · bright, mineral']],cta:'Request a Table'},\n    {k:'band',items:[{t:'Request a table for dinner'",
  "{k:'feature',title:\"Today's Oysters\",eyebrow:'Selections change daily',items:OYSTER_BOARD,cta:'Request a Table'},\n    {k:'band',items:[{t:'Request a table for dinner'"),
 # oysters
 ("sub:'What is on the bar today, posted by the kitchen. This page is a board, not a brochure.',chip:'Happy hour oysters · VERIFY',cta1:'Request a Table',cta2:'Call'}",
  "sub:'What is on the bar today, posted by the kitchen. This page is a board, not a brochure.',siteSub:'Our oyster board changes with what comes in from the East and West Coasts. Ask your server what’s on it today.',chip:'Happy hour oysters · VERIFY',cta1:'Request a Table',cta2:'Call',photo:PHOTO.oysters}"),
 ("{k:'feature',title:\"Today's Oysters\",items:[['Blue Point','Long Island · briny, clean finish'],['Kumamoto','Pacific · small, sweet, cucumber'],['Wellfleet','Cape Cod · bright, mineral'],['Beausoleil','New Brunswick · delicate, salty']],cta:'Request a Table',note:'Primary instance of C-03'},\n    {k:'fish'},",
  "{k:'feature',title:\"Today's Oysters\",eyebrow:'Selections change daily',items:OYSTER_BOARD,cta:'Request a Table',note:'Primary instance of C-03'},\n    {k:'rows',siteOnly:true,anchor:'menu',eyebrow:'On the menu',title:'Raw & baked oysters',menu:MG('dinner','Raw Oysters','Baked Oysters'),gf:true,raw:true,groups:[]},\n    {k:'fish',photo:PHOTO.fishZucchini},"),
 # history
 ("title:'Since 1888, at 1830 South Calhoun.',sub:'The documented record and the house legend, kept apart so you can tell which is which.',cta1:'Request a Table',cta2:'Jump to timeline'}",
  "title:'Since 1888, at 1830 South Calhoun.',sub:'The documented record and the house legend, kept apart so you can tell which is which.',cta1:'Request a Table',cta2:'Jump to timeline',photo:PHOTO.diningRoom}"),
 ("items:['Chef-owner Tony West (press-covered)','The rooms as they are — owned photos'],cta:'Visit & parking'}",
  "items:['Chef-owner Tony West (press-covered)','The rooms as they are — owned photos'],cta:'Visit & parking',photo:PHOTO.owners}"),
 # events
 ("sub:'Special Sunday dinners, private dining in the back room, and off-site catering. Dates and policy to be confirmed.',cta1:'Send an inquiry',cta2:'Call'}",
  "sub:'Special Sunday dinners, private dining in the back room, and off-site catering. Dates and policy to be confirmed.',cta1:'Send an inquiry',cta2:'Call',photo:PHOTO.toast}"),
 ("items:['Room capacity — VERIFY','Sunday buyouts — policy VERIFY','Inquiry: date, headcount, occasion'],cta:'Private dining inquiry'}",
  "items:['Room capacity — VERIFY','Sunday buyouts — policy VERIFY','Inquiry: date, headcount, occasion'],cta:'Private dining inquiry',photo:PHOTO.dinnerWine}"),
 ("text:'Oysters, fish and the dinner movers, brought to your event.'", "text:'Oysters, fish and the dinner movers, brought to your event.',siteText:'Oysters, fish and dinner favorites, brought to your event.'"),
 # visit
 ("chip:'Hours VERIFY',cta1:'Get directions',cta2:'Request a Table'}", "chip:'Hours VERIFY',cta1:'Get directions',cta2:'Request a Table',photo:PHOTO.patio}"),
]
for o, n in P: rep(o, n)

# ---- 6. site-mode plumbing: site-only blocks and copy overrides; spec boards ignore them ----
rep("function siteBlock(b) {\n  if (b.k === 'quote') return null;",
    "function siteBlock(b) {\n  if (b.k === 'quote') return null;\n  if (b.siteSub) b = {...b, sub: b.siteSub};\n  if (b.siteText) b = {...b, text: b.siteText};")
rep("const p = OPTS.site ? {...p0, blocks: p0.blocks.map(siteBlock).filter(Boolean)} : p0;",
    "const p = OPTS.site ? {...p0, blocks: p0.blocks.map(siteBlock).filter(Boolean)} : {...p0, blocks: p0.blocks.filter(b => !b.siteOnly)};")
open(out, 'w').write(s)
print('ok', len(s))

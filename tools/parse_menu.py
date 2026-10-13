import sys, json, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.stack=[]; s.menus=[]; s.cap=None; s.buf=''
    def handle_starttag(s,tag,attrs):
        c=dict(attrs).get('class','') or ''
        s.stack.append(c)
        if tag=='br' : 
            s.stack.pop(); 
            if s.cap: s.buf+='\n'
            return
        if 'menu-wrapper' in c.split(): s.menus.append({'sections':[]})
        elif c=='menu-section': s.menus[-1]['sections'].append({'title':'','items':[]})
        elif c.startswith('menu-item') and c.split()[0]=='menu-item': s.menus[-1]['sections'][-1]['items'].append({'title':'','desc':'','options':[],'price':''})
        for k in ('menu-section-title','menu-section-description','menu-item-title','menu-item-description','menu-item-option','menu-item-price-top','menu-item-price-bottom'):
            if c==k: s.cap=k; s.buf=''
    def handle_endtag(s,tag):
        if not s.stack: return
        c=s.stack.pop()
        if s.cap and c==s.cap:
            t=re.sub(r'[ \t\xa0]+',' ',html.unescape(s.buf)).strip()
            sec=s.menus[-1]['sections'][-1] if s.menus and s.menus[-1]['sections'] else None
            if c=='menu-section-title': sec['title']=t
            elif c=='menu-section-description': sec['desc']=t
            elif c=='menu-item-title': sec['items'][-1]['title']=t
            elif c=='menu-item-description': sec['items'][-1]['desc']=t
            elif c=='menu-item-option': sec['items'][-1]['options'].append(t)
            else:
                if t: sec['items'][-1]['price']=t
            s.cap=None
    def handle_data(s,d):
        if s.cap: s.buf+=d
p=P(); p.feed(open(sys.argv[1]).read())
json.dump(p.menus, sys.stdout, indent=1, ensure_ascii=False)

import sys, os
from PIL import Image, ImageOps
src, dst = sys.argv[1], sys.argv[2]
PLAN = [  # source file, local name, max width
 ('p05_16768104.jpg','home-neon-sign.jpg',1400),
 ('p15_68dd2ee4.jpg','bar-oysters-and-beer.jpg',720),
 ('p36_eba8616a.jpg','dinner-plated-fish.jpg',1200),
 ('p32_dd4dfa4e.jpg','fish-market-plate.jpg',1080),
 ('p34_e5bf829b.jpg','history-at-the-bar.jpg',1200),
 ('p22_90152e57.jpg','lunch-sandwich.jpg',1400),
 ('p29_cd3d475a.jpg','bar-room-crowd.jpg',1000),
 ('p30_ce56df0c.jpg','dinner-shrimp.jpg',1080),
 ('p11_3eda940e.jpg','oysters-on-ice.jpg',1400),
 ('p37_f2cb6385.jpg','fish-with-zucchini.jpg',1000),
 ('p08_2446f991.jpg','dining-room-photo-wall.jpg',1080),
 ('p31_cf5230e6.jpg','owners-at-the-bar.jpg',1400),
 ('p33_e09d6ac9.jpg','toast-at-the-bar.jpg',1080),
 ('p04_11df3120.jpg','dinner-and-wine-at-the-bar.jpg',843),
 ('p25_b1ddb4fc.jpg','patio-and-sign.jpg',1100),
]
for f, name, mw in PLAN:
    im = ImageOps.exif_transpose(Image.open(os.path.join(src, f))).convert('RGB')
    if im.width > mw: im = im.resize((mw, round(im.height * mw / im.width)), Image.LANCZOS)
    im.save(os.path.join(dst, name), 'JPEG', quality=74, optimize=True, progressive=True)
    print(name, im.size, os.path.getsize(os.path.join(dst, name)))

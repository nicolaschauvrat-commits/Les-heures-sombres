import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S=sys.argv[1]
cov=Image.open(f'{S}/cover.jpg').convert('RGB')
F='/usr/share/fonts/truetype/liberation/'
def f(n,s): return ImageFont.truetype(F+n,s)
INK=(7,22,43); GOLD=(232,176,75); CREAM=(247,240,228); GREY=(190,185,175)
def ctext(d,y,t,font,fill,W,spacing=0):
    if spacing:
        w=sum(d.textlength(c,font=font) for c in t)+spacing*(len(t)-1); x=(W-w)/2
        for c in t: d.text((x,y),c,font=font,fill=fill); x+=d.textlength(c,font=font)+spacing
    else:
        w=d.textlength(t,font=font); d.text(((W-w)/2,y),t,font=font,fill=fill)
def make(W,H,cs,top,name):
    bg=cov.resize((W,W)).filter(ImageFilter.GaussianBlur(40)).crop((0,(W-H)//2 if H<W else 0,W,W))
    im=Image.new('RGB',(W,H),INK)
    bgf=cov.resize((H,H)).filter(ImageFilter.GaussianBlur(45)).crop(((H-W)//2,0,(H-W)//2+W,H))
    im.paste(bgf,(0,0))
    ov=Image.new('RGB',(W,H),INK); im=Image.blend(im,ov,0.55)
    d=ImageDraw.Draw(im)
    ctext(d,top,'LES HEURES SOMBRES PRÉSENTE',f('LiberationSerif-Regular.ttf',int(W*0.026)),GREY,W,spacing=4)
    ctext(d,top+int(W*0.05),'DISPONIBLE MAINTENANT',f('LiberationSerif-Bold.ttf',int(W*0.058)),GOLD,W,spacing=3)
    y=top+int(W*0.14)
    c=cov.resize((cs,cs),Image.LANCZOS)
    sh=Image.new('RGBA',(cs+60,cs+60),(0,0,0,0)); ImageDraw.Draw(sh).rectangle((30,30,cs+30,cs+30),fill=(0,0,0,170)); sh=sh.filter(ImageFilter.GaussianBlur(18))
    im.paste(sh,((W-cs)//2-30+8,y-30+14),sh)
    im.paste(c,((W-cs)//2,y))
    y+=cs+int(W*0.045)
    ctext(d,y,'Douze poèmes de Marie-Hélène Soulier, mis en musique',f('LiberationSerif-Italic.ttf',int(W*0.034)),CREAM,W)
    y+=int(W*0.065)
    ctext(d,y,'SPOTIFY  ·  APPLE MUSIC  ·  ET TOUTES LES PLATEFORMES',f('LiberationSans-Regular.ttf',int(W*0.024)),GOLD,W,spacing=2)
    im.save(f'{S}/{name}',quality=93)
make(1080,1350,820,60,'LHS-AHS-SORTIE-4x5.jpg')
make(1080,1920,900,250,'LHS-AHS-SORTIE-9x16.jpg')

"""Regenerate editable SVGs and upload bitmaps; no application capture or build.
Python 3 + Pillow + fontTools + CairoSVG. Run from any working directory.
"""
from pathlib import Path
import base64, io, json, html, shutil, hashlib, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools import subset
from PIL import Image, ImageDraw, ImageFont
import cairosvg

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
for d in ['svg','upload','extras','assets','review']:
    (ROOT/d).mkdir(exist_ok=True)
for filename in ['logo.png','ChillRound-LICENSE.txt']:
    if (REPO/'site/assets'/filename).exists():
        shutil.copy2(REPO/'site/assets'/filename, ROOT/'assets'/filename)
FONT = REPO/'maintenance/fonts/ChillRoundF.ttf'
if FONT.exists(): shutil.copy2(FONT,ROOT/'assets/ChillRoundF.ttf')
else: FONT=ROOT/'assets/ChillRoundF.ttf'
font = TTFont(FONT)
family = font['name'].getDebugName(1)
glyphs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font['head'].unitsPerEm
logo64 = base64.b64encode((ROOT/'assets/logo.png').read_bytes()).decode()
OUTLINE = False
TEXTS = []
INK = '#713b56'

def text(s,x,y,size,color=INK,anchor='start'):
    TEXTS.append(s)
    width=sum(glyphs[cmap[ord(c)]].width for c in s)*size/upm
    if anchor=='middle': x-=width/2
    if OUTLINE:
        parts=[]; cursor=0
        for c in s:
            g=glyphs[cmap[ord(c)]]; p=SVGPathPen(glyphs); g.draw(p)
            parts.append(f'<path transform="translate({cursor} 0)" d="{p.getCommands()}"/>'); cursor+=g.width
        return f'<g aria-label="{html.escape(s)}" fill="{color}" transform="translate({x} {y}) scale({size/upm} {-size/upm})">'+''.join(parts)+'</g>'
    return f'<text x="{x}" y="{y}" font-family="UtaeSteamRound, {family}" font-size="{size}" fill="{color}">{html.escape(s)}</text>'

def icon(x,y,s,angle=0):
    return f'<g id="product-icon" transform="translate({x} {y}) rotate({angle} {s/2} {s/2})"><image width="{s}" height="{s}" href="data:image/png;base64,{logo64}"/></g>'

def bg(w,h,quiet=False):
    fill='#2a202b' if quiet else 'url(#blush)'
    parts=[f'<rect width="{w}" height="{h}" fill="{fill}"/>']
    if quiet:
        parts += [f'<ellipse cx="{w*.05}" cy="{h*.7}" rx="{w*.24}" ry="{h*.65}" fill="#634154" opacity=".35"/>',f'<ellipse cx="{w*.98}" cy="{h*.2}" rx="{w*.22}" ry="{h*.58}" fill="#634154" opacity=".35"/>']
    else:
        parts += [f'<ellipse cx="{w*.88}" cy="{h*.53}" rx="{w*.38}" ry="{h*.73}" fill="#f7c0d8" opacity=".45"/>',f'<ellipse cx="{w*.96}" cy="{h*.52}" rx="{w*.26}" ry="{h*.58}" fill="#ffe3ed"/>']
        for x,y,r in [(.08,.12,.025),(.52,.12,.013),(.91,.87,.018),(.12,.88,.013)]:
            parts.append(f'<circle cx="{w*x}" cy="{h*y}" r="{min(w,h)*r}" fill="#d68aa9" opacity=".35"/>')
    return '<g id="background">'+''.join(parts)+'</g>'

def brand(x,y,size):
    return '<g id="product-title">'+text('utae',x,y,size)+text('avatar',x,y+size*.92,size)+'</g>'

def horizontal(w,h,small=False):
    s=h*(.93 if small else .94)
    available=w-s-h*.035-s*.055-w*.075-w*.035
    title_width=sum(glyphs[cmap[ord(c)]].width for c in 'avatar')/upm
    size=min(h*.31,available/title_width)
    return bg(w,h)+brand(w*.075,h*.43,size)+icon(w-s-h*.035,(h-s)/2,s,-6 if not small else 0)

def vertical(w,h):
    s=min(w*.89,h*.53)
    return bg(w,h)+brand(w*.13,h*.19,w*.21)+icon((w-s)/2,h*.42,s,-7)

def hero(w,h):
    return bg(w,h)+f'<ellipse cx="{w/2}" cy="910" rx="500" ry="90" fill="#d68aa9" opacity=".12"/>'+icon(w/2-380,140,760)

def promo(w,h,kind='promo'):
    a=bg(w,h)
    if kind=='header':
        return a+text('utae avatar',w*.16,h*.39,64)+text('让形象动起来。',w*.16,h*.64,90)+icon(w*.66,h*.20,h*.58)
    a+=text('utae avatar',w*.065,h*.19,h*.065)
    a+=text('让形象',w*.065,h*.43,h*.125)+text('动起来。',w*.065,h*.60,h*.125)
    if kind=='promo':
        a+=text('超高性能的 Live2D 虚拟形象动捕工具',w*.065,h*.78,h*.035)
    return a+icon(w*.57,h*.14,h*.72,-7)

def about(w,h,title,lines):
    a=bg(w,h)+text('utae avatar',40,60,25)+text(title,40,137,45)
    for i,s in enumerate(lines): a+=text(s,40,192+i*34,22)
    return a+icon(w-210,h-210,185,-5)

specs=[
 ('store-header',920,430,'required',lambda w,h:horizontal(w,h)),
 ('store-small',462,174,'required',lambda w,h:horizontal(w,h,True)),
 ('store-main',1232,706,'required',lambda w,h:horizontal(w,h)),
 ('store-vertical',748,896,'required',vertical),
 ('library-capsule',600,900,'required',vertical),
 ('library-header',920,430,'required',lambda w,h:horizontal(w,h)),
 ('library-hero',3840,1240,'required',hero),
 ('library-logo',1280,300,'required',lambda w,h:text('utae avatar',40,225,225)),
 ('shortcut-icon',512,512,'required',lambda w,h:icon(0,0,w)),
 ('app-icon',184,184,'required',lambda w,h:f'<rect width="{w}" height="{h}" fill="#ffedf5"/>'+icon(0,0,w)),
 ('store-background',1438,810,'optional',lambda w,h:bg(w,h,True)),
 ('event-cover',800,450,'conditional-event',lambda w,h:promo(w,h,'cover')),
 ('event-header',1920,622,'conditional-event',lambda w,h:promo(w,h,'header')),
 ('promo-landscape',1920,1080,'extra',promo),
 ('about-intro',1200,660,'extra',promo),
 ('about-tracking',1200,400,'extra',lambda w,h:about(w,h,'让表情，跟上你。',['摄像头与兼容 iPhone 来源','面捕矫正 · 参数平滑 · 麦克风嘴型辅助'])),
 ('about-models',1200,400,'extra',lambda w,h:about(w,h,'把形象，调成喜欢的样子。',['模型库 · 表情编辑 · 动作快捷键','参数绑定与图层设置'])),
 ('about-output',1200,400,'extra',lambda w,h:about(w,h,'准备好，就出镜。',['Spout2 直播输出','PNG 图片与分层 TIFF 导出'])),
]
defs='<defs><linearGradient id="blush" x2="1" y2="1"><stop stop-color="#fff8fa"/><stop offset="1" stop-color="#f9dce9"/></linearGradient></defs>'
def svg(w,h,body,style=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>utae avatar</title><metadata>Editable layout; original raster brand icon retained. PNG exports use straight alpha.</metadata>{style}{defs}{body}</svg>'

# Collect every character before subsetting the embedded font.
for name,w,h,status,fn in specs: fn(w,h)
subfont=TTFont(FONT); opts=subset.Options(); opts.flavor='woff2'
sub=subset.Subsetter(options=opts); sub.populate(text=''.join(TEXTS)); sub.subset(subfont)
# Rename the modified subset to avoid the OFL reserved font name.
for record in subfont['name'].names:
    if record.nameID in (1,2,3,4,6):
        value='Regular' if record.nameID==2 else 'UtaeSteamRound'
        record.string=value.encode(record.getEncoding(),errors='replace')
subfont.flavor='woff2'; buf=io.BytesIO(); subfont.save(buf)
(ROOT/'assets/UtaeSteamRound.woff2').write_bytes(buf.getvalue())
style='<style>@font-face{font-family:UtaeSteamRound;src:url(data:font/woff2;base64,'+base64.b64encode(buf.getvalue()).decode()+') format("woff2")}</style>'
manifest=[]
for name,w,h,status,fn in specs:
    OUTLINE=False; source=svg(w,h,fn(w,h),style)
    (ROOT/'svg'/f'{name}.svg').write_text(source,encoding='utf-8')
    OUTLINE=True; rendered=svg(w,h,fn(w,h))
    folder='extras' if status=='extra' else 'upload'
    path=ROOT/folder/f'{name}.png'
    cairosvg.svg2png(bytestring=rendered.encode(),write_to=str(path))
    im=Image.open(path)
    if name=='app-icon':
        path=path.with_suffix('.jpg'); im.convert('RGB').save(path,quality=96,subsampling=0)
        (ROOT/folder/f'{name}.png').unlink()
    assert im.size==(w,h)
    manifest.append(dict(name=name,width=w,height=h,status=status,source=f'svg/{name}.svg',file=str(path.relative_to(ROOT)).replace('\\','/'),alpha='straight' if name in ('library-logo','shortcut-icon') else 'opaque',sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    print(name,w,h,flush=True)

# ICO is an additional convenience, the documented shortcut PNG is sufficient.
Image.open(ROOT/'upload/shortcut-icon.png').save(ROOT/'upload/shortcut-icon.ico',sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
(ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

# Contact sheet is a rendered image, never a screenshot of the app.
sheet=Image.new('RGB',(1440,((len(manifest)+2)//3)*360),'#f4edf0'); draw=ImageDraw.Draw(sheet)
labelfont=ImageFont.truetype(str(FONT),20)
for i,m in enumerate(manifest):
    x=(i%3)*480; y=(i//3)*360
    draw.text((x+24,y+16),f"{m['name']}  {m['width']}×{m['height']}",fill=INK,font=labelfont)
    im=Image.open(ROOT/m['file']).convert('RGBA'); im.thumbnail((432,284),Image.Resampling.LANCZOS)
    sheet.paste(im,(x+24+(432-im.width)//2,y+54+(284-im.height)//2),im)
sheet.save(ROOT/'review/contact-sheet.jpg',quality=93)
small=Image.open(ROOT/'upload/store-small.png').convert('RGB')
proof=Image.new('RGB',(500,180),'#fff8fa')
proof.paste(small.resize((120,45),Image.Resampling.LANCZOS),(20,20))
proof.paste(small.resize((184,69),Image.Resampling.LANCZOS),(20,95))
proof.save(ROOT/'review/small-capsule-proof.png')

# Alpha sanity check against a known half-transparent pixel at the encoding boundary.
probe=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=b'<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"><rect width="1" height="1" fill="#ff0000" opacity="0.5"/></svg>'))).convert('RGBA').getpixel((0,0))
assert probe==(255,0,0,128),probe
checks={'dimensions':'18/18 passed','alpha_probe_rgba':probe,'png_encoding':'straight (unassociated) alpha','app_icon':'RGB JPEG','svg':'native text with embedded OFL subset; individual background shapes; original embedded PNG icon','screenshots':'missing; no generated artwork is a product screenshot'}
(ROOT/'review/validation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')

labels={'required':'必需静态物料','optional':'可选背景','conditional-event':'活动条件适用','extra':'介绍与宣传 · 非截图'}
cards=[]
for m in manifest:
    cards.append(f'<article><img src="{m["file"]}" alt="{m["name"]}" loading="lazy"><h2>{m["name"]}</h2><p>{m["width"]} × {m["height"]} · {labels[m["status"]]}</p><nav><a href="{m["source"]}" download>SVG 源文件</a><a href="{m["file"]}" download>位图文件</a></nav></article>')
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>utae avatar · Steam 物料</title>
<style>@font-face{font-family:Round;src:url(assets/ChillRoundF.ttf)}*{box-sizing:border-box}body{margin:0;background:#fff8fa;color:#713b56;font-family:Round,system-ui,sans-serif}main{max-width:1440px;margin:auto;padding:40px 24px}h1{font-size:36px}p{line-height:1.7}aside{padding:20px 24px;border-radius:20px;background:#f9dce9}a{color:inherit;text-underline-offset:4px}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;margin-top:28px}article{padding:18px;background:#f5eaf0;border-radius:24px}article img{display:block;width:100%;height:250px;object-fit:contain}h2{font-size:20px;margin:18px 0 0;overflow-wrap:anywhere}nav{display:flex;gap:20px;flex-wrap:wrap}nav a{background:#fff8fa;border-radius:12px;padding:9px 13px;text-decoration:none}a:hover{color:#a54370}a:focus-visible{outline:3px solid #a54370;outline-offset:3px}</style>
<main><h1>utae avatar · Steam 视觉物料</h1><p>让形象动起来。<br>18 张可编辑 SVG 与对应位图 · 规范核对于 2026-10-24</p>
<aside><strong>还缺至少 5 张真实产品截图，当前不能视为上架资料全部齐备。</strong><p>SVG 保留可编辑文字和背景，图标为内嵌原始 PNG。Steam 上传使用位图，介绍宣传图不能放入截图槽。未上传或发布。</p><nav><a href="README.txt">完整规范与交付说明</a><a href="manifest.json">尺寸和文件校验</a><a href="review/contact-sheet.jpg">素材总览</a><a href="review/small-capsule-proof.png">小尺寸校样</a></nav></aside>
<section>'''+''.join(cards)+'</section></main></html>'
(ROOT/'index.html').write_text(page,encoding='utf-8')

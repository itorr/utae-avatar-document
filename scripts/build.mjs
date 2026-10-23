import {readFile,writeFile,mkdir,cp,readdir} from 'node:fs/promises';
import {setPriority,constants} from 'node:os';
import {marked} from 'marked';
import {createHash} from 'node:crypto';
setPriority(0,constants.priority.PRIORITY_BELOW_NORMAL);
const origin='https://avatar.utae.cn';
const assetVersion=createHash('sha256').update(await readFile('site/site.css')).update(await readFile('site/site.mjs')).digest('hex').slice(0,12);
const pages=[['index','说明书'],['quickstart','快速开始'],['models','模型与表情'],['tracking','连接面捕'],['binding','转换与绑定'],['output','直播输出与截图'],['settings','设置与性能'],['faq','常见问题'],['terms','使用声明']];
const escape=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
const url=id=>id==='index'?'/docs/':`/docs/${id}/`;
function shell(title,path,body){return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(title)} · utae avatar</title><meta name="description" content="utae avatar，超高性能的 Live2D 虚拟形象动捕工具。模型、面捕、表情与直播输出使用说明。"><link rel="canonical" href="${origin}${path}"><meta property="og:title" content="${escape(title)} · utae avatar"><meta property="og:image" content="${origin}/assets/logo.png"><meta property="og:type" content="website"><meta name="theme-color" content="#fff7fb"><link rel="icon" href="/assets/logo.png"><link rel="stylesheet" href="/assets/site.css?v=${assetVersion}"><script type="module" src="/assets/site.mjs?v=${assetVersion}"></script></head><body><a class="skip" href="#main">跳到正文</a><header class="header"><a class="brand" href="/"><img src="/assets/logo.png" width="32" height="32" alt="">utae <strong>avatar</strong></a><nav aria-label="主导航"><a href="/" ${path==='/'?'aria-current="page"':''}>首页</a><a href="/docs/" ${path.startsWith('/docs/')?'aria-current="page"':''}>说明书</a></nav></header>${body}<footer><a class="brand" href="/">utae avatar</a><span>让每一个表情，都成为你</span><small>© 沈阳神奇海螺传媒工作室 · <a href="/docs/terms/">使用声明</a></small></footer></body></html>`;}
await mkdir('dist/assets',{recursive:true});
await cp('site/assets','dist/assets',{recursive:true});
await cp('site/site.css','dist/assets/site.css');await cp('site/site.mjs','dist/assets/site.mjs');
const search=[];
for(const [id,title] of pages){
 let md=await readFile(`docs/${id}.md`,'utf8');
 md=md.replace(/\]\((\w+)\.md\)/g,(_,target)=>`](${url(target)})`);
 const html=marked.parse(md,{gfm:true});
 const nav=pages.map(([key,label])=>`<a href="${url(key)}" ${key===id?'aria-current="page"':''}>${label}</a>`).join('');
 const i=pages.findIndex(p=>p[0]===id);
 const pager=`<nav class="pager" aria-label="文章翻页">${i>0?`<a href="${url(pages[i-1][0])}">← ${pages[i-1][1]}</a>`:'<span></span>'}${i<pages.length-1?`<a href="${url(pages[i+1][0])}">${pages[i+1][1]} →</a>`:''}</nav>`;
 const body=`<div class="docs-layout"><aside><p class="eyebrow">使用说明书</p><label class="search-label" for="search">查找文档</label><input id="search" type="search" placeholder="模型、面捕、输出…" autocomplete="off"><div id="results" aria-live="polite" hidden></div><nav class="doc-nav" aria-label="说明书章节">${nav}</nav></aside><main id="main" class="article"><p class="eyebrow">UTAE AVATAR / 使用说明</p>${html}${pager}</main></div>`;
 await mkdir(`dist${url(id)}`,{recursive:true});await writeFile(`dist${url(id)}index.html`,shell(title,url(id),body));
 search.push({title,url:url(id),text:md.replace(/[#*`\[\]]/g,'')});
}
await writeFile('dist/assets/search.json',JSON.stringify(search));
await writeFile('dist/index.html',shell('让形象动起来。','/',await readFile('site/home.html','utf8')));
await writeFile('dist/404.html',shell('没有找到这一页','/404.html','<main id="main" class="article error"><p class="eyebrow">404</p><h1>这一页走丢了</h1><p>回到说明书，继续找到你需要的内容。</p><a class="cta" href="/docs/">打开说明书 →</a></main>'));
await writeFile('dist/CNAME','avatar.utae.cn\n');await writeFile('dist/.nojekyll','');
await writeFile('dist/robots.txt',`User-agent: *\nAllow: /\nSitemap: ${origin}/sitemap.xml\n`);
await writeFile('dist/sitemap.xml',`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${['/',...pages.map(p=>url(p[0]))].map(p=>`<url><loc>${origin}${p}</loc></url>`).join('')}</urlset>`);
console.log(`已编译首页和 ${pages.length} 篇说明书；进程为 BELOW NORMAL，单进程构建。`);

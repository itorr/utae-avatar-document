import {readFile,readdir,stat} from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve('dist');let count=0;
async function visit(dir){for(const e of await readdir(dir,{withFileTypes:true})){const file=path.join(dir,e.name);if(e.isDirectory()){await visit(file);continue}if(!e.name.endsWith('.html'))continue;const html=await readFile(file,'utf8');count++;for(const match of html.matchAll(/(?:href|src)="([^"]+)"/g)){const target=match[1];if(!target.startsWith('/')||target.startsWith('//'))continue;let resolved=path.join(root,target.split(/[?#]/)[0]);if(target.endsWith('/'))resolved=path.join(resolved,'index.html');await stat(resolved).catch(()=>{throw Error(`断链 ${file}: ${target}`)})}if(!html.includes('id="main"')||!html.includes('lang="zh-CN"'))throw Error(`页面缺少语义结构: ${file}`)}}
await visit(root);
const css=await readFile('site/site.css','utf8');if(/border-(left|right|top|bottom)\s*:/.test(css))throw Error('禁止单边装饰线');
const index=JSON.parse(await readFile('dist/assets/search.json','utf8'));if(index.length!==9)throw Error('搜索索引不完整');
if((await readFile('dist/CNAME','utf8')).trim()!=='avatar.utae.cn')throw Error('域名不匹配');
console.log(`已验证 ${count} 个 HTML 页面、本地链接、资源、9 篇搜索索引和域名。`);

const themes=['pink','purple','blue','green'];
const themeInputs=[...document.querySelectorAll('input[name="theme"]')];
const applyTheme=value=>{
 if(!themes.includes(value))return;
 document.documentElement.dataset.theme=value;
 for(const input of themeInputs)input.checked=input.value===value;
};
try{applyTheme(localStorage.getItem('avatar-site-theme')||'pink')}catch{applyTheme('pink')}
for(const input of themeInputs)input.addEventListener('change',()=>{
 if(!input.checked)return;
 applyTheme(input.value);
 try{localStorage.setItem('avatar-site-theme',input.value)}catch{}
});
const search=document.querySelector('#search');
if(search){
 const results=document.querySelector('#results');let data;
 search.addEventListener('input',async()=>{
  const q=search.value.trim();results.replaceChildren();results.hidden=!q;if(!q)return;
  try{data??=await fetch('/assets/search.json').then(r=>{if(!r.ok)throw Error('search');return r.json()});
   if(search.value.trim()!==q)return;
   const matches=data.filter(p=>(p.title+' '+p.text).toLowerCase().includes(q.toLowerCase()));
   for(const page of matches){const a=document.createElement('a');a.href=page.url;a.textContent=page.title;results.append(a)}
   if(!matches.length){const p=document.createElement('p');p.textContent='没有找到，试试其他关键词';results.append(p)}
  }catch{results.textContent='搜索暂时不可用，请使用下方章节目录'}
 });
}

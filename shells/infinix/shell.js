const markup = Promise.all([fetch(new URL('./shell.html', import.meta.url)).then(r=>{if(!r.ok)throw Error('Shell unavailable');return r.text()}),fetch(new URL('./shell.css', import.meta.url)).then(r=>r.text())]);
export class InfinixShell extends HTMLElement {
 async connectedCallback(){
  if(this.shadowRoot)return;
  const root=this.attachShadow({mode:'open'});
  try{
   const [html,css]=await markup;
   root.innerHTML=`<style>${css}</style>${html}`;
   const width=Number(this.getAttribute('screen-width')),height=Number(this.getAttribute('screen-height'));
   if(width>0&&height>0)this.style.setProperty('--aspect',String(width/height));
   root.querySelector('[data-model]').textContent=this.getAttribute('model')||'Preview';
   root.querySelector('.device').dataset.notch=this.getAttribute('notch')||'none';
   root.querySelector('.device').dataset.notchPosition=this.getAttribute('notch-position')||'top_center';
   this.setAttribute('data-ready','true');
  }catch{root.textContent='Device shell unavailable';this.setAttribute('data-error','true')}
 }
}
if(!customElements.get('infinix-shell'))customElements.define('infinix-shell',InfinixShell);

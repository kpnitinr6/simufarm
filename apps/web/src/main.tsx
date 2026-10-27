import React,{useEffect,useState} from 'react';
import {createRoot} from 'react-dom/client';
import type {DeviceProfile} from '@simufarm/device-schema';
import './style.css';
type Preview=DeviceProfile & {url:string;review_status:string};
function App(){
 const [profiles,setProfiles]=useState<Preview[]>([]);const [error,setError]=useState('');
 useEffect(()=>{const script=document.createElement('script');script.type='module';script.src='/assets/shells/vivo/shell.js';script.onerror=()=>setError('Shell unavailable. Run the static generator.');document.head.appendChild(script);fetch('/catalog.json').then(r=>{if(!r.ok)throw Error();return r.json()}).then(setProfiles).catch(()=>setError('Generate the static catalog to begin.'));},[]);
 return <><header><a className="wordmark" href="/">simu<span>farm</span></a><span className="stage">STAGE A · VIVO PROOF OF CONCEPT</span><span className="budget">$0 infrastructure</span></header><main><section className="intro"><div><span className="eyebrow">A SMALL START. A SHARED FOUNDATION.</span><h1>One shell.<br/><em>Three perspectives.</em></h1><p>Original device frames, sourced profiles, and a catalog that grows without copying runtimes.</p></div><aside><strong>03</strong><span>Vivo static previews</span><small>India variants · evidence attached<br/>Human review pending</small></aside></section><section className="catalog" aria-label="Vivo static catalog">{error?<p role="alert">{error}</p>:profiles.map(p=><article key={p.id}><div className="preview">{React.createElement('vivo-shell',{model:p.model,'screen-width':p.screen.width_px,'screen-height':p.screen.height_px,notch:p.notch.type})}</div><div className="card-info"><div><small>vivo</small><h2>{p.model}</h2></div><span>Android {p.os_version}</span></div><div className="card-detail">{p.screen.width_px} × {p.screen.height_px} <span>·</span> {p.ram_gb} GB RAM</div><a className="open" href={p.url}>Open static preview <span>↗</span></a></article>)}</section><footer><span>Visuals only. Original CSS artwork; no manufacturer logos or wallpapers.</span><span>Runtime off · Stage B awaits approval</span></footer></main></>;
}
createRoot(document.getElementById('root')!).render(<App/>);

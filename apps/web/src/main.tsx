import React, {useEffect, useState} from 'react';
import {createRoot} from 'react-dom/client';
import type {DeviceProfile} from '@simufarm/device-schema';
import './style.css';
type Preview = DeviceProfile & {url: string; review_status: string};
function App() {
 const [profiles, setProfiles] = useState<Preview[]>([]);
 const [error, setError] = useState('');
 const [brand, setBrand] = useState('all');
 const [cohortOnly, setCohortOnly] = useState(false);
 useEffect(() => {
  fetch('/catalog.json').then(r => {if (!r.ok) throw Error(); return r.json()}).then((data: Preview[]) => {
   for (const shell of new Set(data.map(p => p.shell_id))) {
    const script = document.createElement('script'); script.type = 'module';
    script.src = `/assets/shells/${encodeURIComponent(shell)}/shell.js`;
    script.onerror = () => setError('A shell is unavailable. Run the static generator.');
    document.head.appendChild(script);
   }
   setProfiles(data);
  }).catch(() => setError('Generate the static catalog to begin.'));
 }, []);
 const brands = [...new Set(profiles.map(p => p.brand))].sort();
 const visible = profiles.filter(p => (brand === 'all' || p.brand === brand) && (!cohortOnly || p.brand !== 'vivo' || p.id === 'vivo-x100'));
 return <><header><a className="wordmark" href="/">simu<span>farm</span></a><span className="stage">STAGE B · BRAND SHELL COLLECTION</span><span className="budget">$0 infrastructure</span></header><main><section className="intro"><div><span className="eyebrow">A SHARED FOUNDATION. MORE POSSIBILITIES.</span><h1>Many frames.<br/><em>One foundation.</em></h1><p>Original device artwork meets sourced profiles. Explore the brand collection, with every runtime still switched off.</p></div><aside><strong>{String(brands.length).padStart(2, '0')}</strong><span>brand shells · {profiles.length} static previews</span><small>20 reference devices + 2 retained Vivo drafts<br/>Human review pending</small></aside></section><section className="controls" aria-label="Catalog filters"><label>Brand <select value={brand} onChange={e => setBrand(e.target.value)}><option value="all">All brands</option>{brands.map(b => <option key={b} value={b}>{b}</option>)}</select></label><label className="cohort"><input type="checkbox" checked={cohortOnly} onChange={e => setCohortOnly(e.target.checked)}/> Reference cohort only</label><span aria-live="polite">{visible.length} previews</span></section><section className="catalog" aria-label="Brand static catalog">{error ? <p role="alert">{error}</p> : visible.map(p => <article key={p.id} data-brand={p.brand}><div className="preview">{React.createElement(`${p.shell_id}-shell`, {model: p.model, 'screen-width': p.screen.width_px, 'screen-height': p.screen.height_px, notch: p.notch.type, 'notch-position': p.notch.position})}</div><div className="card-info"><div><small>{p.brand}</small><h2>{p.model}</h2></div><span>Android {p.os_version}</span></div><div className="card-detail">{p.screen.width_px} × {p.screen.height_px} <span>·</span> {p.ram_gb} GB RAM</div><a className="open" href={p.url}>Open static preview <span>↗</span></a></article>)}</section><footer><span>Visuals only. Original CSS artwork; no manufacturer logos or wallpapers.</span><span>Runtime off · Stage C requires approval</span></footer></main></>;
}
createRoot(document.getElementById('root')!).render(<App/>);

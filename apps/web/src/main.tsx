import React, {useEffect, useState} from 'react';
import {createRoot} from 'react-dom/client';
import type {DeviceProfile} from '@simufarm/device-schema';
import './style.css';
type Preview = DeviceProfile & {url: string; review_status: string; cohort?: "reference" | "generated"};
function App() {
 const [profiles, setProfiles] = useState<Preview[]>([]);
 const [error, setError] = useState('');
 const [brand, setBrand] = useState('all');
 const [cohortOnly, setCohortOnly] = useState(false);
 const [collection, setCollection] = useState('reference');
 const [query, setQuery] = useState('');
 const [page, setPage] = useState(0);
 const pageSize = 24;
 useEffect(() => setPage(0), [brand, cohortOnly, collection, query]);
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
 const brands = [...new Set(profiles.map(p => p.shell_id))].sort();
 const generatedCount = profiles.filter(p => p.cohort === 'generated').length;
 const selected = profiles.filter(p => (p.cohort || 'reference') === collection);
 const visible = selected.filter(p => (brand === 'all' || p.shell_id === brand) && (!cohortOnly || p.shell_id !== 'vivo' || p.id === 'vivo-x100') && `${p.brand} ${p.model}`.toLowerCase().includes(query.toLowerCase()));
 const pageCount = Math.max(1, Math.ceil(visible.length / pageSize));
 const currentPage = Math.min(page, pageCount - 1);
 const cards = visible.slice(currentPage * pageSize, (currentPage + 1) * pageSize);
 return <><header><a className="wordmark" href="/">simu<span>farm</span></a><span className="stage">STATIC DEVICE COLLECTION</span><span className="budget">$0 infrastructure</span></header><main><section className="intro"><div><span className="eyebrow">A SHARED FOUNDATION. MORE POSSIBILITIES.</span><h1>Many frames.<br/><em>One foundation.</em></h1><p>Original device artwork meets sourced profiles. Explore the brand collection, with every runtime still switched off.</p></div><aside><strong>{String(brands.length).padStart(2, '0')}</strong><span>brand shells · {generatedCount} generated drafts</span><small>22 reference drafts preserved<br/>Human review pending</small></aside></section><section className="controls" aria-label="Catalog filters"><label>Collection <select aria-label="Collection" value={collection} onChange={e => {setCollection(e.target.value); setCohortOnly(false)}}><option value="reference">Reference drafts (22)</option><option value="generated">Generated drafts ({generatedCount})</option></select></label><label>Search <input aria-label="Search models" value={query} onChange={e => setQuery(e.target.value)}/></label><label>Brand <select aria-label="Brand" value={brand} onChange={e => setBrand(e.target.value)}><option value="all">All brands</option>{brands.map(b => <option key={b} value={b}>{b}</option>)}</select></label><label className="cohort"><input disabled={collection !== "reference"} type="checkbox" checked={cohortOnly} onChange={e => setCohortOnly(e.target.checked)}/> Reference cohort only</label><span aria-live="polite">{visible.length} previews</span></section><section className="catalog" aria-label="Brand static catalog">{error ? <p role="alert">{error}</p> : cards.map(p => <article key={p.id} data-brand={p.brand}><div className="preview">{React.createElement(`${p.shell_id}-shell`, {model: p.model, 'screen-width': p.screen.width_px, 'screen-height': p.screen.height_px, notch: p.notch.type, 'notch-position': p.notch.position})}</div><div className="card-info"><div><small>{p.brand}</small><h2>{p.model}</h2></div><span>Android {p.os_version}</span></div><div className="card-detail">{p.screen.width_px} × {p.screen.height_px} <span>·</span> {p.ram_gb} GB RAM</div><a className="open" href={p.url}>Open static preview <span>↗</span></a></article>)}</section><nav className="pagination" aria-label="Catalog pages"><button disabled={currentPage === 0} onClick={() => setPage(currentPage - 1)}>Previous</button><span>Page {currentPage + 1} of {pageCount}</span><button disabled={currentPage + 1 >= pageCount} onClick={() => setPage(currentPage + 1)}>Next</button></nav><footer><span><a href="/assets/stage-c-attribution.txt">Generated data attribution · CC BY-SA 4.0</a><br/>Visuals only. Original CSS artwork; no manufacturer logos or wallpapers.</span><span>Runtime off · Human technical review pending</span></footer></main></>;
}
createRoot(document.getElementById('root')!).render(<App/>);

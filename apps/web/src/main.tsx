import React, {useEffect, useState} from 'react';
import {createRoot} from 'react-dom/client';
import type {DeviceProfile} from '@simufarm/device-schema';
import '@simufarm/simulator-renderer';
import './style.css';
function App() {
 const [profiles,setProfiles]=useState<DeviceProfile[]>([]);
 const [error,setError]=useState('');
 useEffect(()=>{fetch('/api/profiles').then(r=>{if(!r.ok)throw Error('API unavailable');return r.json()}).then(setProfiles).catch(()=>setError('Start the API to load approved profiles.'));},[]);
 return <main><small>SIMUFARM / DEVELOPMENT</small><h1>A device lab.<br/>Built from profiles.</h1><p>Static previews, interactive shells, and shared Android base images.</p><section><h2>Approved device catalog</h2>{error?<p role="alert">{error}</p>:profiles.length?profiles.map(p=><article key={p.id}><h3>{p.brand} {p.model}</h3><p>{p.os_family} · {p.screen.width_px} × {p.screen.height_px}</p></article>):<p>No approved profiles yet. The 1,000-device target list awaits human review.</p>}</section><footer>Emulator-only testing has fidelity limits. iOS support is visual only.</footer></main>;
}
createRoot(document.getElementById('root')!).render(<App/>);

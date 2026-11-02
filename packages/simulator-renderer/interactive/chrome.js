const styles = fetch(new URL('./chrome.css', import.meta.url)).then(response => {
  if (!response.ok) throw Error('Interactive styles unavailable');
  return response.text();
});

export async function installChrome(host) {
  const stage = host.closest('.device-stage');
  if (!stage || stage.querySelector('[data-chrome-toolbar]')) return;
  const root = host.shadowRoot;
  const device = root.querySelector('.device');
  const screen = root.querySelector('.screen');
  const status = root.querySelector('.status');
  const originalStatus = status.innerHTML;
  const originalLabel = device.getAttribute('aria-label');
  const originalStyle = host.getAttribute('style');
  const aspect = Number(host.getAttribute('screen-width')) / Number(host.getAttribute('screen-height'));
  const toolbar = document.createElement('div');
  toolbar.dataset.chromeToolbar = '';
  toolbar.style.cssText = 'margin-top:24px;display:flex;flex-wrap:wrap;gap:8px;font:12px system-ui;color:#34304e';
  toolbar.innerHTML = `<button type="button" data-enable aria-pressed="false">Enable interactive chrome</button>
    <div data-controls hidden><button type="button" data-rotate aria-pressed="false">Rotate landscape</button>
    <button type="button" data-dark aria-pressed="false">Dark mode</button>
    <label>Mock time <input data-time aria-label="Mock time" type="time" value="09:41"></label></div>
    <small style="flex-basis:100%">Mock UI only · no Android apps or cellular services</small>`;
  stage.append(toolbar);
  for (const button of toolbar.querySelectorAll('button')) button.style.cssText = 'border:1px solid #c5c0e2;border-radius:8px;padding:8px 10px;background:#fff;color:#453c70;font:inherit;cursor:pointer';
  toolbar.querySelector('[data-controls]').style.cssText = 'gap:8px;align-items:center;flex-wrap:wrap';
  const style = document.createElement('style');
  style.textContent = await styles;
  root.append(style);
  const panel = document.createElement('section');
  panel.className = 'sf-panel'; panel.hidden = true;
  panel.setAttribute('aria-label', 'Mock OS controls');
  panel.innerHTML = `<button type="button" data-status aria-expanded="false">Mock status panel</button>
    <div data-status-panel hidden><p>Wi-Fi · Demo network</p><p>Battery · 85% (simulated)</p><p>No cellular service</p></div>
    <label>Try typing<input aria-label="Mock text input" placeholder="Type something…" autocomplete="off" spellcheck="false"></label>
    <button type="button" data-keyboard-toggle aria-expanded="false">Show keyboard</button>`;
  screen.append(panel);
  const keyboard = document.createElement('section');
  keyboard.className = 'sf-keyboard'; keyboard.hidden = true;
  keyboard.setAttribute('aria-label', 'Mock keyboard');
  for (const letters of ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']) {
    const row = document.createElement('div'); row.className = 'sf-key-row';
    for (const letter of letters) {
      const key = document.createElement('button'); key.type = 'button'; key.textContent = letter;
      key.dataset.key = letter; row.append(key);
    }
    keyboard.append(row);
  }
  const actions = document.createElement('div'); actions.className = 'sf-key-row';
  actions.innerHTML = '<button type="button" data-key=" ">Space</button><button type="button" data-key="Backspace">Backspace</button><button type="button" data-key="Done">Done</button>';
  keyboard.append(actions); screen.append(keyboard);
  const input = panel.querySelector('input');
  const enable = toolbar.querySelector('[data-enable]');
  const controls = toolbar.querySelector('[data-controls]');
  const rotate = toolbar.querySelector('[data-rotate]');
  const dark = toolbar.querySelector('[data-dark]');
  const time = toolbar.querySelector('[data-time]');
  const keyboardToggle = panel.querySelector('[data-keyboard-toggle]');
  const statusToggle = panel.querySelector('[data-status]');
  const statusPanel = panel.querySelector('[data-status-panel]');
  let enabled = false, landscape = false;
  function showKeyboard(show) {
    keyboard.hidden = !show;
    keyboardToggle.setAttribute('aria-expanded', String(show));
    keyboardToggle.textContent = show ? 'Hide keyboard' : 'Show keyboard';
  }
  enable.addEventListener('click', () => {
    enabled = !enabled;
    enable.setAttribute('aria-pressed', String(enabled));
    enable.textContent = enabled ? 'Disable interactive chrome' : 'Enable interactive chrome';
    controls.hidden = !enabled; controls.style.display = enabled ? "flex" : "none"; panel.hidden = !enabled;
    device.dataset.interactive = String(enabled);
    if (enabled) {
      device.removeAttribute('role'); device.setAttribute('aria-label', 'Interactive mock device');
      status.innerHTML = '<span data-clock></span><span aria-label="Simulated Wi-Fi and battery">Wi-Fi · 85%</span>';
      root.querySelector('[data-clock]').textContent = time.value;
    } else {
      device.setAttribute('role', 'img'); device.setAttribute('aria-label', originalLabel);
      status.innerHTML = originalStatus; showKeyboard(false); landscape = false;
      statusPanel.hidden = true; statusToggle.setAttribute('aria-expanded', 'false');
      device.dataset.theme = 'light'; dark.setAttribute('aria-pressed', 'false');
      rotate.setAttribute('aria-pressed', 'false'); rotate.textContent = 'Rotate landscape';
      if (originalStyle === null) host.removeAttribute('style'); else host.setAttribute('style', originalStyle);
    }
  });
  rotate.addEventListener('click', () => {
    landscape = !landscape;
    host.style.setProperty('--aspect', String(landscape ? 1 / aspect : aspect));
    host.style.maxWidth = landscape ? '440px' : '300px';
    rotate.setAttribute('aria-pressed', String(landscape));
    rotate.textContent = landscape ? 'Rotate portrait' : 'Rotate landscape';
  });
  dark.addEventListener('click', () => {
    const isDark = device.dataset.theme !== 'dark'; device.dataset.theme = isDark ? 'dark' : 'light';
    dark.setAttribute('aria-pressed', String(isDark));
  });
  time.addEventListener('input', () => { root.querySelector('[data-clock]').textContent = time.value; });
  keyboardToggle.addEventListener('click', () => showKeyboard(keyboard.hidden));
  input.addEventListener('focus', () => showKeyboard(true));
  root.addEventListener('keydown', event => {
    if (event.key === 'Escape') { showKeyboard(false); keyboardToggle.focus(); }
  });
  statusToggle.addEventListener('click', () => {
    statusPanel.hidden = !statusPanel.hidden;
    statusToggle.setAttribute('aria-expanded', String(!statusPanel.hidden));
  });
  keyboard.addEventListener('pointerdown', event => { if (event.target.closest('button')) event.preventDefault(); });
  keyboard.addEventListener('click', event => {
    const key = event.target.closest('[data-key]'); if (!key) return;
    const value = key.dataset.key;
    if (value === 'Done') { showKeyboard(false); keyboardToggle.focus(); return; }
    const start = input.selectionStart, end = input.selectionEnd;
    if (value === 'Backspace') input.setRangeText('', start === end ? Math.max(0, start - 1) : start, end, 'end');
    else input.setRangeText(value, start, end, 'end');
    input.dispatchEvent(new Event('input', {bubbles:true}));
  });
  host.dataset.chromeReady = 'true';
  host.dataset.chromeReadyMs = String(Math.round(performance.now()));
}

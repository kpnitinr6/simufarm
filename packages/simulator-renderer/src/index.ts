// P0 reusable shell primitive. Real device assets are gated on approved profiles.
export class DeviceShell extends HTMLElement {
  connectedCallback() {
    if (this.shadowRoot) return;
    const root = this.attachShadow({mode: 'open'});
    root.innerHTML = `<style>:host{display:block;border:8px solid #26354a;border-radius:32px;background:#fff;overflow:hidden;aspect-ratio:9/19;max-width:300px}main{height:100%;padding:20px;box-sizing:border-box}</style><main><slot></slot></main>`;
  }
}
if (!customElements.get('device-shell')) customElements.define('device-shell', DeviceShell);

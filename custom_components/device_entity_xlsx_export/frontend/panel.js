class DeviceEntityXlsxExportPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._devices = [];
    this._entities = [];
    this._busy = false;
    this._loaded = false;
    this._includeDisabled = true;
    this._includeAttributes = true;
  }

  set hass(value) {
    this._hass = value;
    if (!this._loaded) {
      this._loaded = true;
      this.loadDevices();
    }
  }
  set narrow(value) { this._narrow = value; }
  set panel(value) { this._panel = value; }

  async loadDevices() {
    this.render("Geräte werden geladen …");
    try {
      const response = await this._hass.callApi("GET", "device_entity_xlsx_export/devices");
      this._devices = response.devices;
      this.render();
    } catch (error) { this.render(`Geräte konnten nicht geladen werden: ${error.message || error}`); }
  }

  async loadEntities() {
    const id = this.shadowRoot.querySelector("#device").value;
    if (!id) { this._entities = []; this.render(); return; }
    this._selected = id;
    this._includeDisabled = this.shadowRoot.querySelector("#disabled").checked;
    this._includeAttributes = this.shadowRoot.querySelector("#attributes").checked;
    this._filename = this.shadowRoot.querySelector("#filename").value;
    this._busy = true; this.render();
    try {
      const response = await this._hass.callApi("GET", `device_entity_xlsx_export/entities?device_id=${encodeURIComponent(id)}&include_disabled=${this._includeDisabled}`);
      this._entities = response.entities;
      this._deviceInfo = response.device;
    } catch (error) { this._message = `Entitäten konnten nicht geladen werden: ${error.message || error}`; }
    this._busy = false; this.render();
  }

  async exportFile() {
    const id = this.shadowRoot.querySelector("#device").value;
    if (!id) return;
    const filename = this.shadowRoot.querySelector("#filename").value.trim();
    const includeDisabled = this.shadowRoot.querySelector("#disabled").checked;
    const includeAttributes = this.shadowRoot.querySelector("#attributes").checked;
    this._selected = id; this._filename = filename; this._includeDisabled = includeDisabled; this._includeAttributes = includeAttributes; this._busy = true; this._message = "Excel-Datei wird erstellt …"; this.render();
    try {
      const response = await fetch("/api/device_entity_xlsx_export/export", {
        method: "POST",
        headers: { "Authorization": `Bearer ${this._hass.auth.data.access_token}`, "Content-Type": "application/json" },
        body: JSON.stringify({ device_id: id, filename, include_disabled: includeDisabled, include_attributes: includeAttributes })
      });
      if (!response.ok) throw new Error((await response.json()).error || `HTTP ${response.status}`);
      const blob = await response.blob();
      const disposition = response.headers.get("Content-Disposition") || "";
      const match = disposition.match(/filename="([^"]+)"/);
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob); link.download = match ? match[1] : "entity_export.xlsx";
      document.body.appendChild(link); link.click(); link.remove(); URL.revokeObjectURL(link.href);
      this._message = `Download gestartet: ${link.download}`;
    } catch (error) { this._message = `Export fehlgeschlagen: ${error.message || error}`; }
    this._busy = false; this.render();
  }

  esc(value) { const node = document.createElement("span"); node.textContent = value ?? ""; return node.innerHTML; }

  render(status = "") {
    const selected = this._selected || "";
    const options = this._devices.map(d => `<option value="${this.esc(d.id)}" ${d.id === selected ? "selected" : ""}>${this.esc(d.name)} (${d.entity_count})</option>`).join("");
    const rows = this._entities.map(e => `<tr class="${e.disabled_by ? "disabled" : ""}"><td><code>${this.esc(e.entity_id)}</code></td><td>${this.esc(e.name)}</td><td>${this.esc(e.state || "—")}</td><td>${this.esc(e.unit)}</td><td>${this.esc(e.platform)}</td><td>${e.disabled_by ? `<span class="tag">deaktiviert</span>` : (e.available ? "aktiv" : "nicht geladen")}</td></tr>`).join("");
    this.shadowRoot.innerHTML = `<style>
      :host{display:block;background:var(--primary-background-color);min-height:100%;color:var(--primary-text-color);font-family:var(--paper-font-body1_-_font-family,Arial,sans-serif)}
      .wrap{max-width:1200px;margin:auto;padding:24px}.hero{display:flex;gap:16px;align-items:center;margin-bottom:22px}.icon{font-size:34px}.hero h1{margin:0;font-size:28px}.hero p{margin:4px 0 0;color:var(--secondary-text-color)}
      .card{background:var(--card-background-color);border-radius:14px;box-shadow:var(--ha-card-box-shadow,0 2px 8px #0002);padding:20px;margin-bottom:18px}.grid{display:grid;grid-template-columns:minmax(260px,2fr) minmax(200px,1fr);gap:16px}.field label{display:block;font-weight:600;margin-bottom:7px}.field select,.field input{box-sizing:border-box;width:100%;padding:11px;border:1px solid var(--divider-color);border-radius:8px;background:var(--card-background-color);color:var(--primary-text-color);font-size:15px}
      .checks{display:flex;gap:24px;flex-wrap:wrap;margin:18px 0}.checks label{display:flex;align-items:center;gap:8px}.actions{display:flex;gap:10px;flex-wrap:wrap}button{border:0;border-radius:9px;padding:11px 18px;font-size:15px;font-weight:600;cursor:pointer}button.primary{background:var(--primary-color);color:#fff}button.secondary{background:var(--secondary-background-color);color:var(--primary-text-color)}button:disabled{opacity:.55;cursor:wait}.message{margin-top:14px;color:var(--secondary-text-color)}
      .summary{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:12px}.summary h2{margin:0;font-size:20px}.table-wrap{overflow:auto;max-height:58vh}table{width:100%;border-collapse:collapse;font-size:14px}th{text-align:left;position:sticky;top:0;background:var(--card-background-color);z-index:1}th,td{padding:10px;border-bottom:1px solid var(--divider-color);white-space:nowrap}tr.disabled{opacity:.75}.tag{color:var(--warning-color,#d97706);font-weight:600}code{color:var(--primary-color)}
      @media(max-width:700px){.wrap{padding:14px}.grid{grid-template-columns:1fr}.hero h1{font-size:23px}}
    </style><div class="wrap"><div class="hero"><div class="icon">📊</div><div><h1>Excel Export</h1><p>Gerät wählen, Entitäten prüfen und direkt als XLSX herunterladen.</p></div></div>
      <div class="card"><div class="grid"><div class="field"><label for="device">Gerät</label><select id="device"><option value="">Bitte Gerät auswählen …</option>${options}</select></div><div class="field"><label for="filename">Dateiname (optional)</label><input id="filename" value="${this.esc(this._filename || "")}" placeholder="z. B. nibe_heat_pump.xlsx"></div></div>
      <div class="checks"><label><input id="disabled" type="checkbox" ${this._includeDisabled ? "checked" : ""}> Deaktivierte Entitäten einschließen</label><label><input id="attributes" type="checkbox" ${this._includeAttributes ? "checked" : ""}> Attribute in Excel einschließen</label></div>
      <div class="actions"><button class="secondary" id="show" ${this._busy ? "disabled" : ""}>Entitäten anzeigen</button><button class="primary" id="export" ${this._busy || !selected ? "disabled" : ""}>Excel herunterladen</button></div><div class="message">${this.esc(status || this._message || "")}</div></div>
      ${this._entities.length ? `<div class="card"><div class="summary"><h2>${this.esc(this._deviceInfo?.Name)} – ${this._entities.length} Entitäten</h2></div><div class="table-wrap"><table><thead><tr><th>Entity ID</th><th>Name</th><th>Zustand</th><th>Einheit</th><th>Integration</th><th>Status</th></tr></thead><tbody>${rows}</tbody></table></div></div>` : ""}
    </div>`;
    this.shadowRoot.querySelector("#device")?.addEventListener("change", e => { this._selected = e.target.value; this._entities = []; this.render(); });
    this.shadowRoot.querySelector("#show")?.addEventListener("click", () => this.loadEntities());
    this.shadowRoot.querySelector("#export")?.addEventListener("click", () => this.exportFile());
  }
}
if (!customElements.get("device-entity-xlsx-export-panel")) customElements.define("device-entity-xlsx-export-panel", DeviceEntityXlsxExportPanel);

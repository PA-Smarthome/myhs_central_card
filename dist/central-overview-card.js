/* Central Overview Card v1.4.0 | MIT | Home Assistant Lovelace | no dependencies */
(() => {
  'use strict';
  const TAG = 'central-overview-card';
  const EDITOR_TAG = 'central-overview-card-editor';
  if (customElements.get(TAG)) return;

  // Public, installation-independent defaults. No personal entity IDs or URLs.
  const KINDS = {
    alarm:       {label:'Sicherheit Zentral',  icon:'mdi:shield-home',       tone:'error',   source:'auto'},
    windows:     {label:'Fenster Zentral',     icon:'mdi:window-closed',     tone:'error',   source:'auto'},
    lights:      {label:'Licht Zentral',       icon:'mdi:lightbulb-group',   tone:'warning', source:'auto'},
    energy:      {label:'Energie Zentral',  icon:'mdi:power-plug',        tone:'success', source:'auto'},
    heating:     {label:'Heizung Zentral',     icon:'mdi:radiator',          tone:'orange',  source:'auto'},
    climate:     {label:'Klima Zentral',       icon:'mdi:air-conditioner',   tone:'info',    source:'auto'},
    audio:       {label:'Audio Zentral',       icon:'mdi:music',             tone:'cyan',    source:'auto'},
    shading:     {label:'Beschattung Zentral', icon:'mdi:blinds',            tone:'purple',  source:'auto'},
    media:       {label:'Media Zentral',   icon:'mdi:television',        tone:'info',    source:'auto'},
    air:         {label:'Lüftung Zentral',    icon:'mdi:air-filter',        tone:'success', source:'selected'},
    lock:        {label:'Zutritt Zentral',     icon:'mdi:lock',              tone:'success', source:'auto'},
    alarmclock:  {label:'Wecker Zentral',      icon:'mdi:alarm',             tone:'warning', source:'selected'},
    presence:    {label:'Präsenz Zentral',     icon:'mdi:motion-sensor',     tone:'pink',    source:'auto'},
    people:      {label:'Anwesenheit Zentral', icon:'mdi:account-group',    tone:'pink',    source:'auto'},
    vehicles:    {label:'Fahrzeuge Zentral',   icon:'mdi:car',               tone:'info',    source:'selected'},
    automations: {label:'Automatik Zentral',   icon:'mdi:robot',             tone:'warning', source:'auto'},
  };
  // All color references are native Home Assistant theme variables.
  const COLOR_VARS = {
    error:   'var(--error-color, var(--red-color, #f44336))',
    success: 'var(--success-color, var(--green-color, #4caf50))',
    warning: 'var(--warning-color, var(--amber-color, #ffc107))',
    info:    'var(--info-color, var(--blue-color, #2196f3))',
    orange:  'var(--orange-color, #ff9800)',
    cyan:    'var(--cyan-color, #00bcd4)',
    purple:  'var(--purple-color, #9c27b0)',
    pink:    'var(--pink-color, #e91e63)',
    red:     'var(--red-color, #f44336)',
    green:   'var(--green-color, #4caf50)',
    yellow:  'var(--yellow-color, #ffeb3b)',
    blue:    'var(--blue-color, #2196f3)',
    amber:   'var(--amber-color, #ffc107)',
  };
  const COLOR_LABELS = {error:'Fehler (Rot)', success:'Erfolg (Grün)', warning:'Warnung (Gelb)',
    info:'Info (Blau)', orange:'Orange', cyan:'Cyan', purple:'Lila', pink:'Pink',
    red:'Rot', green:'Grün', yellow:'Gelb', blue:'Blau', amber:'Amber'};
  const createTile = (kind) => ({kind, label:KINDS[kind].label, icon:KINDS[kind].icon,
    source:KINDS[kind].source, entities:[], enabled:true, navigation_path:'',
    tone:['alarm','lock'].includes(kind)?'auto':KINDS[kind].tone, include_zones:kind==='people'});
  const createConfig = () => ({type:`custom:${TAG}`, columns:2, gap:8, show_labels:true,
    alarm_home_legacy:false, tiles:Object.keys(KINDS).map(createTile)});
  const strings = (value) => Array.isArray(value) ? value.filter(v => typeof v === 'string') : [];
  const uniq = (items) => [...new Set(items.filter(Boolean))];
  // Built-in Home Assistant Material Design icons only: never require local icon packs.
  const mdiIcon = (candidate, kind) =>
    (typeof candidate === 'string' && /^mdi:[a-z0-9][a-z0-9-]*$/i.test(candidate))
      ? candidate : (KINDS[kind]?.icon || 'mdi:help-circle');
  const hasState = (entity) => Boolean(entity && !['unknown','unavailable'].includes(entity.state));
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (x) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));
  const countMessage = (n, singular, plural) => n === 1 ? singular : plural(n);
  const stateById = (hass, id) => hass?.states?.[id];
  function areaId(hass, id) {
    const meta = hass?.entities?.[id];
    return meta?.area_id || (meta?.device_id && hass?.devices?.[meta.device_id]?.area_id) ||
      stateById(hass,id)?.attributes?.area_id || null;
  }
  function groupChildren(hass, id, visited = new Set()) {
    if (!id || visited.has(id)) return [];
    visited.add(id);
    const st = stateById(hass,id);
    const members = st?.attributes?.entity_id;
    const ids = Array.isArray(members) ? members : (typeof members === 'string' ? members.split(',').map(s=>s.trim()) : []);
    if (!ids.length) return st ? [id] : [];
    return uniq(ids.flatMap(child => groupChildren(hass,child,visited)));
  }
  function autoCandidate(kind, st) {
    const id = st.entity_id;
    const domain = id.split('.')[0];
    const deviceClass = String(st.attributes?.device_class || '').toLowerCase();
    const hvac = st.attributes?.hvac_modes || [];
    switch (kind) {
      case 'alarm':       return domain === 'alarm_control_panel';
      case 'windows':     return domain === 'binary_sensor' && ['window','opening'].includes(deviceClass);
      case 'lights':      return domain === 'light';
      case 'energy':      return domain === 'switch' && ['outlet','plug'].includes(deviceClass);
      case 'heating':     return domain === 'climate' && hvac.includes('heat') && !hvac.includes('cool');
      case 'climate':     return domain === 'climate' && hvac.includes('cool');
      case 'audio':       return domain === 'media_player' && ['speaker','receiver'].includes(deviceClass);
      case 'shading':     return domain === 'cover';
      case 'media':       return domain === 'media_player' && deviceClass === 'tv';
      case 'lock':        return domain === 'lock';
      case 'presence':    return domain === 'binary_sensor' && ['motion','presence','occupancy'].includes(deviceClass);
      case 'people':      return domain === 'person';
      case 'automations': return domain === 'automation';
      default:            return false; // Don't guess air quality, alarms, or vehicle movement.
    }
  }
  function resolveEntities(hass, tile) {
    const source = tile.source || KINDS[tile.kind]?.source || 'selected';
    let ids = [];
    if (source === 'group') ids = groupChildren(hass, tile.entity);
    else if (source === 'selected') ids = uniq([...strings(tile.entities), ...(['alarm','lock'].includes(tile.kind) && tile.entity ? [tile.entity] : [])]);
    else {
      ids = ['alarm','lock'].includes(tile.kind) && tile.entity ? [tile.entity] :
        Object.values(hass?.states || {}).filter(st => autoCandidate(tile.kind,st)).map(st => st.entity_id);
      // Expand aggregation entities to their individual members so an open
      // window group doesn't hide the actual number of open windows.
      ids = uniq(ids.flatMap(id => {
        const e=stateById(hass,id);
        return e?.attributes?.entity_id ? groupChildren(hass,id) : [id];
      }));
    }
    if (tile.prefix) ids = ids.filter(id => id.startsWith(tile.prefix));
    if (tile.area) ids = ids.filter(id => areaId(hass,id) === tile.area);
    return uniq(ids).map(id => stateById(hass,id)).filter(Boolean);
  }
  function activeCountByRooms(hass, arr) {
    const rooms = uniq(arr.map(st => areaId(hass,st.entity_id)));
    const withoutArea = arr.filter(st => !areaId(hass,st.entity_id)).length;
    return {count:rooms.length + withoutArea, rooms:rooms.length>0 && withoutArea===0};
  }
  function result(text, active=false, extra={}) {return {text, active, ...extra};}
  function compute(hass, tile, legacy=false) {
    const kind = tile.kind;
    const list = resolveEntities(hass,tile);
    const source = tile.source || KINDS[kind]?.source;
    const candidateCount = list.length;
    const needsSetup = ['air','alarmclock','vehicles'].includes(kind) && !candidateCount;
    const none = () => result(needsSetup ? 'Quelle auswählen' : 'Keine Entitäten gefunden', false, {missing:true});
    if (!candidateCount) return none();
    const usable = list.filter(hasState);
    if (!usable.length) return result('Nicht verfügbar',false,{missing:true});
    if (kind === 'alarm' || kind === 'lock') {
      if (list.length > 1 && source === 'auto') return result('Entität auswählen',false,{missing:true});
      const st = usable[0], s = st.state;
      if (kind === 'alarm') {
        const names = {disarmed:'Unscharf · Zuhause',armed_home:legacy?'Unscharf · Zuhause':'Scharf · Zuhause',
          armed_away:'Scharf · Abwesend',armed_night:'Scharf · Nacht',armed_vacation:'Scharf · Urlaub',
          armed_holiday:'Scharf · Urlaub',pending:'Wird aktiviert',arming:'Wird aktiviert',
          disarming:'Wird deaktiviert',triggered:'Alarm ausgelöst'};
        const okay = legacy ? s === 'armed_home' : s === 'disarmed';
        const waiting = ['pending','arming','disarming'].includes(s);
        return result(names[s] || s, !okay, {tone: okay?'success':waiting?'warning':'error', colorize:true});
      }
      const names = {locked:'Verriegelt',unlocked:'Entriegelt',locking:'Wird verriegelt',
        unlocking:'Wird entriegelt',jammed:'Blockiert'};
      const okay = s === 'locked';
      return result(names[s] || s,!okay,{tone: s === 'jammed' ? 'error' : okay ? 'success' : 'warning',
        colorize:true, icon:s === 'unlocked'?'mdi:lock-open-variant':s === 'jammed'?'mdi:lock-alert':undefined});
    }
    if (kind === 'windows') {
      const count = usable.filter(st => st.state === 'on' || st.state === 'open').length;
      return result(count===0?'Alle geschlossen':countMessage(count,'1 geöffnet',n=>`${n} geöffnet`),count>0);
    }
    if (kind === 'lights' || kind === 'media' || kind === 'presence') {
      const on = usable.filter(st => kind==='media' ? ['on','playing','paused','idle'].includes(st.state) : st.state === 'on');
      const {count,rooms} = activeCountByRooms(hass,on);
      const offText = kind==='lights'?'Alles aus':kind==='media'?'Alle Fernseher aus':'Keine Bewegung';
      const message = !count ? offText : rooms ? countMessage(count,'In 1 Raum aktiv',n=>`In ${n} Räumen aktiv`) :
        countMessage(count,'1 Gerät aktiv',n=>`${n} Geräte aktiv`);
      return result(message,count>0);
    }
    if (kind === 'energy' || kind === 'alarmclock') {
      const on = usable.filter(st => ['on','active'].includes(st.state)).length;
      const word = kind==='energy'?'Gerät':'Wecker';
      return result(on===0?(kind==='energy'?'Keine Geräte aktiv':'Kein Wecker aktiv'):
        countMessage(on,`1 ${word} aktiv`,n=>`${n} ${kind==='energy'?'Geräte':'Wecker'} aktiv`),on>0);
    }
    if (kind === 'heating' || kind === 'climate') {
      const modes = [{s:'heat',word:'heizen'},{s:'cool',word:'kühlen'},
        {s:'fan_only',word:'lüften'},{s:'heat_cool',word:'automatisch'},{s:'auto',word:'auto'}];
      const parts = modes.map(m => ({...m,count:usable.filter(st=>st.state===m.s).length}))
        .filter(m=>m.count && (kind === 'climate' || !['fan_only'].includes(m.s)))
        .map(m=>`${m.count} ${m.count===1?'Raum':'Räume'} ${m.word}`);
      return result(parts.length ? parts.join(' · ') : 'Keine Räume im aktiven Modus', parts.length>0);
    }
    if (kind === 'audio') {
      const playing = activeCountByRooms(hass,usable.filter(st=>st.state==='playing')).count;
      const paused = activeCountByRooms(hass,usable.filter(st=>st.state==='paused')).count;
      return result(playing?countMessage(playing,'Spielt in 1 Raum',n=>`Spielt in ${n} Räumen`):
        paused?countMessage(paused,'Pausiert in 1 Raum',n=>`Pausiert in ${n} Räumen`):'Alle Räume aus',playing>0);
    }
    if (kind === 'shading') {
      const positional = usable.filter(st=> Number.isFinite(Number(st.attributes?.current_position)) &&
        st.attributes?.current_position !== undefined && st.attributes?.current_position !== null);
      const auto = tile.automation_entity && stateById(hass,tile.automation_entity)?.state === 'on';
      if (!positional.length) {
        const opened = usable.filter(st=>st.state==='open').length;
        const closed = usable.filter(st=>st.state==='closed').length;
        return result(opened===usable.length?'Alle offen':closed===usable.length?'Alle geschlossen':
          `${opened} offen · ${closed} geschlossen`, Boolean(auto || closed>0), {icon:auto?'mdi:blinds-horizontal':undefined});
      }
      const total=positional.length;
      const open=positional.filter(st=>Number(st.attributes.current_position)===100).length;
      const closed=positional.filter(st=>Number(st.attributes.current_position)===0).length;
      const partial=total-open-closed;
      const words = [open?`${open} offen`:null,partial?`${partial} teilweise`:null,closed?`${closed} zu`:null].filter(Boolean);
      return result(open===total?'Alle offen':closed===total?'Alle geschlossen':words.join(' · '),
        Boolean(auto||closed||partial), {icon:auto?'mdi:blinds-horizontal':closed===total?'mdi:blinds':'mdi:blinds-open'});
    }
    if (kind === 'air') {
      const okay = (tile.good_states || 'gut,good,ok,okay,ausgewogen').split(',').map(s=>s.trim().toLowerCase());
      const threshold = tile.threshold === '' || tile.threshold === undefined ? null : Number(tile.threshold);
      let noRule=false;
      const bad=usable.filter(st=>{
        const numeric=Number(st.state);
        if (Number.isFinite(numeric) && st.state.trim()!=='' && threshold===null) {noRule=true;return false;}
        if (Number.isFinite(numeric) && st.state.trim()!=='' && threshold!==null)
          return (tile.comparison === 'below') ? numeric < threshold : numeric > threshold;
        return !okay.includes(st.state.toLowerCase());
      });
      if (noRule && threshold===null) return result('Grenzwert einstellen',false,{missing:true});
      const {count,rooms}=activeCountByRooms(hass,bad);
      return result(!count?'Raumluft in Ordnung': rooms ? countMessage(count,'1 Raum prüfen!',n=>`${n} Räume prüfen!`) :
        countMessage(count,'1 Sensor prüfen!',n=>`${n} Sensoren prüfen!`),count>0);
    }
    if (kind === 'people') {
      const home = usable.filter(st=>st.state==='home' || (tile.include_zones && st.state !== 'not_home'));
      const count=home.length;
      return result(count===0?'Alle abwesend':count===usable.length?'Alle anwesend':
        countMessage(count,'1 Person anwesend',n=>`${n} Personen anwesend`),count>0);
    }
    if (kind === 'vehicles') {
      const wanted=(tile.active_state || 'on').toLowerCase();
      const moving=usable.filter(st=>st.state.toLowerCase()===wanted).length;
      return result(moving===0?'Fahrzeuge parken':countMessage(moving,'1 Fahrzeug fährt',n=>`${n} Fahrzeuge fahren`),moving>0);
    }
    if (kind === 'automations') {
      const count=usable.filter(st=>st.state==='on').length;
      return result(count===0?'Alle deaktiviert':count===usable.length?'Alle aktiviert':
        countMessage(count,'1 Automation aktiviert',n=>`${n} Automationen aktiviert`),count>0);
    }
    return result('Unbekannter Kacheltyp',false,{missing:true});
  }

  const CARD_CSS = `
    :host {display:block;}
    ha-card {background:none; border:0; box-shadow:none; padding:0; overflow:visible;}
    .grid {display:grid; grid-template-columns:repeat(var(--co-columns, 2),minmax(0,1fr));
      gap:var(--co-gap,8px);}
    button.tile {box-sizing:border-box; appearance:none; font:inherit;
      font-family:var(--primary-font-family,inherit); text-align:left;
      display:grid; grid-template-rows:30px minmax(26px,auto) 18px;
      align-content:center; justify-items:start; row-gap:1px;
      padding:10px 11px; min-width:0; width:100%; min-height:102px;
      border:1px solid var(--ha-card-border-color,var(--divider-color,transparent));
      border-radius:var(--ha-card-border-radius,12px);
      color:var(--primary-text-color);
      background:var(--ha-card-background,var(--card-background-color,#fff));
      box-shadow:var(--ha-card-box-shadow,0 1px 2px rgb(0 0 0 / 3%));
      cursor:default;
      transition:box-shadow .18s ease, border-color .18s ease, background .18s ease, transform .18s ease;
    }
    button.tile.clickable {cursor:pointer;}
    button.tile.clickable:hover {transform:translateY(-1px);
      box-shadow:0 3px 10px rgb(0 0 0 / 7%);
      border-color:color-mix(in srgb,var(--tile-color) 25%,var(--divider-color,#ddd));}
    button.tile.clickable:active {transform:translateY(0);}
    button.tile:focus-visible {outline:2px solid var(--primary-color); outline-offset:2px;}
    /* Original v1.2 gradient, exactly: 135deg, 32% through 14%, transparent by 68%. */
    button.tile.colored {background:linear-gradient(135deg,
      color-mix(in srgb,var(--tile-color) 32%, transparent) 0%,
      color-mix(in srgb,var(--tile-color) 32%, transparent) 14%,
      transparent 68%),var(--ha-card-background,var(--card-background-color,#fff));}
    .icon {box-sizing:border-box; height:30px; width:30px; display:flex;
      align-items:center; justify-content:flex-start;
      color:var(--tile-fg,var(--secondary-text-color));}
    ha-icon {--mdc-icon-size:25px; width:25px; height:25px;}
    .state {color:var(--tile-fg,var(--secondary-text-color));
      font-size:16px; line-height:26px; font-weight:700;
      width:100%; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;}
    .label {color:var(--primary-text-color); font-size:13px; line-height:18px;
      opacity:.8; width:100%; min-width:0;
      overflow:hidden; text-overflow:ellipsis; white-space:nowrap;}
    button.tile:not(:has(.label)) {grid-template-rows:30px minmax(26px,auto); min-height:82px;}
    .empty {padding:16px;color:var(--secondary-text-color);font-size:13px;}
    @media (prefers-reduced-motion:reduce) {
      button.tile {transition:none;}
      button.tile.clickable:hover {transform:none;}
    }
  `;
  class CentralOverviewCard extends HTMLElement {
    constructor() {super();this.attachShadow({mode:'open'});this._config=null;this._hass=null;this._rendered=false;}
    static getStubConfig() {const {type, ...config} = createConfig(); return config;}
    static getConfigElement() {return document.createElement(EDITOR_TAG);}
    getCardSize() {
      const n=(this._config?.tiles || []).filter(t=>t.enabled!==false && KINDS[t.kind]).length;
      const cols=Math.max(1,Math.min(4,Number(this._config?.columns)||2));
      return Math.max(1,Math.ceil((Math.ceil(n/cols)*110 + 8)/50));
    }
    getGridOptions() {return {columns:12,rows:'auto'};}
    setConfig(config) {
      if (!config || !Array.isArray(config.tiles)) {
        if (config && !config.tiles) config={...createConfig(),...config};
        else throw new Error('central-overview-card: tiles muss eine Liste sein.');
      }
      this._config={...createConfig(),...config,tiles:config.tiles.map(t=>({...t,icon:mdiIcon(t.icon,t.kind)}))};
      this._update();
    }
    set hass(hass) {this._hass=hass;this._update();}
    get hass() {return this._hass;}
    _update() {
      if (!this._config) return;
      if (!this._rendered) {
        this.shadowRoot.innerHTML=`<style>${CARD_CSS}</style><ha-card><div class="grid"></div></ha-card>`;
        this.shadowRoot.querySelector('.grid').addEventListener('click',(ev)=>{
          const btn=ev.target.closest('button.tile');
          if (!btn) return;
          const i=Number(btn.dataset.index), tile=this._config.tiles[i];
          if (!tile?.navigation_path || !btn.classList.contains('clickable')) return;
          const path=String(tile.navigation_path).trim();
          // Limit navigation to local dashboard URLs/anchors.
          if (!path || !(path.startsWith('/') || path.startsWith('#')) || path.startsWith('//')) return;
          history.pushState(null,'',path);
          window.dispatchEvent(new Event('location-changed'));
        });
        this._rendered=true;
      }
      const grid=this.shadowRoot.querySelector('.grid');
      grid.style.setProperty('--co-columns',String(Math.max(1,Math.min(4,Number(this._config.columns)||2))));
      grid.style.setProperty('--co-gap',`${Math.max(0,Math.min(40,Number(this._config.gap) || 0))}px`);
      if (!this._hass) {grid.innerHTML='<div class="empty">Home Assistant verbindet …</div>';return;}
      const enabled=this._config.tiles.map((t,i)=>({t,i})).filter(({t})=>t.enabled!==false && KINDS[t.kind]);
      if (!enabled.length) {grid.innerHTML='<div class="empty">Keine Kacheln ausgewählt.</div>';return;}
      grid.innerHTML=enabled.map(({t,i})=>{
        const status=compute(this._hass,t,Boolean(this._config.alarm_home_legacy));
        const selectedTone=t.tone && t.tone!=='auto' ? t.tone : (status.tone || KINDS[t.kind].tone);
        const color=COLOR_VARS[selectedTone] || COLOR_VARS.info;
        const colored=status.colorize || status.active;
        const textTone=colored ? color : 'var(--secondary-text-color)';
        const icon=mdiIcon(status.icon || t.icon,t.kind);
        const label=t.label === undefined ? KINDS[t.kind].label : t.label;
        const navigable=typeof t.navigation_path==='string' &&
          (t.navigation_path.startsWith('#') || (t.navigation_path.startsWith('/') && !t.navigation_path.startsWith('//')));
        const aria=`${label}: ${status.text}`;
        return `<button type="button" class="tile ${colored?'colored':''} ${navigable?'clickable':''}"
          data-index="${i}" style="--tile-color:${color};--tile-fg:${textTone}" aria-label="${esc(aria)}">
          <div class="icon"><ha-icon icon="${esc(icon)}"></ha-icon></div>
          <div class="state" title="${esc(status.text)}">${esc(status.text)}</div>
          ${this._config.show_labels!==false ? `<div class="label" title="${esc(label)}">${esc(label)}</div>`:''}
        </button>`;
      }).join('');
    }
  }

  const EDIT_CSS=`
    :host {display:block;color:var(--primary-text-color);font-family:var(--primary-font-family,inherit);}
    .panel {display:grid;gap:14px;}.global,.tile-editor {padding:12px;background:var(--card-background-color,var(--ha-card-background,#fff));
      border:1px solid var(--divider-color,#ddd);border-radius:12px;}
    h3 {margin:0 0 10px;font-size:15px;}p.help {margin:4px 0 10px;font-size:12px;line-height:1.4;color:var(--secondary-text-color);}
    .fields {display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;}
    label {display:flex;flex-direction:column;gap:4px;font-size:12px;color:var(--secondary-text-color);min-width:0;}
    label.wide {grid-column:1 / -1;}
    input,select {box-sizing:border-box;min-height:36px;border:1px solid var(--divider-color,#bbb);border-radius:7px;
      background:var(--card-background-color,var(--ha-card-background,#fff));color:var(--primary-text-color);font:inherit;font-size:14px;padding:6px 8px;width:100%;}
    input[type=checkbox] {width:17px;min-height:17px;accent-color:var(--primary-color,#03a9f4);}
    label.check {flex-direction:row;align-items:center;color:var(--primary-text-color);}
    ha-entity-picker, ha-icon-picker {width:100%;min-height:40px;display:block;}
    ha-icon-picker:not(:defined) {display:none;}
    .icon-fallback {display:none;}
    ha-icon-picker:not(:defined) + .icon-fallback {display:flex;}
    .fields > .wide {grid-column:1 / -1;}
    details {border:1px solid var(--divider-color,#ddd);border-radius:11px;overflow:hidden;}
    summary {padding:10px;cursor:pointer;font-size:14px;font-weight:600;}
    .tile-editor {border:0;border-top:1px solid var(--divider-color,#ddd);border-radius:0;display:grid;gap:12px;}
    .actions {display:flex;gap:6px;align-items:center;justify-content:flex-end;}
    button {background:var(--secondary-background-color,var(--card-background-color,#fff));color:var(--primary-text-color);
      border:1px solid var(--divider-color,#ddd);border-radius:7px;padding:6px 9px;min-height:32px;cursor:pointer;}
    button.primary {background:var(--primary-color,#03a9f4);color:var(--text-primary-color,#fff);border:0;}
    .entity-list {display:flex;flex-wrap:wrap;gap:5px;}
    .chip {font-size:12px;display:inline-flex;align-items:center;gap:6px;background:var(--secondary-background-color,#eee);
      border-radius:6px;padding:2px 5px;max-width:100%;overflow-wrap:anywhere;}
    .chip button {min-height:20px;padding:0 4px;}
    .add-row {display:grid;grid-template-columns:minmax(0,1fr) auto;gap:6px;align-items:end;}
    .footer {display:flex;gap:8px;align-items:center;}
    .footer select {flex:1;}
    .warning {color:var(--warning-color,#f90);}
  `;
  const sourceLabels={auto:'Automatisch erkennen',selected:'Entitäten auswählen',group:'Gruppe / Helfer verwenden'};
  class CentralOverviewEditor extends HTMLElement {
    constructor() {super();this.attachShadow({mode:'open'});this._config=null;this._hass=null;this._lastEmitted='';}
    setConfig(config) {
      const raw=JSON.stringify(config);
      if (raw === this._lastEmitted) return; // keep keyboard focus while editing
      this._config={...createConfig(),...config, tiles:(config.tiles||[]).map(t=>({...t,icon:mdiIcon(t.icon,t.kind),entities:strings(t.entities)}))};
      this._render();
    }
    set hass(hass) {
      const redraw=!this._hass;this._hass=hass;
      if(redraw && this._config)this._render();
      else this.shadowRoot.querySelectorAll('ha-entity-picker').forEach(el=>{el.hass=hass;});
    }
    get hass() {return this._hass;}
    _emit(structural=false) {
      this._config={...this._config,tiles:[...this._config.tiles]};
      this._lastEmitted=JSON.stringify(this._config);
      this.dispatchEvent(new CustomEvent('config-changed',{detail:{config:this._config},bubbles:true,composed:true}));
      if (structural) this._render();
    }
    _setTile(i,field,value,structural=false) {
      const previous=this._config.tiles[i];
      // The native picker also lists installed custom icon collections; constrain
      // the card to the built-in mdi: icons requested for universal distribution.
      if (field==='icon') value=mdiIcon(value,previous.kind);
      let tile={...previous, [field]:value};
      if (field==='kind' && KINDS[value]) {
        const oldDefaults=KINDS[previous.kind] || {};
        const defaults=KINDS[value];
        if (!previous.label || previous.label===oldDefaults.label) tile.label=defaults.label;
        if (!previous.icon || previous.icon===oldDefaults.icon) tile.icon=defaults.icon;
        if (!previous.tone || previous.tone===oldDefaults.tone || previous.tone==='auto')
          tile.tone=['alarm','lock'].includes(value)?'auto':defaults.tone;
        if (previous.source===oldDefaults.source) tile.source=defaults.source;
        tile.entities=[];
        delete tile.entity;
      }
      this._config.tiles[i]=tile;
      this._emit(structural);
    }
    _render() {
      if (!this._config) return;
      const cfg=this._config;
      const areas=Object.values(this._hass?.areas || {}).sort((a,b)=>String(a.name).localeCompare(String(b.name)));
      const option=(value,label,current)=>`<option value="${esc(value)}" ${value===current?'selected':''}>${esc(label)}</option>`;
      const tileHtml=cfg.tiles.map((tile,i)=>{
        const k=KINDS[tile.kind]||KINDS.lights;
        const mode=tile.source||k.source;
        const isGroup=mode==='group',isSelected=mode==='selected';
        return `<details data-i="${i}"><summary>${tile.enabled===false?'○':'●'} ${esc(tile.label||k.label)} · ${esc(sourceLabels[mode]||mode)}</summary>
          <div class="tile-editor" data-i="${i}">
            <div class="actions"><label class="check" style="margin-right:auto"><input type="checkbox" data-field="enabled" ${tile.enabled!==false?'checked':''}>Anzeigen</label>
            <button type="button" data-action="up" title="Nach oben" ${i===0?'disabled':''}>↑</button>
            <button type="button" data-action="down" title="Nach unten" ${i===cfg.tiles.length-1?'disabled':''}>↓</button>
            <button type="button" data-action="delete" title="Kachel entfernen">Entfernen</button></div>
            <div class="fields">
              <label>Typ<select data-field="kind">${Object.entries(KINDS).map(([v,d])=>option(v,d.label,tile.kind)).join('')}</select></label>
              <label>Datenquelle<select data-field="source">${Object.entries(sourceLabels).map(([v,d])=>option(v,d,mode)).join('')}</select></label>
              <label>Untertitel<input data-field="label" value="${esc(tile.label??k.label)}" placeholder="${esc(k.label)}"></label>
              <div class="wide"><ha-icon-picker data-field="icon" label="Symbol aus Home Assistant" value="${esc(mdiIcon(tile.icon,tile.kind))}"></ha-icon-picker>
                <label class="icon-fallback">Symbol (mdi:)<input data-field="icon" value="${esc(mdiIcon(tile.icon,tile.kind))}" placeholder="mdi:home"></label></div>
              <label>Aktiv-Farbe (HA-Standard)<select data-field="tone">${['alarm','lock'].includes(tile.kind)?option('auto','Abhängig vom Zustand',tile.tone||'auto'):''}${Object.entries(COLOR_LABELS).map(([v,d])=>option(v,d,tile.tone||k.tone)).join('')}</select></label>
              <label class="wide">Navigation (# oder /dashboard/...)<input data-field="navigation_path" value="${esc(tile.navigation_path||'')}" placeholder="#details"></label>
              ${mode==='auto'?`<label>Bereich<select data-field="area">${option('','Alle Bereiche',tile.area||'')}${areas.map(a=>option(a.area_id||a.id,a.name,tile.area||'')).join('')}</select></label>
                <label>Entitäts-ID beginnt mit (optional)<input data-field="prefix" value="${esc(tile.prefix||'')}" placeholder="z. B. light.wohn"></label>`:''}
              ${(isGroup || ['alarm','lock'].includes(tile.kind)) ? `<label class="wide">${isGroup?'Gruppe/Helfer':'Einzelne Entität (optional)'}
                <ha-entity-picker data-field="entity" allow-custom-entity value="${esc(tile.entity||'')}"></ha-entity-picker></label>`:''}
              ${isSelected ? `<div class="wide">
                <label>Ausgewählte Entitäten</label><div class="entity-list">${strings(tile.entities).map((id,j)=>`<span class="chip">${esc(id)}<button data-action="remove-entity" data-j="${j}" title="Entität entfernen">×</button></span>`).join('')}</div>
                <div class="add-row"><ha-entity-picker data-field="new-entity" allow-custom-entity></ha-entity-picker><button data-action="add-entity">Hinzufügen</button></div>
                <p class="help">Entitäten werden nur aus der Installation des jeweiligen Nutzers gelesen. Auch mehrere sind möglich.</p></div>`:''}
              ${tile.kind==='shading' ? `<label class="wide">Automatik-Entität (optional)<ha-entity-picker data-field="automation_entity" value="${esc(tile.automation_entity||'')}"></ha-entity-picker></label>`:''}
              ${tile.kind==='air' ? `<label class="wide">Gute Zustände (kommagetrennt)<input data-field="good_states" value="${esc(tile.good_states??'gut,good,ok,okay,ausgewogen')}"></label>
                <label>Grenzwert für Zahlensensoren<input type="number" step="any" data-field="threshold" value="${esc(tile.threshold??'')}"></label>
                <label>Warnung bei<select data-field="comparison">${option('above','Wert größer als',tile.comparison||'above')}${option('below','Wert kleiner als',tile.comparison||'above')}</select></label>`:''}
              ${tile.kind==='vehicles'?`<label class="wide">Zustand, der „fährt“ bedeutet<input data-field="active_state" value="${esc(tile.active_state||'on')}" placeholder="on"></label>`:''}
              ${tile.kind==='people'?`<label class="check wide"><input type="checkbox" data-field="include_zones" ${tile.include_zones?'checked':''}>Personen in anderen Zonen als „anwesend“ zählen</label>`:''}
            </div>
          </div></details>`;
      }).join('');
      this.shadowRoot.innerHTML=`<style>${EDIT_CSS}</style><div class="panel">
        <div class="global"><h3>Zentralübersicht</h3><p class="help">Universelle Kacheln: Auto-Erkennung über Home-Assistant-Domänen und Geräteklassen, eigene Entitäten oder Gruppen. Keine festen Benutzer-IDs.</p>
          <div class="fields"><label>Spalten<select data-global="columns">${[1,2,3,4].map(v=>option(String(v),String(v),String(cfg.columns||2))).join('')}</select></label>
          <label>Abstand (Pixel)<input type="number" min="0" max="40" data-global="gap" value="${esc(cfg.gap??8)}"></label>
          <label class="check wide"><input type="checkbox" data-global="show_labels" ${cfg.show_labels!==false?'checked':''}>Untertitel anzeigen</label>
          <label class="check wide"><input type="checkbox" data-global="alarm_home_legacy" ${cfg.alarm_home_legacy?'checked':''}>Alte Alarm-Anzeige: armed_home als „unscharf“ (nicht empfohlen)</label>
          </div></div>
        <h3>Kacheln (${cfg.tiles.length})</h3>${tileHtml}
        <div class="footer"><select id="new-kind">${Object.entries(KINDS).map(([v,d])=>option(v,d.label,'')).join('')}</select>
          <button type="button" class="primary" id="add-tile">+ Kachel</button></div>
        <p class="help">Für Fahrzeuge, Wecker und Raumluft ist eine Datenquelle notwendig. Audio und Fernseher werden automatisch nur erkannt, wenn die Geräteklasse zugeordnet ist.</p>
      </div>`;
      this.shadowRoot.querySelectorAll('ha-icon-picker').forEach(el=>{
        el.value=el.getAttribute('value') || '';
        el.addEventListener('value-changed',e=>{
          e.stopPropagation();
          const i=Number(el.closest('[data-i]').dataset.i);
          this._setTile(i,'icon',e.detail?.value || '');
        });
      });
      this.shadowRoot.querySelectorAll('ha-entity-picker').forEach(el=>{
        if (this._hass) el.hass=this._hass;
        // Property is the preferred value binding for frontend custom elements.
        if (el.dataset.field!=='new-entity') el.value=el.getAttribute('value')||'';
        el.addEventListener('value-changed',e=>{
          e.stopPropagation();
          if (el.dataset.field==='new-entity') {el.dataset.pending=e.detail?.value||'';return;}
          const i=Number(el.closest('[data-i]').dataset.i);
          this._setTile(i,el.dataset.field,e.detail?.value||'');
        });
      });
      const delegated=(e)=>{
        const el=e.target;
        const globalField=el.dataset?.global;
        if (globalField) {
          this._config[globalField]=el.type==='checkbox' ? el.checked : el.type==='number'||globalField==='columns' ? Number(el.value) : el.value;
          this._emit();return;
        }
        const field=el.dataset?.field;
        if (!field || field==='new-entity' || ['ha-entity-picker','ha-icon-picker'].includes(el.localName)) return;
        const i=Number(el.closest('[data-i]').dataset.i);
        const val=el.type==='checkbox' ? el.checked : el.value;
        this._setTile(i,field,val,['kind','source','enabled'].includes(field));
      };
      // 'change' for selects/checkboxes, 'input' for text/number. Do not rerender on every keypress.
      const panel=this.shadowRoot.querySelector('.panel');
      panel.addEventListener('change',delegated);
      panel.addEventListener('input',e=>{
        if (!['INPUT','TEXTAREA'].includes(e.target.tagName) || e.target.type==='checkbox') return;
        delegated(e);
      });
      panel.addEventListener('click',e=>{
        const el=e.target.closest('button');if(!el)return;
        if (el.id==='add-tile') {this._config.tiles.push(createTile(this.shadowRoot.querySelector('#new-kind').value));this._emit(true);return;}
        const action=el.dataset.action;if(!action)return;
        const container=el.closest('[data-i]');if(!container)return;
        const i=Number(container.dataset.i);
        if (action==='delete') this._config.tiles.splice(i,1);
        if (action==='up' && i>0) [this._config.tiles[i-1],this._config.tiles[i]]=[this._config.tiles[i],this._config.tiles[i-1]];
        if (action==='down' && i<this._config.tiles.length-1) [this._config.tiles[i+1],this._config.tiles[i]]=[this._config.tiles[i],this._config.tiles[i+1]];
        if (action==='remove-entity') this._config.tiles[i].entities.splice(Number(el.dataset.j),1);
        if (action==='add-entity') {
          const picker=container.querySelector('ha-entity-picker[data-field="new-entity"]');
          const id=picker?.dataset.pending || picker?.value || '';
          if (!id) return;
          this._config.tiles[i].entities=uniq([...(this._config.tiles[i].entities||[]),id]);
        }
        this._emit(true);
      });
    }
  }
  customElements.define(TAG,CentralOverviewCard);
  customElements.define(EDITOR_TAG,CentralOverviewEditor);
  window.customCards=window.customCards||[];
  if (!window.customCards.some(c=>c.type===TAG)) {
    window.customCards.push({type:TAG,name:'Zentralübersicht (universell)',
      description:'16 konfigurierbare Status-Kacheln für Sicherheit, Fenster, Licht, Klima und mehr.',preview:true});
  }
})();

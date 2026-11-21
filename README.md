# MYHS Central Card

**MYHS Cards for Home Assistant**

A modern, customizable dashboard card that brings your smart home's most important information together in one place. MYHS Central Card features **16 status tiles**, subtle theme-aware gradients, and a **built-in visual editor**—without requiring `custom:button-card` or additional icon packs.

**Version 1.1.2** · **16 tile types** · **Visual editor** · **Native Home Assistant icons**

![MYHS Central Card preview](images/preview.png)

*Preview uses demonstration data. Tile content and colors depend on your Home Assistant setup.*

## Highlights

- **One clear overview:** Security, lights, climate, media, presence, and more in a single card.
- **Visual configuration:** Add, remove, reorder, rename, and customize tiles directly in Home Assistant.
- **Flexible entity selection:** Use automatic discovery, individual entities, or groups/helpers.
- **Native styling:** Material Design Icons (`mdi:`), Home Assistant theme colors, and light/dark theme support.
- **Adjustable layout:** Choose 1–4 columns, tile spacing, labels, and navigation targets.
- **Display-focused:** Tiles show status and optionally navigate to a view; they do not directly operate devices.

## Installation

### HACS / Home Assistant Marketplace

1. Open **HACS** (or **Marketplace**) in Home Assistant.
2. Add this GitHub repository as a **custom Dashboard repository** if it is not listed in the catalog.
3. Install **MYHS Central Card** and reload your dashboard.
4. Select **MYHS Central Card** in **Edit dashboard → Add card**.

> HACS installs from a GitHub repository, not from a downloaded ZIP file. See [GITHUB-UPLOAD.md](GITHUB-UPLOAD.md) for repository setup and publishing instructions.

### Manual installation

1. Copy `dist/central-overview-card.js` to `/config/www/central-overview-card.js`.
2. In **Settings → Dashboards → Resources**, add `/local/central-overview-card.js` as a **JavaScript module**.
3. Reload Home Assistant and add **MYHS Central Card** to your dashboard.

## Visual editor

Configure your card directly in Home Assistant—no YAML required.

![MYHS Central Card visual editor](images/editor.png)

From **Edit dashboard → Edit card**, you can:

- Add, remove, hide, and reorder tiles.
- Select a tile type and its data source.
- Choose entities, areas, or groups/helpers.
- Change the label, native `mdi:` icon, accent color, and navigation target.
- Set the number of columns (1–4), spacing, and label visibility.

## Available tiles

| Tile | Status displayed | Default data source |
| --- | --- | --- |
| Security | Alarm panel state | `alarm_control_panel` |
| Windows | Open windows | Window/opening binary sensors |
| Lights | Active lights or rooms | `light` |
| Energy | Active plugs and outlets | Outlet/plug switches |
| Heating | Heating and auto modes | Heating `climate` entities |
| Climate | Cooling, heating, and ventilation | Cooling-capable `climate` entities |
| Audio | Playing and paused speakers | Speaker/receiver media players |
| Shading | Open, closed, and partial covers | `cover` |
| Media | Active TVs | TV media players |
| Air quality | Sensor states or threshold alerts | User-selected sensors |
| Access | Lock status | `lock` |
| Alarms / Timers | Active alarm switches | User-selected entities |
| Motion | Detected motion/presence | Motion/presence binary sensors |
| People | People at home | `person` |
| Vehicles | Vehicles in a configured state | User-selected entities |
| Automations | Enabled automations | `automation` |

**Automatic discovery** uses Home Assistant domains and device classes—not device names or personal entity IDs. If a device lacks the required device class, select it manually. Air quality, alarm-clock, and vehicle tiles require a user-selected source by default.

## Configuration

The visual editor is the recommended way to get started. Advanced users can also configure the card in YAML:

```yaml
type: custom:central-overview-card
columns: 2
gap: 8
tiles:
  - kind: windows
    label: Windows
    source: auto
    tone: error
    navigation_path: '#windows'
  - kind: lights
    label: Lights
    source: auto
    tone: warning
  - kind: people
    label: Presence
    source: auto
    tone: pink
```

Without a custom `tiles` list, the card starts with all 16 tile types. Available data-source modes are `auto` (discover matching entities), `selected` (choose entities), and `group` (use a group or helper). Optional settings include area filtering, state thresholds, and custom navigation targets.

The technical card type remains **`custom:central-overview-card`** for compatibility with existing dashboards.

## Design and compatibility

- Uses a **135° gradient** with Home Assistant theme colors, fading from the upper-left corner.
- Supports light and dark themes without custom `--custom_*` color variables.
- Uses built-in Material Design Icons (`mdi:`); no third-party icon library is needed.
- Works with user-provided entities and groups—no hard-coded installation-specific IDs.

**Security note:** Home Assistant's `armed_home` state means the alarm is *armed while home*. The optional `alarm_home_legacy` setting changes its display for compatibility with older configurations and is disabled by default.

## Updates and troubleshooting

**Seeing an old design?** Update the card through HACS and fully reload Home Assistant. For manual installations, changing the resource URL to `/local/central-overview-card.js?v=112` can bypass a cached JavaScript file.

**Seeing a commit hash instead of `1.1.2` in HACS?** Publish a regular GitHub release tagged `v1.1.2`. The version shown by HACS is determined by GitHub releases, while the label inside the visual editor comes from the card's JavaScript. If your repository already has a higher version tag, plan your release sequence accordingly.

**Missing devices?** Check their domain and device class, or select the entities manually in the visual editor.

## Development

```bash
node --check dist/central-overview-card.js
node tests/smoke.cjs
# Optional browser test (requires Playwright and Chromium)
python tests/browser_smoke.py
```

Syntax, status calculations, and visual-editor interactions have been tested locally. The preview images use sample data. Testing on a production Home Assistant installation and full public HACS publication has not yet been completed.

## License

Licensed under the [MIT License](LICENSE).

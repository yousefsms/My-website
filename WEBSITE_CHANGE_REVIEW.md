# Website Change Review - DM04 Spectral Viewer

## Implementation Summary
- **New Component**: Added a distinct `dm04-explorer` section to `DataStream.html` for "Azimuth-resolved spectra".
- **Independent Control**: Implemented independent filters for Nozzle, NPR, Microphone, and Polar Angle (phi).
- **Lazy Loading**: Added an explicit 'Load selected spectrum' button to prevent eager loading of large (~25MB) HTML files.
- **Catalog-Driven**: The viewer is powered by `media/figures/dm04/catalog.json`.
- **Styling**: Created `css/dm04-spectra.css` for a consistent look-and-feel with existing tools while maintaining independent IDs.
- **JS Logic**: Created `js/dm04-spectra.js` with an IIFE to ensure scope isolation from DM02/03.

## Catalog Schema Contract
File: `media/figures/dm04/catalog.json`
Format: Array of objects
Fields:
- `nozzle`: (string) Nozzle geometry (e.g., "Diamond")
- `npr`: (string) Nozzle Pressure Ratio (e.g., "12.5")
- `mic`: (string) Microphone index (1-based)
- `phi_deg`: (string/number) Physical polar angle in degrees
- `html`: (string) Relative URL to the Plotly HTML file (e.g., "media/figures/dm04/dm_04_...html")
- `png`: (string, optional) Relative URL to a PNG fallback/export
- `file_bytes`: (number) File size in bytes for the size hint

## Status
- **UI**: Implemented and integrated into `DataStream.html`.
- **Catalog**: `catalog.json` generated with 180 entries.
- **Catalog Sync**: COMPLETED.
- **Verification**: Numerical and HTTP verification passed.

## Final Sync & Verification
- **Asset Count**: 180 HTML files synced to `media/figures/dm04/`.
- **Shared JS**: `plotly.min.js` synced as `sharedplotly.min.js`.
- **HTML Modification**: Updated all 180 HTML files to use `sharedplotly.min.js`.
- **Payload**: ~3.3 GB on-demand assets.
- **Content Hashing**: Source/web 180 SHA256 hash matches.
- **UI Update**: `dm04-spectra.js` updated to implement a single iframe with a LOAD button.
- **Data Validation**:
    - Verified 180 files exist and are JSON valid.
    - Verified `phi_deg` uses 9 actual physical values (not 90 hardcode).
    - Numerical 0-error checks passed for sampled cases (NPR 4.3 Mic 1&8).
    - HTTP proof `canonicalplotlybundle/3nozzleassets` PASS.
- **Verification Tests**:
    - File integrity check via SHA256 in Python script.
    - Local HTTP server test (127.0.0.1:8000) confirmed accessibility.
- **Visual Review**: BROWSERVISUALREVIEWPENDING.

## 2024-05-24: DM04 UI Improvement
- **Goal**: Remove independent `phi` selector and make it read-only (driven by microphone selection).
- **Changes**:
    - `DataStream.html`: Replaced `phi` dropdown with `#dm04-phi-value` display.
    - `js/dm04-spectra.js`: Removed `phi` filtering logic; updated `handleFilterChange` to automatically resolve `phi` from `catalog.json` when a microphone is selected.
    - `css/dm04-spectra.css`: Added `.dm04-phi-display` style for the read-only field.
    - **Verification**: Validated that `(nozzle, npr, mic)` uniquely maps to `phi_deg` in `catalog.json`.
    - **Cache**: Updated version hashes for CSS and JS.

## 2024-05-24: DM04 UI/UX & Bug Fix Overhaul
- **Goal**: Resolve loading overlay bug, transition to Polar Angle-first selection, and filter Mic9.
- **Bug Fix (Loading Fallback)**: 
    - Root Cause: Large Plotly HTML files (~25MB) can cause the `iframe.onload` event to delay or fail in some browsers, leaving the "Loading..." overlay indefinitely.
    - Solution: Implemented a 30-second timeout (`LOAD_TIMEOUT_MS = 30000`). If the iframe fails to load within this window, the overlay updates to provide a direct "Open Full Size in New Tab" button, ensuring user access.
- **UI Overhaul (Selection Logic)**:
    - Transitioned from `Nozzle -> NPR -> Mic` to `Nozzle -> NPR -> Polar Angle (φ) -> Mic`.
    - Updated `DataStream.html` and `js/dm04-spectra.js` to implement this hierarchy.
    - Polar angles are now dynamically derived from `catalog.json` and sorted numerically.
- **Data Filtering (Mic9 Exclusion)**:
    - Implemented a filter in `loadCatalog()` to exclude any entry where `mic === '9'`.
    - This removes Mic9 from the public UI and selection logic without deleting raw assets from the drive.
- **Verification**:
    - Verified that selecting a Nozzle updates NPR options.
    - Verified that selecting NPR updates Phi options.
    - Verified that selecting Phi updates Mic options (excluding Mic9).
    - Verified the loading timeout triggers the fallback button.

## 2024-05-25: Bug Fix & UI Refinement
- **Bug Fix (Loading Deadlock)**: 
    - **Symptom**: Iframe occasionally stuck on "Loading..." overlay due to async race conditions and `loading="lazy"` behavior.
    - **Fix**: 
        - Changed `iframe.loading` to `'eager'` on click.
        - Implemented "Handlers-First" assignment: `onload` and `onerror` are now set before `src` is assigned.
        - Ensured iframe is `display: block` immediately to allow the browser to start the paint/load cycle.
        - Maintained 30s timeout fallback to prevent permanent deadlock.
- **UI Refinement (Selection Hierarchy)**:
    - **Change**: Removed the "Microphone" dropdown entirely.
    - **Logic**: The catalog mapping is now `Nozzle -> NPR -> Polar Angle (phi)`. 
    - **Verification**: Confirmed via Python that `(nozzle, npr, phi_deg)` uniquely maps to a single entry (and thus a single microphone) across the 160 filtered cases.
    - **Constraint**: `Mic9` remains excluded.
- **Validation**:
    - Verified `DataStream.html` no longer contains the `#dm04-mic` element.
    - Verified `js/dm04-spectra.js` routing logic is simplified to 3 controls.
    - Updated JS version hash in `DataStream.html`.

## 2024-05-26: Final Verification and Catalog Filtering
- **Data Modification**: Physically filtered "Mic9" entries from `media/figures/dm04/catalog.json`.
- **Public Count**: Reduced from 180 to 160 entries.
- **Structural Validation**: 
    - Verified 20 groups of exactly 8 microphones (Mics 1-8).
    - Verified each group has unique (Nozzle, NPR, phi_deg) combinations.
- **UI/UX Confirmation**: 
    - Confirmed `DataStream.html` uses Nozzle, NPR, and Polar Angle (φ) selectors only.
    - Confirmed the "Microphone" selector has been removed.
- **JS Implementation**:
    - Validated `js/dm04-spectra.js` logic for:
        - Defensive Mic9 filtering (double-layer: catalog file + JS `filter()`).
        - Iframe `loading="eager"` and "Handlers-First" assignment.
        - 30s timeout fallback with direct link.
- **Automated Tests**: 
    - Ran Node.js DOM-stub test suite (`test_dm04_logic.js`).
    - PASSED: Catalog loading, selection hierarchy, and iframe load sequence.
- **HTTP Status**: Verified assets available via local 127.0.0.1:8000.


### DM04 UI/UX Cleanup (Complete)
- **HTML**: 
    - Removed manual load button.
    - Integrated metadata and actions into a `dm04-details-panel`.
- **CSS**: 
    - Implemented full-width override for `.dm04-explorer` on desktop.
    - Added responsive height for landscape/portrait orientations.
    - Styled the new details panel.
- **JS**: 
    - Replaced manual button click with a debounced auto-load trigger (200ms).
    - Added URL deduplication to prevent redundant loads.
- **Verification**: 
    - Catalog still filters out Mic9 (160 entries).
    - Auto-load triggers correctly on final filter selection.
## 2024-05-27: DM04 Layout & Sizing Optimization
- **Goal**: Center the DM04 spectral viewer and implement responsive height clamps for the Plotly iframe.
- **Changes**:
    - `css/dm04-spectra.css`:
        - Updated `.dm04-container` to use `width: min(calc(100% - 40px), 1280px)` and `margin-inline: auto` for consistent centering.
        - Updated `.dm04-display-container` to use `height: clamp(500px, 70svh, 850px)` for the default (desktop) view.
        - Updated `.dm04-iframe` to `border: 0` and `display: block` (via JS when loaded) to prevent inner scrollbars and overflow.
        - Refined `@media` queries for mobile portrait (`68svh`, min 420px) and mobile landscape (`80svh`, min 260px).
        - Removed redundant `@media (orientation: landscape)` block to simplify.
- **Verification**:
    - Layout centering verified on desktop (1280px max).
    - Iframe height adjusts responsively across viewports.
    - No internal scrollbars introduced by the iframe itself.

## Updates - 2025-05-22 (Calculated Jet Velocity & Diameter)
- **Jet Velocity ($U_j$):** Updated in `dm02`, `dm03`, and `dm04` catalogs.
  - Formula: $U_j = \sqrt{\frac{2\gamma RT_0}{\gamma-1} (1 - NPR^{-\frac{\gamma-1}{\gamma}})}$
  - Constants: $\gamma=1.4$, $R=287$ J/(kg·K), $T_0=295$ K.
  - Provenance: Calculated from selected nominal NPR using MATLAB cold jet model.
  - Values range from $\approx 449.4$ m/s (NPR 4.3) to $\approx 565.0$ m/s (NPR 15).
- **Equivalent Diameter ($D_{eq}$):** Added $D_{eq} \approx 29$mm as an approximate value across all catalogs.
- **UI Footers:** Updated `js/dm02-explorer.js` and `js/dm04-spectra.js` to explicitly label these as "calculated" and not "measured".
- **Layout:** Verified `css/dm04-spectra.css` for centered layout (max-width 1280px, responsive iframe).


## 2025-05-24: Narrow Website Copy Tidy
- **Captions**: Updated  and  to use descriptive case formats: .
- **Footers**: Simplified footer metadata to show only , removing repetitive model assumptions.
- **Physics**: Relocated velocity derivation to the 'Azimuth-resolved spectra' info box in  with a readable HTML-formatted isentropic velocity equation.
- **Constraints**: Used standard HTML (sub/sup/&radic;) for accessibility and responsiveness; no external libraries added.

## 2026-11-19: Acoustic Explorer Fix (DM02/DM03 Sync)
- **Goal**: Preserve Nozzle/NPR selections when switching between Measurement Points (DM02) and Filled Surface (DM03).
- **Changes**:
    - Implemented cross-explorer state synchronization for Nozzle and NPR.
    - Added numeric catalog NPR vs. string select-value normalization to ensure consistent matching across different data sources.
    - Updated selection logic to automatically trigger figure reload when the mode switches, maintaining the current physical case.
- **Verification**:
    - Added regression tests in `test_dm02_logic.js` covering the mode-switch preservation and NPR normalization.
    - Verified visual continuity in browser: switching DM02 $\leftrightarrow$ DM03 no longer resets the case selection.

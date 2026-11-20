/**
 * DM04 Spectral Viewer Logic
 * Independent scope from DM02/03 to avoid collisions.
 */
(function() {
    'use strict';

    const CATALOG_URL = 'media/figures/dm04/catalog.json';
    const LOAD_TIMEOUT_MS = 30000; 
    const DEBOUNCE_MS = 200;

    let catalog = [];
    let currentSelection = {
        nozzle: '',
        npr: '',
        phi: ''
    };
    let debounceTimer = null;
    let currentLoadUrl = '';

    function init() {
        const container = document.getElementById('dm04-container');
        if (!container) return;
        loadCatalog();
    }

    async function loadCatalog() {
        try {
            const response = await fetch(CATALOG_URL, { cache: 'no-store' });
            if (!response.ok) throw new Error('Catalog not found');
            const data = await response.json();
            
            catalog = data.filter(e => String(e.mic) !== '9');
            populateFilters();
        } catch (err) {
            console.error('DM04 Catalog Error:', err);
            updateFallback('Figures being prepared. Please check back soon.');
        }
    }

    function populateFilters() {
        const nozzleSel = document.getElementById('dm04-nozzle');
        const nprSel = document.getElementById('dm04-npr');
        if (!nozzleSel || !nprSel) return;

        const nozzles = [...new Set(catalog.map(e => e.nozzle))].sort();
        nozzleSel.innerHTML = '<option value="">-- Select Nozzle --</option>';
        nozzles.forEach(n => {
            nozzleSel.innerHTML += `<option value="${n}">${n}</option>`;
        });

        nprSel.innerHTML = '<option value="">-- Select NPR --</option>';
    }

    function handleFilterChange(event) {
        const targetId = event.target.id;
        const nozzleSel = document.getElementById('dm04-nozzle');
        const nprSel = document.getElementById('dm04-npr');
        const phiSel = document.getElementById('dm04-phi');

        const nozzle = nozzleSel.value;
        const npr = nprSel.value;
        const phi = phiSel.value;

        currentSelection.nozzle = nozzle;
        currentSelection.npr = npr;
        currentSelection.phi = phi;

        if (targetId === 'dm04-nozzle') {
            nprSel.innerHTML = '<option value="">-- Select NPR --</option>';
            phiSel.innerHTML = '<option value="">-- Select polar angle --</option>';
            if (nozzle) {
                const nprs = [...new Set(catalog.filter(e => e.nozzle === nozzle).map(e => e.npr))].sort((a, b) => parseFloat(a) - parseFloat(b));
                nprs.forEach(n => {
                    nprSel.innerHTML += `<option value="${n}">${n}</option>`;
                });
            }
        } 
        else if (targetId === 'dm04-npr') {
            phiSel.innerHTML = '<option value="">-- Select polar angle --</option>';
            if (nozzle && npr) {
                const filtered = catalog.filter(e => e.nozzle === nozzle && e.npr === npr);
                const phis = [...new Set(filtered.map(e => e.phi_deg))].sort((a, b) => parseFloat(a) - parseFloat(b));
                phis.forEach(p => {
                    phiSel.innerHTML += `<option value="${p}">${p}°</option>`;
                });
            }
        }

        triggerAutoLoad();
    }

    function triggerAutoLoad() {
        if (debounceTimer) clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            const entry = getSelectedEntry();
            if (entry && entry.html) {
                if (currentLoadUrl !== entry.html) {
                    currentLoadUrl = entry.html;
                    loadSpectrum(entry);
                }
            }
        }, DEBOUNCE_MS);
    }

    function getSelectedEntry() {
        return catalog.find(e => 
            e.nozzle === currentSelection.nozzle && 
            e.npr === currentSelection.npr && 
            String(e.phi_deg) === String(currentSelection.phi)
        );
    }

    function loadSpectrum(entry) {
        if (!entry) return;
        const iframe = document.getElementById('dm04-iframe');
        const fallback = document.getElementById('dm04-fallback');
        const metadata = document.getElementById('dm04-metadata');
        const linkFull = document.getElementById('dm04-link-full');

        fallback.style.display = 'flex';
        fallback.innerHTML = '<div class="text-center"><p>Loading spectrum... (large file, please wait)</p></div>';
        iframe.style.display = 'block';
        iframe.loading = 'eager';

        let timeoutTriggered = false;
        const timeoutId = setTimeout(() => {
            timeoutTriggered = true;
            fallback.style.display = 'flex';
            fallback.innerHTML = `<div class="text-center"><p>The plot is taking longer than expected to load.</p><a href="${entry.html}" target="_blank" class="btn-dm04 btn-dm04-primary">Open Full Size in New Tab</a></div>`;
        }, LOAD_TIMEOUT_MS);

        iframe.onload = () => {
            if (!timeoutTriggered) {
                clearTimeout(timeoutId);
                fallback.style.display = 'none';
                
                const uj = entry.uj_m_s ? entry.uj_m_s.toFixed(1) : '---';
                const deq = entry.deq_mm ? entry.deq_mm : '---';

                metadata.innerHTML = `
                    <div style="margin-bottom: 10px;"><strong>Case:</strong> ${entry.nozzle.toLowerCase()} nozzle (cold jet) NPR ${entry.npr} @ φ=${entry.phi_deg}°</div>
                    <div style="font-size: 12px; color: #666; border-top: 1px solid #ddd; padding-top: 8px;">
                        U<sub>j</sub> ≈ ${uj} m/s, D<sub>eq</sub> ≈ ${deq} mm
                    </div>
                `;
                linkFull.href = entry.html;
            }
        };

        iframe.onerror = () => {
            clearTimeout(timeoutId);
            fallback.style.display = 'flex';
            fallback.innerHTML = '<div class="text-center"><p>Error loading spectrum. Please try the "Open Full Size" link.</p></div>';
        };

        iframe.src = entry.html;
    }

    function updateFallback(msg) {
        const fallback = document.getElementById('dm04-fallback');
        fallback.innerHTML = `<div class="text-center"><p>${msg}</p></div>`;
    }

    window.addEventListener('DOMContentLoaded', () => {
        init();
        const nozzleSel = document.getElementById('dm04-nozzle');
        const nprSel = document.getElementById('dm04-npr');
        const phiSel = document.getElementById('dm04-phi');
        if (nozzleSel) nozzleSel.addEventListener('change', handleFilterChange);
        if (nprSel) nprSel.addEventListener('change', handleFilterChange);
        if (phiSel) phiSel.addEventListener('change', handleFilterChange);
    });
}
)();

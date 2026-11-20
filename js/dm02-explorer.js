async function initDM02Explorer() {
    const catalogs = {
        dm02: 'media/figures/dm02/catalog.json',
        dm03: 'media/figures/dm03/catalog.json'
    };
    let catalogData = {
        dm02: [],
        dm03: []
    };

    try {
        const [res02, res03] = await Promise.all([
            fetch(catalogs.dm02),
            fetch(catalogs.dm03)
        ]);
        if (!res02.ok || !res03.ok) throw new Error('Failed to load catalogs');
        catalogData.dm02 = await res02.json();
        catalogData.dm03 = await res03.json();
    } catch (err) {
        console.error('DM02/03 Explorer Error:', err);
        document.getElementById('dm02-container').innerHTML = '<div class="alert alert-danger">Error loading figure catalogs. Please try refreshing the page.</div>';
        return;
    }

    const viewSelect = document.getElementById('dm-view');
    const nozzleSelect = document.getElementById('dm02-nozzle');
    const nprSelect = document.getElementById('dm02-npr');
    const display = document.getElementById('dm02-display');
    const iframe = document.getElementById('dm02-iframe');
    const fallback = document.getElementById('dm02-fallback');
    const meta = document.getElementById('dm02-metadata');
    const linkFull = document.getElementById('dm02-link-full');
    const linkPng = document.getElementById('dm02-link-png');

    let debounceTimer = null;

    function updateNPROptions(isViewChange = false) {
        const view = viewSelect.value;
        const nozzle = nozzleSelect.value;
        const currentCatalog = catalogData[view];
        const availableNPRs = currentCatalog.filter(item => item.nozzle === nozzle);
        
        const previousNPR = nprSelect.value;

        nprSelect.innerHTML = '<option value="">-- Select NPR --</option>';
        availableNPRs.forEach(item => {
            const option = document.createElement('option');
            option.value = item.npr;
            option.textContent = `NPR ${item.npr}`;
            nprSelect.appendChild(option);
        });

        if (isViewChange && previousNPR && availableNPRs.some(item => String(item.npr) === String(previousNPR))) {
            nprSelect.value = previousNPR;
            debouncedUpdateFigure();
        } else {
            nprSelect.value = '';
            updateFigure();
        }
    }

    function updateFigure() {
        const view = viewSelect.value;
        const nozzle = nozzleSelect.value;
        const nprValue = nprSelect.value;

        if (!nprValue) {
            fallback.style.display = 'flex';
            fallback.innerHTML = '<p>Select an NPR to load the figure.</p>';
            iframe.style.display = 'none';
            meta.innerHTML = 'Select a case to see details.';
            return;
        }

        const npr = parseFloat(nprValue);
        const currentCatalog = catalogData[view];
        const figure = currentCatalog.find(item => item.nozzle === nozzle && item.npr === npr);

        if (!figure) {
            fallback.style.display = 'flex';
            fallback.innerHTML = '<div class="dm02-fallback">No data available for this combination.</div>';
            return;
        }

        fallback.style.display = 'flex';
        fallback.innerHTML = `
            <div style="text-align:center">
                <img src="${figure.png}" alt="Preview of ${figure.label}" loading="lazy">
                <p style="margin-top:10px; font-size:14px; color:#666;">Loading interactive plot...</p>
            </div>
        `;

        iframe.style.display = 'none';
        iframe.src = ''; 
        
        setTimeout(() => {
            iframe.src = figure.html;
            iframe.style.display = 'block';
            fallback.style.display = 'none';
        }, 100);

        const range = figure.vmin !== undefined ? `${figure.vmin} dB to ${figure.vmax} dB` : 'Physical units (r/Deq)';
        const uj = figure.uj_m_s ? figure.uj_m_s.toFixed(1) : '---';
        const deq = figure.deq_mm ? figure.deq_mm : '---';

        meta.innerHTML = `
            <strong>Figure:</strong> ${figure.label} (${view === 'dm02' ? 'Measurement Points' : 'Filled Surface'})<br>
            <strong>Acoustic Range:</strong> ${range} (normalized per case)<br>
            <div style="font-size: 12px; color: #666; border-top: 1px solid #ddd; padding-top: 8px;">
                U<sub>j</sub> ≈ ${uj} m/s, D<sub>eq</sub> ≈ ${deq} mm
            </div>
        `;

        linkFull.href = figure.html;
        linkPng.href = figure.png;
    }

    function debouncedUpdateFigure() {
        if (debounceTimer) clearTimeout(debounceTimer);
        debounceTimer = setTimeout(updateFigure, 200);
    }

    viewSelect.addEventListener('change', () => updateNPROptions(true));
    nozzleSelect.addEventListener('change', () => updateNPROptions(false));
    nprSelect.addEventListener('change', debouncedUpdateFigure);

    updateNPROptions();
}

document.addEventListener('DOMContentLoaded', initDM02Explorer);

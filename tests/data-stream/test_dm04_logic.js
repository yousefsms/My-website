const fs = require('fs');

// --- DOM STUBS ---
const elements = {};
const mockElement = (id) => {
    const el = {
        id,
        innerHTML: '',
        value: '',
        style: {},
        disabled: false,
        loading: '',
        addEventListener: (event, cb) => { elements[id].listeners = elements[id].listeners || {}; elements[id].listeners[event] = cb; },
        onload: null,
        onerror: null,
        src: '',
        classList: {
            add: () => {},
            remove: () => {}
        }
    };
    elements[id] = el;
    return el;
};

global.document = {
    getElementById: (id) => elements[id] || null,
    addEventListener: (event, cb) => { global.document.listeners = global.document.listeners || {}; global.document.listeners[event] = cb; }
};
global.window = {
    addEventListener: (event, cb) => { global.window.listeners = global.window.listeners || {}; global.window.listeners[event] = cb; }
};
global.fetch = async (url) => {
    if (url.includes('catalog.json')) {
        const data = JSON.parse(fs.readFileSync('media/figures/dm04/catalog.json', 'utf8'));
        return {
            ok: true,
            json: async () => data
        };
    }
    throw new Error('404 Not Found');
};

// Initialize required elements
['dm04-container', 'dm04-nozzle', 'dm04-npr', 'dm04-phi', 'dm04-iframe', 'dm04-fallback', 'dm04-metadata', 'dm04-link-full', 'dm04-link-png'].forEach(mockElement);

// Load the JS file
const jsCode = fs.readFileSync('js/dm04-spectra.js', 'utf8');
eval(jsCode);

// Simulate DOMContentLoaded
if (global.window.listeners && global.window.listeners['DOMContentLoaded']) {
    global.window.listeners['DOMContentLoaded']();
}

// Test 1: Catalog Loading and Mic9 Filtering
async function testCatalog() {
    console.log('Testing Catalog Loading...');
    await new Promise(r => setTimeout(r, 100));
    
    const nozzleSel = elements['dm04-nozzle'];
    if (nozzleSel.innerHTML === '<option value="">-- Select Nozzle --</option>') {
        console.error('FAILED: Nozzles not populated');
        return false;
    }
    console.log('PASSED: Nozzles populated');
    return true;
}

// Test 2: Selection Hierarchy
function testHierarchy() {
    console.log('Testing Selection Hierarchy...');
    const nozzleSel = elements['dm04-nozzle'];
    const nprSel = elements['dm04-npr'];
    const phiSel = elements['dm04-phi'];

    const nozzleMatch = nozzleSel.innerHTML.match(/value="([^"]+)"/);
    if (!nozzleMatch) { console.error('FAILED: Nozzle options not found'); return false; }
    nozzleSel.value = nozzleMatch[1];
    nozzleSel.listeners['change']({ target: nozzleSel });
    
    if (nprSel.innerHTML === '<option value="">-- Select NPR --</option>') {
        console.error('FAILED: NPR not populated after nozzle selection');
        return false;
    }
    console.log('PASSED: NPR populated after nozzle selection');

    const nprMatch = nprSel.innerHTML.match(/value="([^"]+)"/);
    if (!nprMatch) { console.error('FAILED: NPR options not found'); return false; }
    nprSel.value = nprMatch[1];
    nprSel.listeners['change']({ target: nprSel });
    
    if (phiSel.innerHTML === '<option value="">-- Select Phi --</option>') {
        console.error('FAILED: Phi not populated after NPR selection');
        return false;
    }
    console.log('PASSED: Phi populated after NPR selection');

    return true;
}

// Test 3: Iframe Load Sequence
async function testIframeLoad() {
    console.log('Testing Iframe Load Sequence...');
    const iframe = elements['dm04-iframe'];
    const fallback = elements['dm04-fallback'];

    const nozzleSel = elements['dm04-nozzle'];
    const nprSel = elements['dm04-npr'];
    const phiSel = elements['dm04-phi'];

    const nozzleVal = nozzleSel.innerHTML.match(/value="([^"]+)"/)[1];
    nozzleSel.value = nozzleVal;
    nozzleSel.listeners['change']({ target: nozzleSel });

    const nprVal = nprSel.innerHTML.match(/value="([^"]+)"/)[1];
    nprSel.value = nprVal;
    nprSel.listeners['change']({ target: nprSel });

    const phiVal = phiSel.innerHTML.match(/value="([^"]+)"/)[1];
    phiSel.value = phiVal;
    phiSel.listeners['change']({ target: phiSel });

    // Wait for debounce timer (200ms)
    await new Promise(r => setTimeout(r, 300));

    if (iframe.loading !== 'eager') {
        console.error('FAILED: Iframe loading not set to eager');
        return false;
    }
    if (fallback.style.display !== 'flex') {
        console.error('FAILED: Fallback overlay not shown');
        return false;
    }
    if (!iframe.onload) {
        console.error('FAILED: iframe.onload handler not set');
        return false;
    }

    // Trigger onload
    iframe.onload();
    if (fallback.style.display !== 'none') {
        console.error('FAILED: Fallback overlay not hidden after load');
        return false;
    }

    console.log('PASSED: Iframe load sequence correct');
    return true;
}

async function runTests() {
    const t1 = await testCatalog();
    const t2 = testHierarchy();
    const t3 = testIframeLoad();
    
    if (t1 && t2 && t3) {
        console.log('\nALL LOGIC TESTS PASSED');
        process.exit(0);
    } else {
        console.log('\nSOME TESTS FAILED');
        process.exit(1);
    }
}

runTests();

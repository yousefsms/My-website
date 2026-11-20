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
        addEventListener: (event, cb) => { 
            elements[id].listeners = elements[id].listeners || {}; 
            elements[id].listeners[event] = cb; 
        },
        onload: null,
        onerror: null,
        src: '',
        appendChild: (child) => {
            // Basic mock of appendChild that adds to innerHTML for the options mock to work
            if (child.tagName === 'OPTION') {
                elements[id].innerHTML += `<option value="${child.value}">${child.textContent}</option>`;
            } else {
                // For other elements, just do nothing as we don't need them in these tests
            }
        },
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
    createElement: (tag) => {
        const el = { 
            tagName: tag.toUpperCase(), 
            value: '', 
            textContent: '', 
            appendChild: () => {} 
        };
        return el;
    },
    addEventListener: (event, cb) => { global.document.listeners = global.document.listeners || {}; global.document.listeners[event] = cb; }
};

global.window = {
    addEventListener: (event, cb) => { global.window.listeners = global.window.listeners || {}; global.window.listeners[event] = cb; }
};

global.fetch = async (url) => {
    if (url.includes('dm02/catalog.json')) {
        const data = JSON.parse(fs.readFileSync('media/figures/dm02/catalog.json', 'utf8'));
        return { ok: true, json: async () => data };
    }
    if (url.includes('dm03/catalog.json')) {
        const data = JSON.parse(fs.readFileSync('media/figures/dm03/catalog.json', 'utf8'));
        return { ok: true, json: async () => data };
    }
    throw new Error('404 Not Found');
};

// Initialize required elements
['dm-view', 'dm02-nozzle', 'dm02-npr', 'dm02-display', 'dm02-iframe', 'dm02-fallback', 'dm02-metadata', 'dm02-link-full', 'dm02-link-png'].forEach(mockElement);

// Set default values as they would be in HTML
elements['dm-view'].value = 'dm02';
elements['dm02-nozzle'].value = 'diamond';

// Mock HTMLOptions for nprSelect.options
Object.defineProperty(elements['dm02-npr'], 'options', {
    get() {
        const inner = elements['dm02-npr'].innerHTML;
        const options = [];
        const regex = /<option value="([^"]*)">([^<]*)<\/option>/g;
        let match;
        while ((match = regex.exec(inner)) !== null) {
            options.push({ value: match[1] });
        }
        return options;
    }
});

// Load the JS file
const jsCode = fs.readFileSync('js/dm02-explorer.js', 'utf8');
eval(jsCode);

async function runTests() {
    console.log('Starting DM02 Logic Tests...');

    try {
        // Call initDM02Explorer directly and await it
        await initDM02Explorer();
        console.log('initDM02Explorer completed successfully');
    } catch (err) {
        console.error('Error during initDM02Explorer:', err);
        process.exit(1);
    }

    const viewSel = elements['dm-view'];
    const nozzleSel = elements['dm02-nozzle'];
    const nprSel = elements['dm02-npr'];
    const iframe = elements['dm02-iframe'];
    const fallback = elements['dm02-fallback'];

    if (!nozzleSel.listeners || !nozzleSel.listeners['change']) {
        console.error('FAILED: Listeners not attached.');
        process.exit(1);
    }

    // Test 1: Initial state - should be populated because "diamond" is default
    console.log('Test 1: Initial state...');
    if (nprSel.innerHTML.includes('NPR')) {
        console.log('PASSED: NPR select populated with default nozzle');
    } else {
        console.error('FAILED: NPR select not populated with default nozzle');
    }

    // Test 2: Nozzle selection populates NPRs
    console.log('Test 2: Nozzle selection populates NPRs...');
    nozzleSel.value = 'rectangular';
    nozzleSel.listeners['change']({ target: nozzleSel });
    if (nprSel.innerHTML.includes('NPR')) {
        console.log('PASSED: NPRs populated');
    } else {
        console.error('FAILED: NPRs not populated');
    }

    // Test 3: NPR selection loads figure
    console.log('Test 3: NPR selection loads figure...');
    // Use a known NPR from catalog to be sure
    const nprVal = nprSel.options[1].value; // Option 0 is "-- Select NPR --"
    nprSel.value = nprVal;
    nprSel.listeners['change']({ target: nprSel });
    
    // Wait for debounce AND the internal setTimeout for iframe.src
    await new Promise(r => setTimeout(r, 600));
    if (iframe.src !== '' && iframe.style.display === 'block') {
        console.log('PASSED: Figure loaded');
    } else {
        console.error(`FAILED: Figure not loaded. src=${iframe.src}, display=${iframe.style.display}`);
    }

    // Test 4: View change preserves NPR and updates figure
    console.log('Test 4: View change preserves NPR and updates figure...');
    const currentSrc = iframe.src;
    const currentView = viewSel.value;
    
    // Ensure we are testing a numeric NPR value that might be a string in the select
    nprSel.value = nprVal;
    nprSel.listeners['change']({ target: nprSel });
    await new Promise(r => setTimeout(r, 600));

    viewSel.value = (currentView === 'dm02') ? 'dm03' : 'dm02';
    viewSel.listeners['change']({ target: viewSel });
    
    // Wait for debounce AND internal setTimeout
    await new Promise(r => setTimeout(r, 600));
    if (nprSel.value === nprVal && iframe.src !== '' && iframe.src !== currentSrc) {
        console.log('PASSED: View change preserved NPR and updated figure');
    } else {
        console.error(`FAILED: View change did not preserve NPR or update figure. npr=${nprSel.value}, src=${iframe.src}, oldSrc=${currentSrc}`);
        process.exit(1);
    }

    // Test 5: Nozzle change resets display
    console.log('Test 5: Nozzle change resets display...');
    nozzleSel.value = 'elliptic';
    nozzleSel.listeners['change']({ target: nozzleSel });
    if (fallback.style.display === 'flex' && iframe.style.display === 'none') {
        console.log('PASSED: Nozzle change reset display');
    } else {
        console.error('FAILED: Nozzle change reset display');
    }

    console.log('\nDM02 Logic Tests Completed');
}

runTests().catch(err => {
    console.error(err);
    process.exit(1);
});

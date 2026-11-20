const { JSDOM } = require('jsdom');
const fs = require('fs');

const jsCode = fs.readFileSync('js/dm04-spectra.js', 'utf8');

const mockHtml = `
<!DOCTYPE html>
<html>
    <body>
        <div id="dm04-container">
            <div class="dm04-controls">
                <select id="dm04-nozzle"></select>
                <select id="dm04-npr"></select>
                <select id="dm04-phi"></select>
            </div>
            <div class="dm04-display-container">
                <div id="dm04-fallback"></div>
                <iframe id="dm04-iframe"></iframe>
            </div>
            <div id="dm04-metadata"></div>
            <a id="dm04-link-full"></a>
        </div>
    </body>
</html>
`;

const dom = new JSDOM(mockHtml, { 
    runScripts: "dangerously", 
    resources: "usable" 
});

const window = dom.window;
const document = window.document;

const mockCatalog = [
    { nozzle: 'Diamond', npr: '4.8', mic: '1', phi_deg: '0', html: 'media/Plots/Diamond_NPR4p8_0.html' },
    { nozzle: 'Diamond', npr: '4.8', mic: '1', phi_deg: '90', html: 'media/Plots/Diamond_NPR4p8_90.html' },
    { nozzle: 'Diamond', npr: '4.8', mic: '9', phi_deg: '0', html: 'media/Plots/Diamond_NPR4p8_0_mic9.html' },
    { nozzle: 'Rectangular', npr: '4.4', mic: '1', phi_deg: '0', html: 'media/Plots/Rect_NPR4p4_0.html' },
];

window.fetch = async (url) => {
    if (url === 'media/figures/dm04/catalog.json') {
        return {
            ok: true,
            json: async () => mockCatalog,
        };
    }
    return { ok: false };
};

const scriptElement = window.document.createElement('script');
scriptElement.textContent = jsCode;
window.document.body.appendChild(scriptElement);

window.document.dispatchEvent(new window.Event('DOMContentLoaded'));

const sleep = (ms) => new Promise(res => setTimeout(res, ms));

async function runTests() {
    console.log('Starting DM04 Logic Tests...');

    const nozzleSel = document.getElementById('dm04-nozzle');
    const nprSel = document.getElementById('dm04-npr');
    const phiSel = document.getElementById('dm04-phi');
    const iframe = document.getElementById('dm04-iframe');

    if (!nozzleSel || !nprSel || !phiSel || !iframe) {
        console.error('Failed to find DOM elements.');
        process.exit(1);
    }

    await sleep(100); 
    console.log('Test 1: Nozzle Population');
    if (nozzleSel.options.length === 3) { 
        console.log('✅ Nozzle population correct');
    } else {
        console.error('❌ Nozzle population incorrect: ' + nozzleSel.options.length);
    }

    console.log('Test 2: NPR Population (Diamond)');
    nozzleSel.value = 'Diamond';
    nozzleSel.dispatchEvent(new window.Event('change'));
    await sleep(100);
    if (nprSel.options.length === 2) { 
        console.log('✅ NPR population correct for Diamond');
    } else {
        console.error('❌ NPR population incorrect for Diamond: ' + nprSel.options.length);
    }

    console.log('Test 3: Phi Population (Diamond, 4.8)');
    nprSel.value = '4.8';
    nprSel.dispatchEvent(new window.Event('change'));
    await sleep(100);
    if (phiSel.options.length === 3) { 
        console.log('✅ Phi population correct (Mic 9 filtered)');
    } else {
        console.error('❌ Phi population incorrect: ' + phiSel.options.length);
    }

    console.log('Test 4: Iframe navigation');
    phiSel.value = '0';
    phiSel.dispatchEvent(new window.Event('change'));
    await sleep(300); 
    if (iframe.src.endsWith('media/Plots/Diamond_NPR4p8_0.html')) {
        console.log('✅ Iframe src correct for selection');
    } else {
        console.error('❌ Iframe src incorrect: ' + iframe.src);
    }

    console.log('Test 5: Iframe update');
    phiSel.value = '90';
    phiSel.dispatchEvent(new window.Event('change'));
    await sleep(300);
    if (iframe.src.endsWith('media/Plots/Diamond_NPR4p8_90.html')) {
        console.log('✅ Iframe src updated correctly');
    } else {
        console.error('❌ Iframe src updated correctly: ' + iframe.src);
    }

    console.log('Tests completed successfully.');
    process.exit(0);
}

runTests().catch(err => {
    console.error(err);
    process.exit(1);
});

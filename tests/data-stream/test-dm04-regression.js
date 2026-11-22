const fs = require('fs');
const path = require('path');

const htmlPath = path.join(__dirname, '../../DataStream.html');
const html = fs.readFileSync(htmlPath, 'utf8');

function assert(condition, message) {
    if (!condition) {
        console.error(`❌ ${message}`);
        process.exit(1);
    }
    console.log(`✅ ${message}`);
}

console.log('Running DM04 Regression Tests...');

// 1. Verify iframe with name="iframe_dm04" exists
assert(html.includes('name="iframe_dm04"'), 'DataStream.html should contain an iframe with name="iframe_dm04"');

// 2. Verify plotIframeNames does NOT include iframe_dm04 (to prevent zero-dimension relayout regression)
// We check for the specific array pattern to avoid matching the iframe name attribute
const arrayPattern = /var plotIframeNames = \[[^\]]*iframe_dm04[^\]]*\]/;
assert(!arrayPattern.test(html), 'plotIframeNames array should NOT include "iframe_dm04"');
assert(html.includes('var plotIframeNames'), 'plotIframeNames variable should be defined');

// 3. Verify fit logic uses load listener/fitPlotlyFrame
assert(html.includes('iframe.addEventListener(\'load\''), 'Should use load event listener for iframes');
assert(html.includes('function fitPlotlyFrame'), 'Should define fitPlotlyFrame function');
assert(html.includes('scheduleFits(iframe)'), 'Should call scheduleFits in the load listener');

console.log('All DM04 regression tests passed.');
process.exit(0);

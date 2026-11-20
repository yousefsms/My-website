# Data Stream Tests

This directory contains tests for the DataStream spectral viewer logic.

## Purpose
Validates the catalog loading, selection hierarchy, and iframe loading sequence for both DM02 (Measurement Points) and DM04 (Azimuth-resolved spectra) logic suites.

## Invocation
Run via npm:
`npm test`
or directly:
`node tests/data-stream/test_dm02_logic.js`
`node tests/data-stream/test_dm04_logic.js`

## Asset Locations
Tests assume that `media/figures/dm04/catalog.json` and `media/figures/dm02/catalog.json` are present and valid.

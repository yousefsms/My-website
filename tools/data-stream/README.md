# Data Stream Tools

This directory contains post-processing and maintenance scripts for the DataStream spectral viewer.

## Purpose
These scripts are used to generate catalogs, update footers, and validate the HTML/JSON assets for the DM02, DM03, and DM04 datasets.

## Canonical Figure Generators
**Note**: These scripts are for website maintenance only. The canonical scientific figure generators (source scripts) are located in:
`/Users/yoyo/03_Dissertation_Work/figure_recreation/scripts`

## Invocation Assumptions
Scripts are designed to be run from the repository root:
`python3 tools/data-stream/script_name.py`

## Asset Locations
Generated Plotly HTML files and `catalog.json` files must remain under:
- `media/figures/dm02/`
- `media/figures/dm03/`
- `media/figures/dm04/`

import os

review_file = 'WEBSITE_CHANGE_REVIEW.md'
if os.path.exists(review_file):
    with open(review_file, 'r') as f:
        content = f.read()
    
    # Adding a new section for the recent changes
    new_entry = """
## Updates - 2025-05-22 (Calculated Jet Velocity & Diameter)
- **Jet Velocity ($U_j$):** Updated in `dm02`, `dm03`, and `dm04` catalogs.
  - Formula: $U_j = \\sqrt{\\frac{2\\gamma RT_0}{\\gamma-1} (1 - NPR^{-\\frac{\\gamma-1}{\\gamma}})}$
  - Constants: $\\gamma=1.4$, $R=287$ J/(kg·K), $T_0=295$ K.
  - Provenance: Calculated from selected nominal NPR using MATLAB cold jet model.
  - Values range from $\\approx 449.4$ m/s (NPR 4.3) to $\\approx 565.0$ m/s (NPR 15).
- **Equivalent Diameter ($D_{eq}$):** Added $D_{eq} \\approx 29$mm as an approximate value across all catalogs.
- **UI Footers:** Updated `js/dm02-explorer.js` and `js/dm04-spectra.js` to explicitly label these as "calculated" and not "measured".
- **Layout:** Verified `css/dm04-spectra.css` for centered layout (max-width 1280px, responsive iframe).
"""
    with open(review_file, 'a') as f:
        f.write(new_entry)
    print(f"Updated {review_file}")
else:
    print(f"{review_file} not found.")

import re

with open('/Users/yoyo/01_Code/My-website/DataStream.html', 'r') as f:
    content = f.read()

# 1. Update CSS
# Remove the :first-child rule and add the new utility classes
css_to_remove = """
        /* Constrain the heated jet figure as it is too large */
        .analysis-figures-container figure.blog-image:first-child {
            max-width: 800px;
        }"""
css_to_add = """
        .analysis-media-wide {
            width: 100%;
            margin: 0 auto;
        }

        .analysis-media-compact {
            max-width: 600px !important;
            width: 100%;
            height: auto;
            margin: 0 auto;
            display: block;
            text-align: center;
        }"""
content = content.replace(css_to_remove, css_to_add)

# 2. Replace the "Additional 2D Analyses" section
# Find the start of the section and the start of the footer
section_start_text = '<section class="blog-detail pt-100 pb-100">\n    <div class="container"><div class="row"><div class="col-lg-8 offset-lg-2">\n                        <div class="blog-content">\n                            <div class="blog-heading mt-50" style="border-top: 1px solid #eee; padding-top: 30px;">'
footer_start_text = '<!--Footer Start-->'

# We want to replace the block between the start of the "Additional 2D Analyses" section and the footer.
# Since there are multiple blog-detail sections, we find the one containing "Additional 2D Analyses".
search_text = 'Additional 2D Analyses'
search_index = content.find(search_text)
section_start_index = content.rfind('<section class="blog-detail pt-100 pb-100">', 0, search_index)
footer_index = content.find(footer_start_text)

# The replacement HTML:
replacement_html = """
        <section class="blog-detail pt-100 pb-100">
    <div class="container">
        <!-- Heading and Intro (Centered Standard) -->
        <div class="row">
            <div class="col-lg-8 offset-lg-2">
                <div class="blog-content">
                    <div class="blog-heading mt-50" style="border-top: 1px solid #eee; padding-top: 30px;">
                        <h2 class="text-center">Additional 2D Analyses</h2>
                        <p class="text-center">Below are comparative power spectra and parameter sweeps.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Wide Plotly Iframe (Centered Wide) -->
        <div class="row">
            <div class="col-lg-10 offset-lg-1">
                <div class="plotly_centering analysis-media-wide">
                    <iframe src="media/Plots/AR4 M1p44 Rectangular NPR 4p4 vs AR2 M2 Rectangular&Diamond NPR10.html" name="iframe_2D" scrolling="no" frameborder="0" style="width: 100%; height: clamp(400px, 80vh, 900px);"></iframe>
                </div>
            </div>
        </div>

        <!-- Links List (Centered Standard) -->
        <div class="row">
            <div class="col-lg-8 offset-lg-2">
                <ul class="mt-30" style="list-style: none; padding: 0; text-align: center;">
                    <li class="mb-2"><a href="media/Plots/Rectangular_M1p44_AR4_NPR4p4_Spectra.html" target="iframe_2D" style="color:#9A2A2A;">Power spectra of M1.44 AR4 Rectangular nozzle @ NPR4.4</a></li>
                    <li class="mb-2"><a href="media/Plots/Spectra_Diam_vs_Rect_NPR4p8_MajorMinor.html" target="iframe_2D" style="color:#9A2A2A;">Power spectra of M2 AR2 Diamond vs. Rectangular nozzle @ NPR4.8</a></li>
                    <li class="mb-2"><a href="media/Plots/plotly OASPLvsNPR.html" target="iframe_2D" style="color:#9A2A2A;">NPR parameter sweep of M1.44 AR4 Rectangular nozzle</a></li>
                </ul>
            </div>
        </div>

        <!-- Figures (Mixed Sizing) -->
        <div class="row">
            <div class="col-lg-10 offset-lg-1">
                <div class="analysis-figures-container">
                    <!-- Compact Figure: Heated Jet -->
                    <figure class="blog-image analysis-media-compact">
                        <img src="media/images/blog/Project Y/NPR4p3_AcousticSurface-1.png" alt="" loading="lazy">
                        <figcaption>Acoustic surface of heated jet at 900 K and a pressure ratio of 4.3 atmospheres.</figcaption>
                    </figure>

                    <!-- Wide Figure: Diamond Jet -->
                    <figure class="blog-image analysis-media-wide">
                        <img src="media/images/blog/Project Y/DiamondJet.png" alt="" loading="lazy">
                        <figcaption>Volumetric, averaged velocity field of supersonic diamond jet at NPR 4.3. The high speed core and low speed shear layer are highlighted in this figure.</figcaption>
                    </figure>
                </div>
            </div>
        </div>
    </div>
</section>
"""

content = content[:section_start_index] + replacement_html + content[footer_index:]

with open('/Users/yoyo/01_Code/My-website/DataStream.html', 'w') as f:
    f.write(content)

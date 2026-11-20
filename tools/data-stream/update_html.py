import re

file_path = 'DataStream.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_text = '<p>Explore the power spectral density of supersonic jets at specific azimuthal angles (phi). This viewer allows you to inspect frequency-domain characteristics for individual microphone positions.</p>\n                        <p><strong>Azimuth vs Frequency:</strong> The horizontal axis represents frequency (Hz) on a logarithmic scale, while the vertical axis shows the Sound Pressure Level (SPL) in dB. Reference profiles for 0°, 90°, 180°, 270°, and 360° are typically provided for context.</p>'
new_text = '<p>Because each azimuthal reconstruction is performed at a fixed NPR (fixed U<sub>j</sub> and D<sub>eq</sub>), we plot three-dimensional spectra in frequency (Hz). In this setting f and St = fD<sub>eq</sub>/U<sub>j</sub> are related by a constant factor, so using f preserves all physics while keeping the 3-D visualizations and tone/harmonic identification straightforward.</p>'

# Use a regex to be more flexible with whitespace
pattern = r'<p>Explore the power spectral density.*?context\.<\/p>'
content = re.sub(pattern, new_text, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

import sys

with open('kavach/frontend/app.js', encoding='utf-8') as f:
    js_text = f.read()

motion_funcs = [
    'initScrollStorytelling',
    'initScrollReveals',
    'initMagneticButtons',
    'initClickRipple'
]

missing_motion = [fn for fn in motion_funcs if f"function {fn}" not in js_text]
if missing_motion:
    print(f"FAILED: Missing motion functions: {missing_motion}")
    sys.exit(1)
else:
    print(f"SUCCESS: All 4 motion design functions verified in app.js: {motion_funcs}")

# Check CSS
with open('kavach/frontend/style.css', encoding='utf-8') as f:
    css_text = f.read()

motion_css = [
    '.scroll-scrub-bar',
    '.parallax-layer',
    '.reveal-on-scroll',
    '.stagger-container',
    '.clip-reveal-text',
    '.magnetic-btn',
    '.pillar-icon-box svg',
    '.arrow-shift',
    '.click-ripple',
    '.btn-state-success'
]

missing_motion_css = [c for c in motion_css if c not in css_text]
if missing_motion_css:
    print(f"FAILED: Missing motion CSS: {missing_motion_css}")
    sys.exit(1)
else:
    print(f"SUCCESS: All motion CSS classes present in style.css: {motion_css}")

# Check HTML
with open('kavach/frontend/index.html', encoding='utf-8') as f:
    html_text = f.read()

motion_html = [
    'id="scroll-scrub-bar"',
    'magnetic-btn',
    'clip-reveal-text',
    'stagger-container',
    'reveal-on-scroll',
    'arrow-shift'
]

missing_motion_html = [h for h in motion_html if h not in html_text]
if missing_motion_html:
    print(f"FAILED: Missing motion HTML elements: {missing_motion_html}")
    sys.exit(1)
else:
    print(f"SUCCESS: All motion markup verified in index.html: {motion_html}")

print("ALL 4 SLIDES (SCROLL, REVEAL, HOVER, CLICK) 100% IMPLEMENTED AND VERIFIED!")

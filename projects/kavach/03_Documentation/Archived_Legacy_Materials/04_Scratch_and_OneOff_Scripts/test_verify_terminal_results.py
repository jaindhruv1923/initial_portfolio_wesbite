import sys

# 1. Check index.html
with open('kavach/frontend/index.html', encoding='utf-8') as f:
    html = f.read()

required_html = [
    'id="terminal-results-section"',
    'id="btn-run-term-verification"',
    'id="tab-btn-master"',
    'id="tab-btn-pytest"',
    'id="tab-btn-cigate"',
    'id="tab-btn-cyber"',
    'id="tab-btn-cliscanner"',
    'id="tab-btn-runs"',
    'id="term-search-input"',
    'id="cli-terminal-screen"',
    'id="term-inspector-drawer"',
    'id="cli-simulator-container"',
    'Empirical CLI &amp; Terminal Verification Suite'
]

missing_html = [h for h in required_html if h not in html]
if missing_html:
    print(f"FAILED index.html missing: {missing_html}")
    sys.exit(1)
print(f"SUCCESS: All {len(required_html)} required HTML elements present in index.html")

# 2. Check app.js
with open('kavach/frontend/app.js', encoding='utf-8') as f:
    js = f.read()

required_js_funcs = [
    'initTerminalMissionControl',
    'switchTerminalTab',
    'renderTerminalScreen',
    'filterTerminalRows',
    'setTerminalFilter',
    'toggleRawTerminalLog',
    'selectTerminalCheck',
    'loadCliPromptPreset',
    'executeCliSimulation',
    'runLiveTerminalVerification',
    'copyTerminalLogs',
    'downloadRawTerminalLogs',
    'resetTerminalView'
]

missing_js = [fn for fn in required_js_funcs if f"function {fn}" not in js]
if missing_js:
    print(f"FAILED app.js missing functions: {missing_js}")
    sys.exit(1)
print(f"SUCCESS: All {len(required_js_funcs)} required JS functions present in app.js")

required_window_exports = [
    'window.switchTerminalTab',
    'window.runLiveTerminalVerification',
    'window.copyTerminalLogs',
    'window.downloadRawTerminalLogs',
    'window.resetTerminalView',
    'window.filterTerminalRows',
    'window.setTerminalFilter',
    'window.toggleRawTerminalLog',
    'window.selectTerminalCheck',
    'window.loadCliPromptPreset',
    'window.executeCliSimulation',
    'window.initTerminalMissionControl'
]

missing_exports = [exp for exp in required_window_exports if exp not in js]
if missing_exports:
    print(f"FAILED app.js missing window exports: {missing_exports}")
    sys.exit(1)
print(f"SUCCESS: All {len(required_window_exports)} window exports present in app.js")

# 3. Check style.css
with open('kavach/frontend/style.css', encoding='utf-8') as f:
    css = f.read()

required_css_classes = [
    '#terminal-results-section',
    '.term-hud-strip',
    '.term-hud-card',
    '.terminal-mission-control',
    '.terminal-window-header',
    '.term-btn',
    '.terminal-tabs-strip',
    '.term-tab',
    '.terminal-toolbar-bar',
    '.term-search-input',
    '.terminal-screen-wrapper',
    '.term-row',
    '.term-status-badge',
    '.term-diagnostic-box',
    '.terminal-inspector-drawer',
    '.cli-simulator-box',
    '.cli-stepper-bar',
    '.runs-table'
]

missing_css = [c for c in required_css_classes if c not in css]
if missing_css:
    print(f"FAILED style.css missing classes: {missing_css}")
    sys.exit(1)
print(f"SUCCESS: All {len(required_css_classes)} required CSS classes present in style.css")

print("\n[SUCCESS] ALL TERMINAL & CLI MISSION CONTROL VALIDATIONS 100% PASSED!")

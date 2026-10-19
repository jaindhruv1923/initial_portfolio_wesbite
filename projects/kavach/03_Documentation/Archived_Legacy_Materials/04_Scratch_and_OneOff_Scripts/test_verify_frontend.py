import sys

with open('kavach/frontend/app.js', encoding='utf-8') as f:
    js_text = f.read()

# Verify key functions exist in app.js
required_funcs = [
    'renderFlowchartNodes',
    'selectFlowchartStep',
    'toggleFlowchartSimulation',
    'stepFlowchartSimulation',
    'resetFlowchartSimulation',
    'updateFlowchartTelemetry',
    'renderFlowchartInspector',
    'loadCustomExploitPreset',
    'analyzeCustomExploitLive',
    'clearCustomExploitInput',
    'resetCustomExploitOutput',
    'selectAttackScenario',
    'runAttackSimulation'
]

missing = [fn for fn in required_funcs if f"function {fn}" not in js_text]
if missing:
    print(f"FAILED: Missing functions: {missing}")
    sys.exit(1)
else:
    print(f"SUCCESS: All {len(required_funcs)} core functions present in app.js")

# Verify window exports
window_exports = [
    'window.selectFlowchartStep',
    'window.toggleFlowchartSimulation',
    'window.stepFlowchartSimulation',
    'window.resetFlowchartSimulation',
    'window.renderFlowchartNodes',
    'window.clearCustomExploitInput',
    'window.loadCustomExploitPreset',
    'window.analyzeCustomExploitLive'
]

missing_exports = [exp for exp in window_exports if exp not in js_text]
if missing_exports:
    print(f"FAILED: Missing window exports: {missing_exports}")
    sys.exit(1)
else:
    print("SUCCESS: All window exports present!")

# Check CSS rules
with open('kavach/frontend/style.css', encoding='utf-8') as f:
    css_text = f.read()

required_css = [
    '.flowchart-controls-bar',
    '.flow-status-pill',
    '.flow-pulse-dot',
    '.btn-flow-primary',
    '.btn-flow-secondary',
    '.flow-telemetry-badge',
    '.flow-progress-track',
    '.flow-progress-fill',
    '.flow-node.completed',
    '.flow-node.active',
    '.flow-node-latency-pill',
    '.flow-node-footer',
    '.defense-stepper',
    '.defense-sim-grid',
    '.defense-sim-col',
    '.sim-pane-header',
    '@keyframes viewFadeIn'
]

missing_css = [c for c in required_css if c not in css_text]
if missing_css:
    print(f"FAILED: Missing CSS classes: {missing_css}")
    sys.exit(1)
else:
    print(f"SUCCESS: All {len(required_css)} required CSS selectors and animations verified in style.css!")

print("ALL FRONTEND VALIDATIONS PASSED!")

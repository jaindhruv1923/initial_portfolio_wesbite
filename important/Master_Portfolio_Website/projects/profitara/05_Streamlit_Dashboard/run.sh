#!/bin/bash
# ─────────────────────────────────────────────────────────────────
#  PROFITARA GOLDEN — One-Click Launcher
#  Run this script from the profitara_streamlit/ folder
# ─────────────────────────────────────────────────────────────────

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PROFITARA GOLDEN — Retail Intelligence Platform"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q
echo "✅ Dependencies ready"
echo ""
echo "🚀 Launching dashboard at http://localhost:8501"
echo "   Press Ctrl+C to stop"
echo ""
streamlit run app.py --server.port 8501 --server.headless false

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def print_nb(path):
    print('='*70)
    print('FILE:', path)
    print('='*70)
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    print(f"Total cells: {len(nb['cells'])}")
    for idx, c in enumerate(nb['cells']):
        t = c['cell_type']
        s = ''.join(c['source']).strip()
        lines = [l for l in s.split('\n') if l.strip()]
        first = lines[0] if lines else ''
        print(f"Cell {idx:02d} [{t:8s}]: {first[:80]} (lines: {len(lines)})")
        if t == 'markdown':
            print("   >>> Content preview:")
            for l in lines[:3]:
                print(f"       {l[:100]}")
        elif t == 'code':
            print("   >>> Code preview:")
            for l in lines[:2]:
                print(f"       {l[:100]}")

print_nb('03_ML_Pipeline_and_Models/Naukri_Saaf_ML_Pipeline_v3_1_FINAL.ipynb')
print_nb('03_ML_Pipeline_and_Models/Naukri_Saaf_ML_Pipeline_v4_PRODUCTION.ipynb')

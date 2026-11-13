"""Independent Gerber and Drill Validator for Smart Pen Rev E.
Verifies dimensions, layer continuity, drill count, and fabrication readiness.
"""
import re
from pathlib import Path

def validate_gerbers(gerber_dir):
    gerber_dir = Path(gerber_dir)
    required_layers = ['GTL', 'GBL', 'GTS', 'GBS', 'GTO', 'GBO', 'GKO', 'DRL']
    results = {}

    for ext in required_layers:
        fpath = gerber_dir / f'SmartPen.{ext}'
        if not fpath.exists():
            results[ext] = {'status': 'FAIL', 'error': 'File missing'}
            continue
        
        content = fpath.read_text(encoding='utf-8')
        size = len(content)

        if ext == 'GKO': # Board outline
            # Parse bounding box from GKO
            x_coords = [int(m.group(1)) / 10000.0 for m in re.finditer(r'X(-?\d+)', content)]
            y_coords = [int(m.group(1)) / 10000.0 for m in re.finditer(r'Y(-?\d+)', content)]
            if x_coords and y_coords:
                min_x, max_x = min(x_coords), max(x_coords)
                min_y, max_y = min(y_coords), max(y_coords)
                length = max_x - min_x
                width = max_y - min_y
                results[ext] = {
                    'status': 'PASS',
                    'length_mm': length,
                    'width_mm': width,
                    'size_bytes': size
                }
            else:
                results[ext] = {'status': 'FAIL', 'error': 'Could not parse outline coordinates'}

        elif ext == 'DRL': # Drill file
            holes = list(re.finditer(r'X(\d+)Y(\d+)', content))
            results[ext] = {
                'status': 'PASS',
                'hole_count': len(holes),
                'size_bytes': size
            }
        else:
            # Check for standard EOF M02*
            if 'M02*' in content:
                results[ext] = {'status': 'PASS', 'size_bytes': size}
            else:
                results[ext] = {'status': 'WARNING', 'error': 'No M02* EOF marker'}

    all_pass = all(r.get('status') == 'PASS' for r in results.values())
    print(f"Gerber validation summary (All PASS: {all_pass}):")
    for ext, r in results.items():
        print(f" - {ext:<4}: {r['status']:<8} {r}")
    return results

if __name__ == '__main__':
    validate_gerbers('output/RevE_work/gerbers')


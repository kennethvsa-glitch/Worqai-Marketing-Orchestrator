#!/usr/bin/env python3
"""Final audit — corrected to ignore comments."""

from pathlib import Path

base_dirs = [
    Path('C:/Users/kenne/OneDrive/Documentos/worqai-marketing/production/Carousels to remake/priority 1/batch 3/reframed/Approved/Approved of approved'),
    Path('C:/Users/kenne/OneDrive/Documentos/worqai-marketing/production/Carousels to remake/priority 1/batch 3/reframed/Approved'),
]

results = []
for base_dir in base_dirs:
    if not base_dir.exists(): continue
    for f in sorted(base_dir.glob('*.html')):
        content = f.read_text(encoding='utf-8')
        issues = []

        if '<script>' not in content: issues.append('MISSING_SCRIPT')
        if 'function go(' not in content: issues.append('MISSING_GO')
        if 'nodeType' not in content: issues.append('MISSING_NODETYPE')
        if '.glass-tag' not in content: issues.append('MISSING_GLASS_TAG')
        if 'contentEditable' not in content: issues.append('MISSING_CONTENTEDITABLE')
        if 'data-movable' not in content: issues.append('MISSING_MOVABLE')
        if 'dataset.movable' not in content: issues.append('MISSING_DATASET_MOVABLE')
        if "style.position='relative'" not in content: issues.append('MISSING_JS_POSITION')
        if "style.cursor='move'" not in content: issues.append('MISSING_JS_CURSOR')
        if 'dataset.dx' not in content: issues.append('MISSING_DATA_DX')
        if 'dataset.dy' not in content: issues.append('MISSING_DATA_DY')
        if 'restoreOffsets' not in content or 'restoreOffsets()' not in content: issues.append('MISSING_RESTORE')
        if 'getBoundingClientRect' not in content: issues.append('MISSING_SCALE')
        if 'touchend' not in content: issues.append('MISSING_TOUCH')
        if 'ArrowRight' not in content or 'ArrowLeft' not in content: issues.append('MISSING_KEYBOARD')
        if 'isDragging' not in content: issues.append('MISSING_IS_DRAGGING')
        if 'pointer-events:none' not in content: issues.append('MISSING_DRAG_DISABLE')
        
        # Check e.preventDefault() is ONLY in slide path, not box path
        md_start = content.find('wrap.addEventListener')
        slide_start = content.find('slideDrag=true')
        if md_start > 0 and slide_start > md_start:
            box_path = content[md_start:slide_start]
            # Remove comments before checking
            lines = box_path.split('\n')
            code_only = '\n'.join(l for l in lines if not l.strip().startswith('//'))
            if 'e.preventDefault()' in code_only:
                issues.append('BOX_PATH_HAS_PREVENT_DEFAULT')
        
        status = 'PASS' if not issues else 'FAIL'
        results.append({'file': f.name, 'dir': base_dir.name, 'status': status, 'issues': issues, 'count': len(issues)})

total = len(results)
passed = sum(1 for r in results if r['status'] == 'PASS')
failed = total - passed

print('=' * 70)
print('QUANTUM V4 EDITOR AUDIT — FINAL (Comments Ignored)')
print('=' * 70)
print(f'Total: {total} | PASS: {passed} | FAIL: {failed}')
print()

if failed > 0:
    for r in results:
        if r['status'] == 'FAIL':
            print(f'[FAIL] {r["file"]} ({r["dir"]}) — {r["count"]} issues:')
            for issue in r['issues']:
                print(f'  X {issue}')
    print()

from collections import Counter
all_issues = [i for r in results for i in r['issues']]
if all_issues:
    print('Issue frequency:')
    for issue, count in Counter(all_issues).most_common():
        print(f'  {count}x {issue}')
    print()

print('=' * 70)
print('AUDIT COMPLETE')
print('=' * 70)

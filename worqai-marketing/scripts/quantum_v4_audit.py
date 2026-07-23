#!/usr/bin/env python3
"""
Quantum V4 Editor Audit — Corrected version for post-fix verification.
"""

import re
from pathlib import Path

base_dirs = [
    Path('C:/Users/kenne/OneDrive/Documentos/worqai-marketing/production/Carousels to remake/priority 1/batch 3/reframed/Approved/Approved of approved'),
    Path('C:/Users/kenne/OneDrive/Documentos/worqai-marketing/production/Carousels to remake/priority 1/batch 3/reframed/Approved'),
]

checks = {
    'has_script_block': 'Has <script> block',
    'has_go_function': 'Has go() navigation function',
    'has_slide_drag': 'Has slide-level drag handler',
    'has_element_drag': 'Has element-level drag (findContainer)',
    'has_contenteditable': 'Sets contentEditable=true on text elements',
    'has_editor_css': 'Has editor CSS (data-editable styles)',
    'has_scale_factor': 'Has scale factor for preview scaling',
    'has_drag_vs_click': 'Has isBoxDragging / drag-vs-click distinction',
    'has_position_save': 'Saves drag position via data-dx/data-dy',
    'has_restore_offsets': 'Has restoreOffsets() for saved positions',
    'has_touchend_nav': 'Has touch navigation (mobile)',
    'has_keyboard_nav': 'Has keyboard arrow navigation',
    'no_preventDefault_on_box_click': 'NO preventDefault on box mousedown (edit works)',
    'has_preventDefault_on_slide_drag': 'Has preventDefault on slide drag',
    'has_container_drag': 'findContainer returns boxes not text',
}

results = []
all_pass = True

for base_dir in base_dirs:
    if not base_dir.exists():
        print(f'DIR NOT FOUND: {base_dir}')
        continue
    for f in sorted(base_dir.glob('*.html')):
        content = f.read_text(encoding='utf-8')
        issues = []

        if '<script>' not in content or '</script>' not in content:
            issues.append('MISSING_SCRIPT_BLOCK')
        if 'function go(' not in content:
            issues.append('MISSING_GO_FUNCTION')
        if 'slideDrag=true' not in content and 'slideDrag = true' not in content:
            issues.append('MISSING_SLIDE_DRAG')
        if 'findContainer' not in content:
            issues.append('MISSING_FIND_CONTAINER')
        if 'DRAGGABLE_CONTAINERS' not in content:
            issues.append('MISSING_DRAGGABLE_CONTAINERS')
        if "contentEditable='true'" not in content and 'contentEditable="true"' not in content:
            issues.append('MISSING_CONTENTEDITABLE')
        if 'editableSelectors' not in content:
            issues.append('MISSING_EDITABLE_SELECTORS')
        if '/* === EDITOR:' not in content:
            issues.append('MISSING_EDITOR_CSS')
        if 'rect.width' not in content and 'getBoundingClientRect' not in content:
            issues.append('SCALE_FACTOR_NO_RECT')
        if 'isBoxDragging' not in content:
            issues.append('MISSING_IS_BOX_DRAGGING')
        if 'data-dx' not in content or 'data-dy' not in content:
            issues.append('MISSING_POSITION_SAVE')
        if 'dataset.dx' not in content:
            issues.append('DX_DATASET_NOT_USED')
        if 'restoreOffsets' not in content:
            issues.append('MISSING_RESTORE_OFFSETS')
        if 'restoreOffsets()' not in content:
            issues.append('RESTORE_NOT_CALLED')
        if 'touchend' not in content:
            issues.append('MISSING_TOUCH_NAV')
        if 'ArrowRight' not in content or 'ArrowLeft' not in content:
            issues.append('MISSING_KEYBOARD_NAV')

        # CRITICAL: No preventDefault on box mousedown (lines before slideDrag)
        mousedown_section = content[content.find('wrap.addEventListener(\'mousedown\'):'):]
        if 'wrap.addEventListener(\'mousedown\',function(e){' in content or 'wrap.addEventListener("mousedown",function(e){' in content:
            # Find the mousedown handler and check if it has preventDefault inside the box path
            box_section = content[content.find('const box=findContainer(e.target);'):content.find('slideDrag=true')]
            if 'preventDefault' in box_section:
                issues.append('BOX_CLICK_PREVENTS_EDIT')

        # Must have preventDefault in slide drag section
        slide_section = content[content.find('slideDrag=true'):content.find('document.addEventListener(\'mousemove\'')]
        if 'preventDefault' not in slide_section and 'e.preventDefault()' not in slide_section:
            issues.append('SLIDE_DRAG_NO_PREVENT_DEFAULT')

        # findContainer must return boxes, not text elements
        if 'el.matches(sel)' not in content and 'el.matches&&el.matches' not in content.replace(' ', ''):
            issues.append('CONTAINER_MATCHES_MISSING')

        # Check that data-dragging disables pointer events on child text
        if '[data-dragging="true"] [data-editable="true"]' not in content:
            issues.append('DRAG_NO_DISABLE_POINTER_EVENTS_ON_CHILDREN')

        pass_status = 'PASS' if not issues else 'FAIL'
        if issues:
            all_pass = False

        results.append({
            'file': f.name,
            'dir': base_dir.name,
            'status': pass_status,
            'issues': issues,
            'issue_count': len(issues)
        })

total = len(results)
passed = sum(1 for r in results if r['status'] == 'PASS')
failed = total - passed

all_issues = []
for r in results:
    all_issues.extend(r['issues'])
issue_counts = {}
for i in all_issues:
    issue_counts[i] = issue_counts.get(i, 0) + 1

report_lines = []
report_lines.append('=' * 70)
report_lines.append('QUANTUM V4 EDITOR AUDIT REPORT (Post-Fix)')
report_lines.append('Carousel Editor Functionality Deep Check')
report_lines.append('=' * 70)
report_lines.append('')
report_lines.append(f'Total files audited: {total}')
report_lines.append(f'PASS: {passed}')
report_lines.append(f'FAIL: {failed}')
report_lines.append('')

if failed > 0:
    report_lines.append('--- FAILED FILES ---')
    for r in results:
        if r['status'] == 'FAIL':
            report_lines.append('')
            report_lines.append(f'[FAIL] {r["file"]} ({r["dir"]}) - {r["issue_count"]} issues')
            for issue in r['issues']:
                report_lines.append(f'  X {issue}')
    report_lines.append('')

if issue_counts:
    report_lines.append('--- ISSUE FREQUENCY ---')
    for issue, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
        report_lines.append(f'  {count:2d}x {issue}')
    report_lines.append('')

report_lines.append('--- CHECKS PERFORMED ---')
for key, desc in checks.items():
    report_lines.append(f'  OK - {desc}')
report_lines.append('')
report_lines.append('=' * 70)
report_lines.append('AUDIT COMPLETE')
report_lines.append('=' * 70)

report = '\n'.join(report_lines)
print(report)

report_path = Path('C:/Users/kenne/OneDrive/Documentos/worqai-marketing/production/Carousels to remake/priority 1/batch 3/reframed/QUANTUM_V4_AUDIT_REPORT_V2.txt')
report_path.write_text(report, encoding='utf-8')
print(f'\nReport saved to: {report_path}')

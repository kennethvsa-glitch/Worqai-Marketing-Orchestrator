import re
from pathlib import Path

base = Path('production/Carousels to remake/priority 1/batch 3/reframed/Approved/Approved of approved')
files = list(base.glob('*.html'))

fixes_log = []

for f in files:
    content = f.read_text(encoding='utf-8')
    original = content
    file_fixes = []
    fname_lower = f.name.lower()
    
    # Determine theme from filename
    theme = 'dark'  # default
    if 'light' in fname_lower and 'dark' not in fname_lower:
        theme = 'light'
    elif 'darkblue' in fname_lower or 'dark-blue' in fname_lower:
        theme = 'darkblue'
    elif 'grey' in fname_lower or 'gray' in fname_lower:
        theme = 'grey'
    elif 'dark' in fname_lower and 'light' not in fname_lower:
        theme = 'dark'
    
    # Fix 1: Background colors to match theme
    if theme == 'light':
        # Fix dark backgrounds to light
        if 'background: #1a1a2e;' in content or 'background:#1a1a2e;' in content:
            content = content.replace('background: #1a1a2e;', 'background: #F5F5F5;')
            content = content.replace('background:#1a1a2e;', 'background:#F5F5F5;')
            file_fixes.append('background #1a1a2e -> #F5F5F5 (light theme)')
        if 'background: #0f172a;' in content or 'background:#0f172a;' in content:
            content = content.replace('background: #0f172a;', 'background: #F5F5F5;')
            content = content.replace('background:#0f172a;', 'background:#F5F5F5;')
            file_fixes.append('background #0f172a -> #F5F5F5 (light theme)')
        if 'background: #0A0A0A;' in content or 'background:#0A0A0A;' in content:
            content = content.replace('background: #0A0A0A;', 'background: #F5F5F5;')
            content = content.replace('background:#0A0A0A;', 'background:#F5F5F5;')
            file_fixes.append('background #0A0A0A -> #F5F5F5 (light theme)')
    elif theme == 'dark':
        # Fix light backgrounds to dark
        if 'background: #F5F5F5;' in content or 'background:#F5F5F5;' in content:
            content = content.replace('background: #F5F5F5;', 'background: #0A0A0A;')
            content = content.replace('background:#F5F5F5;', 'background:#0A0A0A;')
            file_fixes.append('background #F5F5F5 -> #0A0A0A (dark theme)')
        if 'background: #FAFAFA;' in content or 'background:#FAFAFA;' in content:
            # Only for html/body, not for slides with glass blocks
            content = content.replace('html,body{background: #FAFAFA;', 'html,body{background: #0A0A0A;')
            content = content.replace('html,body{background:#FAFAFA;', 'html,body{background:#0A0A0A;')
            content = content.replace('background: #FAFAFA; font-family', 'background: #0A0A0A; font-family')
            file_fixes.append('background #FAFAFA -> #0A0A0A (dark theme)')
    
    # Fix 2: Counter transparency - make solid colors
    # Light theme: rgba(10,10,10,0.2) -> #0A0A0A, rgba(10,10,10,0.35) -> #0A0A0A
    # Dark theme: rgba(255,255,255,0.2) -> #FAFAFA, rgba(255,255,255,0.35) -> #FAFAFA
    if theme == 'light':
        if 'rgba(10,10,10,0.2)' in content:
            content = content.replace('rgba(10,10,10,0.2)', '#0A0A0A')
            file_fixes.append('counter rgba(10,10,10,0.2) -> #0A0A0A (solid)')
        if 'rgba(10,10,10,0.35)' in content:
            content = content.replace('rgba(10,10,10,0.35)', '#0A0A0A')
            file_fixes.append('counter rgba(10,10,10,0.35) -> #0A0A0A (solid)')
        if 'rgba(10,10,10,0.45)' in content:
            content = content.replace('rgba(10,10,10,0.45)', '#0A0A0A')
            file_fixes.append('counter rgba(10,10,10,0.45) -> #0A0A0A (solid)')
    elif theme == 'dark':
        if 'rgba(255,255,255,0.2)' in content:
            content = content.replace('rgba(255,255,255,0.2)', '#FAFAFA')
            file_fixes.append('counter rgba(255,255,255,0.2) -> #FAFAFA (solid)')
        if 'rgba(255,255,255,0.35)' in content:
            content = content.replace('rgba(255,255,255,0.35)', '#FAFAFA')
            file_fixes.append('counter rgba(255,255,255,0.35) -> #FAFAFA (solid)')
        if 'rgba(255,255,255,0.45)' in content:
            content = content.replace('rgba(255,255,255,0.45)', '#FAFAFA')
            file_fixes.append('counter rgba(255,255,255,0.45) -> #FAFAFA (solid)')
    
    # Fix 3: Source tag opacity - bump to 1.0
    if 'opacity:0.45' in content or 'opacity: 0.45' in content:
        content = content.replace('opacity:0.45', 'opacity:1.0')
        content = content.replace('opacity: 0.45', 'opacity: 1.0')
        file_fixes.append('source-tag opacity 0.45 -> 1.0')
    if 'opacity:0.40' in content or 'opacity: 0.40' in content:
        content = content.replace('opacity:0.40', 'opacity:1.0')
        content = content.replace('opacity: 0.40', 'opacity: 1.0')
        file_fixes.append('source-tag opacity 0.40 -> 1.0')
    
    if content != original:
        f.write_text(content, encoding='utf-8')
    
    if file_fixes:
        fixes_log.append(f.name + ' (' + theme + '):')
        for fix in file_fixes:
            fixes_log.append('  - ' + fix)

print('=== AoA CSS FIXES ===')
print('Files scanned: ' + str(len(files)))
files_changed = len([x for x in fixes_log if not x.startswith('  -')])
print('Files with fixes: ' + str(files_changed))
print()
for line in fixes_log:
    print(line)

# Save log
log_path = base / 'CSS_FIX_LOG_AOA.txt'
log_path.write_text('\n'.join(fixes_log), encoding='utf-8')
print('\nLog saved to: ' + str(log_path))

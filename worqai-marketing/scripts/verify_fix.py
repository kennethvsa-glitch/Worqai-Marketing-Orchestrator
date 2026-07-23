from pathlib import Path

f = Path('C:/Users/kenne/OneDrive/Documentos/worqai-marketing/production/Carousels to remake/priority 1/batch 3/reframed/Approved/Approved of approved/TEST_background-carousel_worqai-lime.html')
content = f.read_text(encoding='utf-8')

print('nodeType check:', 'nodeType!==1' in content or 'nodeType !== 1' in content)
# Find editable selectors line
if 'EDITABLE_SELECTORS' in content:
    sel_line = content.split('EDITABLE_SELECTORS')[1].split("'")[0]
    print('glass-tag in editable:', '.glass-tag' in sel_line)
else:
    print('EDITABLE_SELECTORS not found')
print('movable dataset:', 'data-movable' in content)
print('dataset.movable:', 'dataset.movable' in content)
print('no preventDefault in drag path:', 'DO NOT preventDefault' in content)
print('has preventDefault in slide:', 'preventDefault' in content.split('slideDrag=true')[1].split('document.addEventListener')[0] if 'slideDrag=true' in content else False)
print('position relative via JS:', "style.position='relative'" in content)
print('cursor move:', "style.cursor='move'" in content)
print('data-dx save:', 'dataset.dx=elStartX+dx' in content.replace(' ',''))
print('data-dy save:', 'dataset.dy=elStartY+dy' in content.replace(' ',''))

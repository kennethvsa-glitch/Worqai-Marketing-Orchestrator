#!/usr/bin/env python3
"""
Quantum V4 Editor Fix v3 — Corrects drag-vs-edit interaction in all carousel files.
Key fixes:
1. Handle text nodes in findDraggable (e.target can be a text node)
2. Make individual elements draggable (not just containers)
3. Add .glass-tag to editable selectors
4. Make all text elements editable, including those inside glass-blocks
5. Robust drag-vs-click with no preventDefault on mousedown
"""

import re
from pathlib import Path

base_dirs = [
    Path('C:/Users/kenne/OneDrive/Documentos/worqai-marketing/production/Carousels to remake/priority 1/batch 3/reframed/Approved/Approved of approved'),
    Path('C:/Users/kenne/OneDrive/Documentos/worqai-marketing/production/Carousels to remake/priority 1/batch 3/reframed/Approved'),
]

new_script = r'''<script>
let cur=0;
const slides=document.querySelectorAll('.slide');
const track=document.getElementById('track');
const prevBtn=document.getElementById('prev');
const nextBtn=document.getElementById('next');
const dots=document.querySelectorAll('.dot');
const wrap=document.getElementById('wrap');

function go(n){
  cur=Math.max(0,Math.min(n,slides.length-1));
  track.style.transform='translateX(-'+cur*1080+'px)';
  dots.forEach((d,i)=>d.classList.toggle('on',i===cur));
  if(prevBtn) prevBtn.disabled=cur===0;
  if(nextBtn) nextBtn.disabled=cur===slides.length-1;
}
function move(d){go(cur+d);}
if(prevBtn) prevBtn.addEventListener('click',()=>move(-1));
if(nextBtn) nextBtn.addEventListener('click',()=>move(1));

// --- ELEMENT EDITOR: make ALL text elements editable + draggable ---
const EDITABLE_SELECTORS='.headline,.body-text,.glass-text,.glass-tag,.stat-context,.stat-ctx,.proof-stmt,.proof-ctx,.cta-headline-out,.cta-headline-above,.cta-offer,.cta-fine,.cta-closing,.cta-micro,.url-text,.hook-display,.hook-sub,.label,.lime-badge,.pill-tag,.source-tag,.src,.site-url,.counter,.brand-anchor,.proof-city,.proof-metric,.deco-num,.cta-headline';
document.querySelectorAll(EDITABLE_SELECTORS).forEach(el=>{
  el.contentEditable='true';
  el.dataset.editable='true';
  el.dataset.movable='true';
  el.style.position='relative';
  el.style.cursor='move';
  el.title='Click to edit. Drag to move.';
});

// Also make glass-blocks, cta-cards, hook-stacks draggable as units
const CONTAINER_SELECTORS='.glass-block,.cta-card,.hook-stack,.content,.swipe-pill,.url-box,.pill-tag';
document.querySelectorAll(CONTAINER_SELECTORS).forEach(el=>{
  el.dataset.movable='true';
  el.style.position='relative';
  el.style.cursor='move';
});

// --- FIND DRAGGABLE ELEMENT (handle text nodes) ---
function findDraggable(el){
  // If text node, get parent element first
  if(el && el.nodeType!==1) el=el.parentElement;
  while(el && el!==document.body && !el.classList.contains('wrap')){
    if(el.dataset && el.dataset.movable==='true') return el;
    el=el.parentElement;
  }
  return null;
}

// --- RESTORE SAVED POSITIONS ---
function restoreOffsets(){
  document.querySelectorAll('[data-dx]').forEach(el=>{
    const dx=parseFloat(el.dataset.dx||0);
    const dy=parseFloat(el.dataset.dy||0);
    if(dx||dy) el.style.transform='translate('+dx+'px,'+dy+'px)';
  });
}
restoreOffsets();

// --- UNIFIED DRAG: element vs slide ---
let dragEl=null, dragStartX=0, dragStartY=0, elStartX=0, elStartY=0;
let isDragging=false;
let slideDrag=false, slideDragStartX=0, slideStartTrans=0, slideScale=1;

wrap.addEventListener('mousedown',function(e){
  // 1. Try to find a draggable element or container
  const el=findDraggable(e.target);
  if(el){
    dragEl=el;
    dragStartX=e.clientX;
    dragStartY=e.clientY;
    isDragging=false;
    elStartX=parseFloat(dragEl.dataset.dx||0);
    elStartY=parseFloat(dragEl.dataset.dy||0);
    // DO NOT preventDefault — let browser place cursor for editing
    return;
  }
  // 2. Slide drag on empty background
  slideDrag=true;
  slideDragStartX=e.clientX;
  const cage=document.querySelector('.preview-cage');
  if(cage){
    const rect=cage.getBoundingClientRect();
    const w=parseFloat(getComputedStyle(cage).width);
    if(w>0) slideScale=rect.width/w;
  }
  slideStartTrans=-cur*1080;
  wrap.style.cursor='grabbing';
  track.style.transition='none';
  e.preventDefault();
});

document.addEventListener('mousemove',function(e){
  if(dragEl){
    const dx=e.clientX-dragStartX;
    const dy=e.clientY-dragStartY;
    if(!isDragging && (Math.abs(dx)>3||Math.abs(dy)>3)){
      isDragging=true;
      e.preventDefault(); // prevent text selection during drag
      dragEl.dataset.dragging='true';
      wrap.style.cursor='grabbing';
    }
    if(isDragging){
      dragEl.style.transform='translate('+(elStartX+dx)+'px,'+(elStartY+dy)+'px)';
    }
    return;
  }
  if(slideDrag){
    const dx=(e.clientX-slideDragStartX)/slideScale;
    track.style.transform='translateX('+(slideStartTrans+dx)+'px)';
  }
});

document.addEventListener('mouseup',function(e){
  if(dragEl){
    if(isDragging){
      const dx=e.clientX-dragStartX;
      const dy=e.clientY-dragStartY;
      dragEl.dataset.dx=elStartX+dx;
      dragEl.dataset.dy=elStartY+dy;
      delete dragEl.dataset.dragging;
    }
    dragEl=null;
    isDragging=false;
    wrap.style.cursor='grab';
    return;
  }
  if(slideDrag){
    const dx=(e.clientX-slideDragStartX)/slideScale;
    slideDrag=false;
    wrap.style.cursor='grab';
    track.style.transition='transform 0.42s cubic-bezier(0.4,0,0.2,1)';
    if(Math.abs(dx)>120) move(dx<0?1:-1);
    else go(cur);
  }
});

// --- TOUCH SWIPE (mobile) ---
let sx=0;
wrap.addEventListener('touchstart',e=>{sx=e.touches[0].clientX;},{passive:true});
wrap.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>40)move(dx<0?1:-1);});

// --- KEYBOARD NAV ---
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')move(1);if(e.key==='ArrowLeft')move(-1);});

wrap.style.cursor='grab';
go(0);
</script>'''

editor_css = '''
/* === EDITOR: draggable elements + editable text === */
[data-editable="true"],[data-movable="true"]{position:relative;cursor:move;}
[data-editable="true"]:hover,[data-movable="true"]:hover{outline:1px dashed rgba(199,255,58,0.35);outline-offset:2px;}
[data-editable="true"]:focus,[data-movable="true"]:focus{outline:2px solid #C7FF3A;outline-offset:2px;}
[data-dragging="true"]{outline:2px solid #FF8B70!important;outline-offset:3px!important;cursor:grabbing!important;z-index:100!important;}
[data-dragging="true"] [data-editable="true"]{pointer-events:none;}
'''

files_changed = 0
total = 0
for base_dir in base_dirs:
    if not base_dir.exists():
        continue
    for f in sorted(base_dir.glob('*.html')):
        total += 1
        content = f.read_text(encoding='utf-8')
        original = content

        # Replace script block
        script_match = re.search(r'<script>.*?</script>', content, re.DOTALL)
        if script_match:
            content = content[:script_match.start()] + new_script + content[script_match.end():]
        else:
            content = content.replace('</body>', new_script + '\n</body>')

        # Replace editor CSS
        if '/* === EDITOR:' in content:
            content = re.sub(r'/\* === EDITOR:.*?\*/', editor_css, content, flags=re.DOTALL)
        else:
            content = content.replace('</style>', editor_css + '</style>')

        if content != original:
            f.write_text(content, encoding='utf-8')
            files_changed += 1

print(f'Total files: {total}')
print(f'Files updated with corrected editor v3: {files_changed}')

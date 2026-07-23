#!/usr/bin/env python3
"""
Quantum V4 Editor Fix — Corrects drag-vs-edit interaction in all carousel files.
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

// --- ELEMENT EDITOR: make all text editable ---
const editableSelectors='.headline,.body-text,.glass-text,.stat-context,.stat-ctx,.proof-stmt,.proof-ctx,.cta-headline-out,.cta-headline-above,.cta-offer,.cta-fine,.cta-closing,.cta-micro,.url-text,.hook-display,.hook-sub,.label,.lime-badge,.pill-tag,.source-tag,.src,.site-url,.counter,.brand-anchor,.proof-city,.proof-metric,.deco-num,.cta-headline';
document.querySelectorAll(editableSelectors).forEach(el=>{
  el.contentEditable='true';
  el.dataset.editable='true';
  el.title='Click to edit. Drag the box border to move.';
});

// --- FIND DRAGGABLE CONTAINER (box, not text) ---
const DRAGGABLE_CONTAINERS=['.glass-block','.cta-card','.hook-stack','.content','.swipe-pill','.url-box','.pill-tag'];
function findContainer(el){
  while(el && el!==document.body && !el.classList.contains('wrap')){
    for(let sel of DRAGGABLE_CONTAINERS){
      if(el.matches && el.matches(sel)) return el;
    }
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

// --- UNIFIED DRAG: box vs slide ---
let dragBox=null, dragStartX=0, dragStartY=0, boxStartX=0, boxStartY=0;
let isBoxDragging=false;
let slideDrag=false, slideDragStartX=0, slideStartTrans=0, slideScale=1;

wrap.addEventListener('mousedown',function(e){
  // 1. Try to find a draggable container (box)
  const box=findContainer(e.target);
  if(box){
    dragBox=box;
    dragStartX=e.clientX;
    dragStartY=e.clientY;
    isBoxDragging=false;
    boxStartX=parseFloat(dragBox.dataset.dx||0);
    boxStartY=parseFloat(dragBox.dataset.dy||0);
    // DO NOT preventDefault here — let browser handle click for text editing
    return;
  }
  // 2. Slide drag (on empty background)
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
  if(dragBox){
    const dx=e.clientX-dragStartX;
    const dy=e.clientY-dragStartY;
    if(!isBoxDragging && (Math.abs(dx)>3||Math.abs(dy)>3)){
      isBoxDragging=true;
      e.preventDefault(); // now prevent text selection
      dragBox.dataset.dragging='true';
      wrap.style.cursor='grabbing';
    }
    if(isBoxDragging){
      dragBox.style.transform='translate('+(boxStartX+dx)+'px,'+(boxStartY+dy)+'px)';
    }
    return;
  }
  if(slideDrag){
    const dx=(e.clientX-slideDragStartX)/slideScale;
    track.style.transform='translateX('+(slideStartTrans+dx)+'px)';
  }
});

document.addEventListener('mouseup',function(e){
  if(dragBox){
    if(isBoxDragging){
      const dx=e.clientX-dragStartX;
      const dy=e.clientY-dragStartY;
      dragBox.dataset.dx=boxStartX+dx;
      dragBox.dataset.dy=boxStartY+dy;
      delete dragBox.dataset.dragging;
    }
    dragBox=null;
    isBoxDragging=false;
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

# Editor CSS (minimal, keep existing if present, add only what's needed)
editor_css_addition = '''
/* === EDITOR: draggable boxes + editable text === */
.glass-block,.cta-card,.hook-stack,.content,.swipe-pill,.url-box,.pill-tag{position:relative;}
[data-editable="true"]:hover{outline:1px dashed rgba(199,255,58,0.25);outline-offset:2px;}
[data-editable="true"]:focus{outline:2px solid #C7FF3A;outline-offset:2px;}
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

        # Replace existing <script> block
        script_match = re.search(r'<script>.*?</script>', content, re.DOTALL)
        if script_match:
            content = content[:script_match.start()] + new_script + content[script_match.end():]
        else:
            content = content.replace('</body>', new_script + '\n</body>')

        # Replace editor CSS block if present, or add it
        if '/* === EDITOR:' in content:
            # Remove old editor CSS block
            content = re.sub(r'/\* === EDITOR:.*?\*/', editor_css_addition, content, flags=re.DOTALL)
        else:
            content = content.replace('</style>', editor_css_addition + '</style>')

        if content != original:
            f.write_text(content, encoding='utf-8')
            files_changed += 1

print(f'Total files: {total}')
print(f'Files updated with corrected editor: {files_changed}')

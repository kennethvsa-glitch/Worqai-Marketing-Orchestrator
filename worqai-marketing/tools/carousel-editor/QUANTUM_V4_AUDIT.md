# Quantum-V4 Audit Report: Carousel Editor

## Critical Bugs Found

### 1. SELECTION-1: `preventDefault()` blocks text editing
**Line 757:** `e.preventDefault()` is called on EVERY mousedown inside a selectable element. This prevents the browser from placing the text cursor, making text editing impossible.

**Fix:** Only call `preventDefault()` when we actually start dragging (on mousemove > 3px threshold).

### 2. SELECTION-2: Text node `e.target` crashes silently
When clicking on text inside a div, `e.target` is a TEXT NODE, not an element. Text nodes don't have `.dataset`, `.classList`, or `.parentElement` (well, they do have parentNode but not parentElement). The `findEditable()` function will crash or fail silently.

**Fix:** Always normalize `e.target` to its parent element first.

### 3. SELECTION-3: No selectable attribute on all elements
The editor only finds elements with pre-existing classes (`glass-block`, `cta-card`, etc.). Any element without those classes is completely unselectable.

**Fix:** On load, add `data-editor-selectable` to ALL meaningful elements (divs, spans, h1-h6, p, etc.) so EVERYTHING is clickable.

### 4. SELECTION-4: Deselect doesn't clear parent UI state
The parent receives `selector: null` but the `selectElement()` function in parent checks `if (!info || !info.selector)` which returns early and doesn't update the UI to show "no selection" state.

**Fix:** Parent must properly handle null selection and clear the inspector.

### 5. PROPERTIES-1: Opacity slider doesn't update iframe
The `propOpacity` slider has `input` event but no mechanism to actually send the value to the iframe.

**Fix:** Wire ALL input events to send `postMessage` to iframe immediately.

### 6. PROPERTIES-2: No live preview of changes
When you change a color or opacity in the sidebar, the iframe doesn't update until you blur or press Enter.

**Fix:** All style inputs should send `postMessage` on both `input` (for live preview) and `change` (for undo checkpoint).

### 7. DRAG-1: Drag state conflicts with text selection
When dragging starts, the browser might still try to select text. The `user-select: none` CSS is not injected into the iframe during drag.

**Fix:** Inject `user-select: none` on `wrap` during active drag, remove on mouseup.

### 8. TEXT-EDIT-1: Double-click handler doesn't work
The dblclick handler sets `contentEditable = 'true'` but `e.preventDefault()` from mousedown already fired, which may prevent the dblclick from working.

**Fix:** Remove mousedown `preventDefault()`, use a click-vs-drag threshold instead.

### 9. EXPORT-1: Exported file includes editor artifacts
The export removes `.editor-selected` class but doesn't remove `data-editor-dx`, `data-editor-dy`, injected `<script>`, injected `<style>`, and `contenteditable` attributes.

**Fix:** Clean ALL editor artifacts on export.

### 10. LAYERS-1: Layer tree click doesn't select
The layer tree click handler sends `selectElement` message but the iframe message handler doesn't properly handle `selectElement` from parent to select and highlight.

**Fix:** Wire layer tree click through properly.

---

## Rebuild Plan

### Phase 1: Iframe Script (Clean Architecture)
- Mark ALL elements as `data-editor-selectable` on load
- Smart mousedown: normalize target, find selectable ancestor, select with lime outline
- Smart drag: track delta, only start drag after 4px movement
- NO preventDefault on mousedown
- Text edit: dblclick → contenteditable=true, blur → report change
- Property application: listen for parent `postMessage` to apply styles
- Export-ready: all modifications stored as inline styles/data attributes

### Phase 2: Parent UI (Full Control)
- Left sidebar: file drop, slide thumbs, layer tree (clickable)
- Right sidebar: ALL properties work instantly
  - Position X/Y (with drag handles)
  - Size (read-only display)
  - Opacity (0-100 slider, live preview)
  - Text color (color picker, live preview)
  - Background color (color picker, live preview)
  - Font size (slider + number input, live preview)
  - Font weight (dropdown, live preview)
  - Border radius (slider, live preview)
  - Z-index (number input, live preview)
  - Text content (textarea, live preview)
- Top toolbar: open, undo, redo, zoom, export
- Canvas: click empty = deselect, click element = select, drag = move

### Phase 3: Verification
- Test with actual carousel file
- Verify every property changes live
- Verify export is clean
- Verify undo/redo works

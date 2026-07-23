# Carousel Editor Tool — Design Plan

**Project:** worqai-marketing Carousel Editor  
**Location:** `C:/Users/kenne/OneDrive/Documentos/worqai-marketing/tools/carousel-editor/`  
**Date:** 2025-01-14  
**Version:** 1.0  
**Format:** Single HTML file (standalone, zero build step)

---

## 1. Executive Summary

Build a **standalone, browser-based Carousel Editor Tool** for editing worqai Instagram-style carousel HTML files. The tool opens any of the 52+ carousel HTML files, provides a visual editor for repositioning and restyling elements, supports inline text editing, and exports the modified HTML — all in a single `.html` file with no external build dependencies (icons via CDN only).

The editor runs entirely in the browser using an **iframe sandbox** for carousel preview, with **postMessage** bridging between the editor UI and the iframe content. All modifications are tracked in memory with full **undo/redo** support.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  EDITOR UI (parent window)                                  │
│  ┌──────────┬──────────────────────────┬──────────┐         │
│  │ LEFT     │     CENTER PREVIEW       │ RIGHT    │         │
│  │ SIDEBAR  │     ┌────────────┐       │ SIDEBAR  │         │
│  │ (files,  │     │  <iframe>  │       │(element  │         │
│  │  layers) │     │  sandbox   │       │ inspector│         │
│  │          │     │  1080x1080 │       │          │         │
│  │          │     │  scaled    │       │          │         │
│  └──────────┘     └────────────┘       └──────────┘         │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ BOTTOM STATUS BAR (coords, selected element, zoom %)    │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ TOP TOOLBAR (file, undo/redo, zoom, export, theme)      │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼ postMessage
              ┌─────────────────┐
              │ IFRAME (carousel│
              │  HTML loaded    │
              │  as blob URL)   │
              │                 │
              │  ┌───────────┐  │
              │  │ injected  │  │
              │  │ editor.js │  │
              │  │ (select,  │  │
              │  │  drag,    │  │
              │  │  edit)    │  │
              │  └───────────┘  │
              └─────────────────┘
```

### Core Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Iframe sandbox** | Isolates carousel CSS/JS from editor UI; prevents style conflicts; allows `contenteditable` and drag events without polluting editor |
| **postMessage bridge** | Secure cross-origin-like communication between editor and iframe; bidirectional (iframe → editor: selection change, drag events; editor → iframe: apply style, apply transform) |
| **Single HTML file** | Zero build step; open in any browser; easy to share; no server required; works offline |
| **In-memory undo stack** | Store JSON snapshots of element modifications (position, text, styles); replay on undo |
| **Blob URL loading** | Read file via `FileReader` → create `Blob` → `URL.createObjectURL()` → load in iframe; avoids file path issues |
| **CSS-only scaling** | Transform `scale()` on iframe wrapper, not modifying carousel CSS; preserves 1080px coordinate space for all edits |

---

## 3. UI Layout & Design System

### 3.1 Color Palette

```css
:root {
  --editor-bg: #0A0A0A;
  --panel-bg: rgba(255, 255, 255, 0.05);
  --panel-border: rgba(255, 255, 255, 0.08);
  --panel-hover: rgba(255, 255, 255, 0.08);
  --accent: #C7FF3A;           /* lime */
  --accent-hover: #D4FF6A;
  --accent-dim: rgba(199, 255, 58, 0.15);
  --text-primary: #FAFAFA;
  --text-secondary: #888888;
  --text-muted: #555555;
  --danger: #FF5C3C;
  --danger-bg: rgba(255, 92, 60, 0.12);
  --success: #C7FF3A;
  --warning: #FF8B70;
  --glass-blur: 16px;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --shadow-elevation: 0 8px 32px rgba(0, 0, 0, 0.4);
}
```

### 3.2 Layout Grid

```
+----------------------------------------------------------+
|  [Logo]  File  |  Undo  Redo  |  Zoom 100%  Fit  | Export |  ← 52px tall
+----------------------------------------------------------+
| +---------+  +--------------------------------+  +---------+ |
| |         |  |                                |  |         | |
| | LEFT    |  |     PREVIEW CANVAS             |  | RIGHT   | |
| | SIDEBAR |  |     ┌──────────────────┐      |  | SIDEBAR | |
| | 260px   |  |     │                  │      |  | 280px   | |
| |         |  |     │   IFRAME         │      |  |         | |
| | - File  |  |     │   1080 x 1080    │      |  | - Props | |
| |   tree  |  |     │   scaled to fit  │      |  | - Style | |
| | - Layer |  |     │                  │      |  | - Text  | |
| |   list  |  |     │   [selection     │      |  | - Pos   | |
| | - Slide |  |     │    border]       │      |  | - Z     | |
| |   nav   |  |     │                  │      |  |         | |
| |         |  |     └──────────────────┘      |  |         | |
| +---------+  +--------------------------------+  +---------+ |
| +----------------------------------------------------------+ |
| |  Status: X: 452  Y: 198  |  .headline  |  Slide 3/7     | ← 28px
+----------------------------------------------------------+
```

### 3.3 Glassmorphism Panel Style

```css
.glass-panel {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 16px;
  transition: background 0.2s, border-color 0.2s;
}
.glass-panel:hover {
  border-color: rgba(199, 255, 58, 0.2);
}
.glass-panel.active {
  border-color: #C7FF3A;
  background: rgba(199, 255, 58, 0.05);
}
```

### 3.4 Component Inventory

| Component | Purpose | File |
|-----------|---------|------|
| **TopToolbar** | File open, undo/redo, zoom controls, export, theme toggle | inline |
| **LeftSidebar** | File tree (recent), layer tree (DOM tree of current slide), slide thumbnails | inline |
| **PreviewCanvas** | Center area with iframe, zoom/pan, grid overlay, selection border | inline |
| **RightSidebar** | Element inspector: properties, styles, text editing | inline |
| **StatusBar** | Mouse coordinates, selected element tag/class, current slide index | inline |
| **IframeInjector** | Injected script into iframe: selection logic, drag handler, text editor | inline (as string) |
| **UndoManager** | Stack-based history with JSON snapshots | inline |
| **FileLoader** | FileReader API, drag & drop, recent files in localStorage | inline |
| **ExportEngine** | Apply modifications to raw HTML string, trigger download | inline |

---

## 4. Detailed Component Specifications

### 4.1 TopToolbar (height: 52px)

```
┌────────────────────────────────────────────────────────────────────┐
│ [🎠] worqai Carousel Editor    │  File ▾  │  ↶ Undo  ↷ Redo  │  [−] 100% [+]  │ Fit │  [Export]  │  🌙 │
└────────────────────────────────────────────────────────────────────┘
```

**Elements:**
- **Logo/text**: "worqai Carousel Editor" with lime accent dot
- **File dropdown**: Open File (triggers file input), Open Recent (submenu from localStorage), separator, Reload Original
- **Undo/Redo**: Disabled when stack empty; keyboard shortcuts Ctrl+Z / Ctrl+Y / Ctrl+Shift+Z
- **Zoom**: `-` / `+` buttons (step 10%), display current %, reset to fit button
- **Fit**: Auto-scale to fit canvas width/height with 24px padding
- **Export**: Button with lime accent, exports modified HTML as download
- **Theme toggle**: Moon/sun icon for editor UI dark/light (default dark)

**Zoom behavior:**
- Scale is applied to the `.preview-wrapper` CSS transform (`transform: scale(s)`)
- Origin: `top center` to anchor from top
- Iframe native size remains 1080x1080; all coordinates are in native pixels
- Mouse coordinates are converted using `e.offsetX / scale` for status bar display

### 4.2 LeftSidebar (width: 260px, scrollable)

**Section A: File Browser** (collapsible)
- **Open File** button: styled upload button (`<input type="file" accept=".html" hidden>`)
- **Drag & drop zone**: Entire window listens for `dragover`/`drop`; highlight border when dragging
- **Recent Files**: List of last 10 files from localStorage; show filename + last opened date; click to reload (if file handle available, or re-prompt)
- **File info**: Current filename, file size, number of slides

**Section B: Slide Navigator** (collapsible)
- Horizontal strip of slide thumbnails (miniature previews)
- Each thumbnail: 80px wide, aspect-ratio 1:1, border-radius 6px
- Current slide: lime border (`2px solid #C7FF3A`)
- Click to navigate to that slide (send `go(n)` message to iframe)
- Navigation also updates when user swipes in preview

**Section C: Layer Tree** (collapsible, main content)
- Hierarchical tree of DOM elements in the current slide
- Filtered: only meaningful elements (text nodes, containers, positioned elements)
- Exclude: `.glow`, `.band`, `.brand-w`, decorative SVGs (unless explicitly selected)
- Tree item format: `[icon] .class-name  "Text content..."`
- Selected element: lime background, left border accent
- Click to select element in iframe (send `selectElement` postMessage)
- Hover: highlight element in iframe (send `hoverElement` postMessage)
- Expand/collapse for nested containers (`.content`, `.glass-block`, `.cta-card`, etc.)

### 4.3 PreviewCanvas (center, fluid)

```
┌────────────────────────────────────────┐
│  +----------------------------------+  │
│  │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │  │  ← padding area (dark bg with
│  │  ░  +----------------------+  ░  │  │     subtle grid pattern)
│  │  ░  │                      │  ░  │  │
│  │  ░  │   IFRAME             │  ░  │  │
│  │  ░  │   1080 x 1080        │  ░  │  │
│  │  ░  │   [selection border  │  ░  │  │
│  │  ░  │    with handles]     │  ░  │  │
│  │  ░  │                      │  ░  │  │
│  │  ░  +----------------------+  ░  │  │
│  │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │  │
│  +----------------------------------+  │
│          [slide counter  3 / 7]         │
└────────────────────────────────────────┘
```

**Background**: Dark (#0A0A0A) with subtle CSS grid pattern:
```css
background-image: 
  linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
  linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
background-size: 40px 40px;
```

**Iframe container**:
```css
.iframe-wrapper {
  width: 1080px;
  height: 1080px;
  transform-origin: top center;
  transition: transform 0.2s ease;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
  border-radius: 4px;
  overflow: hidden;
}
```

**Selection overlay** (drawn by injected iframe script, not parent):
- When element selected: 2px lime border (`#C7FF3A`) with 2px offset
- Corner resize handles: 8px squares at corners (optional for v1; position-only for MVP)
- Hover outline: 1px dashed lime at 35% opacity (from existing carousel CSS)
- Dragging outline: 2px solid coral (`#FF8B70`) from existing carousel CSS

**Pan behavior** (when zoomed in):
- Middle-click + drag or spacebar + drag to pan canvas
- Canvas has `overflow: hidden` and transform translate

### 4.4 RightSidebar (width: 280px, scrollable)

**Tab system**: 3 tabs — Properties | Styles | Advanced

**Tab 1: Properties** (default)

| Field | Type | Description |
|-------|------|-------------|
| **Element Label** | text display | Tag + classes (e.g., `div.headline`) |
| **Text Content** | textarea | Inline text editing (syncs with iframe) |
| **Position X** | number input | `left` or `translateX` offset in px |
| **Position Y** | number input | `top` or `translateY` offset in px |
| **Width** | number input | Computed width (read-only for most) |
| **Height** | number input | Computed height (read-only) |
| **Z-Index** | number input | CSS `z-index` value |
| **Opacity** | slider (0-100) | CSS `opacity` |

**Tab 2: Styles**

| Field | Type | Description |
|-------|------|-------------|
| **Text Color** | color picker | Inline `<input type="color">` with hex display |
| **Font Size** | slider + number | px value (12-120 range) |
| **Font Weight** | dropdown | 400, 500, 600, 700, 800, 900 |
| **Background Color** | color picker | For `.glass-block`, `.cta-card`, etc. |
| **Border Color** | color picker | For bordered elements |
| **Border Radius** | slider | px value (0-50) |
| **Text Shadow** | toggle | Enable/disable existing text shadow |
| **Box Shadow** | toggle | Enable/disable |
| **CSS Classes** | tag list | Add/remove classes; editable tags |
| **Custom CSS** | textarea | Raw CSS rules for element (advanced) |

**Tab 3: Advanced**

| Field | Type | Description |
|-------|------|-------------|
| **Data Attributes** | key-value list | Edit `data-*` attributes |
| **Inline Styles** | textarea | Full inline style attribute editor |
| **HTML Editor** | textarea | Raw innerHTML (with syntax highlighting if feasible) |
| **Reset Position** | button | Remove `transform: translate()` and `data-dx/dy` |
| **Reset All Styles** | button | Revert element to original state |
| **Delete Element** | danger button | Remove element from DOM (with confirmation) |

**All fields update in real-time** — debounced 50ms, with undo checkpoint on blur or Enter.

### 4.5 StatusBar (height: 28px)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  🖱️  X: 452  Y: 198  │  Selected: div.headline  │  Slide: 3 / 7  │  Zoom: 65%     │
└─────────────────────────────────────────────────────────────────────────────────┘
```

- **Mouse coords**: Relative to iframe 1080x1080 coordinate space (converted from screen coords using scale)
- **Selected element**: Tag name + primary class (truncated if > 30 chars)
- **Slide counter**: "Current / Total" — click to open slide navigator
- **Zoom level**: Current percentage

---

## 5. Iframe Injection Strategy

### 5.1 Injected Script (`iframe-editor.js`)

This script is injected into the iframe after the carousel HTML loads. It runs in the iframe context and communicates with the parent via `window.parent.postMessage`.

**Core modules:**

```javascript
// ==== 1. SELECTION ENGINE ====
// Click on element → find nearest editable/movable element (bubble up)
// Ignore: .wrap (container), .track (track), body, html
// Send to parent: { type: 'elementSelected', tag, className, id, text, 
//   rect: {x,y,width,height}, computedStyle, attributes }
// Visual: add 2px lime border via CSS class .editor-selected

// ==== 2. DRAG ENGINE ====
// mousedown on selected element → start drag
// Calculate offset: mouse position - element rect
// mousemove → update element.style.transform = `translate(${dx}px, ${dy}px)`
// mouseup → save data-dx, data-dy attributes; send final position to parent
// Support: both inline positioned elements and elements with existing transform
// Snap: optional 10px grid snap (Shift to disable)

// ==== 3. TEXT EDIT ENGINE ====
// Double-click on selected text element → activate contenteditable
// contenteditable="true" set on element
// On blur/Enter → remove contenteditable, send updated text to parent
// Parent updates its textarea; undo checkpoint created
// Prevent: drag during text edit mode

// ==== 4. NAVIGATION BRIDGE ====
// Listen for parent messages: { type: 'goToSlide', index }
// Listen for parent messages: { type: 'selectElement', selector }
// Report back: { type: 'slideChanged', index, total }
// Report back: { type: 'elementHovered', selector } (for layer tree sync)

// ==== 5. STYLE APPLICATION ====
// Listen for parent messages: { type: 'applyStyle', property, value }
// Apply: element.style[property] = value
// Report back: { type: 'styleChanged', property, value, computed }

// ==== 6. TRANSFORM PARSER ====
// Parse existing transform: translate(x, y)
// Maintain original transform + editor offset as separate values
// Store: data-editor-dx, data-editor-dy
// Apply: transform = `${original} translate(${dx}px, ${dy}px)`
// This preserves carousel animations and existing transforms
```

### 5.2 postMessage Protocol

**Parent → Iframe:**

| Message | Payload | Action |
|---------|---------|--------|
| `loadHtml` | `{ html: string }` | Load full HTML string into iframe (via blob URL) |
| `goToSlide` | `{ index: number }` | Navigate to slide N (call `go(N)`) |
| `selectElement` | `{ selector: string }` | Select element by CSS selector |
| `applyStyle` | `{ selector, property, value }` | Set CSS style on element |
| `applyTransform` | `{ selector, dx, dy }` | Set translate offset |
| `setText` | `{ selector, text }` | Set textContent/innerHTML |
| `setAttribute` | `{ selector, attr, value }` | Set HTML attribute |
| `removeAttribute` | `{ selector, attr }` | Remove HTML attribute |
| `requestElementInfo` | `{ selector }` | Send full element info back |
| `toggleEditable` | `{ selector, enabled }` | Toggle contenteditable |
| `createUndoCheckpoint` | `{ }` | Mark current state for undo (iframe does nothing, parent manages) |
| `ping` | `{ }` | Health check |

**Iframe → Parent:**

| Message | Payload | Action |
|---------|---------|--------|
| `ready` | `{ slideCount, currentSlide }` | Iframe loaded, editor injected, ready for commands |
| `elementSelected` | `{ selector, tag, classes, id, text, rect, styles, attributes }` | User clicked element |
| `elementHovered` | `{ selector }` | Mouse hover on element (for layer tree) |
| `elementMoved` | `{ selector, dx, dy, rect }` | Drag completed, new position |
| `textChanged` | `{ selector, text }` | Text edited |
| `styleChanged` | `{ selector, property, value }` | Style modified (from iframe context) |
| `slideChanged` | `{ index, total }` | Slide navigation occurred (swipe, button, keyboard) |
| `mouseMove` | `{ x, y }` | Mouse position in 1080x1080 space (for status bar) |
| `error` | `{ message, stack }` | Iframe error reporting |

### 5.3 Injection Method

```javascript
// In parent window:
function loadCarousel(htmlString) {
  const blob = new Blob([htmlString], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  iframe.src = url;
  
  iframe.onload = () => {
    const injectedScript = iframe.contentDocument.createElement('script');
    injectedScript.textContent = EDITOR_SCRIPT_STRING; // inline JS string
    iframe.contentDocument.head.appendChild(injectedScript);
    
    // Also inject CSS for selection/hover styles (extends existing)
    const injectedStyle = iframe.contentDocument.createElement('style');
    injectedStyle.textContent = EDITOR_CSS_STRING;
    iframe.contentDocument.head.appendChild(injectedStyle);
    
    // Send ready handshake
    iframe.contentWindow.postMessage({ type: 'editorReady' }, '*');
  };
}
```

---

## 6. Undo/Redo System

### 6.1 Stack Architecture

```javascript
class UndoManager {
  constructor() {
    this.stack = [];      // Array of snapshots
    this.index = -1;      // Current position
    this.maxSize = 100;   // Limit stack depth
  }
  
  // Snapshot format:
  // {
  //   type: 'elementModified' | 'textChanged' | 'styleChanged' | 'elementMoved' | 'batch',
  //   selector: '.slide[data-slide="3"] .headline',
  //   before: { transform: '...', text: '...', styles: {...} },
  //   after:  { transform: '...', text: '...', styles: {...} },
  //   timestamp: Date.now()
  // }
  
  push(snapshot) {
    // Remove any redo states (everything after current index)
    this.stack = this.stack.slice(0, this.index + 1);
    this.stack.push(snapshot);
    if (this.stack.length > this.maxSize) this.stack.shift();
    else this.index++;
    this.updateUI();
  }
  
  undo() {
    if (this.index < 0) return;
    const snapshot = this.stack[this.index];
    this.applySnapshot(snapshot.before);
    this.index--;
    this.updateUI();
  }
  
  redo() {
    if (this.index >= this.stack.length - 1) return;
    this.index++;
    const snapshot = this.stack[this.index];
    this.applySnapshot(snapshot.after);
    this.updateUI();
  }
  
  applySnapshot(state) {
    // Send postMessage to iframe to apply the state
    Object.entries(state).forEach(([prop, value]) => {
      iframe.contentWindow.postMessage({
        type: 'applyStyle',
        selector: state.selector,
        property: prop,
        value: value
      }, '*');
    });
  }
  
  updateUI() {
    // Enable/disable undo/redo buttons
    // Update button opacity/visual state
  }
}
```

### 6.2 Checkpoint Triggers (what creates an undo state)

| Action | Checkpoint? | Notes |
|--------|-------------|-------|
| Element drag end (mouseup) | ✅ Yes | Full element state before/after |
| Text edit blur / Enter | ✅ Yes | Text content before/after |
| Style property change (blur/Enter) | ✅ Yes | Style value before/after |
| Continuous style slider | ❌ No | Debounced; only checkpoint on mouseup |
| Slide navigation | ❌ No | State-independent |
| Element selection | ❌ No | No state change |
| File open | ✅ Yes (separate) | Save entire file state |

### 6.3 Batch Operations

For multi-element changes (e.g., "Reset all positions"), create a single batch snapshot:
```javascript
{
  type: 'batch',
  operations: [
    { selector, before, after },
    { selector, before, after },
    ...
  ]
}
```

---

## 7. Export Engine

### 7.1 Export Strategy

The export produces a **modified HTML file** that is a valid, standalone carousel — just like the original, but with edits applied.

**Export steps:**

1. **Get original HTML string** (stored in memory from FileReader)
2. **Parse with DOMParser** (or use the iframe's document)
3. **Apply all modifications** from the undo stack / modification registry:
   - For each modified element, apply `transform`, `style`, `data-dx`, `data-dy`, updated text
4. **Clean up editor artifacts**:
   - Remove injected editor `<script>` and `<style>` tags
   - Remove `contenteditable="true"` attributes
   - Remove `data-editable="true"`, `data-movable="true"` (if not desired in final)
   - Remove `.editor-selected` class and any editor-only CSS classes
   - Remove event listeners (they're not in the HTML anyway)
5. **Preserve existing editor CSS** (the carousel files already have editor CSS at the bottom; keep it for future editing)
6. **Serialize back to HTML string** using `new XMLSerializer().serializeToString(doc)`
7. **Format HTML** (basic indentation for readability, optional)
8. **Trigger download** via `<a download="filename.html" href="data:text/html,..."></a>`

### 7.2 Modification Registry

Instead of tracking only via undo stack, maintain a parallel registry of current modifications for fast export:

```javascript
const modificationRegistry = {
  // Key: CSS selector (unique per slide)
  // Value: { styles: {}, attributes: {}, text: '', transform: {dx, dy} }
  '.slide[data-slide="3"] .headline': {
    styles: { color: '#FF0000', fontSize: '80px' },
    attributes: { 'data-dx': '12', 'data-dy': '-5' },
    text: 'Nuevo titulo aqui',
    transform: { dx: 12, dy: -5 }
  }
};
```

### 7.3 Export Filename Convention

```
Original: reframed_carousel_7-segundos_worqai-lime.html
Export:   reframed_carousel_7-segundos_worqai-lime_EDITED.html
          (or prompt user for custom filename)
```

---

## 8. File Handling & Persistence

### 8.1 Open File

```javascript
function openFile(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    const html = e.target.result;
    storeOriginal(html);
    loadIntoIframe(html);
    addToRecentFiles(file);
  };
  reader.readAsText(file);
}
```

### 8.2 Drag & Drop

```javascript
window.addEventListener('dragover', (e) => {
  e.preventDefault();
  document.body.classList.add('drag-active'); // visual feedback
});
window.addEventListener('dragleave', (e) => {
  document.body.classList.remove('drag-active');
});
window.addEventListener('drop', (e) => {
  e.preventDefault();
  document.body.classList.remove('drag-active');
  const file = e.dataTransfer.files[0];
  if (file && file.name.endsWith('.html')) openFile(file);
});
```

### 8.3 localStorage Schema

```javascript
// Recent files (last 10)
localStorage.setItem('carouselEditor_recentFiles', JSON.stringify([
  { name: 'reframed_carousel_7-segundos_worqai-lime.html', 
    size: 45231, 
    lastOpened: '2025-01-14T10:30:00Z',
    handle: null // FileSystemFileHandle if available (File System Access API)
  },
  ...
]));

// Settings
localStorage.setItem('carouselEditor_settings', JSON.stringify({
  defaultZoom: 'fit',
  theme: 'dark',           // 'dark' | 'light'
  showGrid: true,
  snapToGrid: false,
  gridSize: 10,
  sidebarLeftWidth: 260,
  sidebarRightWidth: 280,
  lastDirectory: null      // Directory handle if File System Access API supported
}));
```

### 8.4 File System Access API (Optional Enhancement)

If available (Chrome/Edge), use `showOpenFilePicker()` for a native file dialog and `showDirectoryPicker()` for batch opening of the `Approved/` directory. This allows true save-in-place (overwrite original) rather than download-only.

```javascript
async function openWithFilePicker() {
  const [handle] = await window.showOpenFilePicker({
    types: [{ description: 'HTML Files', accept: { 'text/html': ['.html'] } }],
    multiple: false
  });
  const file = await handle.getFile();
  return { handle, file };
}
```

---

## 9. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl/Cmd + O` | Open file dialog |
| `Ctrl/Cmd + S` | Export/download |
| `Ctrl/Cmd + Z` | Undo |
| `Ctrl/Cmd + Y` | Redo |
| `Ctrl/Cmd + Shift + Z` | Redo (alternate) |
| `←` / `→` | Navigate slides (when not editing text) |
| `Delete` | Delete selected element (with confirmation) |
| `Escape` | Deselect element / cancel drag / exit text edit |
| `Space` | Hold to pan canvas (when zoomed) |
| `Tab` | Navigate UI panels (standard accessibility) |
| `Shift + Drag` | Disable snap-to-grid during drag |
| `Ctrl + D` | Duplicate selected element |
| `Ctrl + 0` | Reset zoom to 100% |
| `Ctrl + -` / `Ctrl + =` | Zoom out / zoom in |

---

## 10. CSS Implementation Notes

### 10.1 Editor UI CSS (inline in single file)

```css
/* === ROOT & RESET === */
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { 
  height: 100%; 
  overflow: hidden; 
  background: #0A0A0A; 
  color: #FAFAFA; 
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 13px;
}

/* === LAYOUT === */
.editor-root {
  display: grid;
  grid-template-rows: 52px 1fr 28px;
  grid-template-columns: 260px 1fr 280px;
  grid-template-areas: 
    "toolbar toolbar toolbar"
    "left canvas right"
    "status status status";
  height: 100vh;
  gap: 1px;
  background: #0A0A0A;
}

/* === GLASS PANELS === */
.glass-panel {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 16px;
  overflow: auto;
}
.glass-panel::-webkit-scrollbar { width: 6px; }
.glass-panel::-webkit-scrollbar-track { background: transparent; }
.glass-panel::-webkit-scrollbar-thumb { 
  background: rgba(255,255,255,0.15); 
  border-radius: 3px; 
}

/* === BUTTONS === */
.btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 12px; border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.05);
  color: #FAFAFA; font-size: 12px; font-weight: 500;
  cursor: pointer; transition: all 0.15s;
}
.btn:hover { background: rgba(255,255,255,0.1); border-color: rgba(199,255,58,0.3); }
.btn:active { transform: scale(0.97); }
.btn-accent { background: #C7FF3A; color: #0A0A0A; border-color: #C7FF3A; }
.btn-accent:hover { background: #D4FF6A; }
.btn:disabled { opacity: 0.3; cursor: default; }
.btn:disabled:hover { border-color: rgba(255,255,255,0.1); }

/* === INPUTS === */
input[type="text"], input[type="number"], textarea, select {
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 6px; padding: 6px 10px;
  color: #FAFAFA; font-size: 12px;
  outline: none; transition: border-color 0.15s;
  width: 100%;
}
input:focus, textarea:focus, select:focus {
  border-color: #C7FF3A;
  box-shadow: 0 0 0 2px rgba(199,255,58,0.15);
}
input[type="color"] {
  padding: 2px; height: 32px; cursor: pointer;
}

/* === SLIDER === */
input[type="range"] {
  -webkit-appearance: none; appearance: none;
  height: 4px; background: rgba(255,255,255,0.15);
  border-radius: 2px; outline: none;
}
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none; width: 14px; height: 14px;
  background: #C7FF3A; border-radius: 50%; cursor: pointer;
  box-shadow: 0 0 8px rgba(199,255,58,0.4);
}

/* === LAYER TREE === */
.layer-item {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 8px; border-radius: 6px;
  cursor: pointer; font-size: 12px;
  color: #888; transition: all 0.15s;
}
.layer-item:hover { background: rgba(255,255,255,0.05); color: #FAFAFA; }
.layer-item.selected { 
  background: rgba(199,255,58,0.1); 
  color: #C7FF3A; 
  border-left: 2px solid #C7FF3A; 
}
.layer-item .tag-name { font-family: monospace; font-size: 11px; opacity: 0.7; }

/* === PREVIEW CANVAS === */
.canvas-area {
  grid-area: canvas;
  display: flex; align-items: center; justify-content: center;
  background: #0A0A0A;
  background-image: 
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  overflow: hidden; position: relative;
}
.iframe-wrapper {
  width: 1080px; height: 1080px;
  transform-origin: top center;
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
  border-radius: 4px; overflow: hidden;
  position: relative;
}
iframe { width: 100%; height: 100%; border: none; display: block; }

/* === DRAG OVERLAY === */
.drag-overlay {
  position: absolute; inset: 0;
  border: 3px dashed #C7FF3A;
  background: rgba(199,255,58,0.05);
  display: none; align-items: center; justify-content: center;
  pointer-events: none; z-index: 1000;
}
.drag-overlay.active { display: flex; }
.drag-overlay-text { font-size: 20px; font-weight: 700; color: #C7FF3A; }

/* === TOOLTIP === */
.tooltip {
  position: absolute; padding: 6px 10px;
  background: rgba(0,0,0,0.8); border-radius: 6px;
  font-size: 11px; color: #FAFAFA; pointer-events: none;
  opacity: 0; transition: opacity 0.15s; z-index: 1000;
}
.tooltip.show { opacity: 1; }

/* === ANIMATIONS === */
@keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; } }
.panel-enter { animation: fadeIn 0.2s ease; }

/* === RESPONSIVE === */
@media (max-width: 1200px) {
  .editor-root { grid-template-columns: 200px 1fr 240px; }
}
@media (max-width: 900px) {
  .editor-root { 
    grid-template-columns: 1fr; 
    grid-template-rows: 52px 1fr 28px;
    grid-template-areas: "toolbar" "canvas" "status";
  }
  .sidebar-left, .sidebar-right { display: none; } /* Mobile: hide sidebars, use overlay panels */
}
```

### 10.2 Injected Iframe CSS (extends existing carousel editor CSS)

```css
/* Editor selection styles (injected into iframe) */
.editor-selected {
  outline: 2px solid #C7FF3A !important;
  outline-offset: 3px !important;
  cursor: move !important;
}
.editor-hover {
  outline: 1px dashed rgba(199, 255, 58, 0.35) !important;
  outline-offset: 2px !important;
}
.editor-dragging {
  outline: 2px solid #FF8B70 !important;
  outline-offset: 3px !important;
  cursor: grabbing !important;
  z-index: 100 !important;
  opacity: 0.9 !important;
}
.editor-text-editing {
  outline: 2px solid #C7FF3A !important;
  outline-offset: 2px !important;
  cursor: text !important;
  background: rgba(199, 255, 58, 0.05) !important;
}
/* Prevent selection on non-editable elements during drag */
.editor-noselect {
  user-select: none !important;
  -webkit-user-select: none !important;
}
```

---

## 11. Implementation Steps (Phase Plan)

### Phase 1: Foundation (Day 1)

1. **Create file structure** — `tools/carousel-editor/` directory
2. **Write base HTML skeleton** — single HTML file with all sections (toolbar, sidebars, canvas, status)
3. **Implement CSS framework** — glassmorphism panels, dark theme, lime accents, layout grid
4. **Implement file loading** — FileReader, drag & drop, file input, recent files list
5. **Implement iframe loading** — Blob URL, injection of placeholder script
6. **Test with sample carousel** — Load one of the existing carousel files

**Deliverable:** Editor loads and displays carousel in preview pane.

### Phase 2: Iframe Editor Core (Day 2)

7. **Write iframe injection script** (inline JS string):
   - Element selection (click → find editable parent → highlight)
   - Drag engine (mousedown → mousemove → mouseup, with translate transform)
   - Text editing (double-click → contenteditable → blur saves)
   - PostMessage bridge (send selection, drag end, text change events)
8. **Implement postMessage handler in parent** — receive iframe messages, update UI state
9. **Implement element selection in parent** — click in layer tree → select in iframe
10. **Implement basic property panel** — Position X/Y, Z-index, Opacity
11. **Implement undo stack** — Track element moves and text changes

**Deliverable:** Can select elements, drag them, edit text, undo/redo works.

### Phase 3: Inspector & Styling (Day 3)

12. **Full right sidebar inspector** — Tabs (Properties, Styles, Advanced)
13. **Style controls** — Color picker, font size slider, font weight, background color
14. **Real-time style application** — Parent → iframe `applyStyle` messages
15. **Computed styles display** — Read current styles from iframe element
16. **Element info panel** — Tag, classes, dimensions, position display
17. **Reset/Delete operations** — Reset position, reset all styles, delete element

**Deliverable:** Full style editing capability for text, colors, sizes, positions.

### Phase 4: Navigation & Polish (Day 4)

18. **Slide navigation** — Thumbnails in left sidebar, sync with iframe swipe/buttons
19. **Zoom & pan** — Zoom controls, mouse wheel zoom, middle-click pan
20. **Status bar** — Live coordinates, selected element info, slide counter
21. **Keyboard shortcuts** — All shortcuts implemented
22. **Export engine** — Apply modifications, clean artifacts, download HTML
23. **localStorage persistence** — Settings, recent files, last directory

**Deliverable:** Complete editor with all features functional.

### Phase 5: Testing & Refinement (Day 5)

24. **Test with 5+ carousel files** — Different themes (dark/light), different structures
25. **Test edge cases** — SVG backgrounds, inline styles, CSS variables, existing transforms
26. **Bug fixes** — Transform parsing, coordinate conversion, iframe reload state
27. **UI refinement** — Animation smoothness, responsive adjustments, error states
28. **Performance** — Large files (some are 500+ lines), iframe memory, undo stack limits
29. **Documentation** — Write inline help/tooltips, README for the tool

**Deliverable:** Production-ready tool, tested with actual worqai carousel files.

---

## 12. Carousel-Specific Adaptations

Based on analysis of the 52+ carousel files, the editor must handle these specific patterns:

### 12.1 Element Types to Support

| Element Class | Type | Editable? | Movable? | Notes |
|--------------|------|-----------|----------|-------|
| `.headline` | Text | ✅ Yes | ✅ Yes | Large display text, may contain `<span class="lime">` |
| `.body-text` | Text | ✅ Yes | ✅ Yes | Paragraph text |
| `.glass-text` | Text | ✅ Yes | ✅ Yes | Inside `.glass-block` |
| `.glass-tag` | Text | ✅ Yes | ✅ Yes | Small uppercase label |
| `.stat-num`, `.stat-pct` | Text | ✅ Yes | ✅ Yes | Large numbers |
| `.stat-context` | Text | ✅ Yes | ✅ Yes | Stat description |
| `.proof-stmt`, `.proof-ctx` | Text | ✅ Yes | ✅ Yes | Proof section text |
| `.cta-headline-out`, `.cta-offer`, `.cta-fine`, `.cta-closing`, `.cta-micro` | Text | ✅ Yes | ✅ Yes | CTA text elements |
| `.url-text` | Text | ✅ Yes | ✅ Yes | URL display |
| `.hook-display`, `.hook-sub` | Text | ✅ Yes | ✅ Yes | Hook section |
| `.label`, `.lime-badge`, `.pill-tag`, `.source-tag` | Text | ✅ Yes | ✅ Yes | Labels/badges |
| `.site-url`, `.counter`, `.brand-anchor` | Text | ✅ Yes | ✅ Yes | Brand elements |
| `.proof-city`, `.proof-metric` | Text | ✅ Yes | ✅ Yes | Proof metrics |
| `.deco-num` | Text | ✅ Yes | ✅ Yes | Decorative numbers |
| `.glass-block` | Container | ❌ No (text only) | ✅ Yes | Unit draggable |
| `.cta-card` | Container | ❌ No (text only) | ✅ Yes | Unit draggable |
| `.hook-stack` | Container | ❌ No (text only) | ✅ Yes | Unit draggable |
| `.content` | Container | ❌ No | ✅ Yes | Main content area |
| `.swipe-pill`, `.url-box` | Container | ✅ Yes | ✅ Yes | Interactive units |
| `.brand-w`, `.glow`, `.band`, `.coral`, `.left-spine` | Decorative | ❌ No | ❌ No | Background elements, skip in layer tree |
| `svg` (background) | SVG | ❌ No | ❌ No | Skip in layer tree |
| `.warning`, `.followup`, `.fu-card`, `.col` | Container | ❌ No | ✅ Yes | Complex nested containers |
| `.echo-line`, `.echo-byline`, `.echo-eyebrow` | Text | ✅ Yes | ✅ Yes | Echo stack elements |
| `.terminal`, `.term-bar`, `.term-body` | Container | ❌ No | ✅ Yes | Terminal blocks |
| `.big-item`, `.big-num`, `.big-text-*` | Text | ✅ Yes | ✅ Yes | List items |
| `.cols-grid`, `.col` | Container | ❌ No | ✅ Yes | Grid columns |
| `.text-backdrop` | Utility | N/A | N/A | CSS class for glass backdrop, not independent |

### 12.2 CSS Variable Awareness

The carousels use extensive CSS variables (`:root`). The editor should:
- **Read** CSS variables when inspecting element styles (e.g., `color: var(--lime)` → resolve to `#C7FF3A`)
- **Allow editing** by applying inline styles (which override CSS variables via specificity)
- **Preserve** original CSS variables in exported HTML (do not inline them unless explicitly changed)

### 12.3 Existing Editor CSS Handling

Some carousel files already contain editor CSS at the bottom (`[data-editable="true"]`, etc.). The injected script should:
- **Preserve** these styles (they're useful for standalone editing)
- **Enhance** with additional `.editor-selected`, `.editor-hover`, `.editor-dragging` classes
- **Not conflict** with existing drag/selection logic (replace with improved version if needed)

### 12.4 Transform Handling

Many elements have inline `style="top:...;left:..."` or are positioned via CSS. The editor's drag engine must:
- **Detect existing position**: `position: absolute/relative/fixed` via `getComputedStyle()`
- **Convert to translate**: If element is not `position: absolute`, wrap it or use `translate()` for dragging
- **Preserve existing transforms**: If element already has `transform: scale(...) rotate(...)`, append `translate()` via `transform: ... translate(dx, dy)`
- **Store offsets**: Use `data-editor-dx` and `data-editor-dy` (separate from `data-dx/dy` which some carousels already use)

---

## 13. Risk Assessment & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Iframe security restrictions** | High | Use `blob:` URL (same-origin), no CORS issues; postMessage with `*` targetOrigin is safe since we control both frames |
| **Large HTML files (500+ lines)** | Medium | DOM operations are fast; use `requestAnimationFrame` for drag; lazy-load slide thumbnails |
| **Complex CSS selectors** | Medium | Use `data-editor-id` attributes on elements for reliable selector references; regenerate if DOM changes |
| **Undo stack memory** | Medium | Limit to 100 states; store compact snapshots (only changed properties) |
| **Browser compatibility** | Medium | Target modern browsers (Chrome/Edge/Firefox/Safari); use feature detection for File System Access API |
| **Text content with HTML tags** | Medium | Use `innerHTML` preservation; if user edits text containing `<span class="lime">`, use `contenteditable` which preserves child elements |
| **Carousel JavaScript conflicts** | Medium | Injected editor script runs after carousel JS; use event delegation carefully; namespaced CSS classes (`editor-*`) |
| **Mobile/tablet usage** | Low | Editor is desktop-focused; responsive design hides sidebars on small screens |
| **Export corrupting original** | High | Always export as new file (`_EDITED.html`); never overwrite original; preserve original in memory for "Reload Original" |

---

## 14. Future Enhancements (Post-MVP)

| Feature | Priority | Description |
|---------|----------|-------------|
| **Batch export** | High | Select multiple files, apply same edits (e.g., change brand color across all), export all |
| **Template system** | Medium | Save "style presets" (color schemes, font pairings) and apply to any carousel |
| **Image replacement** | Medium | Click an image/SVG → upload replacement → auto-resize/fit |
| **Multi-select** | Medium | Shift/Ctrl click to select multiple elements; group move/align |
| **Alignment tools** | Medium | Snap to center, distribute evenly, align left/right/top/bottom |
| **Preview mode** | Medium | Toggle editor overlays off to see "final" look without selection borders |
| **Fullscreen mode** | Low | Hide all UI, show only carousel at 100% scale |
| **Dark/light theme toggle for carousels** | Low | Switch `--bg` and `--text` variables to flip entire carousel theme |
| **Keyboard nudge** | Medium | Arrow keys move selected element 1px (Shift = 10px) |
| **Copy/paste styles** | Low | Copy all styles from one element, paste to another |
| **Slide reordering** | Medium | Drag slides in thumbnail strip to reorder (update DOM order) |
| **Element duplication** | Medium | Ctrl+D duplicates selected element within same slide |
| **History timeline** | Low | Visual timeline of edits, click to jump to any state |
| **File System Access integration** | Medium | Open/save directly to disk (Chrome/Edge) without download dialog |
| **Collaboration** | Low | WebRTC or simple sync for real-time collaboration (not applicable for local tool) |

---

## 15. Appendix A: Sample Carousel Structure Reference

```html
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8">
  <title>worqai ...</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk..." rel="stylesheet">
  <style>
    :root { --lime:#C7FF3A; --bg:#FAFAFA; --slide-bg:linear-gradient(...); ... }
    /* ... extensive carousel CSS ... */
    /* === EDITOR: draggable elements + editable text === */
    [data-editable="true"],[data-movable="true"] { ... }
  </style>
</head>
<body>
  <div class="preview-cage">
    <div class="viewer">
      <div class="wrap" id="wrap">
        <div class="track" id="track">
          <div class="slide" data-slide="1">
            <div class="brand-w" style="top:-12%;left:-8%;">W</div>
            <div class="glow" style="top:-25%;right:-10%;"></div>
            <div class="band"></div>
            <div class="left-spine"></div>
            <div class="deco-num">01</div>
            <div class="content">
              <div class="label">worqai - contra el filtro</div>
              <div class="echo-eyebrow">7 segundos - el filtro</div>
              <div class="echo-stack">
                <div class="echo-line heavy">7 SEGUNDOS</div>
                ...
              </div>
              ...
            </div>
            <div class="brand-anchor">...</div>
            <div class="site-url">worqai.io</div>
            <div class="counter">01 / 07</div>
          </div>
          <!-- more slides ... -->
        </div>
      </div>
      <div class="controls">...</div>
    </div>
  </div>
  <script>
    let cur=0; const slides=...; function go(n){...}
    // carousel navigation logic
    // existing editor drag logic (will be enhanced/replaced by iframe injection)
  </script>
</body>
</html>
```

---

## 16. Appendix B: File Output Location

The final editor file should be saved at:

```
C:/Users/kenne/OneDrive/Documentos/worqai-marketing/tools/carousel-editor/
├── index.html              ← The standalone editor tool (this is the deliverable)
├── plan.md                 ← This document
├── README.md               ← User guide for the tool
└── assets/                 ← (optional) if any external assets needed
    └── icons.svg           ← (optional) inline SVG icons if not using CDN
```

The `index.html` is a single self-contained file that can be opened directly in any modern browser by double-clicking it — no server, no build step, no installation.

---

*End of Plan*

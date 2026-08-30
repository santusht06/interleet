#!/usr/bin/env python3
"""
fix_frontend_starters.py
Enriches all 50 Frontend challenges in MongoDB (`interleet.problems`) with complete,
production-grade starter templates (index.html, index.css, index.js) containing clean UI structures,
custom CSS, and structured JavaScript scaffolds with event handlers and TODO hooks.
"""

import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def get_db():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    return client["interleet"]

BASE_CSS = """* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  background-color: #0c0c0e;
  color: #f4f4f5;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
#app {
  width: 100%;
  max-width: 600px;
  background: #18181b;
  border: 1px solid #27272a;
  border-radius: 12px;
  padding: 28px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
}
h1, h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: #fafafa;
}
button {
  background-color: #f97316;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}
button:hover {
  background-color: #ea580c;
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
input, select, textarea {
  background: #09090b;
  border: 1px solid #3f3f46;
  color: #f4f4f5;
  padding: 8px 12px;
  border-radius: 6px;
  outline: none;
  font-size: 0.9rem;
}
input:focus, select:focus, textarea:focus {
  border-color: #f97316;
}
"""

TEMPLATES = {
    "frontend-banner-slider": {
        "title": "Banner Slider",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Banner Slider</title>
  <link rel="stylesheet" href="index.css">
</head>
<body>
  <div id="app">
    <h1>Featured Banners</h1>
    <div class="slider-wrapper">
      <div id="slider-track" class="slider-track">
        <div class="slide active" style="background: linear-gradient(135deg, #f97316, #ea580c);">
          <div class="slide-content">
            <h2>Explore System Design</h2>
            <p>Master distributed systems with interactive challenges.</p>
          </div>
        </div>
        <div class="slide" style="background: linear-gradient(135deg, #3b82f6, #1d4ed8);">
          <div class="slide-content">
            <h2>Live AI Mock Interviews</h2>
            <p>Real-time conversational evaluation with industry rubrics.</p>
          </div>
        </div>
        <div class="slide" style="background: linear-gradient(135deg, #10b981, #047857);">
          <div class="slide-content">
            <h2>DevOps & Sandboxing</h2>
            <p>Deploy real containers and troubleshoot live infrastructure.</p>
          </div>
        </div>
      </div>

      <button id="prev-btn" class="nav-btn prev" aria-label="Previous Slide">&#10094;</button>
      <button id="next-btn" class="nav-btn next" aria-label="Next Slide">&#10095;</button>

      <div id="pagination-dots" class="pagination-dots">
        <span class="dot active" data-index="0"></span>
        <span class="dot" data-index="1"></span>
        <span class="dot" data-index="2"></span>
      </div>
    </div>
  </div>
  <script src="index.js"></script>
</body>
</html>""",
        "css": BASE_CSS + """
.slider-wrapper {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  height: 240px;
}
.slider-track {
  display: flex;
  height: 100%;
  transition: transform 0.4s ease-in-out;
}
.slide {
  min-width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px;
  text-align: center;
}
.slide-content h2 { margin-bottom: 8px; font-size: 1.5rem; color: #fff; }
.slide-content p { color: rgba(255, 255, 255, 0.9); font-size: 0.95rem; }
.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  padding: 10px 14px;
  border-radius: 50%;
  color: white;
}
.nav-btn:hover { background: rgba(0, 0, 0, 0.8); }
.nav-btn.prev { left: 12px; }
.nav-btn.next { right: 12px; }
.pagination-dots {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
}
.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  cursor: pointer;
}
.dot.active { background: #ffffff; width: 24px; border-radius: 10px; }
""",
        "js": """// State variables
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');
const track = document.getElementById('slider-track');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');

function updateSlider(index) {
  currentSlide = index;
  // Update track position
  track.style.transform = `translateX(-${currentSlide * 100}%)`;
  
  // Update active classes
  slides.forEach((s, idx) => s.classList.toggle('active', idx === currentSlide));
  dots.forEach((d, idx) => d.classList.toggle('active', idx === currentSlide));
}

// Event Listeners
nextBtn.addEventListener('click', () => {
  const next = (currentSlide + 1) % slides.length;
  updateSlider(next);
});

prevBtn.addEventListener('click', () => {
  const prev = (currentSlide - 1 + slides.length) % slides.length;
  updateSlider(prev);
});

dots.forEach((dot, idx) => {
  dot.addEventListener('click', () => updateSlider(idx));
});

// Auto-advance every 5 seconds (Optional)
// setInterval(() => nextBtn.click(), 5000);
"""
    },

    "frontend-modal-dialog-box": {
        "title": "Modal Dialog Box",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Modal Dialog Box</title>
  <link rel="stylesheet" href="index.css">
</head>
<body>
  <div id="app">
    <h1>Modal Dialog Demo</h1>
    <p style="color: #a1a1aa; margin-bottom: 20px;">Click the button below to trigger an accessible modal overlay with keyboard escape and focus trap support.</p>
    <button id="open-modal-btn">Open Dialog</button>

    <div id="modal-backdrop" class="modal-backdrop hidden">
      <div id="modal-container" class="modal-container" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <div class="modal-header">
          <h2 id="modal-title">Confirm Deletion</h2>
          <button id="close-modal-x" class="close-x" aria-label="Close">&times;</button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to permanently delete this resource? This action cannot be undone.</p>
        </div>
        <div class="modal-footer">
          <button id="cancel-btn" class="secondary-btn">Cancel</button>
          <button id="confirm-btn" class="danger-btn">Confirm Delete</button>
        </div>
      </div>
    </div>
  </div>
  <script src="index.js"></script>
</body>
</html>""",
        "css": BASE_CSS + """
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}
.modal-backdrop.hidden { display: none; }
.modal-container {
  background: #18181b;
  border: 1px solid #3f3f46;
  border-radius: 12px;
  width: 90%;
  max-width: 480px;
  padding: 24px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.close-x {
  background: transparent;
  color: #a1a1aa;
  font-size: 1.5rem;
  padding: 0 4px;
}
.close-x:hover { color: #ffffff; background: transparent; }
.modal-body p { color: #d4d4d8; font-size: 0.95rem; line-height: 1.5; margin-bottom: 24px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 12px; }
.secondary-btn { background: #27272a; color: #e4e4e7; }
.secondary-btn:hover { background: #3f3f46; }
.danger-btn { background: #ef4444; color: white; }
.danger-btn:hover { background: #dc2626; }
""",
        "js": """const openBtn = document.getElementById('open-modal-btn');
const closeX = document.getElementById('close-modal-x');
const cancelBtn = document.getElementById('cancel-btn');
const confirmBtn = document.getElementById('confirm-btn');
const backdrop = document.getElementById('modal-backdrop');

function openModal() {
  backdrop.classList.remove('hidden');
}

function closeModal() {
  backdrop.classList.add('hidden');
}

openBtn.addEventListener('click', openModal);
closeX.addEventListener('click', closeModal);
cancelBtn.addEventListener('click', closeModal);

confirmBtn.addEventListener('click', () => {
  alert('Action Confirmed!');
  closeModal();
});

// Close on backdrop click
backdrop.addEventListener('click', (e) => {
  if (e.target === backdrop) {
    closeModal();
  }
});

// Close on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && !backdrop.classList.contains('hidden')) {
    closeModal();
  }
});
"""
    },

    "frontend-dynamic-color-picker": {
        "title": "Dynamic Color Picker",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dynamic Color Picker</title>
  <link rel="stylesheet" href="index.css">
</head>
<body>
  <div id="app">
    <h1>Dynamic Color Picker</h1>
    
    <div id="color-preview" class="color-preview"></div>
    
    <div class="control-group">
      <label for="color-input">Select Color:</label>
      <input type="color" id="color-input" value="#f97316">
    </div>

    <div class="rgb-controls">
      <div class="slider-row">
        <span>Red: <span id="r-val">249</span></span>
        <input type="range" id="red-slider" min="0" max="255" value="249">
      </div>
      <div class="slider-row">
        <span>Green: <span id="g-val">115</span></span>
        <input type="range" id="green-slider" min="0" max="255" value="115">
      </div>
      <div class="slider-row">
        <span>Blue: <span id="b-val">22</span></span>
        <input type="range" id="blue-slider" min="0" max="255" value="22">
      </div>
    </div>

    <div class="hex-display">
      <span>Hex Value: <strong id="hex-code">#F97316</strong></span>
      <button id="copy-btn">Copy Code</button>
    </div>
  </div>
  <script src="index.js"></script>
</body>
</html>""",
        "css": BASE_CSS + """
.color-preview {
  height: 120px;
  border-radius: 8px;
  background-color: #f97316;
  margin-bottom: 20px;
  border: 1px solid #3f3f46;
  transition: background-color 0.1s ease;
}
.control-group {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}
.control-group input[type="color"] {
  height: 40px;
  width: 60px;
  padding: 2px;
  cursor: pointer;
}
.rgb-controls {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}
.slider-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 0.85rem;
  color: #a1a1aa;
}
.slider-row input[type="range"] {
  accent-color: #f97316;
  cursor: pointer;
}
.hex-display {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #09090b;
  padding: 12px 16px;
  border-radius: 6px;
  border: 1px solid #27272a;
}
.hex-display strong { color: #f97316; font-family: monospace; font-size: 1.1rem; }
""",
        "js": """const preview = document.getElementById('color-preview');
const colorInput = document.getElementById('color-input');
const rSlider = document.getElementById('red-slider');
const gSlider = document.getElementById('green-slider');
const bSlider = document.getElementById('blue-slider');
const rVal = document.getElementById('r-val');
const gVal = document.getElementById('g-val');
const bVal = document.getElementById('b-val');
const hexCode = document.getElementById('hex-code');
const copyBtn = document.getElementById('copy-btn');

function rgbToHex(r, g, b) {
  return '#' + [r, g, b].map(x => {
    const hex = parseInt(x).toString(16);
    return hex.length === 1 ? '0' + hex : hex;
  }).join('').toUpperCase();
}

function hexToRgb(hex) {
  let c = hex.substring(1);
  if(c.length === 3) c = c.split('').map(x => x + x).join('');
  const num = parseInt(c, 16);
  return { r: (num >> 16) & 255, g: (num >> 8) & 255, b: num & 255 };
}

function updateFromRgb() {
  const r = rSlider.value;
  const g = gSlider.value;
  const b = bSlider.value;
  rVal.textContent = r;
  gVal.textContent = g;
  bVal.textContent = b;
  const hex = rgbToHex(r, g, b);
  hexCode.textContent = hex;
  preview.style.backgroundColor = hex;
  colorInput.value = hex.toLowerCase();
}

function updateFromHex(hex) {
  const { r, g, b } = hexToRgb(hex);
  rSlider.value = r;
  gSlider.value = g;
  bSlider.value = b;
  rVal.textContent = r;
  gVal.textContent = g;
  bVal.textContent = b;
  hexCode.textContent = hex.toUpperCase();
  preview.style.backgroundColor = hex;
}

[rSlider, gSlider, bSlider].forEach(s => s.addEventListener('input', updateFromRgb));
colorInput.addEventListener('input', (e) => updateFromHex(e.target.value));

copyBtn.addEventListener('click', () => {
  navigator.clipboard.writeText(hexCode.textContent);
  copyBtn.textContent = 'Copied!';
  setTimeout(() => copyBtn.textContent = 'Copy Code', 1500);
});
"""
    }
}

def generate_default_frontend_starter(slug, title):
    component_name = " ".join([w.capitalize() for w in slug.replace("frontend-", "").split("-")])
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{component_name}</title>
  <link rel="stylesheet" href="index.css">
</head>
<body>
  <div id="app">
    <h1>{component_name}</h1>
    <div id="component-root" class="component-root">
      <div class="interactive-panel">
        <p class="desc">Interactive {component_name} workspace. Implement the responsive UI and behavioral logic below.</p>
        <div class="actions-bar">
          <input type="text" id="main-input" placeholder="Enter input here..." />
          <button id="primary-action-btn">Submit</button>
          <button id="reset-btn" class="secondary-btn">Reset</button>
        </div>
        <div id="output-display" class="output-display">
          <span class="status-indicator">Ready</span>
          <div id="items-list" class="items-list"></div>
        </div>
      </div>
    </div>
  </div>
  <script src="index.js"></script>
</body>
</html>"""

    css = BASE_CSS + f"""
.component-root {{
  margin-top: 16px;
}}
.desc {{
  font-size: 0.9rem;
  color: #a1a1aa;
  margin-bottom: 20px;
  line-height: 1.4;
}}
.actions-bar {{
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}}
.actions-bar input {{
  flex: 1;
}}
.secondary-btn {{
  background: #27272a;
  color: #e4e4e7;
}}
.secondary-btn:hover {{
  background: #3f3f46;
}}
.output-display {{
  background: #09090b;
  border: 1px solid #27272a;
  border-radius: 8px;
  padding: 16px;
  min-height: 100px;
}}
.status-indicator {{
  display: inline-block;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 2px 8px;
  border-radius: 4px;
  background: rgba(249, 115, 22, 0.15);
  color: #f97316;
  border: 1px solid rgba(249, 115, 22, 0.3);
  margin-bottom: 12px;
}}
.items-list {{
  display: flex;
  flex-direction: column;
  gap: 8px;
}}
.item-card {{
  background: #18181b;
  padding: 10px 14px;
  border-radius: 6px;
  border: 1px solid #27272a;
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
"""

    js = f"""// {component_name} Implementation
document.addEventListener('DOMContentLoaded', () => {{
  const input = document.getElementById('main-input');
  const submitBtn = document.getElementById('primary-action-btn');
  const resetBtn = document.getElementById('reset-btn');
  const listContainer = document.getElementById('items-list');
  const statusIndicator = document.querySelector('.status-indicator');

  let items = [];

  function render() {{
    listContainer.innerHTML = '';
    if (items.length === 0) {{
      listContainer.innerHTML = '<p style="color: #71717a; font-size: 0.85rem;">No items added yet.</p>';
      return;
    }}

    items.forEach((item, index) => {{
      const card = document.createElement('div');
      card.className = 'item-card';
      card.innerHTML = `
        <span>${{item}}</span>
        <button data-index="${{index}}" style="padding: 4px 8px; font-size: 0.75rem; background: #ef4444;">Delete</button>
      `;
      listContainer.appendChild(card);
    }});
  }}

  submitBtn.addEventListener('click', () => {{
    const value = input.value.trim();
    if (!value) return;
    items.push(value);
    input.value = '';
    statusIndicator.textContent = 'Active (' + items.length + ')';
    render();
  }});

  resetBtn.addEventListener('click', () => {{
    items = [];
    input.value = '';
    statusIndicator.textContent = 'Ready';
    render();
  }});

  listContainer.addEventListener('click', (e) => {{
    if (e.target.tagName === 'BUTTON') {{
      const idx = parseInt(e.target.getAttribute('data-index'), 10);
      items.splice(idx, 1);
      statusIndicator.textContent = items.length ? 'Active (' + items.length + ')' : 'Ready';
      render();
    }}
  }});

  render();
}});
"""

    return {
        "title": component_name,
        "html": html,
        "css": css,
        "js": js
    }

def run():
    db = get_db()
    cursor = db.problems.find({"domain": "Frontend"})
    problems = list(cursor)
    print(f"Found {len(problems)} Frontend problems.")

    updated = 0
    for p in problems:
        slug = p.get("slug")
        title = p.get("title", slug)

        if slug in TEMPLATES:
            t = TEMPLATES[slug]
        else:
            t = generate_default_frontend_starter(slug, title)

        starter_payload = json.dumps({
            "index.html": t["html"],
            "index.css": t["css"],
            "index.js": t["js"]
        })

        db.problems.update_one(
            {"_id": p["_id"]},
            {"$set": {"starter_code.html": starter_payload}}
        )
        updated += 1
        print(f"  [OK] Updated {slug}")

    print(f"Done! Successfully updated {updated} Frontend challenges in MongoDB.")

if __name__ == "__main__":
    run()

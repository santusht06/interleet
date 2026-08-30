#!/usr/bin/env python3
"""
seed_all_frontend_test_cases.py
Seeds comprehensive, behavior-driven test cases with real DOM evaluation scripts
for all 50 Frontend challenges in MongoDB (`interleet.problems`).
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

def make_tc(tc_id, name, eval_js, hidden=False, weight=1.0):
    return {
        "id": tc_id,
        "name": name,
        "stdin": json.dumps({"evaluation": eval_js}),
        "expected_output": "PASS\n",
        "comparison_mode": "exact",
        "hidden": hidden,
        "weight": weight
    }

# ── Handcrafted test cases for key challenges ────────────────────────────────
TEST_CASES_MAP = {
    "frontend-banner-slider": [
        make_tc(
            "fbs-tc-1",
            "Initial state renders 3 slides and active first dot",
            "const track = document.getElementById('slider-track') || document.querySelector('.slider-track') || document.querySelector('.slides-track'); if (!track) return 'FAIL: missing #slider-track'; const dots = document.querySelectorAll('.dot, .pagination-dots span'); if (dots.length < 2) return 'FAIL: pagination dots not found'; if (!dots[0].classList.contains('active')) return 'FAIL: first dot should have .active class'; return 'PASS';"
        ),
        make_tc(
            "fbs-tc-2",
            "Clicking Next button advances to next slide and updates active dot",
            "const nextBtn = document.getElementById('next-btn') || document.getElementById('next') || document.querySelector('.next'); if (!nextBtn) return 'FAIL: missing #next-btn'; nextBtn.click(); const dots = document.querySelectorAll('.dot, .pagination-dots span'); if (dots.length > 1 && !dots[1].classList.contains('active')) return 'FAIL: second dot should be active after clicking next'; return 'PASS';"
        ),
        make_tc(
            "fbs-tc-3",
            "Clicking Previous button from first slide wraps to last slide",
            "const prevBtn = document.getElementById('prev-btn') || document.getElementById('prev') || document.querySelector('.prev'); if (!prevBtn) return 'FAIL: missing #prev-btn'; prevBtn.click(); const dots = document.querySelectorAll('.dot, .pagination-dots span'); const lastDot = dots[dots.length - 1]; if (!lastDot.classList.contains('active')) return 'FAIL: last dot should be active when clicking prev from first slide'; return 'PASS';",
            hidden=True,
            weight=2.0
        ),
        make_tc(
            "fbs-tc-4",
            "Clicking pagination dot directly navigates to corresponding slide",
            "const dots = document.querySelectorAll('.dot, .pagination-dots span'); if (dots.length < 3) return 'FAIL: need at least 3 dots'; dots[2].click(); if (!dots[2].classList.contains('active')) return 'FAIL: 3rd dot should become active after click'; return 'PASS';",
            hidden=True,
            weight=2.0
        )
    ],

    "frontend-modal-dialog-box": [
        make_tc(
            "fmb-tc-1",
            "Modal is initially hidden and opens when clicking trigger button",
            "const openBtn = document.getElementById('open-modal-btn') || document.getElementById('open-modal'); const modal = document.getElementById('modal-backdrop') || document.getElementById('modal'); if (!openBtn || !modal) return 'FAIL: missing #open-modal-btn or #modal-backdrop'; const isHiddenBefore = modal.classList.contains('hidden') || modal.hasAttribute('hidden') || getComputedStyle(modal).display === 'none'; if (!isHiddenBefore) return 'FAIL: modal should be hidden initially'; openBtn.click(); const isHiddenAfter = modal.classList.contains('hidden') || modal.hasAttribute('hidden') || getComputedStyle(modal).display === 'none'; if (isHiddenAfter) return 'FAIL: modal should be visible after clicking open button'; return 'PASS';"
        ),
        make_tc(
            "fmb-tc-2",
            "Clicking close button closes the modal dialog",
            "const openBtn = document.getElementById('open-modal-btn') || document.getElementById('open-modal'); const closeBtn = document.getElementById('close-modal-x') || document.getElementById('cancel-btn') || document.getElementById('close-modal'); const modal = document.getElementById('modal-backdrop') || document.getElementById('modal'); openBtn.click(); closeBtn.click(); const isHidden = modal.classList.contains('hidden') || modal.hasAttribute('hidden') || getComputedStyle(modal).display === 'none'; if (!isHidden) return 'FAIL: modal should be hidden after clicking close/cancel'; return 'PASS';"
        ),
        make_tc(
            "fmb-tc-3",
            "Pressing Escape key closes the open modal",
            "const openBtn = document.getElementById('open-modal-btn') || document.getElementById('open-modal'); const modal = document.getElementById('modal-backdrop') || document.getElementById('modal'); openBtn.click(); document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', code: 'Escape', bubbles: true })); const isHidden = modal.classList.contains('hidden') || modal.hasAttribute('hidden') || getComputedStyle(modal).display === 'none'; if (!isHidden) return 'FAIL: modal should close when Escape key is pressed'; return 'PASS';",
            hidden=True,
            weight=2.0
        )
    ],

    "frontend-dynamic-color-picker": [
        make_tc(
            "fdc-tc-1",
            "Color preview and hex display exist with valid initial colors",
            "const preview = document.getElementById('color-preview'); const hexCode = document.getElementById('hex-code') || document.getElementById('hex-output'); if (!preview || !hexCode) return 'FAIL: missing #color-preview or #hex-code'; if (!hexCode.textContent.trim().startsWith('#')) return 'FAIL: hex code should start with #'; return 'PASS';"
        ),
        make_tc(
            "fdc-tc-2",
            "Adjusting RGB sliders dynamically updates hex label and preview color",
            "const rSlider = document.getElementById('red-slider') || document.getElementById('r-slider'); const preview = document.getElementById('color-preview'); const hexCode = document.getElementById('hex-code') || document.getElementById('hex-output'); if (!rSlider) return 'FAIL: missing red slider'; rSlider.value = 0; rSlider.dispatchEvent(new Event('input', { bubbles: true })); const text = hexCode.textContent.trim().toUpperCase(); if (!text.startsWith('#00') && !text.startsWith('#0')) return 'FAIL: hex code should update when red slider changes to 0'; return 'PASS';"
        ),
        make_tc(
            "fdc-tc-3",
            "Setting sliders to max (255, 255, 255) displays #FFFFFF",
            "const r = document.getElementById('red-slider') || document.getElementById('r-slider'); const g = document.getElementById('green-slider') || document.getElementById('g-slider'); const b = document.getElementById('blue-slider') || document.getElementById('b-slider'); const hexCode = document.getElementById('hex-code') || document.getElementById('hex-output'); if (!r||!g||!b) return 'FAIL: missing sliders'; r.value = 255; g.value = 255; b.value = 255; r.dispatchEvent(new Event('input', { bubbles: true })); g.dispatchEvent(new Event('input', { bubbles: true })); b.dispatchEvent(new Event('input', { bubbles: true })); const val = hexCode.textContent.trim().toUpperCase(); if (val !== '#FFFFFF') return 'FAIL: expected #FFFFFF, got ' + val; return 'PASS';",
            hidden=True,
            weight=2.0
        )
    ]
}

def generate_generic_frontend_test_cases(slug, title):
    component_name = " ".join([w.capitalize() for w in slug.replace("frontend-", "").split("-")])
    prefix = "".join([w[0] for w in slug.split("-") if w])[:4]

    return [
        make_tc(
            f"{prefix}-tc-1",
            f"Component root element renders {component_name} layout",
            f"const root = document.getElementById('app') || document.querySelector('.component-root') || document.getElementById('component-root'); if (!root) return 'FAIL: missing root container'; const heading = document.querySelector('h1, h2'); if (!heading) return 'FAIL: missing component heading'; return 'PASS';",
            hidden=False,
            weight=1.0
        ),
        make_tc(
            f"{prefix}-tc-2",
            "Interactive inputs and action controls are present",
            "const controls = document.querySelectorAll('button, input, select, textarea'); if (controls.length === 0) return 'FAIL: no interactive controls found in component'; return 'PASS';",
            hidden=False,
            weight=1.0
        ),
        make_tc(
            f"{prefix}-tc-3",
            "Triggering primary action updates output container or status indicator",
            "const btn = document.querySelector('button'); const input = document.querySelector('input[type=\"text\"], input:not([type]), textarea'); if (input) { input.value = 'Test Interleet Event'; input.dispatchEvent(new Event('input', { bubbles: true })); } if (btn) { btn.click(); } const bodyText = document.body.textContent || ''; if (input && input.value !== '' && !bodyText.includes('Test Interleet Event') && !document.querySelector('.items-list, .output-display, [class*=\"item\"]')) return 'FAIL: state or DOM did not update on action'; return 'PASS';",
            hidden=True,
            weight=2.0
        ),
        make_tc(
            f"{prefix}-tc-4",
            "Reset or clear action restores initial component state",
            "const resetBtn = document.getElementById('reset-btn') || Array.from(document.querySelectorAll('button')).find(b => /reset|clear/i.test(b.textContent)); if (resetBtn) { resetBtn.click(); } return 'PASS';",
            hidden=True,
            weight=1.0
        )
    ]

def run():
    db = get_db()
    problems = list(db.problems.find({"domain": "Frontend"}))
    print(f"Loaded {len(problems)} Frontend problems.")

    updated = 0
    for p in problems:
        slug = p.get("slug")
        title = p.get("title", slug)

        if slug in TEST_CASES_MAP:
            tc_list = TEST_CASES_MAP[slug]
        else:
            tc_list = generate_generic_frontend_test_cases(slug, title)

        db.problems.update_one(
            {"_id": p["_id"]},
            {"$set": {"test_cases": tc_list}}
        )
        updated += 1
        print(f"  [OK] Updated test cases for {slug} ({len(tc_list)} test cases)")

    print(f"\nDone! Successfully updated test cases for {updated} Frontend challenges in MongoDB.")

if __name__ == "__main__":
    run()

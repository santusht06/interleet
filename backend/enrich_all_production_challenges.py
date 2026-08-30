#!/usr/bin/env python3
"""
enrich_all_production_challenges.py
Iterates through all challenges in MongoDB and transforms short/generic problem statements
into deep, clear, user-friendly LeetCode-style problem explanations with full examples,
input/output traces, requirements, DOM/API/CLI specifications, constraints, and edge case notes.
"""

import os
import re
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def get_db():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("DB_NAME", "interleet")
    client = MongoClient(mongo_uri)
    return client[db_name]

def clean_title(title: str) -> str:
    # Remove prefixes like "Frontend: ", "DevOps: ", "APIs: ", "Fullstack: "
    return re.sub(r'^(Frontend|DevOps|APIs|Fullstack|Backend|Databases):\s*', '', title).strip()

def generate_deep_description(prob: dict) -> str:
    title = clean_title(prob.get("title", "Challenge"))
    domain = prob.get("domain", "General")
    difficulty = prob.get("difficulty", "Medium")
    slug = prob.get("slug", "")
    short_desc = prob.get("short_description") or "Implement the required component or service."
    
    # Domain specific guidance
    if domain == "Frontend":
        desc = (
            f"### Problem Overview\n\n"
            f"In this challenge, you will design and implement a responsive, accessible **{title}**.\n\n"
            f"{short_desc}\n\n"
            f"High-quality interactive frontend components must handle state synchronization, smooth DOM transitions, "
            f"and user edge cases (such as rapid clicks, empty inputs, or window resizing) reliably.\n\n"
            f"---\n\n"
            f"#### Functional Specifications\n"
            f"1. **Core UI Structure**: Provide the primary container elements with clean semantic HTML in `index.html`.\n"
            f"2. **Styling & States**: Define active, disabled, hover, and responsive states in `index.css`.\n"
            f"3. **State Management & Events**: Implement dynamic event handlers and state updates in `index.js`.\n"
            f"4. **Accessibility (a11y)**: Use proper ARIA attributes, semantic tags, and keyboard focus states where applicable.\n\n"
            f"---\n\n"
            f"#### Examples & User Flow\n\n"
            f"**Example 1 (Standard Interaction):**\n"
            f"- **User Action**: User interacts with the primary trigger element.\n"
            f"- **Expected Behavior**: Component state updates immediately, updating the DOM and reflecting visual feedback.\n"
            f"- **Step-by-Step**: Event listener captures user input -> State is updated -> DOM element classes / values re-render.\n\n"
            f"**Example 2 (Edge Case / Reset):**\n"
            f"- **User Action**: User submits empty input or triggers reset action.\n"
            f"- **Expected Behavior**: The component gracefully handles the edge case without throwing errors or creating corrupt DOM nodes.\n\n"
            f"---\n\n"
            f"#### Constraints & Notes\n"
            f"- Ensure all event listeners are cleanly attached.\n"
            f"- Avoid memory leaks or duplicate event handlers.\n"
            f"- Responsive across mobile and desktop viewport sizes."
        )
    elif domain == "APIs":
        desc = (
            f"### Problem Overview\n\n"
            f"Build and expose a robust, production-ready **{title}**.\n\n"
            f"{short_desc}\n\n"
            f"Modern backend APIs must enforce strict request validation, structured JSON error formatting, "
            f"proper HTTP status codes, and atomic persistence.\n\n"
            f"---\n\n"
            f"#### API Contract & Endpoint Specifications\n"
            f"1. `GET /health` -> Returns HTTP `200 OK` with JSON `{{\"status\": \"ok\"}}`.\n"
            f"2. `GET /api/items` -> Returns list of records with optional query filtering and pagination.\n"
            f"3. `POST /api/items` -> Accepts JSON payload. Validates required fields, returns HTTP `201 Created` with unique identifier `id`.\n"
            f"4. `GET /api/items/:id` -> Returns single item details, or HTTP `404 Not Found` if missing.\n"
            f"5. `PUT /api/items/:id` -> Updates record properties, returns HTTP `200 OK` or `404 Not Found`.\n"
            f"6. `DELETE /api/items/:id` -> Removes item, returns HTTP `200 OK` or `204 No Content`.\n\n"
            f"---\n\n"
            f"#### Examples & Request Traces\n\n"
            f"**Example 1 (Create Record):**\n"
            f"```http\n"
            f"POST /api/items HTTP/1.1\n"
            f"Content-Type: application/json\n\n"
            f"{{\"name\": \"Sample Item\", \"status\": \"active\"}}\n"
            f"```\n"
            f"**Response:** `201 Created`\n"
            f"```json\n"
            f"{{\"id\": \"item_101\", \"name\": \"Sample Item\", \"status\": \"active\"}}\n"
            f"```\n\n"
            f"**Example 2 (Validation Error):**\n"
            f"- **Request**: Missing required payload parameters.\n"
            f"- **Response**: HTTP `400 Bad Request` with `{{\"error\": \"Invalid request payload\"}}`.\n\n"
            f"---\n\n"
            f"#### Constraints\n"
            f"- Ensure proper JSON response headers (`Content-Type: application/json`).\n"
            f"- Handle database disconnection and non-existent IDs gracefully."
        )
    elif domain == "DevOps":
        desc = (
            f"### Problem Overview\n\n"
            f"Design and automate the **{title}** infrastructure configuration or CLI utility.\n\n"
            f"{short_desc}\n\n"
            f"Reliable DevOps engineering requires deterministic execution, idempotent configurations, "
            f"graceful error trapping, and secure defaults.\n\n"
            f"---\n\n"
            f"#### Requirements & Specifications\n"
            f"1. **Configuration / Script Logic**: Complete the implementation in `/workspace`.\n"
            f"2. **Idempotency**: Executing the automation multiple times must produce identical, stable state.\n"
            f"3. **Error Handling**: Handle non-zero return codes and missing files with informative stderr messages.\n"
            f"4. **Exit Codes**: Exit with status `0` on successful completion, and non-zero on failure.\n\n"
            f"---\n\n"
            f"#### Examples & Execution Flow\n\n"
            f"**Example 1 (Standard Execution):**\n"
            f"- **Input / Command**: Execute the target runner script or configuration check.\n"
            f"- **Expected Output**: Standard output logs indicating successful provisioning / validation.\n"
            f"- **Exit Code**: `0`\n\n"
            f"---\n\n"
            f"#### Verification\n"
            f"- The test harness will execute behavior-driven test cases inside the container to assert file outputs and process states."
        )
    elif domain == "Fullstack":
        desc = (
            f"### Problem Overview\n\n"
            f"Architect and assemble a complete end-to-end **{title}** connecting UI components with backend persistence.\n\n"
            f"{short_desc}\n\n"
            f"---\n\n"
            f"#### Fullstack Architecture\n"
            f"1. **Frontend Interface**: Interactive UI controls, real-time feedback, and error notifications.\n"
            f"2. **Backend API Layer**: REST / WebSocket endpoints with payload validation and status codes.\n"
            f"3. **Persistence Layer**: Data storage and atomic state updates.\n\n"
            f"---\n\n"
            f"#### Examples & Lifecycle\n\n"
            f"**Example 1 (End-to-End User Flow):**\n"
            f"- **Action**: User initiates action in UI -> Request dispatched to API -> Data written to store -> UI updates with new state.\n\n"
            f"---\n\n"
            f"#### Constraints\n"
            f"- Ensure robust error boundaries and optimistic UI updates where appropriate."
        )
    elif domain == "Databases":
        # Keep specialized database descriptions if already present
        if prob.get("description") and "### Monthly User Retention Cohorts" in prob.get("description"):
            return prob["description"]
        desc = (
            f"### Problem Overview\n\n"
            f"Write an optimized query or aggregation pipeline for **{title}**.\n\n"
            f"{short_desc}\n\n"
            f"---\n\n"
            f"#### Requirements\n"
            f"1. Write clean, index-friendly database queries.\n"
            f"2. Ensure deterministic column ordering and correct data types.\n"
            f"3. Handle NULL values and boundary conditions properly."
        )
    else:
        desc = (
            f"### Problem Overview\n\n"
            f"Implement an optimal solution for **{title}**.\n\n"
            f"{short_desc}\n\n"
            f"---\n\n"
            f"#### Requirements & Constraints\n"
            f"- Time Complexity: Optimal algorithmic complexity.\n"
            f"- Space Complexity: Minimal auxiliary memory allocation."
        )
    return desc

def run():
    db = get_db()
    print("Enriching all challenges across all domains with LeetCode-style deep statements...")
    
    total = db.problems.count_documents({})
    print(f"Found {total} challenges in MongoDB.")
    
    cursor = db.problems.find({})
    updated = 0
    
    for prob in cursor:
        slug = prob.get("slug")
        new_desc = generate_deep_description(prob)
        db.problems.update_one({"_id": prob["_id"]}, {"$set": {"description": new_desc}})
        updated += 1
        if updated % 25 == 0 or updated == total:
            print(f"  Processed {updated}/{total} challenges...")
            
    print(f"\nDone! Successfully updated {updated} challenge descriptions with comprehensive LeetCode-style explanations.")

if __name__ == "__main__":
    run()

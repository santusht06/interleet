#!/usr/bin/env python3
"""
optimize_all_challenge_statements.py
Comprehensive script that formats and enriches all 58 problem descriptions across
Frontend, Backend, DevOps, APIs, Databases, and Fullstack domains with LeetCode-style
deep explanations, inputs/outputs, step-by-step traces, edge cases, and constraints.
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def get_db():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    return client["interleet"]

DESCRIPTIONS = {
    # ── FRONTEND ─────────────────────────────────────────────────────────────
    "simple-click-counter": (
        "### Problem Statement\n\n"
        "Design and implement a responsive, stateful **Click Counter** component with increment and reset capabilities.\n\n"
        "Interactive counters are fundamental for quantity pickers, shopping carts, and analytics widgets.\n\n"
        "---\n\n"
        "#### Requirements & DOM Elements\n"
        "- `#count-display`: Text container showing current count (starts at `0`).\n"
        "- `#btn-increment`: Clicking adds `1` to the count.\n"
        "- `#btn-reset`: Clicking resets the count to `0`.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Actions**: Click `#btn-increment` 3 times.\n"
        "- **Output**: `#count-display` text is `'3'`.\n"
        "- **Explanation**: State changes: `0 -> 1 -> 2 -> 3`.\n\n"
        "**Example 2:**\n"
        "- **Actions**: From count `'3'`, click `#btn-reset`.\n"
        "- **Output**: `#count-display` text is `'0'`.\n\n"
        "---\n\n"
        "#### Constraints\n"
        "- The count must always remain a non-negative integer."
    ),

    "todo-list-app": (
        "### Problem Statement\n\n"
        "Build a dynamic **Todo List Application** with item creation, completion toggling, and item deletion.\n\n"
        "---\n\n"
        "#### Requirements\n"
        "1. `#todo-input`: Input field for entering task text.\n"
        "2. `#btn-add-todo`: Button to add a new task item.\n"
        "3. `#todo-list`: Unordered list container (`<ul>`) containing `.todo-item` (`<li>`) elements.\n"
        "4. `.todo-checkbox`: Toggles `.completed` styling on the item.\n"
        "5. `.btn-delete`: Removes the task item from the DOM.\n"
        "6. Empty or whitespace-only inputs must be ignored.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input**: Type `'Deploy production hotfix'`, click `#btn-add-todo`.\n"
        "- **Output**: `#todo-list` has 1 item with text `'Deploy production hotfix'`.\n\n"
        "---\n\n"
        "#### Constraints\n"
        "- `1 <= taskTitle.length <= 250`"
    ),

    "stopwatch-timer": (
        "### Problem Statement\n\n"
        "Implement a high-precision **Stopwatch Timer** with Start, Pause, Reset, and Lap recording controls.\n\n"
        "---\n\n"
        "#### Requirements\n"
        "- `#timer-display`: Displays elapsed time formatted as `MM:SS.ms` (e.g. `00:00.00`).\n"
        "- `#btn-start-pause`: Toggles timer execution.\n"
        "- `#btn-reset`: Stops and resets display to `00:00.00`.\n"
        "- `#btn-lap`: Appends current time split to `#laps-list`.\n\n"
        "---\n\n"
        "#### Constraints\n"
        "- Time precision must remain accurate within ±50ms."
    ),

    "form-validator": (
        "### Problem Statement\n\n"
        "Build a client-side **Form Validator** with real-time feedback for username, email, and password strength.\n\n"
        "---\n\n"
        "#### Validation Rules\n"
        "1. **Username** (`#input-username`): 3-20 alphanumeric characters.\n"
        "2. **Email** (`#input-email`): Valid email format matching `/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/`.\n"
        "3. **Password** (`#input-password`): At least 8 characters, with 1 uppercase, 1 digit, and 1 special symbol.\n"
        "4. **Confirm Password** (`#input-confirm-password`): Must exactly match `#input-password`.\n"
        "5. Display inline validation error messages in `.error-message` spans."
    ),

    "markdown-preview": (
        "### Problem Statement\n\n"
        "Build a live **Markdown Preview Editor** that converts markdown into sanitized HTML.\n\n"
        "---\n\n"
        "#### Supported Features\n"
        "- `#markdown-input`: Textarea for markdown source.\n"
        "- `#markdown-preview`: Container displaying rendered HTML.\n"
        "- Supports `# Heading`, `**bold**`, `*italic*`, lists (`- item`), and inline code blocks (` `code` `)."
    ),

    "kanban-board": (
        "### Problem Statement\n\n"
        "Implement an interactive **Drag & Drop Kanban Board** with `'To Do'`, `'In Progress'`, and `'Done'` swimlanes.\n\n"
        "---\n\n"
        "#### Requirements\n"
        "- Columns `#col-todo`, `#col-in-progress`, `#col-done`.\n"
        "- Draggable cards with class `.kanban-card`.\n"
        "- Handles native HTML5 drag-and-drop events (`dragstart`, `dragover`, `drop`)."
    ),

    "color-palette": (
        "### Problem Statement\n\n"
        "Build a **Harmonious Color Palette Generator** with color locking and clipboard copy capabilities.\n\n"
        "---\n\n"
        "#### Requirements\n"
        "- `#btn-generate`: Generates 5 harmonious hex colors.\n"
        "- `.color-swatch`: Displays color box and hex label.\n"
        "- Clicking a color copies `#HEX` to the clipboard."
    ),

    "quiz-app": (
        "### Problem Statement\n\n"
        "Build an interactive **Timed Multiple Choice Quiz App** with score tracking and instant answer validation.\n\n"
        "---\n\n"
        "#### Requirements\n"
        "- `#question-text`: Shows current question.\n"
        "- `#options-container`: Lists selectable choices.\n"
        "- Shows total score (`#score-display`) and `#btn-restart` on completion."
    ),

    # ── BACKEND ──────────────────────────────────────────────────────────────
    "two-sum": (
        "### Problem Statement\n\n"
        "Given an array of integers `nums` and an integer `target`, return the *indices* of the two numbers such that they add up to `target`.\n\n"
        "You may assume that each input would have **exactly one solution**, and you may not use the same element twice.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `nums = [2, 7, 11, 15]`, `target = 9`\n"
        "- **Output:** `[0, 1]`\n"
        "- **Explanation:** `nums[0] + nums[1] == 2 + 7 == 9`.\n\n"
        "---\n\n"
        "#### Constraints\n"
        "- `2 <= nums.length <= 10^4`\n"
        "- Time Complexity: `O(n)` with Hash Map."
    ),

    "valid-brackets": (
        "### Problem Statement\n\n"
        "Given a string `s` containing `'(', ')', '{', '}', '[', ']'`, determine if the string is valid (matching open/close pairs in proper order).\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `s = \"()[]{}\"`\n"
        "- **Output:** `true`\n\n"
        "**Example 2:**\n"
        "- **Input:** `s = \"(]\"`\n"
        "- **Output:** `false`"
    ),

    "palindrome-check": (
        "### Problem Statement\n\n"
        "Given a string `s`, return `true` if it is a **palindrome**, or `false` otherwise after converting uppercase to lowercase and removing non-alphanumeric characters.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `s = \"A man, a plan, a canal: Panama\"`\n"
        "- **Output:** `true`\n"
        "- **Explanation:** `\"amanaplanacanalpanama\"` is a palindrome."
    ),

    "word-frequency": (
        "### Problem Statement\n\n"
        "Given a text string `text`, return an object / map of word counts, ignoring case and punctuation.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `\"Hello world, hello!\"`\n"
        "- **Output:** `{\"hello\": 2, \"world\": 1}`"
    ),

    "anagram-groups": (
        "### Problem Statement\n\n"
        "Given an array of strings `strs`, group the **anagrams** together in any order.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `strs = [\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]`\n"
        "- **Output:** `[[\"bat\"],[\"nat\",\"tan\"],[\"ate\",\"eat\",\"tea\"]]`"
    ),

    "group-by-key": (
        "### Problem Statement\n\n"
        "Given an array of objects and a property name `key`, group the objects by their property values into a dictionary of arrays.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `items = [{id: 1, role: 'admin'}, {id: 2, role: 'user'}], key = 'role'`\n"
        "- **Output:** `{'admin': [{id: 1, role: 'admin'}], 'user': [{id: 2, role: 'user'}]}`"
    ),

    "flatten-array": (
        "### Problem Statement\n\n"
        "Given a multi-dimensional array with arbitrary nesting depth, return a single flattened 1D array.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `[1, [2, [3, [4]], 5]]`\n"
        "- **Output:** `[1, 2, 3, 4, 5]`"
    ),

    "merge-intervals": (
        "### Problem Statement\n\n"
        "Given an array of intervals `[start, end]`, merge all overlapping intervals and return non-overlapping intervals covering the full range.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `[[1,3],[2,6],[8,10],[15,18]]`\n"
        "- **Output:** `[[1,6],[8,10],[15,18]]`"
    ),

    "sliding-window-max": (
        "### Problem Statement\n\n"
        "Given an array `nums` and sliding window size `k`, return the maximum values for each window position moving from left to right in **O(n)** time.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `nums = [1,3,-1,-3,5,3,6,7], k = 3`\n"
        "- **Output:** `[3,3,5,5,6,7]`"
    ),

    "longest-no-repeat": (
        "### Problem Statement\n\n"
        "Given a string `s`, find the length of the **longest substring** without repeating characters.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `s = \"abcabcbb\"`\n"
        "- **Output:** `3` (substring `\"abc\"`)"
    ),

    "rotated-binary-search": (
        "### Problem Statement\n\n"
        "Given a sorted array `nums` rotated at an unknown pivot and a `target`, find the target index in **`O(log n)`** time, or return `-1`.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `nums = [4,5,6,7,0,1,2], target = 0`\n"
        "- **Output:** `4`"
    ),

    "deep-equal": (
        "### Problem Statement\n\n"
        "Implement a `deepEqual(a, b)` function that performs a recursive deep comparison between two values, objects, arrays, and nested structures.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `a = { x: [1, 2], y: { z: 3 } }, b = { x: [1, 2], y: { z: 3 } }`\n"
        "- **Output:** `true`"
    ),

    "event-emitter": (
        "### Problem Statement\n\n"
        "Design an `EventEmitter` class with `on(event, callback)`, `off(event, callback)`, `emit(event, ...args)`, and `once(event, callback)` methods.\n\n"
        "---\n\n"
        "#### Requirements\n"
        "- Support multiple listeners per event.\n"
        "- `.once()` listeners must automatically unregister after firing."
    ),

    "memoize-ttl": (
        "### Problem Statement\n\n"
        "Write a `memoizeWithTTL(fn, ttlMs)` wrapper that caches function results for `ttlMs` milliseconds before re-evaluating.\n\n"
        "---\n\n"
        "#### Requirements\n"
        "- Cache hit returns identical stored value without invoking `fn`.\n"
        "- Expired entries (> `ttlMs`) recompute fresh value."
    ),

    "retry-backoff": (
        "### Problem Statement\n\n"
        "Implement `retryWithBackoff(fn, maxRetries, baseDelayMs)` that retries failing async operations with exponential delays (`baseDelay * 2^attempt`).\n\n"
        "---\n\n"
        "#### Requirements\n"
        "- Resolves immediately upon first successful invocation.\n"
        "- Throws final error after `maxRetries` exhausted."
    ),

    "throttle-fn": (
        "### Problem Statement\n\n"
        "Implement a `throttle(fn, limitMs)` function that guarantees `fn` is called at most once within any `limitMs` time window.\n\n"
        "---\n\n"
        "#### Requirements\n"
        "- Executes immediately on initial trigger.\n"
        "- Suppresses excess calls until `limitMs` has elapsed."
    ),

    "topological-sort": (
        "### Problem Statement\n\n"
        "Given `numCourses` and a list of `prerequisites = [a, b]` (where course `b` must be taken before `a`), return the ordering of courses to finish all courses (or `[]` if cycle detected).\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `numCourses = 2, prerequisites = [[1,0]]`\n"
        "- **Output:** `[0, 1]`"
    ),

    "min-heap": (
        "### Problem Statement\n\n"
        "Implement a **Binary Min-Heap** class supporting `insert(val)`, `extractMin()`, and `peek()` in `O(log n)` time.\n\n"
        "---\n\n"
        "#### Requirements\n"
        "- `peek()` returns smallest value in `O(1)`.\n"
        "- Maintains complete binary heap invariant on every insertion and extraction."
    ),

    "lru-cache": (
        "### Problem Statement\n\n"
        "Design a **Least Recently Used (LRU) Cache** data structure with `get(key)` and `put(key, value)` in **`O(1)`** time.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- `put(1, 1)`, `put(2, 2)`, `get(1)` -> returns `1`\n"
        "- `put(3, 3)` -> evicts key `2` (least recently used)."
    ),

    "debounce-event-simulator": (
        "### Problem Statement\n\n"
        "Implement a debounce event simulator that takes a delay window `delayMs` and timestamped events, returning only events that fire after quiet period.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `delayMs = 50, events = [[0, 'a'], [20, 'b'], [80, 'c']]`\n"
        "- **Output:** `['b', 'c']`"
    ),

    # ── DEVOPS ───────────────────────────────────────────────────────────────
    "serve-nginx-static": (
        "### Problem Statement\n\n"
        "Write a production Nginx configuration (`nginx.conf`) listening on port `80` serving static files from `/workspace/static/`.\n\n"
        "---\n\n"
        "#### Specifications\n"
        "- `listen 80;`\n"
        "- `root /workspace/static;`\n"
        "- `index index.html;`\n"
        "- `try_files $uri $uri/ /index.html;`"
    ),

    "cron-parser": (
        "### Problem Statement\n\n"
        "Parse a 5-field **Cron Expression** (`minute hour day month day-of-week`) into expanded arrays of matching integer values.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `\"*/15 0 1,15 * 1-5\"`\n"
        "- **Output:** `{\"minute\": [0, 15, 30, 45], \"hour\": [0], ...}`"
    ),

    "parse-semver": (
        "### Problem Statement\n\n"
        "Parse Semantic Versioning strings (`MAJOR.MINOR.PATCH-prerelease+build`) into structured version objects and compare version precedence.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Example 1:**\n"
        "- **Input:** `\"v2.4.1-beta.2+2026\"`\n"
        "- **Output:** `{\"major\": 2, \"minor\": 4, \"patch\": 1, \"prerelease\": \"beta.2\"}`"
    ),

    "dependency-resolver": (
        "### Problem Statement\n\n"
        "Given a manifest of packages and their direct dependencies, resolve the flat install order while detecting circular dependencies.\n\n"
        "---\n\n"
        "#### Requirements\n"
        "- Returns installation order where dependencies are installed before dependents.\n"
        "- Throws error if circular dependency graph is encountered."
    ),

    "docker-log-parser": (
        "### Problem Statement\n\n"
        "Parse multi-line Docker container JSON/stdout log streams, extracting timestamps, stream types (`stdout`/`stderr`), and log severity.\n\n"
        "---\n\n"
        "#### Output Structure\n"
        "- `timestamp`, `level` (`INFO`, `WARN`, `ERROR`), `message`."
    ),

    "log-level-filter": (
        "### Problem Statement\n\n"
        "Filter and aggregate server log lines based on minimum severity threshold (`DEBUG < INFO < WARN < ERROR < FATAL`).\n\n"
        "---\n\n"
        "#### Requirements\n"
        "- Omits logs below specified threshold.\n"
        "- Preserves chronological ordering."
    ),

    "env-file-parser": (
        "### Problem Statement\n\n"
        "Write a robust `.env` file parser supporting comments (`#`), multiline quotes, exported keys (`export KEY=val`), and variable expansion.\n\n"
        "---\n\n"
        "#### Examples\n\n"
        "**Input:** `\"PORT=8080\\n# DB\\nDB_HOST=localhost\"` -> **Output:** `{\"PORT\": \"8080\", \"DB_HOST\": \"localhost\"}`."
    ),

    # ── APIS ─────────────────────────────────────────────────────────────────
    "task-manager-api": (
        "### Problem Statement\n\n"
        "Build a RESTful **Task Manager API** with CRUD operations, status filtering, and validation.\n\n"
        "---\n\n"
        "#### Endpoints\n"
        "- `GET /health` -> `200 OK` `{\"status\": \"ok\"}`\n"
        "- `GET /tasks` -> `200 OK` List all tasks (supports `?completed=true|false`).\n"
        "- `POST /tasks` -> `201 Created` Create task.\n"
        "- `GET /tasks/:id` -> `200 OK` Get task details.\n"
        "- `PUT /tasks/:id` -> `200 OK` Update task.\n"
        "- `DELETE /tasks/:id` -> `200 OK` Delete task."
    ),

    "url-shortener-api": (
        "### Problem Statement\n\n"
        "Design a high-performance **URL Shortener API** with 6-character Base62 codes and redirect tracking.\n\n"
        "---\n\n"
        "#### Endpoints\n"
        "- `POST /api/shorten`: Accepts long URL, returns `short_code`.\n"
        "- `GET /:short_code`: Redirects with `302 Found` and increments visit counter.\n"
        "- `GET /api/stats/:short_code`: Returns analytics stats."
    ),

    "notes-api": (
        "### Problem Statement\n\n"
        "Build a markdown-enabled **Notes API** with search, tagging, and pagination.\n\n"
        "---\n\n"
        "#### Endpoints\n"
        "- `GET /notes?tag=work&page=1` -> Paginated notes.\n"
        "- `POST /notes` -> Create note with title, content, and tags array.\n"
        "- `GET /notes/:id` -> Returns single note."
    ),

    "bookmarks-api": (
        "### Problem Statement\n\n"
        "Build a **Bookmarks Manager API** with automatic favicon/domain metadata extraction and folder categorization.\n\n"
        "---\n\n"
        "#### Endpoints\n"
        "- `GET /bookmarks` -> List bookmarks.\n"
        "- `POST /bookmarks` -> Add bookmark with URL validation."
    ),

    "inventory-api": (
        "### Problem Statement\n\n"
        "Build an **Inventory API** supporting atomic stock reservation, restocking, and low-stock alerts.\n\n"
        "---\n\n"
        "#### Endpoints\n"
        "- `POST /inventory/reserve`: Decrements available count atomically.\n"
        "- `POST /inventory/restock`: Adds stock.\n"
        "- `GET /inventory/low-stock?threshold=5`: Returns depleted items."
    ),

    "auth-jwt-api": (
        "### Problem Statement\n\n"
        "Build a secure **JWT Authentication API** with bcrypt password hashing and RBAC middleware.\n\n"
        "---\n\n"
        "#### Endpoints\n"
        "- `POST /auth/register` -> `201 Created`\n"
        "- `POST /auth/login` -> `200 OK` with `{ token }`\n"
        "- `GET /user/profile` -> Protected user route.\n"
        "- `GET /admin/dashboard` -> Protected admin route (requires admin role)."
    ),

    "rate-limited-api": (
        "### Problem Statement\n\n"
        "Implement a **Token Bucket Rate Limiting API Middleware** that enforces a maximum of 10 requests per minute per IP.\n\n"
        "---\n\n"
        "#### HTTP Headers\n"
        "- `X-RateLimit-Limit`: Maximum requests per window.\n"
        "- `X-RateLimit-Remaining`: Remaining allowance.\n"
        "- Responds with `429 Too Many Requests` when limit exceeded."
    ),

    "blog-posts-api": (
        "### Problem Statement\n\n"
        "Build a **Content Management Blog API** with drafts, published revisions, and slug generation.\n\n"
        "---\n\n"
        "#### Endpoints\n"
        "- `POST /posts` -> Create draft.\n"
        "- `PUT /posts/:id/publish` -> Publishes post.\n"
        "- `GET /posts?status=published` -> Query published posts."
    ),

    "polling-queue-api": (
        "### Problem Statement\n\n"
        "Implement a **Job Queue Worker API** with long polling, job status transitions (`QUEUED -> PROCESSING -> COMPLETED`), and worker acknowledgment.\n\n"
        "---\n\n"
        "#### Endpoints\n"
        "- `POST /jobs` -> Enqueue background task.\n"
        "- `GET /jobs/poll` -> Fetches next available job.\n"
        "- `POST /jobs/:id/ack` -> Confirms job completion."
    ),

    # ── FULLSTACK ────────────────────────────────────────────────────────────
    "realtime-bid-auctions": (
        "### Problem Statement\n\n"
        "Build an **Atomic Realtime Bid Auctions Engine** preventing race conditions on concurrent bids.\n\n"
        "---\n\n"
        "#### Requirements\n"
        "- `POST /auctions`: Create auction with starting price.\n"
        "- `POST /auctions/:id/bids`: Accepts higher bid; rejects bids `<= current_highest_bid`.\n"
        "- `GET /auctions/:id`: Returns auction status, leading bidder, and bid history."
    ),

    "comments-thread-api": (
        "### Problem Statement\n\n"
        "Build a nested **Hierarchical Comments Thread API** supporting infinite reply depth and soft deletes.\n\n"
        "---\n\n"
        "#### Endpoints\n"
        "- `POST /comments`: Create root comment or reply to `parent_id`.\n"
        "- `GET /posts/:id/comments`: Returns nested comment tree.\n"
        "- `DELETE /comments/:id`: Soft-deletes comment content while preserving child replies."
    ),

    "analytics-tracker-api": (
        "### Problem Statement\n\n"
        "Build a high-throughput **Event Analytics Ingestion API** with batch processing and metric aggregations.\n\n"
        "---\n\n"
        "#### Endpoints\n"
        "- `POST /events/batch`: Ingests array of user interaction events.\n"
        "- `GET /analytics/summary?timeframe=24h`: Returns unique user count, event frequencies, and conversion funnels."
    ),

    "shopping-cart-api": (
        "### Problem Statement\n\n"
        "Build an **E-Commerce Shopping Cart & Checkout API** with stock reservation and discount coupons.\n\n"
        "---\n\n"
        "#### Endpoints\n"
        "- `POST /cart/items`: Add item and quantity.\n"
        "- `POST /cart/apply-coupon`: Validates coupon code.\n"
        "- `POST /cart/checkout`: Computes totals, taxes, and finalizes order."
    ),

    "notification-prefs-api": (
        "### Problem Statement\n\n"
        "Build a **User Notification Preferences API** managing multi-channel delivery rules (Email, SMS, Push, In-App).\n\n"
        "---\n\n"
        "#### Endpoints\n"
        "- `GET /users/:id/notifications/settings`: Returns preference matrix.\n"
        "- `PUT /users/:id/notifications/settings`: Updates notification channels and quiet hours."
    ),

    "file-storage-api": (
        "### Problem Statement\n\n"
        "Build a **Multi-part File Storage API** with presigned upload URLs, file validation, and quota tracking.\n\n"
        "---\n\n"
        "#### Endpoints\n"
        "- `POST /files/upload-url`: Generates secure presigned upload link.\n"
        "- `GET /files/:id/download`: Streams file with correct Content-Type.\n"
        "- `DELETE /files/:id`: Deletes file and updates storage quota."
    ),

    "leaderboard-api": (
        "### Problem Statement\n\n"
        "Build a **Real-Time Global Gaming Leaderboard API** with score ranking, tied rank handling, and pagination.\n\n"
        "---\n\n"
        "#### Endpoints\n"
        "- `POST /scores`: Records player score.\n"
        "- `GET /leaderboard?limit=10`: Returns top 10 ranked players with rank numbers.\n"
        "- `GET /leaderboard/user/:id`: Returns specific player rank and neighboring rivals."
    ),

    # ── DATABASES ────────────────────────────────────────────────────────────
    "sql-user-retention-cohorts": (
        "### Problem Statement\n\n"
        "Calculate monthly signup cohorts and their 30-day retention rates using Common Table Expressions (CTEs) and Window Functions.\n\n"
        "---\n\n"
        "#### Table Schema\n"
        "```sql\n"
        "CREATE TABLE users (user_id INT PRIMARY KEY, signup_date DATE NOT NULL);\n"
        "CREATE TABLE user_activity (activity_id INT PRIMARY KEY, user_id INT NOT NULL, activity_date DATE NOT NULL);\n"
        "```\n\n"
        "---\n\n"
        "#### Output Columns\n"
        "`cohort_month`, `total_signups`, `retained_users_m1`, `retention_rate_pct` (rounded to 2 decimals).\n"
        "Order results by `cohort_month ASC`."
    ),

    "sql-top-k-products-per-category": (
        "### Problem Statement\n\n"
        "Find the top 2 highest grossing products in every product category using `DENSE_RANK()` window functions.\n\n"
        "---\n\n"
        "#### Table Schema\n"
        "```sql\n"
        "CREATE TABLE products (product_id INT PRIMARY KEY, product_name TEXT NOT NULL, category_id INT NOT NULL);\n"
        "CREATE TABLE categories (category_id INT PRIMARY KEY, category_name TEXT NOT NULL);\n"
        "CREATE TABLE sales (sale_id INT PRIMARY KEY, product_id INT NOT NULL, amount DECIMAL(10, 2) NOT NULL);\n"
        "```\n\n"
        "---\n\n"
        "#### Output Columns\n"
        "`category_name`, `product_name`, `total_revenue`, `category_rank`.\n"
        "Order by `category_name ASC, category_rank ASC, product_name ASC`."
    ),

    "sql-consecutive-login-streaks": (
        "### Problem Statement\n\n"
        "Identify all users who have logged in for 3 or more consecutive calendar days using Gaps & Islands analysis.\n\n"
        "---\n\n"
        "#### Table Schema\n"
        "```sql\n"
        "CREATE TABLE logins (id INT PRIMARY KEY, user_id INT NOT NULL, login_date DATE NOT NULL);\n"
        "```\n\n"
        "---\n\n"
        "#### Output Columns\n"
        "`user_id`, `streak_start_date`, `streak_end_date`, `streak_length`.\n"
        "Order by `user_id ASC, streak_start_date ASC`."
    ),

    "sql-recursive-employee-hierarchy": (
        "### Problem Statement\n\n"
        "Compute managerial reporting depth and full organizational hierarchy path for every employee using Recursive CTEs (`WITH RECURSIVE`).\n\n"
        "---\n\n"
        "#### Table Schema\n"
        "```sql\n"
        "CREATE TABLE employees (employee_id INT PRIMARY KEY, name TEXT NOT NULL, manager_id INT);\n"
        "```\n\n"
        "---\n\n"
        "#### Output Columns\n"
        "`employee_id`, `name`, `hierarchy_level`, `path`.\n"
        "Level 1 for CEO (`manager_id IS NULL`). Path format: `'Alice -> Bob -> Charlie'`.\n"
        "Order by `hierarchy_level ASC, employee_id ASC`."
    ),

    "sql-rolling-7day-average-revenue": (
        "### Problem Statement\n\n"
        "Compute daily revenue and 7-day rolling moving average revenue using SQL window frames (`ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`).\n\n"
        "---\n\n"
        "#### Table Schema\n"
        "```sql\n"
        "CREATE TABLE daily_sales (transaction_date DATE PRIMARY KEY, revenue DECIMAL(10, 2) NOT NULL);\n"
        "```\n\n"
        "---\n\n"
        "#### Output Columns\n"
        "`transaction_date`, `daily_revenue`, `rolling_7d_avg` (rounded to 2 decimal places).\n"
        "Order by `transaction_date ASC`."
    ),

    "mongo-order-fulfillment-aggregation": (
        "### Problem Statement\n\n"
        "Build a MongoDB aggregation pipeline using `$lookup`, `$unwind`, `$group`, and `$sort` to calculate total units sold and gross revenue per vendor.\n\n"
        "---\n\n"
        "#### Output Fields\n"
        "- `vendor_name`: Vendor company name.\n"
        "- `total_units_sold`: Sum of quantities.\n"
        "- `gross_revenue`: Sum of `quantity * unit_price` (rounded to 2 decimal places).\n"
        "Only include orders with `status: 'completed'`. Sort by `gross_revenue DESC`."
    ),

    "redis-rate-limiter-sliding-window": (
        "### Problem Statement\n\n"
        "Implement a 60-second sliding window rate limiter using Redis Sorted Sets (`ZSET`).\n\n"
        "---\n\n"
        "#### Command Sequence\n"
        "1. Remove expired timestamps: `ZREMRANGEBYSCORE ratelimit:usr_99 -inf <window_start>`\n"
        "2. Add current timestamp: `ZADD ratelimit:usr_99 <now> <now>`\n"
        "3. Query active requests in window: `ZCARD ratelimit:usr_99`"
    )
}

def run():
    db = get_db()
    print("Updating challenge statements across all domains...")
    count = 0
    for slug, desc in DESCRIPTIONS.items():
        res = db.problems.update_one({"slug": slug}, {"$set": {"description": desc}})
        if res.matched_count > 0:
            count += 1
            print(f"  [OK] Enriched: {slug}")
        else:
            print(f"  [WARN] Not found in DB: {slug}")

    print(f"\nSuccessfully updated {count} challenge statements!")

if __name__ == "__main__":
    run()

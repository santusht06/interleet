#!/usr/bin/env python3
"""
Deep QA Challenge Execution Matrix Test Suite
============================================
Exhaustively tests code execution across ALL domains, sub-challenge types,
and distinct candidate coding styles / paradigms:
  1. Databases: CTEs vs Subqueries vs Window Functions vs MongoDB vs Redis
  2. APIs: FastAPI route handlers, query params, JSON contracts, status codes
  3. DevOps: Shell pipelines, robust bash scripts, idempotent provisioning
  4. Frontend: Pure DOM, Event handlers, multi-file bundle previews
  5. Backend/DSA: Multi-language (Python, JS, TS, Go, C++, Rust), Two-Pointers, HashMaps
  6. Security & Error Resilience: Syntax errors, runtime crashes, and security sandbox guard

Usage:
  python3 backend/tests/deep_qa_challenge_matrix.py --base-url https://interleet-backend.sharexpress.in
"""

import sys
import os
import json
import time
import argparse
import urllib.request
import urllib.error
import ssl

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

class DeepQAMatrixRunner:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.passed = 0
        self.failed = 0
        self.categories = {}

    def execute(self, payload: dict) -> tuple[int, dict, float]:
        url = f"{self.base_url}/api/v1/execute"
        req_headers = {
            "Content-Type": "application/json",
            "User-Agent": "Interleet-DeepQA-Runner/2.0"
        }
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers=req_headers, method="POST")

        start = time.perf_counter()
        try:
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=40) as resp:
                latency_ms = (time.perf_counter() - start) * 1000
                raw = resp.read().decode("utf-8")
                try:
                    parsed = json.loads(raw)
                except Exception:
                    parsed = {"raw": raw}
                return resp.status, parsed, latency_ms
        except urllib.error.HTTPError as e:
            latency_ms = (time.perf_counter() - start) * 1000
            raw = e.read().decode("utf-8")
            try:
                parsed = json.loads(raw)
            except Exception:
                parsed = {"error": raw}
            return e.code, parsed, latency_ms
        except Exception as e:
            latency_ms = (time.perf_counter() - start) * 1000
            return 500, {"error": str(e)}, latency_ms

    def record(self, domain: str, style_name: str, passed: bool, latency_ms: float, details: str = ""):
        status_tag = "✓ PASS" if passed else "✗ FAIL"
        color = "\033[92m" if passed else "\033[91m"
        reset = "\033[0m"
        print(f" {color}{status_tag}{reset} [{domain:12}] {style_name:52} ({latency_ms:6.1f}ms) {details}")
        if passed:
            self.passed += 1
        else:
            self.failed += 1
        self.categories.setdefault(domain, {"passed": 0, "failed": 0})
        if passed:
            self.categories[domain]["passed"] += 1
        else:
            self.categories[domain]["failed"] += 1

    # ═════════════════════════════════════════════════════════════════════════
    # 1. DATABASE DOMAIN EXECUTION STYLES
    # ═════════════════════════════════════════════════════════════════════════
    def test_database_styles(self):
        print("\n\033[1m=== 1. Databases Domain: Query Styles & Engines ===\033[0m")
        schema_sql = "CREATE TABLE users (user_id INT PRIMARY KEY, signup_date DATE NOT NULL); CREATE TABLE user_activity (activity_id INT PRIMARY KEY, user_id INT NOT NULL, activity_date DATE NOT NULL);"
        fixtures = {
            "users": [{"user_id": 1, "signup_date": "2026-01-10"}, {"user_id": 2, "signup_date": "2026-01-15"}],
            "user_activity": [{"activity_id": 101, "user_id": 1, "activity_date": "2026-02-02"}]
        }
        stdin_cfg = json.dumps({"engine": "sql", "schema_sql": schema_sql, "fixtures": fixtures})

        # 1.1 CTEs (Common Table Expressions) Style
        code_cte = """
        WITH MonthlyCohorts AS (
            SELECT user_id, strftime('%Y-%m', signup_date) AS cohort_month
            FROM users
        ),
        RetainedActivity AS (
            SELECT DISTINCT a.user_id, strftime('%Y-%m', a.activity_date) AS act_month
            FROM user_activity a
        )
        SELECT 
            c.cohort_month,
            COUNT(DISTINCT c.user_id) AS total_signups,
            COUNT(DISTINCT r.user_id) AS retained_users_m1,
            ROUND(COUNT(DISTINCT r.user_id) * 100.0 / COUNT(DISTINCT c.user_id), 2) AS retention_rate_pct
        FROM MonthlyCohorts c
        LEFT JOIN RetainedActivity r 
            ON c.user_id = r.user_id 
            AND r.act_month = strftime('%Y-%m', date(c.cohort_month || '-01', '+1 month'))
        GROUP BY c.cohort_month
        ORDER BY c.cohort_month ASC;
        """
        status, res, latency = self.execute({
            "language": "sql", "execution_mode": "database", "code": code_cte, "stdin": stdin_cfg
        })
        passed = (status == 200 and res.get("exit_code") == 0 and "cohort_month" in res.get("stdout", ""))
        self.record("Databases", "SQL Style A: Common Table Expressions (WITH CTEs)", passed, latency, f"exit={res.get('exit_code')}")

        # 1.2 Subqueries & Derived Tables Style
        code_subqueries = """
        SELECT 
            u_summary.cohort_month,
            u_summary.total_signups,
            COALESCE(act.retained_count, 0) AS retained_users_m1,
            ROUND(COALESCE(act.retained_count, 0) * 100.0 / u_summary.total_signups, 2) AS retention_rate_pct
        FROM (
            SELECT strftime('%Y-%m', signup_date) AS cohort_month, COUNT(user_id) AS total_signups
            FROM users
            GROUP BY strftime('%Y-%m', signup_date)
        ) AS u_summary
        LEFT JOIN (
            SELECT strftime('%Y-%m', u2.signup_date) AS c_month, COUNT(DISTINCT a2.user_id) AS retained_count
            FROM users u2
            JOIN user_activity a2 ON u2.user_id = a2.user_id
            WHERE strftime('%Y-%m', a2.activity_date) = strftime('%Y-%m', date(u2.signup_date, '+1 month'))
            GROUP BY c_month
        ) AS act ON u_summary.cohort_month = act.c_month
        ORDER BY u_summary.cohort_month ASC;
        """
        status, res, latency = self.execute({
            "language": "sql", "execution_mode": "database", "code": code_subqueries, "stdin": stdin_cfg
        })
        passed = (status == 200 and res.get("exit_code") == 0 and "cohort_month" in res.get("stdout", ""))
        self.record("Databases", "SQL Style B: Nested Subqueries / Derived Tables", passed, latency, f"exit={res.get('exit_code')}")

        # 1.3 Window Functions Style (DENSE_RANK)
        schema_prod = "CREATE TABLE products (product_id INT PRIMARY KEY, product_name TEXT, category TEXT, revenue INT);"
        fixtures_prod = {
            "products": [
                {"product_id": 1, "product_name": "Laptop", "category": "Tech", "revenue": 2000},
                {"product_id": 2, "product_name": "Phone", "category": "Tech", "revenue": 1200},
                {"product_id": 3, "product_name": "Shirt", "category": "Apparel", "revenue": 80}
            ]
        }
        code_window = """
        SELECT product_name, category, revenue,
               DENSE_RANK() OVER (PARTITION BY category ORDER BY revenue DESC) as rank
        FROM products
        ORDER BY category ASC, rank ASC;
        """
        status, res, latency = self.execute({
            "language": "sql", "execution_mode": "database", "code": code_window,
            "stdin": json.dumps({"engine": "sql", "schema_sql": schema_prod, "fixtures": fixtures_prod})
        })
        passed = (status == 200 and res.get("exit_code") == 0 and "Laptop" in res.get("stdout", ""))
        self.record("Databases", "SQL Style C: Window Functions (DENSE_RANK OVER)", passed, latency, f"exit={res.get('exit_code')}")

        # 1.4 MongoDB Aggregation Pipeline
        code_mongo = """
        [
            { "$match": { "status": "completed" } },
            { "$unwind": "$items" },
            { "$group": { "_id": "$items.category", "total_sales": { "$sum": "$items.price" } } },
            { "$project": { "category": "$_id", "total_sales": 1, "_id": 0 } },
            { "$sort": { "total_sales": -1 } }
        ]
        """
        mongo_fixtures = {
            "orders": [
                {"status": "completed", "items": [{"category": "Hardware", "price": 500}, {"category": "Software", "price": 120}]},
                {"status": "completed", "items": [{"category": "Hardware", "price": 300}]},
                {"status": "pending", "items": [{"category": "Hardware", "price": 1000}]}
            ]
        }
        status, res, latency = self.execute({
            "language": "mongodb", "execution_mode": "database", "code": code_mongo,
            "stdin": json.dumps({"engine": "mongodb", "fixtures": mongo_fixtures})
        })
        passed = (status == 200 and res.get("exit_code") == 0 and "Hardware" in res.get("stdout", ""))
        self.record("Databases", "NoSQL Style D: MongoDB Multi-Stage Aggregation", passed, latency, f"exit={res.get('exit_code')}")

        # 1.5 Redis In-Memory Sliding Window
        code_redis = """
        # Record event in Redis ZSET
        ZADD rate:user_123 1700000010 "req_1"
        ZADD rate:user_123 1700000045 "req_2"
        ZREMRANGEBYSCORE rate:user_123 -inf 1700000000
        ZCARD rate:user_123
        """
        status, res, latency = self.execute({
            "language": "redis", "execution_mode": "database", "code": code_redis,
            "stdin": json.dumps({"engine": "redis", "fixtures": {}})
        })
        passed = (status == 200 and res.get("exit_code") == 0 and "ZCARD" in res.get("stdout", ""))
        self.record("Databases", "NoSQL Style E: Redis Pipelined Set Operations", passed, latency, f"exit={res.get('exit_code')}")

    # ═════════════════════════════════════════════════════════════════════════
    # 2. APIS DOMAIN EXECUTION STYLES
    # ═════════════════════════════════════════════════════════════════════════
    def test_api_styles(self):
        print("\n\033[1m=== 2. APIs Domain: Frameworks & Request Contracts ===\033[0m")

        # 2.1 Python FastAPI Style (Typed Request/Response)
        code_fastapi = """
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class UserItem(BaseModel):
    name: str
    role: str

database = {}

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserItem):
    user_id = len(database) + 1
    database[user_id] = {"id": user_id, "name": user.name, "role": user.role}
    return database[user_id]

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in database:
        raise HTTPException(status_code=404, detail="User not found")
    return database[user_id]

# Test runner script
item = create_user(UserItem(name="Alex", role="Admin"))
assert item["id"] == 1 and item["name"] == "Alex"
found = get_user(1)
assert found["role"] == "Admin"
print("FASTAPI_ENDPOINTS_OK")
"""
        status, res, latency = self.execute({
            "language": "python", "code": code_fastapi, "stdin": "",
            "expected_output": "FASTAPI_ENDPOINTS_OK\n"
        })
        passed = (status == 200 and res.get("verdict") == "ACCEPTED")
        self.record("APIs", "API Style A: FastAPI Contract & Status Codes", passed, latency, f"verdict={res.get('verdict')}")

        # 2.2 Node.js REST Route Handler Style
        code_node_api = """
const http = require('http');

function router(reqMethod, reqUrl, reqBody) {
    if (reqMethod === 'GET' && reqUrl === '/health') {
        return { status: 200, body: { status: 'healthy', timestamp: 1700000000 } };
    }
    if (reqMethod === 'POST' && reqUrl === '/api/calculate') {
        const { a, b, op } = reqBody;
        let result = op === 'add' ? a + b : a * b;
        return { status: 200, body: { result } };
    }
    return { status: 404, body: { error: 'Not Found' } };
}

const res1 = router('GET', '/health');
const res2 = router('POST', '/api/calculate', { a: 15, b: 25, op: 'add' });

if (res1.body.status === 'healthy' && res2.body.result === 40) {
    console.log("NODE_REST_HANDLER_OK");
}
"""
        status, res, latency = self.execute({
            "language": "javascript", "code": code_node_api, "stdin": "",
            "expected_output": "NODE_REST_HANDLER_OK\n"
        })
        passed = (status == 200 and res.get("verdict") == "ACCEPTED")
        self.record("APIs", "API Style B: Node.js Express/HTTP Route Dispatcher", passed, latency, f"verdict={res.get('verdict')}")

    # ═════════════════════════════════════════════════════════════════════════
    # 3. DEVOPS DOMAIN EXECUTION STYLES
    # ═════════════════════════════════════════════════════════════════════════
    def test_devops_styles(self):
        print("\n\033[1m=== 3. DevOps Domain: Shell Scripts & System Automation ===\033[0m")

        # 3.1 Python Log Parsing & Metrics Pipeline
        code_log_parser = """
import sys, re
from collections import Counter

log_data = '''
192.168.1.1 - - [10/Oct/2026:13:55:36] "GET /api/v1/users HTTP/1.1" 200 2326
192.168.1.2 - - [10/Oct/2026:13:55:37] "POST /api/v1/auth HTTP/1.1" 401 532
192.168.1.1 - - [10/Oct/2026:13:55:38] "GET /api/v1/challenges HTTP/1.1" 200 4512
192.168.1.3 - - [10/Oct/2026:13:55:39] "GET /api/v1/users HTTP/1.1" 500 120
'''

# Parse 200 OK endpoints
pattern = r'"GET (/[^ ]+) HTTP/1.1" 200'
endpoints = re.findall(pattern, log_data)
counts = Counter(endpoints)
print(f"Top: {counts.most_common(1)[0][0]} with {counts.most_common(1)[0][1]} requests")
"""
        status, res, latency = self.execute({
            "language": "python", "code": code_log_parser, "stdin": "",
            "expected_output": "Top: /api/v1/users with 1 requests\n"
        })
        passed = (status == 200 and res.get("verdict") == "ACCEPTED")
        self.record("DevOps", "DevOps Style A: Nginx/Syslog Log Parsing Automation", passed, latency, f"verdict={res.get('verdict')}")

        # 3.2 Linux Environment & File System Verification
        code_fs = """
import os, tempfile

with tempfile.TemporaryDirectory() as tmpdir:
    fpath = os.path.join(tmpdir, "config.json")
    with open(fpath, "w") as f:
        f.write('{"env": "production", "max_conns": 500}')
    assert os.path.exists(fpath)
    with open(fpath) as f:
        data = f.read()
    assert "max_conns" in data
print("DEVOPS_FS_PROVISION_OK")
"""
        status, res, latency = self.execute({
            "language": "python", "code": code_fs, "stdin": "",
            "expected_output": "DEVOPS_FS_PROVISION_OK\n"
        })
        passed = (status == 200 and res.get("verdict") == "ACCEPTED")
        self.record("DevOps", "DevOps Style B: Idempotent Config Provisioning", passed, latency, f"verdict={res.get('verdict')}")

    # ═════════════════════════════════════════════════════════════════════════
    # 4. FRONTEND DOMAIN EXECUTION STYLES
    # ═════════════════════════════════════════════════════════════════════════
    def test_frontend_styles(self):
        print("\n\033[1m=== 4. Frontend Domain: DOM Manipulation & Event Systems ===\033[0m")

        # 4.1 Pure DOM Virtual State Simulation
        code_dom_sim = """
class VirtualDOM {
    constructor() {
        this.elements = {};
    }
    createElement(tag, id, classes = []) {
        this.elements[id] = { tag, id, classes, text: '', attributes: {} };
        return this.elements[id];
    }
    setAttribute(id, key, val) {
        if (this.elements[id]) this.elements[id].attributes[key] = val;
    }
    setText(id, text) {
        if (this.elements[id]) this.elements[id].text = text;
    }
}

const vdom = new VirtualDOM();
vdom.createElement('button', 'submit-btn', ['btn', 'btn-primary']);
vdom.setAttribute('submit-btn', 'disabled', 'true');
vdom.setText('submit-btn', 'Submitting...');

if (vdom.elements['submit-btn'].attributes['disabled'] === 'true') {
    console.log("DOM_STATE_MUTATION_OK");
}
"""
        status, res, latency = self.execute({
            "language": "javascript", "code": code_dom_sim, "stdin": "",
            "expected_output": "DOM_STATE_MUTATION_OK\n"
        })
        passed = (status == 200 and res.get("verdict") == "ACCEPTED")
        self.record("Frontend", "Frontend Style A: Virtual DOM State Management", passed, latency, f"verdict={res.get('verdict')}")

        # 4.2 TypeScript Event Emitter / PubSub
        code_ts_events = """
type EventHandler = (data: any) => void;

class EventEmitter {
    private events: Map<string, EventHandler[]> = new Map();

    on(event: string, handler: EventHandler): void {
        if (!this.events.has(event)) {
            this.events.set(event, []);
        }
        this.events.get(event)!.push(handler);
    }

    emit(event: string, data: any): void {
        const handlers = this.events.get(event) || [];
        for (const handler of handlers) {
            handler(data);
        }
    }
}

const bus = new EventEmitter();
let received = "";
bus.on("modal:open", (payload: { title: string }) => {
    received = payload.title;
});
bus.emit("modal:open", { title: "Confirm Submission" });

if (received === "Confirm Submission") {
    console.log("TS_EVENT_BUS_OK");
}
"""
        status, res, latency = self.execute({
            "language": "typescript", "code": code_ts_events, "stdin": "",
            "expected_output": "TS_EVENT_BUS_OK\n"
        })
        passed = (status == 200 and res.get("verdict") == "ACCEPTED")
        self.record("Frontend", "Frontend Style B: TypeScript Typed Event Bus", passed, latency, f"verdict={res.get('verdict')}")

    # ═════════════════════════════════════════════════════════════════════════
    # 5. MULTI-LANGUAGE DSA / ALGORITHMS EXECUTION
    # ═════════════════════════════════════════════════════════════════════════
    def test_dsa_multilanguage_styles(self):
        print("\n\033[1m=== 5. Multi-Language Algorithms & Execution Engines ===\033[0m")

        # 5.1 Python: Two Pointers / Optimal Hash
        py_code = """
import sys, json
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        diff = target - n
        if diff in seen:
            return [seen[diff], i]
        seen[n] = i
    return []

print(json.dumps(two_sum([2, 7, 11, 15], 9)))
"""
        status, res, latency = self.execute({
            "language": "python", "code": py_code, "stdin": "", "expected_output": "[0, 1]\n"
        })
        passed = (status == 200 and res.get("verdict") == "ACCEPTED")
        self.record("DSA/Backend", "Python 3.12: Two-Sum Optimal O(N) Hash Map", passed, latency, f"verdict={res.get('verdict')}")

        # 5.2 Go: Concurrency / Goroutines & Channels
        go_code = """
package main

import (
	"fmt"
	"sync"
)

func main() {
	var wg sync.WaitGroup
	results := make([]int, 5)

	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()
			results[idx] = idx * idx
		}(i)
	}

	wg.Wait()
	sum := 0
	for _, v := range results {
		sum += v
	}
	fmt.Printf("SUM:%d\\n", sum)
}
"""
        status, res, latency = self.execute({
            "language": "go", "code": go_code, "stdin": "", "expected_output": "SUM:30\n"
        })
        passed = (status == 200 and res.get("verdict") == "ACCEPTED")
        self.record("DSA/Backend", "Go 1.22: Goroutines, WaitGroups & Channels", passed, latency, f"verdict={res.get('verdict')}")

        # 5.3 C++: STL Algorithms & Custom Comparators
        cpp_code = """
#include <iostream>
#include <vector>
#include <algorithm>

struct Task {
    int id;
    int priority;
};

int main() {
    std::vector<Task> tasks = {{1, 10}, {2, 50}, {3, 30}};
    std::sort(tasks.begin(), tasks.end(), [](const Task& a, const Task& b) {
        return a.priority > b.priority;
    });
    std::cout << "TOP_TASK:" << tasks[0].id << std::endl;
    return 0;
}
"""
        status, res, latency = self.execute({
            "language": "cpp", "code": cpp_code, "stdin": "", "expected_output": "TOP_TASK:2\n"
        })
        passed = (status == 200 and res.get("verdict") == "ACCEPTED")
        self.record("DSA/Backend", "C++17: Modern STL Lambda Custom Comparators", passed, latency, f"verdict={res.get('verdict')}")

        # 5.4 Rust: Memory Safety, Iterators & Pattern Matching
        rust_code = """
fn main() {
    let numbers = vec![1, 2, 3, 4, 5, 6];
    let even_sum: i32 = numbers
        .iter()
        .filter(|&&x| x % 2 == 0)
        .map(|&x| x * x)
        .sum();
    println!("RUST_EVEN_SQUARES:{}", even_sum);
}
"""
        status, res, latency = self.execute({
            "language": "rust", "code": rust_code, "stdin": "", "expected_output": "RUST_EVEN_SQUARES:56\n"
        })
        passed = (status == 200 and res.get("verdict") == "ACCEPTED")
        self.record("DSA/Backend", "Rust 1.78: Functional Iterators & Safety", passed, latency, f"verdict={res.get('verdict')}")

    # ═════════════════════════════════════════════════════════════════════════
    # 6. SECURITY GUARDS & FAULT RESILIENCE QA
    # ═════════════════════════════════════════════════════════════════════════
    def test_security_and_fault_resilience(self):
        print("\n\033[1m=== 6. Security Guardrails & Fault Resilience QA ===\033[0m")

        # 6.1 Syntax Error Handling
        code_broken = "def broken():\n    return 42 +"
        status, res, latency = self.execute({
            "language": "python", "code": code_broken, "stdin": ""
        })
        passed = (status == 200 and res.get("verdict") in ["COMPILATION_ERROR", "RUNTIME_ERROR"] and res.get("exit_code") != 0)
        self.record("Resilience", "Syntax Error: Clean Diagnostic Without Crash", passed, latency, f"verdict={res.get('verdict')}")

        # 6.2 Zero Division Runtime Exception
        code_divzero = "x = 10 / 0"
        status, res, latency = self.execute({
            "language": "python", "code": code_divzero, "stdin": ""
        })
        passed = (status == 200 and res.get("verdict") == "RUNTIME_ERROR" and "ZeroDivisionError" in res.get("stderr", ""))
        self.record("Resilience", "Runtime Error: Stack Trace Captured Gracefully", passed, latency, f"verdict={res.get('verdict')}")

        # 6.3 Security Policy Guard Blocking System Access
        code_malicious = "data = open('/etc/passwd').read()"
        status, res, latency = self.execute({
            "language": "python", "code": code_malicious, "stdin": ""
        })
        # Should be blocked by CodeGuard security policy with HTTP 400
        passed = (status == 400 and ("security policy" in str(res).lower() or "not allowed" in str(res).lower()))
        self.record("Security", "CodeGuard Sandbox: Blocks System File Access (/etc/passwd)", passed, latency, f"status={status}")

    # ═════════════════════════════════════════════════════════════════════════
    # RUN ALL AND REPORT
    # ═════════════════════════════════════════════════════════════════════════
    def run_all(self):
        print(f"\n\033[1m🚀 Launching Deep QA Challenge Execution Matrix against {self.base_url}...\033[0m")
        start = time.time()

        self.test_database_styles()
        self.test_api_styles()
        self.test_devops_styles()
        self.test_frontend_styles()
        self.test_dsa_multilanguage_styles()
        self.test_security_and_fault_resilience()

        duration = time.time() - start
        total = self.passed + self.failed
        rate = (self.passed / total * 100) if total > 0 else 0

        print("\n" + "═" * 78)
        print("\033[1mDEEP QA EXECUTION MATRIX REPORT\033[0m")
        print(f" Total Test Variations : {total}")
        print(f" Passed Variations     : \033[92m{self.passed}\033[0m")
        print(f" Failed Variations     : \033[91m{self.failed}\033[0m")
        print(f" Quality Pass Rate     : \033[1m{rate:.1f}%\033[0m")
        print(f" Total Execution Time  : {duration:.2f}s")
        print("─" * 78)
        print("DOMAIN BREAKDOWN:")
        for dom, counts in self.categories.items():
            d_total = counts["passed"] + counts["failed"]
            d_rate = (counts["passed"] / d_total * 100) if d_total > 0 else 0
            print(f"  • {dom:14}: {counts['passed']}/{d_total} passed ({d_rate:.1f}%)")
        print("═" * 78)

        if self.failed > 0:
            sys.exit(1)
        else:
            sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deep QA Challenge Matrix Runner")
    parser.add_argument("--base-url", default="https://interleet-backend.sharexpress.in", help="Target API server URL")
    args = parser.parse_args()

    runner = DeepQAMatrixRunner(base_url=args.base_url)
    runner.run_all()

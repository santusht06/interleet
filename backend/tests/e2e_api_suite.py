#!/usr/bin/env python3
"""
Interleet End-to-End API & User Interaction Test Suite
======================================================
Simulates real candidate workflows across all Interleet subsystems:
  1. Discovery & Platform Health (Landing metrics, health, runtimes)
  2. Domain Exploration (Frontend, Databases, DevOps, APIs, Fullstack)
  3. Single Challenge Inspector (DDL schemas, fixtures, starter code)
  4. Candidate Profile & Global Leaderboard
  5. Multi-Engine Code & Query Execution (SQL, MongoDB, Redis, Python Algorithms)
  6. AI Mock Interview Presets & Archives

Run directly against production:
  python3 backend/tests/e2e_api_suite.py --base-url https://interleet-backend.sharexpress.in
"""

import sys
import os
import json
import time
import argparse
import urllib.request
import urllib.error
import ssl

# Ignore self-signed certificates if testing on dev
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# Test auth token for candidate simulation
TEST_USER_TOKEN = (
    "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiJhZGRmNWUwYS0yMzNmLTQ2NTUtOTVlMi02MTA0YmEwMTUxNzciLCJpYXQiOjE3ODgwOTA1NjEsImV4cCI6MTc4ODY5NTM2MX0."
    "nmpAr54wHiP8BwQv90GJ9d68gIECdnFRXVLtH5WB0AyRbNzOckJ4Ap6NBL7bWBwFvLGSiXXwShRKwpSGam2wVlgeVRv58aYOGReQf-LP-VUu0I4t9ErGh8o288o-fXYzAbwcvoGWO32iMRZ9K1v8RoTVDpqmPK0KnOK0sgyu4TbkDoafCgdsqVKSVF0LXpsdf7GA8SeGqDexmptTeGm_ZYkrrzUdfE5rM0DhuRISy8yvpLfLAhO_3OpAO5vcCXqSWhVLghyJiUvtVHFfSRFy_tE4MBrzzc1FoJ64iu7aeGykwtVP7FM4bWxrGwWFzDTxXRNp_DQzANH2Qgv1k1s9mA"
)

class TestRunner:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.passed = 0
        self.failed = 0
        self.skipped = 0

    def request(self, method: str, path: str, body: dict = None, headers: dict = None, auth: bool = False) -> tuple[int, dict | list | str, float]:
        """Execute HTTP request and return (status_code, parsed_response, latency_ms)."""
        url = f"{self.base_url}{path}"
        req_headers = {
            "Content-Type": "application/json",
            "User-Agent": "Interleet-E2E-Tester/1.0"
        }
        if auth:
            req_headers["Cookie"] = f"user={TEST_USER_TOKEN}"
        if headers:
            req_headers.update(headers)

        data_bytes = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data_bytes, headers=req_headers, method=method.upper())

        start = time.perf_counter()
        try:
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=35) as resp:
                latency_ms = (time.perf_counter() - start) * 1000
                raw = resp.read().decode("utf-8")
                try:
                    parsed = json.loads(raw)
                except Exception:
                    parsed = raw
                return resp.status, parsed, latency_ms
        except urllib.error.HTTPError as e:
            latency_ms = (time.perf_counter() - start) * 1000
            raw = e.read().decode("utf-8")
            try:
                parsed = json.loads(raw)
            except Exception:
                parsed = raw
            return e.code, parsed, latency_ms
        except Exception as e:
            latency_ms = (time.perf_counter() - start) * 1000
            return 500, {"error": str(e)}, latency_ms

    def log_result(self, category: str, test_name: str, passed: bool, latency_ms: float, details: str = ""):
        status_tag = "✓ PASS" if passed else "✗ FAIL"
        color = "\033[92m" if passed else "\033[91m"
        reset = "\033[0m"
        print(f" {color}{status_tag}{reset} [{category:14}] {test_name:42} ({latency_ms:6.1f}ms) {details}")
        if passed:
            self.passed += 1
        else:
            self.failed += 1

    # ── 1. Public Discovery & Platform Health ───────────────────────────────────
    def test_public_endpoints(self):
        print("\n\033[1m=== 1. Public Discovery & Platform Health ===\033[0m")

        # 1.1 Root Engine Health
        status, res, latency = self.request("GET", "/")
        passed = (status == 200 and isinstance(res, dict) and res.get("status") == "ok")
        self.log_result("Public", "GET / (Root Health)", passed, latency, f"service={res.get('service') if isinstance(res, dict) else status}")

        # 1.2 Platform Stats
        status, res, latency = self.request("GET", "/api/public/stats")
        passed = (status == 200 and isinstance(res, dict) and "total_challenges" in res)
        showcase_user = res.get("showcase_user", {}).get("name", "N/A") if isinstance(res, dict) else ""
        details = f"challenges={res.get('total_challenges', 0)}, showcase={showcase_user}" if passed else str(res)
        self.log_result("Public", "GET /api/public/stats", passed, latency, details)

        # 1.3 Execution Runtimes
        status, res, latency = self.request("GET", "/api/v1/runtimes")
        passed = (status == 200 and isinstance(res, dict) and len(res.get("data", [])) > 0)
        runtime_count = len(res.get("data", [])) if passed else 0
        self.log_result("Public", "GET /api/v1/runtimes", passed, latency, f"registered runtimes={runtime_count}")

        # 1.4 Judge Engine Health
        status, res, latency = self.request("GET", "/api/v1/health")
        passed = (status == 200 and isinstance(res, dict) and res.get("status") in ["ok", "healthy"])
        self.log_result("Public", "GET /api/v1/health", passed, latency, f"status={res.get('status') if isinstance(res, dict) else status}")

    # ── 2. Challenges & Domain Queries Suite ───────────────────────────────────
    def test_challenges_queries(self):
        print("\n\033[1m=== 2. Challenge Exploration & Domain Queries ===\033[0m")

        # 2.1 List All Challenges via Platform API
        status, res, latency = self.request("GET", "/api/challenges")
        passed = (status == 200 and isinstance(res, dict) and len(res.get("items", [])) > 0)
        total = res.get("total", len(res.get("items", []))) if passed else 0
        self.log_result("Challenges", "GET /api/challenges (All)", passed, latency, f"total={total} challenges")

        # 2.2 Filter by Every Engineering Domain (Frontend, Databases, DevOps, APIs, Fullstack)
        domains = ["Frontend", "Databases", "DevOps", "APIs", "Fullstack"]
        for domain in domains:
            status, res, latency = self.request("GET", f"/api/challenges?domain={domain}")
            items = res.get("items", []) if isinstance(res, dict) else []
            passed = (status == 200 and len(items) > 0 and all(c.get("domain") == domain for c in items))
            self.log_result("Challenges", f"GET /api/challenges?domain={domain}", passed, latency, f"found {len(items)} challenges")

        # 2.3 Single Database Challenge with Schema & Fixtures (Authenticated)
        status, res, latency = self.request("GET", "/api/challenges/sql-user-retention-cohorts", auth=True)
        passed = (status == 200 and isinstance(res, dict) and bool(res.get("fixtures")) and bool(res.get("schema_sql")))
        self.log_result("Challenges", "GET /api/challenges/sql-user-retention-cohorts", passed, latency, f"tables={list(res.get('fixtures', {}).keys()) if isinstance(res, dict) else []}")

    # ── 3. Candidate Profile & Leaderboard Suite ──────────────────────────────
    def test_leaderboard_and_profiles(self):
        print("\n\033[1m=== 3. Candidate Profile & Leaderboard Suite ===\033[0m")

        # 3.1 Global Leaderboard
        status, res, latency = self.request("GET", "/api/leaderboard?limit=10")
        passed = (status == 200 and isinstance(res, dict) and ("users_count" in res or "items" in res))
        details = f"status={res.get('message', 'Active')}" if passed else str(res)
        self.log_result("Leaderboard", "GET /api/leaderboard", passed, latency, details)

        # 3.2 Authenticated Candidate Profile
        status, res, latency = self.request("GET", "/api/profile", auth=True)
        passed = (status == 200 and isinstance(res, dict) and res.get("success") is True and "user" in res)
        name = res.get("user", {}).get("name", "Candidate") if isinstance(res, dict) else ""
        self.log_result("Profile", "GET /api/profile (Authenticated)", passed, latency, f"name={name}")

        # 3.3 Candidate Dashboard
        status, res, latency = self.request("GET", "/api/dashboard", auth=True)
        passed = (status == 200 and isinstance(res, dict) and "user" in res and "recentActivity" in res)
        streak = res.get("user", {}).get("streak", 0) if isinstance(res, dict) else 0
        self.log_result("Dashboard", "GET /api/dashboard (Authenticated)", passed, latency, f"streak={streak}, recommended={len(res.get('recommendedChallenges', [])) if isinstance(res, dict) else 0}")

    # ── 4. Sandbox Code Execution & Judge Engine Suite ─────────────────────────
    def test_code_execution(self):
        print("\n\033[1m=== 4. Code Execution & Judge Sandbox Tests ===\033[0m")

        # 4.1 SQL Query Execution (Cohort Analysis Query)
        sql_payload = {
            "language": "sql",
            "execution_mode": "database",
            "code": "SELECT strftime('%Y-%m', u.signup_date) AS cohort_month, COUNT(DISTINCT u.user_id) AS total_signups, COUNT(DISTINCT a.user_id) AS retained_users_m1, ROUND(COUNT(DISTINCT a.user_id) * 100.0 / COUNT(DISTINCT u.user_id), 2) AS retention_rate_pct FROM users u LEFT JOIN user_activity a ON u.user_id = a.user_id AND strftime('%Y-%m', a.activity_date) = strftime('%Y-%m', date(u.signup_date, '+1 month')) GROUP BY cohort_month ORDER BY cohort_month ASC;",
            "stdin": json.dumps({
                "engine": "sql",
                "schema_sql": "CREATE TABLE users (user_id INT PRIMARY KEY, signup_date DATE NOT NULL); CREATE TABLE user_activity (activity_id INT PRIMARY KEY, user_id INT NOT NULL, activity_date DATE NOT NULL);",
                "fixtures": {
                    "users": [{"user_id": 1, "signup_date": "2026-01-10"}, {"user_id": 2, "signup_date": "2026-01-15"}],
                    "user_activity": [{"activity_id": 101, "user_id": 1, "activity_date": "2026-02-02"}]
                }
            })
        }
        status, res, latency = self.request("POST", "/api/v1/execute", sql_payload)
        passed = (status == 200 and isinstance(res, dict) and res.get("exit_code") == 0 and "cohort_month" in res.get("stdout", ""))
        self.log_result("Judge", "POST /api/v1/execute (SQL Sandbox)", passed, latency, f"exit_code={res.get('exit_code') if isinstance(res, dict) else status}")

        # 4.2 MongoDB Aggregation Execution
        mongo_payload = {
            "language": "mongodb",
            "execution_mode": "database",
            "code": "[\n  { \"$match\": { \"status\": \"completed\" } },\n  { \"$group\": { \"_id\": \"$vendor\", \"total\": { \"$sum\": 1 } } }\n]",
            "stdin": json.dumps({
                "engine": "mongodb",
                "fixtures": {
                    "orders": [
                        {"vendor": "Acme", "status": "completed"},
                        {"vendor": "Acme", "status": "completed"},
                        {"vendor": "Globex", "status": "cancelled"}
                    ]
                }
            })
        }
        status, res, latency = self.request("POST", "/api/v1/execute", mongo_payload)
        passed = (status == 200 and isinstance(res, dict) and res.get("exit_code") == 0 and "Acme" in res.get("stdout", ""))
        self.log_result("Judge", "POST /api/v1/execute (MongoDB Pipeline)", passed, latency, f"exit_code={res.get('exit_code') if isinstance(res, dict) else status}")

        # 4.3 Redis Commands Execution
        redis_payload = {
            "language": "redis",
            "execution_mode": "database",
            "code": "ZADD leaderboard 1500 player1\nZADD leaderboard 2200 player2\nZREVRANGE leaderboard 0 -1",
            "stdin": json.dumps({
                "engine": "redis",
                "fixtures": {}
            })
        }
        status, res, latency = self.request("POST", "/api/v1/execute", redis_payload)
        passed = (status == 200 and isinstance(res, dict) and res.get("exit_code") == 0 and "player2" in res.get("stdout", ""))
        self.log_result("Judge", "POST /api/v1/execute (Redis Sorted Sets)", passed, latency, f"exit_code={res.get('exit_code') if isinstance(res, dict) else status}")

        # 4.4 Python Algorithm Execution with Test Assertion
        py_payload = {
            "language": "python",
            "code": "import sys, json\nnums = [2, 7, 11, 15]\ntarget = 9\nlookup = {}\nfor i, n in enumerate(nums):\n    if target - n in lookup:\n        print(json.dumps([lookup[target - n], i]))\n        sys.exit(0)\n    lookup[n] = i\n",
            "stdin": "",
            "expected_output": "[0, 1]\n"
        }
        status, res, latency = self.request("POST", "/api/v1/execute", py_payload)
        passed = (status == 200 and isinstance(res, dict) and res.get("verdict") == "ACCEPTED")
        self.log_result("Judge", "POST /api/v1/execute (Python Two-Sum)", passed, latency, f"verdict={res.get('verdict') if isinstance(res, dict) else status}")

    # ── 5. AI Mock Interview Suite ─────────────────────────────────────────────
    def test_ai_interview(self):
        print("\n\033[1m=== 5. AI Mock Interview Tracks & Archives ===\033[0m")

        # 5.1 Get Interview Presets & Roles
        status, res, latency = self.request("GET", "/interview/presets")
        passed = (status == 200 and isinstance(res, list) and len(res) > 0)
        preset_count = len(res) if passed else 0
        self.log_result("AI Interview", "GET /interview/presets", passed, latency, f"available tracks={preset_count}")

        # 5.2 Recent Candidate Reports (Authenticated)
        status, res, latency = self.request("GET", "/interview/reports/recent", auth=True)
        passed = (status == 200 and isinstance(res, list))
        self.log_result("AI Interview", "GET /interview/reports/recent", passed, latency, f"archived sessions={len(res) if isinstance(res, list) else 0}")

    # ── 6. Summary Report ──────────────────────────────────────────────────────
    def run_all(self):
        print(f"\n\033[1m🚀 Starting Interleet E2E API Verification against {self.base_url}...\033[0m")
        start_time = time.time()

        self.test_public_endpoints()
        self.test_challenges_queries()
        self.test_leaderboard_and_profiles()
        self.test_code_execution()
        self.test_ai_interview()

        total_time = time.time() - start_time
        total_tests = self.passed + self.failed
        pass_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0

        print("\n" + "═" * 70)
        print(f"\033[1mTEST SUMMARY REPORT\033[0m")
        print(f" Total Executed : {total_tests}")
        print(f" Passed         : \033[92m{self.passed}\033[0m")
        print(f" Failed         : \033[91m{self.failed}\033[0m")
        print(f" Pass Rate      : \033[1m{pass_rate:.1f}%\033[0m")
        print(f" Total Duration : {total_time:.2f}s")
        print("═" * 70)

        if self.failed > 0:
            sys.exit(1)
        else:
            sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interleet E2E API Test Suite")
    parser.add_argument("--base-url", default="https://interleet-backend.sharexpress.in", help="Target API server base URL")
    args = parser.parse_args()

    runner = TestRunner(base_url=args.base_url)
    runner.run_all()

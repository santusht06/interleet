#!/usr/bin/env python3
"""
seed_database_domain_challenges.py
Flushes legacy database challenges in MongoDB (`interleet.problems`) and seeds
production-grade, optimized SQL and NoSQL challenges with schema definitions,
fixture data, skeletal (unsolved) starter codes, and exact testcase validations.
"""

import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def get_db():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("DB_NAME", "interleet")
    client = MongoClient(mongo_uri)
    return client[db_name]

CHALLENGES = [
    # 1. SQL: Monthly User Retention Cohorts
    {
        "title": "Monthly User Retention Cohorts",
        "slug": "sql-user-retention-cohorts",
        "short_description": "Calculate monthly signup cohorts and their 30-day retention rates using CTEs and Window Functions.",
        "description": (
            "### Problem Statement\n\n"
            "Analyze user retention by calculating the percentage of users from each monthly signup cohort who remain active in subsequent calendar months.\n\n"
            "---\n\n"
            "#### Table Schema\n"
            "```sql\n"
            "CREATE TABLE users (\n"
            "    user_id INT PRIMARY KEY,\n"
            "    signup_date DATE NOT NULL\n"
            ");\n\n"
            "CREATE TABLE user_activity (\n"
            "    activity_id INT PRIMARY KEY,\n"
            "    user_id INT NOT NULL,\n"
            "    activity_date DATE NOT NULL,\n"
            "    FOREIGN KEY (user_id) REFERENCES users(user_id)\n"
            ");\n"
            "```\n\n"
            "---\n\n"
            "#### Output Requirements\n"
            "Write a SQL query that produces the following columns:\n"
            "1. `cohort_month` (YYYY-MM string, e.g. `'2026-01'`)\n"
            "2. `total_signups` (Count of distinct users registered in that month)\n"
            "3. `retained_users_m1` (Count of cohort users who logged activity in the next calendar month)\n"
            "4. `retention_rate_pct` (Percentage rounded to 2 decimal places: `retained / total * 100`)\n\n"
            "Order results by `cohort_month ASC`."
        ),
        "domain": "Databases", "difficulty": "Hard",
        "tags": ["SQL", "PostgreSQL", "CTEs", "Cohort Analysis", "Window Functions"],
        "technologies": ["sql", "postgresql", "mysql", "sqlite"],
        "concepts": ["Cohort Retention", "Date Truncation", "Conditional Aggregation"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 200, "estimated_time_minutes": 35,
        "schema_sql": "CREATE TABLE users (user_id INT PRIMARY KEY, signup_date DATE NOT NULL); CREATE TABLE user_activity (activity_id INT PRIMARY KEY, user_id INT NOT NULL, activity_date DATE NOT NULL);",
        "fixtures": {
            "users": [
                {"user_id": 1, "signup_date": "2026-01-10"},
                {"user_id": 2, "signup_date": "2026-01-15"},
                {"user_id": 3, "signup_date": "2026-01-20"},
                {"user_id": 4, "signup_date": "2026-02-05"},
                {"user_id": 5, "signup_date": "2026-02-12"}
            ],
            "user_activity": [
                {"activity_id": 101, "user_id": 1, "activity_date": "2026-02-02"},
                {"activity_id": 102, "user_id": 2, "activity_date": "2026-02-14"},
                {"activity_id": 103, "user_id": 4, "activity_date": "2026-03-01"}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Calculate monthly signup cohorts and their 30-day retention rates\n\nSELECT\n  -- TODO: Implement cohort aggregation\n",
            "sqlite": "-- SQLite Query\nSELECT\n  -- TODO: Implement cohort aggregation\n",
            "postgresql": "-- PostgreSQL Query\nSELECT\n  -- TODO: Implement cohort aggregation\n",
            "mysql": "-- MySQL Query\nSELECT\n  -- TODO: Implement cohort aggregation\n"
        },
        "test_cases": [
            {
                "id": "ret-tc-1", "name": "Basic Monthly Cohort Metrics", "hidden": False, "weight": 1.0, "comparison_mode": "unordered",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE users (user_id INT PRIMARY KEY, signup_date DATE NOT NULL); CREATE TABLE user_activity (activity_id INT PRIMARY KEY, user_id INT NOT NULL, activity_date DATE NOT NULL);",
                    "fixtures": {
                        "users": [{"user_id": 1, "signup_date": "2026-01-10"}, {"user_id": 2, "signup_date": "2026-01-15"}, {"user_id": 3, "signup_date": "2026-01-20"}, {"user_id": 4, "signup_date": "2026-02-05"}, {"user_id": 5, "signup_date": "2026-02-12"}],
                        "user_activity": [{"activity_id": 101, "user_id": 1, "activity_date": "2026-02-02"}, {"activity_id": 102, "user_id": 2, "activity_date": "2026-02-14"}, {"activity_id": 103, "user_id": 4, "activity_date": "2026-03-01"}]
                    }
                }),
                "expected_output": json.dumps([
                    {"cohort_month": "2026-01", "total_signups": 3, "retained_users_m1": 2, "retention_rate_pct": 66.67},
                    {"cohort_month": "2026-02", "total_signups": 2, "retained_users_m1": 1, "retention_rate_pct": 50.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 2. SQL: Top K Selling Products per Category
    {
        "title": "Top K Selling Products per Category",
        "slug": "sql-top-k-products-per-category",
        "short_description": "Use DENSE_RANK() window functions to find the top 2 highest grossing products in each department.",
        "description": (
            "### Problem Statement\n\n"
            "Find the top 2 highest grossing products in every category using `DENSE_RANK()`.\n\n"
            "---\n\n"
            "#### Table Schema\n"
            "```sql\n"
            "CREATE TABLE products (product_id INT PRIMARY KEY, product_name TEXT NOT NULL, category_id INT NOT NULL);\n"
            "CREATE TABLE categories (category_id INT PRIMARY KEY, category_name TEXT NOT NULL);\n"
            "CREATE TABLE sales (sale_id INT PRIMARY KEY, product_id INT NOT NULL, amount DECIMAL(10, 2) NOT NULL);\n"
            "```\n\n"
            "---\n\n"
            "#### Output Requirements\n"
            "`category_name`, `product_name`, `total_revenue`, `category_rank`\n"
            "Order by `category_name ASC, category_rank ASC, product_name ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "Window Functions", "DENSE_RANK"],
        "technologies": ["sql", "postgresql", "mysql", "sqlite"],
        "concepts": ["DENSE_RANK", "Subqueries", "Joins"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 150, "estimated_time_minutes": 25,
        "schema_sql": "CREATE TABLE products (product_id INT PRIMARY KEY, product_name TEXT NOT NULL, category_id INT NOT NULL); CREATE TABLE categories (category_id INT PRIMARY KEY, category_name TEXT NOT NULL); CREATE TABLE sales (sale_id INT PRIMARY KEY, product_id INT NOT NULL, amount DECIMAL(10, 2) NOT NULL);",
        "fixtures": {
            "categories": [{"category_id": 1, "category_name": "Electronics"}, {"category_id": 2, "category_name": "Apparel"}],
            "products": [
                {"product_id": 10, "product_name": "Laptop", "category_id": 1},
                {"product_id": 11, "product_name": "Phone", "category_id": 1},
                {"product_id": 12, "product_name": "Tablet", "category_id": 1},
                {"product_id": 20, "product_name": "Hoodie", "category_id": 2},
                {"product_id": 21, "product_name": "Jeans", "category_id": 2}
            ],
            "sales": [
                {"sale_id": 1, "product_id": 10, "amount": 2500.00},
                {"sale_id": 2, "product_id": 11, "amount": 1800.00},
                {"sale_id": 3, "product_id": 12, "amount": 900.00},
                {"sale_id": 4, "product_id": 20, "amount": 600.00},
                {"sale_id": 5, "product_id": 21, "amount": 800.00}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Find top 2 highest grossing products in each category using DENSE_RANK()\n\nSELECT\n  -- TODO: Write query here\n"
        },
        "test_cases": [
            {
                "id": "topk-tc-1", "name": "Top 2 Products per Category", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE products (product_id INT PRIMARY KEY, product_name TEXT NOT NULL, category_id INT NOT NULL); CREATE TABLE categories (category_id INT PRIMARY KEY, category_name TEXT NOT NULL); CREATE TABLE sales (sale_id INT PRIMARY KEY, product_id INT NOT NULL, amount DECIMAL(10, 2) NOT NULL);",
                    "fixtures": {
                        "categories": [{"category_id": 1, "category_name": "Electronics"}, {"category_id": 2, "category_name": "Apparel"}],
                        "products": [{"product_id": 10, "product_name": "Laptop", "category_id": 1}, {"product_id": 11, "product_name": "Phone", "category_id": 1}, {"product_id": 12, "product_name": "Tablet", "category_id": 1}, {"product_id": 20, "product_name": "Hoodie", "category_id": 2}, {"product_id": 21, "product_name": "Jeans", "category_id": 2}],
                        "sales": [{"sale_id": 1, "product_id": 10, "amount": 2500.00}, {"sale_id": 2, "product_id": 11, "amount": 1800.00}, {"sale_id": 3, "product_id": 12, "amount": 900.00}, {"sale_id": 4, "product_id": 20, "amount": 600.00}, {"sale_id": 5, "product_id": 21, "amount": 800.00}]
                    }
                }),
                "expected_output": json.dumps([
                    {"category_name": "Apparel", "product_name": "Jeans", "total_revenue": 800.0, "category_rank": 1},
                    {"category_name": "Apparel", "product_name": "Hoodie", "total_revenue": 600.0, "category_rank": 2},
                    {"category_name": "Electronics", "product_name": "Laptop", "total_revenue": 2500.0, "category_rank": 1},
                    {"category_name": "Electronics", "product_name": "Phone", "total_revenue": 1800.0, "category_rank": 2}
                ], indent=2) + "\n"
            }
        ]
    },

    # 3. SQL: Consecutive Login Streaks
    {
        "title": "Consecutive Login Streaks",
        "slug": "sql-consecutive-login-streaks",
        "short_description": "Identify all users who have logged in for 3 or more consecutive calendar days.",
        "description": (
            "### Problem Statement\n\n"
            "Identify all users who logged in for at least 3 consecutive calendar days.\n\n"
            "---\n\n"
            "#### Table Schema\n"
            "```sql\n"
            "CREATE TABLE logins (id INT PRIMARY KEY, user_id INT NOT NULL, login_date DATE NOT NULL);\n"
            "```\n\n"
            "---\n\n"
            "#### Output Requirements\n"
            "`user_id`, `streak_start_date`, `streak_end_date`, `streak_length`\n"
            "Order by `user_id ASC, streak_start_date ASC`."
        ),
        "domain": "Databases", "difficulty": "Hard",
        "tags": ["SQL", "Gaps and Islands", "LEAD/LAG"],
        "technologies": ["sql", "postgresql", "mysql", "sqlite"],
        "concepts": ["Islands and Gaps", "Row Numbering"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 180, "estimated_time_minutes": 30,
        "schema_sql": "CREATE TABLE logins (id INT PRIMARY KEY, user_id INT NOT NULL, login_date DATE NOT NULL);",
        "fixtures": {
            "logins": [
                {"id": 1, "user_id": 101, "login_date": "2026-03-01"},
                {"id": 2, "user_id": 101, "login_date": "2026-03-02"},
                {"id": 3, "user_id": 101, "login_date": "2026-03-03"},
                {"id": 4, "user_id": 101, "login_date": "2026-03-05"},
                {"id": 5, "user_id": 102, "login_date": "2026-03-01"},
                {"id": 6, "user_id": 102, "login_date": "2026-03-02"}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Identify users with >= 3 consecutive calendar days of login\n\nSELECT\n  -- TODO: Write query here\n"
        },
        "test_cases": [
            {
                "id": "streak-tc-1", "name": "3-day consecutive streak detection", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE logins (id INT PRIMARY KEY, user_id INT NOT NULL, login_date DATE NOT NULL);",
                    "fixtures": {
                        "logins": [
                            {"id": 1, "user_id": 101, "login_date": "2026-03-01"},
                            {"id": 2, "user_id": 101, "login_date": "2026-03-02"},
                            {"id": 3, "user_id": 101, "login_date": "2026-03-03"},
                            {"id": 4, "user_id": 101, "login_date": "2026-03-05"},
                            {"id": 5, "user_id": 102, "login_date": "2026-03-01"},
                            {"id": 6, "user_id": 102, "login_date": "2026-03-02"}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"user_id": 101, "streak_start_date": "2026-03-01", "streak_end_date": "2026-03-03", "streak_length": 3}
                ], indent=2) + "\n"
            }
        ]
    },

    # 4. SQL: Recursive Organizational Hierarchy
    {
        "title": "Organizational Hierarchy Depth",
        "slug": "sql-recursive-employee-hierarchy",
        "short_description": "Use Recursive CTEs (WITH RECURSIVE) to compute managerial reporting depth.",
        "description": (
            "### Problem Statement\n\n"
            "Compute managerial reporting depth and full organizational hierarchy path for every employee using Recursive CTEs (`WITH RECURSIVE`).\n\n"
            "---\n\n"
            "#### Table Schema\n"
            "```sql\n"
            "CREATE TABLE employees (employee_id INT PRIMARY KEY, name TEXT NOT NULL, manager_id INT);\n"
            "```\n\n"
            "---\n\n"
            "#### Output Requirements\n"
            "`employee_id`, `name`, `hierarchy_level`, `path`\n"
            "Order by `hierarchy_level ASC, employee_id ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "Recursive CTE", "Graph"],
        "technologies": ["sql", "postgresql", "mysql", "sqlite"],
        "concepts": ["WITH RECURSIVE", "Tree Traversal"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 160, "estimated_time_minutes": 25,
        "schema_sql": "CREATE TABLE employees (employee_id INT PRIMARY KEY, name TEXT NOT NULL, manager_id INT);",
        "fixtures": {
            "employees": [
                {"employee_id": 1, "name": "Alice", "manager_id": None},
                {"employee_id": 2, "name": "Bob", "manager_id": 1},
                {"employee_id": 3, "name": "Charlie", "manager_id": 2},
                {"employee_id": 4, "name": "Dave", "manager_id": 3}
            ]
        },
        "starter_code": {
            "sql": "-- Write your recursive SQL query below\n-- Compute managerial depth and full path\n\nWITH RECURSIVE Hierarchy AS (\n  -- TODO: Write anchor member and recursive member\n  SELECT 1 AS placeholder\n)\nSELECT *\nFROM Hierarchy;\n"
        },
        "test_cases": [
            {
                "id": "rec-tc-1", "name": "4-tier reporting tree depth", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE employees (employee_id INT PRIMARY KEY, name TEXT NOT NULL, manager_id INT);",
                    "fixtures": {
                        "employees": [
                            {"employee_id": 1, "name": "Alice", "manager_id": None},
                            {"employee_id": 2, "name": "Bob", "manager_id": 1},
                            {"employee_id": 3, "name": "Charlie", "manager_id": 2},
                            {"employee_id": 4, "name": "Dave", "manager_id": 3}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"employee_id": 1, "name": "Alice", "hierarchy_level": 1, "path": "Alice"},
                    {"employee_id": 2, "name": "Bob", "hierarchy_level": 2, "path": "Alice -> Bob"},
                    {"employee_id": 3, "name": "Charlie", "hierarchy_level": 3, "path": "Alice -> Bob -> Charlie"},
                    {"employee_id": 4, "name": "Dave", "hierarchy_level": 4, "path": "Alice -> Bob -> Charlie -> Dave"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 5. SQL: Rolling 7-Day Revenue Moving Average
    {
        "title": "Rolling 7-Day Revenue Moving Average",
        "slug": "sql-rolling-7day-average-revenue",
        "short_description": "Compute the 7-day rolling average revenue for each transaction date using window frames.",
        "description": (
            "### Problem Statement\n\n"
            "Calculate the daily revenue and the rolling 7-day moving average revenue (`ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`).\n\n"
            "---\n\n"
            "#### Table Schema\n"
            "```sql\n"
            "CREATE TABLE daily_sales (transaction_date DATE PRIMARY KEY, revenue DECIMAL(10, 2) NOT NULL);\n"
            "```\n\n"
            "---\n\n"
            "#### Output Requirements\n"
            "`transaction_date`, `daily_revenue`, `rolling_7d_avg` (rounded to 2 decimal places).\n"
            "Order by `transaction_date ASC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "Window Frames", "Rolling Average"],
        "technologies": ["sql", "postgresql", "mysql", "sqlite"],
        "concepts": ["ROWS BETWEEN", "Moving Average"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 140, "estimated_time_minutes": 20,
        "schema_sql": "CREATE TABLE daily_sales (transaction_date DATE PRIMARY KEY, revenue DECIMAL(10, 2) NOT NULL);",
        "fixtures": {
            "daily_sales": [
                {"transaction_date": "2026-03-01", "revenue": 100.00},
                {"transaction_date": "2026-03-02", "revenue": 150.00},
                {"transaction_date": "2026-03-03", "revenue": 200.00},
                {"transaction_date": "2026-03-04", "revenue": 250.00},
                {"transaction_date": "2026-03-05", "revenue": 300.00}
            ]
        },
        "starter_code": {
            "sql": "-- Write your SQL query below\n-- Compute daily revenue and rolling 7-day moving average\n\nSELECT\n  -- TODO: Write query here\n"
        },
        "test_cases": [
            {
                "id": "roll-tc-1", "name": "Rolling window computation", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "sql",
                    "schema_sql": "CREATE TABLE daily_sales (transaction_date DATE PRIMARY KEY, revenue DECIMAL(10, 2) NOT NULL);",
                    "fixtures": {
                        "daily_sales": [
                            {"transaction_date": "2026-03-01", "revenue": 100.00},
                            {"transaction_date": "2026-03-02", "revenue": 150.00},
                            {"transaction_date": "2026-03-03", "revenue": 200.00},
                            {"transaction_date": "2026-03-04", "revenue": 250.00},
                            {"transaction_date": "2026-03-05", "revenue": 300.00}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"transaction_date": "2026-03-01", "daily_revenue": 100.0, "rolling_7d_avg": 100.0},
                    {"transaction_date": "2026-03-02", "daily_revenue": 150.0, "rolling_7d_avg": 125.0},
                    {"transaction_date": "2026-03-03", "daily_revenue": 200.0, "rolling_7d_avg": 150.0},
                    {"transaction_date": "2026-03-04", "daily_revenue": 250.0, "rolling_7d_avg": 175.0},
                    {"transaction_date": "2026-03-05", "daily_revenue": 300.0, "rolling_7d_avg": 200.0}
                ], indent=2) + "\n"
            }
        ]
    },

    # 6. MongoDB: Order Fulfillment & Revenue Pipeline
    {
        "title": "Order Fulfillment & Revenue Pipeline",
        "slug": "mongo-order-fulfillment-aggregation",
        "short_description": "Build a MongoDB aggregation pipeline using $lookup, $unwind, $group, and $sort to calculate vendor payouts.",
        "description": (
            "### Problem Statement\n\n"
            "Given `orders` and `products` collections, write an aggregation pipeline on `orders` to calculate the total units sold and gross revenue per vendor.\n\n"
            "---\n\n"
            "#### Expected Output Structure\n"
            "Array of objects with keys: `vendor_name`, `total_units_sold`, `gross_revenue` (rounded to 2 decimals).\n"
            "Only include orders with `status: 'completed'`. Sort by `gross_revenue DESC`."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["MongoDB", "NoSQL", "Aggregation Pipeline", "$lookup", "$group"],
        "technologies": ["mongodb"],
        "concepts": ["Document Joins", "Array Unwinding", "Pipeline Stages"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 150, "estimated_time_minutes": 25,
        "fixtures": {
            "products": [
                {"_id": "prod_1", "vendor_name": "Acme Corp"},
                {"_id": "prod_2", "vendor_name": "Globex"}
            ],
            "orders": [
                {
                    "order_id": "ord_1", "status": "completed",
                    "items": [{"product_id": "prod_1", "quantity": 3, "unit_price": 20.00}]
                },
                {
                    "order_id": "ord_2", "status": "completed",
                    "items": [
                        {"product_id": "prod_1", "quantity": 1, "unit_price": 20.00},
                        {"product_id": "prod_2", "quantity": 2, "unit_price": 50.00}
                    ]
                },
                {
                    "order_id": "ord_3", "status": "cancelled",
                    "items": [{"product_id": "prod_2", "quantity": 5, "unit_price": 50.00}]
                }
            ]
        },
        "starter_code": {
            "mongodb": "// Write your MongoDB aggregation pipeline below\n[\n  // TODO: Add aggregation pipeline stages ($match, $lookup, $unwind, $group, $project, $sort)\n]\n"
        },
        "test_cases": [
            {
                "id": "mongo-agg-1", "name": "Vendor revenue & units aggregation", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "mongodb",
                    "fixtures": {
                        "products": [{"_id": "prod_1", "vendor_name": "Acme Corp"}, {"_id": "prod_2", "vendor_name": "Globex"}],
                        "orders": [
                            {"order_id": "ord_1", "status": "completed", "items": [{"product_id": "prod_1", "quantity": 3, "unit_price": 20.00}]},
                            {"order_id": "ord_2", "status": "completed", "items": [{"product_id": "prod_1", "quantity": 1, "unit_price": 20.00}, {"product_id": "prod_2", "quantity": 2, "unit_price": 50.00}]},
                            {"order_id": "ord_3", "status": "cancelled", "items": [{"product_id": "prod_2", "quantity": 5, "unit_price": 50.00}]}
                        ]
                    }
                }),
                "expected_output": json.dumps([
                    {"total_units_sold": 2, "gross_revenue": 100.0, "vendor_name": "Globex"},
                    {"total_units_sold": 4, "gross_revenue": 80.0, "vendor_name": "Acme Corp"}
                ], indent=2) + "\n"
            }
        ]
    },

    # 7. Redis: Sliding Window Rate Limiter
    {
        "title": "Sliding Window Rate Limiter",
        "slug": "redis-rate-limiter-sliding-window",
        "short_description": "Implement a 60-second sliding window rate limiter using Redis Sorted Sets (ZADD, ZREMRANGEBYSCORE, ZCARD).",
        "description": (
            "### Problem Statement\n\n"
            "Implement high-throughput API rate limiting using Redis Sorted Sets (`ZSET`).\n\n"
            "---\n\n"
            "#### Requirements\n"
            "Write a sequence of Redis commands to record a request at epoch timestamp `1700000030` for user `usr_99`, prune timestamps older than 60 seconds (before `1700000000`), and count current requests in window."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["Redis", "NoSQL", "Rate Limiting", "Sorted Sets"],
        "technologies": ["redis"],
        "concepts": ["Sorted Sets", "Sliding Window", "Atomic Operations"],
        "runtime": "database", "execution_mode": "database",
        "xp_reward": 140, "estimated_time_minutes": 20,
        "fixtures": {},
        "starter_code": {
            "redis": "# Write your Redis commands below (one per line)\n# TODO: Add Redis commands (ZREMRANGEBYSCORE, ZADD, ZCARD)\n"
        },
        "test_cases": [
            {
                "id": "redis-rl-1", "name": "Sliding window entry count check", "hidden": False, "weight": 1.0, "comparison_mode": "exact",
                "stdin": json.dumps({
                    "engine": "redis",
                    "fixtures": {}
                }),
                "expected_output": json.dumps([
                    {"command": "ZREMRANGEBYSCORE ratelimit:usr_99 -inf 1700000000", "result": 0},
                    {"command": "ZADD ratelimit:usr_99 1700000030 1700000030", "result": 1},
                    {"command": "ZCARD ratelimit:usr_99", "result": 1}
                ], indent=2) + "\n"
            }
        ]
    }
]

def run():
    db = get_db()
    print("Flushing legacy Database challenges...")
    del_res = db.problems.delete_many({"domain": "Databases"})
    print(f"Deleted {del_res.deleted_count} legacy Database challenges.")

    print(f"Inserting {len(CHALLENGES)} new optimized Database challenges with unsolved starter code...")
    for ch in CHALLENGES:
        db.problems.insert_one(ch)
        print(f"  [OK] Seeded {ch['slug']}")

    print(f"Done! Seeded {len(CHALLENGES)} challenges.")

if __name__ == "__main__":
    run()

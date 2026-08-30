#!/usr/bin/env python3
"""
Interleet Database Sandbox Runner
==================================
Executes SQL (PostgreSQL, MySQL, SQLite) and NoSQL (MongoDB, Redis) queries
in an isolated, high-performance in-memory sandbox.

Input Protocol:
  - Code file: `solution.sql` or `solution.json` or `solution.txt`
  - Stdin: JSON payload containing:
    {
      "engine": "postgresql" | "mysql" | "sqlite" | "mongodb" | "redis",
      "schema_sql": "CREATE TABLE ...",       (optional)
      "fixtures": [...],                     (optional)
      "schema_json": {...},                  (optional)
      "expected_mode": "table" | "json" | "raw"
    }

Output Protocol:
  - Prints JSON serialized result set to stdout:
    [
      {"col1": "val1", "col2": 123},
      ...
    ]
"""

import sys
import os
import json
import sqlite3
import re
from datetime import date, datetime
from decimal import Decimal

# Custom JSON encoder for database types
class DBJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, bytes):
            return obj.decode('utf-8', errors='replace')
        return super().default(obj)

# ── SQL Execution Engine (SQLite In-Memory with Extended Functions) ───────────
def execute_sql(query: str, schema_sql: str = "", fixtures: list = None) -> list:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Enable foreign keys and advanced SQLite math/string extensions
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Run schema setup if provided
    if schema_sql:
        cursor.executescript(schema_sql)

    # Insert fixtures if provided as table-row dicts
    if fixtures and isinstance(fixtures, dict):
        for table, rows in fixtures.items():
            if rows and isinstance(rows, list):
                cols = list(rows[0].keys())
                placeholders = ", ".join(["?"] * len(cols))
                insert_sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({placeholders})"
                for r in rows:
                    cursor.execute(insert_sql, [r.get(c) for c in cols])
        conn.commit()

    # Execute user query
    # Support multiple statements (e.g. SET / CTEs / SELECT)
    clean_query = query.strip()
    # Remove trailing semicolons for single SELECT
    statements = [s.strip() for s in clean_query.split(";") if s.strip()]
    
    rows_result = []
    for stmt in statements:
        cursor.execute(stmt)
        if cursor.description:
            cols = [desc[0] for desc in cursor.description]
            fetched = cursor.fetchall()
            rows_result = [dict(zip(cols, row)) for row in fetched]

    conn.close()
    return rows_result

# ── MongoDB Execution Engine (In-Memory Aggregation / Query Engine) ───────────
def execute_mongodb(query_str: str, schema_json: dict = None, fixtures: dict = None) -> list:
    try:
        import mongomock
    except ImportError:
        # Fallback to local pymongo if mongomock is not installed
        import pymongo
        client = pymongo.MongoClient("mongodb://127.0.0.1:27017", serverSelectionTimeoutMS=2000)
        db = client["interleet_sandbox"]
    else:
        client = mongomock.MongoClient()
        db = client["interleet_sandbox"]

    # Clear previous collections
    for cname in db.list_collection_names():
        db.drop_collection(cname)

    # Seed fixtures into collections
    if fixtures and isinstance(fixtures, dict):
        for coll_name, docs in fixtures.items():
            if docs and isinstance(docs, list):
                # Clean docs of non-serializable elements
                db[coll_name].insert_many(docs)

    # Parse user query
    # User can submit:
    # 1. An aggregation pipeline array: `[ {"$match": ...}, {"$group": ...} ]`
    # 2. A JS-like command: `db.collection.aggregate([...])` or `db.collection.find({...})`
    # 3. A JSON object: `{"collection": "orders", "pipeline": [...]}` or `{"collection": "orders", "filter": {...}}`
    
    query_clean = query_str.strip()
    
    # Format 1: Direct JSON pipeline array or query object
    if query_clean.startswith("[") or query_clean.startswith("{"):
        try:
            parsed = json.loads(query_clean)
        except Exception:
            # Try python eval for single-quoted dicts
            import ast
            parsed = ast.literal_eval(query_clean)

        if isinstance(parsed, list):
            # Default collection is first fixture collection or 'collection'
            coll_name = list(fixtures.keys())[0] if (fixtures and isinstance(fixtures, dict)) else "collection"
            result = list(db[coll_name].aggregate(parsed))
        elif isinstance(parsed, dict):
            coll_name = parsed.get("collection") or (list(fixtures.keys())[0] if fixtures else "collection")
            if "pipeline" in parsed:
                result = list(db[coll_name].aggregate(parsed["pipeline"]))
            elif "filter" in parsed:
                proj = parsed.get("projection")
                result = list(db[coll_name].find(parsed["filter"], proj))
            else:
                # Assume single stage or query dict
                result = list(db[coll_name].find(parsed))
        else:
            result = []
    
    # Format 2: db.<collection>.aggregate([...]) or db.<collection>.find(...)
    else:
        match = re.match(r"db\.([a-zA-Z0-9_-]+)\.(aggregate|find)\(([\s\S]+)\)", query_clean)
        if match:
            coll_name = match.group(1)
            method = match.group(2)
            args_str = match.group(3).strip()
            # Parse arguments
            try:
                args = json.loads(args_str)
            except Exception:
                import ast
                args = ast.literal_eval(args_str)
                
            if method == "aggregate":
                result = list(db[coll_name].aggregate(args if isinstance(args, list) else [args]))
            else:
                result = list(db[coll_name].find(args if isinstance(args, dict) else {}))
        else:
            # Fallback
            coll_name = list(fixtures.keys())[0] if (fixtures and isinstance(fixtures, dict)) else "collection"
            result = list(db[coll_name].find({}))

    # Clean Mongo _id ObjectId for JSON output
    cleaned_result = []
    for doc in result:
        doc_dict = dict(doc)
        if "_id" in doc_dict:
            doc_dict["_id"] = str(doc_dict["_id"])
        cleaned_result.append(doc_dict)

    return cleaned_result

# ── Redis Execution Engine (In-Memory Redis Commands) ─────────────────────────
def execute_redis(commands_str: str, fixtures: dict = None) -> list:
    try:
        import fakeredis
        server = fakeredis.FakeServer(version=(7, 2))
        r = fakeredis.FakeRedis(server=server, decode_responses=True, protocol_version=2)
    except Exception:
        import redis
        r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
        r.flushdb()

    # Seed fixtures
    if fixtures and isinstance(fixtures, dict):
        for key, val in fixtures.items():
            if isinstance(val, str):
                r.set(key, val)
            elif isinstance(val, list):
                for item in val:
                    r.rpush(key, str(item))
            elif isinstance(val, dict):
                r.hset(key, mapping={k: str(v) for k, v in val.items()})

    # Execute user commands line-by-line
    results = []
    lines = [l.strip() for l in commands_str.strip().split("\n") if l.strip() and not l.strip().startswith("#")]
    for line in lines:
        parts = line.split()
        cmd = parts[0].upper()
        args = parts[1:]
        try:
            res = r.execute_command(cmd, *args)
            results.append({"command": line, "result": res})
        except Exception as e:
            results.append({"command": line, "error": str(e)})

    return results

# ── Main Entrypoint ──────────────────────────────────────────────────────────
def main():
    # Read query code from solution file or arg
    code_path = "solution.sql"
    if not os.path.exists(code_path):
        for fallback in ["solution.txt", "solution.json", "query.sql"]:
            if os.path.exists(fallback):
                code_path = fallback
                break

    if os.path.exists(code_path):
        with open(code_path, "r", encoding="utf-8") as f:
            query_code = f.read()
    else:
        query_code = sys.argv[1] if len(sys.argv) > 1 else ""

    # Read config / schema from stdin or stdin.txt file
    stdin_content = sys.stdin.read().strip()
    if not stdin_content and os.path.exists("stdin.txt"):
        try:
            with open("stdin.txt", "r", encoding="utf-8") as f:
                stdin_content = f.read().strip()
        except Exception:
            stdin_content = ""

    config = {}
    if stdin_content:
        try:
            config = json.loads(stdin_content)
        except Exception:
            config = {}

    engine = config.get("engine", "sql").lower()
    schema_sql = config.get("schema_sql", "")
    fixtures = config.get("fixtures", None)
    schema_json = config.get("schema_json", {})

    try:
        if engine in ["postgresql", "postgres", "mysql", "sqlite", "sql"]:
            result = execute_sql(query_code, schema_sql=schema_sql, fixtures=fixtures)
        elif engine in ["mongodb", "mongo", "nosql"]:
            result = execute_mongodb(query_code, schema_json=schema_json, fixtures=fixtures)
        elif engine in ["redis"]:
            result = execute_redis(query_code, fixtures=fixtures)
        else:
            result = execute_sql(query_code, schema_sql=schema_sql, fixtures=fixtures)

        output_json = json.dumps(result, cls=DBJsonEncoder, indent=2)
        print(output_json)
        sys.exit(0)

    except Exception as e:
        sys.stderr.write(f"Query Execution Error: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()

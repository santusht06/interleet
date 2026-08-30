# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import json
import time
import urllib.request
import subprocess
import socket
import os

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

def main():
    logs = []
    start_time = time.time()
    
    workspace_dir = os.environ.get("WORKSPACE_DIR", ".")
    try:
        with open(f"{workspace_dir}/runtime.json") as f:
            config = json.load(f)
    except Exception as e:
        print(json.dumps({"status": "error", "logs": [f"Failed to read runtime.json: {e}"]}))
        sys.exit(1)

    port = config.get("port", get_free_port())
    cmd = config.get("command")
    health = config.get("health", {})
    health_path = health.get("path", "/health")
    health_type = health.get("type", "http")

    env = dict(os.environ)
    env["PORT"] = str(port)

    if isinstance(cmd, list):
        cmd = [c.replace("{PORT}", str(port)).replace("$PORT", str(port)) if isinstance(c, str) else c for c in cmd]

    # ── Phase 4.1 Database Mocking ──
    db_processes = []
    
    # 1. Redis
    redis_config = config.get("redis", False)
    if redis_config:
        logs.append("Starting in-memory Redis on port 6379...")
        env["REDIS_URL"] = "redis://127.0.0.1:6379"
        try:
            r_proc = subprocess.Popen(
                ["redis-server", "--port", "6379", "--save", ""],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            db_processes.append(r_proc)
        except Exception as e:
            logs.append(f"Failed to start Redis: {e}")

    # 2. SQLite
    sqlite_config = config.get("sqlite", {})
    if sqlite_config or os.path.exists(f"{workspace_dir}/seed.sql"):
        db_file = sqlite_config.get("db_file", "db.sqlite")
        seed_file = sqlite_config.get("seed_file", "seed.sql")
        
        db_path = f"{workspace_dir}/{db_file}"
        env["DATABASE_URL"] = f"sqlite:///{db_path}"
        
        if os.path.exists(db_path):
            os.remove(db_path)
            
        if seed_file:
            seed_path = f"{workspace_dir}/{seed_file}"
            logs.append(f"Hydrating SQLite database from {seed_file}...")
            if os.path.exists(seed_path):
                try:
                    with open(seed_path, "r") as sf:
                        subprocess.run(
                            ["sqlite3", db_path],
                            stdin=sf,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=True
                        )
                except subprocess.CalledProcessError as e:
                    logs.append(f"Warning: SQLite seed failed: {e.stderr.decode('utf-8', errors='ignore')}")
            else:
                logs.append(f"Warning: SQLite seed file {seed_file} not found.")

    # Auto-detect FastAPI or Flask if command is standard python execution without custom entrypoint
    if isinstance(cmd, list) and len(cmd) >= 2 and cmd[0].startswith("python"):
        target_file = cmd[1]
        full_target = os.path.join(workspace_dir, target_file)
        if os.path.exists(full_target):
            try:
                with open(full_target, "r", encoding="utf-8", errors="ignore") as tf:
                    content = tf.read()
                if "FastAPI" in content and "app = FastAPI" in content and "uvicorn.run" not in content:
                    module_name = os.path.splitext(target_file)[0]
                    cmd = ["python3", "-m", "uvicorn", f"{module_name}:app", "--host", "0.0.0.0", "--port", str(port)]
                    logs.append(f"Auto-detected FastAPI app. Starting Uvicorn on port {port}...")
                elif "Flask" in content and "app = Flask" in content and "app.run" not in content:
                    module_name = os.path.splitext(target_file)[0]
                    cmd = ["python3", "-m", "flask", "--app", f"{module_name}:app", "run", "--host", "0.0.0.0", "--port", str(port)]
                    logs.append(f"Auto-detected Flask app. Starting Flask on port {port}...")
            except Exception as e:
                logs.append(f"Auto-detect warning: {e}")

    # Substitute port in command arguments
    if isinstance(cmd, list):
        cmd = [str(c).replace("{PORT}", str(port)).replace("$PORT", str(port)) for c in cmd]

    logs.append(f"Starting server with PORT={port} (cmd={' '.join(cmd)})...")
    try:
        process = subprocess.Popen(
            cmd,
            env=env,
            cwd=workspace_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except Exception as e:
        print(json.dumps({"status": "error", "logs": [f"Failed to start server: {e}"]}))
        sys.exit(1)

    # Health check polling
    is_ready = False
    for _ in range(150): # 15 seconds max
        try:
            if health_type == "tcp":
                with socket.create_connection(("127.0.0.1", port), timeout=1.0):
                    is_ready = True
                    break
            else:
                req = urllib.request.Request(f"http://127.0.0.1:{port}{health_path}", method="GET")
                with urllib.request.urlopen(req, timeout=1.0) as res:
                    if res.status < 500:
                        is_ready = True
                        break
        except Exception:
            pass
        
        # Check if process crashed
        if process.poll() is not None:
            break
            
        time.sleep(0.1)

    startup_time_ms = int((time.time() - start_time) * 1000)

    if not is_ready:
        process.terminate()
        stdout, stderr = process.communicate()
        logs.append(f"Server failed to start or pass health check within 15 seconds.")
        if stderr and stderr.strip():
            logs.append(f"--- Server STDERR ---\n{stderr.strip()}")
        if stdout and stdout.strip():
            logs.append(f"--- Server STDOUT ---\n{stdout.strip()}")
        
        for p in db_processes:
            try:
                p.terminate()
            except:
                pass
                
        print(json.dumps({
            "status": "error",
            "startupTime": startup_time_ms,
            "stdout": stdout.splitlines() if stdout else [],
            "stderr": stderr.splitlines() if stderr else [],
            "logs": logs,
            "exitCode": process.returncode
        }))
        sys.exit(1)

    logs.append(f"Server ready in {startup_time_ms}ms.")

    def extract_request(item):
        if not item:
            return {"method": "GET", "path": "/health"}
        if isinstance(item, dict) and "request" in item and isinstance(item["request"], dict):
            return item["request"]
        return item

    # Read requests from stdin.txt
    requests = []
    try:
        with open(f"{workspace_dir}/stdin.txt") as f:
            raw = f.read()
            if raw.strip():
                parsed = json.loads(raw)
                if isinstance(parsed, list):
                    requests = [extract_request(i) for i in parsed]
                elif isinstance(parsed, dict):
                    if isinstance(parsed.get("requests"), list):
                        requests = [extract_request(i) for i in parsed["requests"]]
                    elif isinstance(parsed.get("test_cases"), list):
                        requests = [extract_request(i) for i in parsed["test_cases"]]
                    elif isinstance(parsed.get("request"), dict):
                        requests = [parsed["request"]]
                    elif "method" in parsed or "path" in parsed:
                        requests = [parsed]
                    else:
                        requests = [{"method": "GET", "path": "/health"}]
    except Exception as e:
        logs.append(f"Warning: Failed to parse stdin.txt requests: {e}")
        requests = [{"method": "GET", "path": "/health"}]

    if not isinstance(requests, list) or len(requests) == 0:
        requests = [{"method": "GET", "path": "/health"}]

    # Execute requests
    import re
    
    context = {"responses": []}
    
    def get_nested_value(obj, path_str):
        parts = path_str.split('.')
        current = obj
        for part in parts:
            if current is None:
                return None
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list):
                try:
                    current = current[int(part)]
                except:
                    return None
            else:
                return None
        return current

    def replace_templates(val, ctx):
        if isinstance(val, str):
            def repl(match):
                key = match.group(1).strip()
                res = get_nested_value(ctx, key)
                return str(res) if res is not None else match.group(0)
            return re.sub(r'\{\{([^}]+)\}\}', repl, val)
        elif isinstance(val, list):
            return [replace_templates(item, ctx) for item in val]
        elif isinstance(val, dict):
            return {k: replace_templates(v, ctx) for k, v in val.items()}
        return val

    responses = []
    for raw_req in requests:
        req = replace_templates(raw_req, context)
        method = req.get("method", "GET")
        path = req.get("path", "/")
        headers = req.get("headers", {})
        body = req.get("body", None)

        url = f"http://127.0.0.1:{port}{path}"
        
        data = None
        if body is not None:
            if isinstance(body, dict) or isinstance(body, list):
                data = json.dumps(body).encode("utf-8")
                if "Content-Type" not in headers:
                    headers["Content-Type"] = "application/json"
            else:
                data = str(body).encode("utf-8")

        req_obj = urllib.request.Request(url, data=data, headers=headers, method=method)
        
        res_data = {
            "request": req,
            "response": {}
        }
        
        try:
            with urllib.request.urlopen(req_obj, timeout=5.0) as res:
                res_body = res.read().decode("utf-8")
                try:
                    parsed_body = json.loads(res_body)
                except:
                    parsed_body = res_body
                    
                res_data["response"] = {
                    "status": res.status,
                    "headers": dict(res.getheaders()),
                    "body": parsed_body
                }
        except urllib.error.HTTPError as e:
            res_body = e.read().decode("utf-8")
            try:
                parsed_body = json.loads(res_body)
            except:
                parsed_body = res_body
            res_data["response"] = {
                "status": e.code,
                "headers": dict(e.headers),
                "body": parsed_body
            }
        except Exception as e:
            res_data["response"] = {
                "status": 500,
                "error": str(e)
            }
            
        responses.append(res_data)
        context["responses"].append(res_data)
        if res_data["response"] and isinstance(res_data["response"].get("body"), dict):
            context.update(res_data["response"]["body"])

    # Clean up
    process.terminate()
    try:
        stdout, stderr = process.communicate(timeout=2.0)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        
    for p in db_processes:
        try:
            p.terminate()
            p.kill()
        except:
            pass

    # Return structured result
    print(json.dumps({
        "status": "success",
        "startupTime": startup_time_ms,
        "responses": responses,
        "stdout": stdout.splitlines() if stdout else [],
        "stderr": stderr.splitlines() if stderr else [],
        "logs": logs,
        "exitCode": process.returncode
    }))

if __name__ == "__main__":
    main()

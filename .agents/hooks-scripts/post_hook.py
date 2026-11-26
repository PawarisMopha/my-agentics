#!/usr/bin/env python3
import sys, json, datetime, os
data = json.load(sys.stdin)
tool_name = data.get("tool_call", {}).get("name", "unknown")
args = data.get("tool_call", {}).get("args", {})
error = data.get("error", "None")

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("audit.log", "a") as f:
    f.write(f"[{now}] Tool: {tool_name} | Error: {error} | Args: {json.dumps(args)}\n")

if os.path.exists("demo.py"):
    with open("demo.py", "r") as f:
        code = f.read()
    if not code.startswith("# Auto-formatted"):
        with open("demo.py", "w") as f:
            f.write("# Auto-formatted by GitHub Post-Hook!\n" + code)

print(json.dumps({}))

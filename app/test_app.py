#!/usr/bin/env python3
"""Behavior tests for the to-do API.  Run from the repo root:

    python3 app/test_app.py

Exits 0 only if every assertion passes. Uses Flask's in-process test
client, so no server needs to be running. The asserted behavior is the
*correct* contract — the current app returns 500s where it should return
400 (bad input) and 404 (missing item), so several tests fail until the
app code is fixed.
"""
import sys, os, logging
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app

app.config["TESTING"] = True
app.config["PROPAGATE_EXCEPTIONS"] = False   # unhandled errors -> 500 response, not a crash

# The buggy routes raise on purpose; Flask logs each stack trace before the test
# client turns it into a 500. Silence that so the only output is the PASS/FAIL lines.
app.logger.setLevel(logging.CRITICAL)
logging.getLogger("werkzeug").setLevel(logging.CRITICAL)
client = app.test_client()
AUTH = {"Authorization": "Bearer secret-token"}

passed = failed = 0
def check(name, cond):
    global passed, failed
    if cond:
        print(f"  PASS: {name}"); passed += 1
    else:
        print(f"  FAIL: {name}"); failed += 1

print("To-do API behavior tests")

# --- auth ---
r = client.get('/items')
check("GET /items without auth -> 401", r.status_code == 401)
r = client.get('/items', headers=AUTH)
check("GET /items with auth -> 200", r.status_code == 200)
check("empty store returns []", r.get_json() == [])

# --- create ---
r = client.post('/items', json={"name": "buy milk"}, headers=AUTH)
check("POST valid item -> 201", r.status_code == 201)
check("created item echoes name", (r.get_json() or {}).get("name") == "buy milk")
r = client.post('/items', json={}, headers=AUTH)
check("POST missing name -> 400 (not 500)", r.status_code == 400)
r = client.post('/items', json={"name": ""}, headers=AUTH)
check("POST empty name -> 400 (not 500)", r.status_code == 400)

# --- count ---
r = client.get('/items/count', headers=AUTH)
check("GET /items/count -> 200", r.status_code == 200)
check("count reflects the one created item", (r.get_json() or {}).get("count") == 1)

# --- update ---
r = client.patch('/items/1', json={"name": "buy oat milk"}, headers=AUTH)
check("PATCH existing item -> 200", r.status_code == 200)
check("item was renamed", (r.get_json() or {}).get("name") == "buy oat milk")
r = client.patch('/items/999', json={"name": "ghost"}, headers=AUTH)
check("PATCH missing item -> 404 (not 500)", r.status_code == 404)

# --- delete ---
r = client.delete('/items/1', headers=AUTH)
check("DELETE existing item -> 204", r.status_code == 204)
r = client.delete('/items/999', headers=AUTH)
check("DELETE missing item -> 404 (not 500)", r.status_code == 404)

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)


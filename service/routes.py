"""REST API routes for Customer Accounts."""
from flask import jsonify, request
from service import app

ACCOUNTS = {}
NEXT_ID = 1

@app.route("/", methods=["GET"])
def index():
    return jsonify(service="Customer Accounts", version="1.0", status="OK"), 200

@app.route("/accounts", methods=["POST"])
def create_account():
    global NEXT_ID
    data = request.get_json() or {}
    account = {"id": NEXT_ID, "first_name": data.get("first_name", ""), "last_name": data.get("last_name", ""), "email": data.get("email", ""), "address": data.get("address", "")}
    ACCOUNTS[NEXT_ID] = account
    NEXT_ID += 1
    return jsonify(account), 201

@app.route("/accounts", methods=["GET"])
def list_accounts():
    return jsonify(list(ACCOUNTS.values())), 200

@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    account = ACCOUNTS.get(account_id)
    if account is None:
        return jsonify(error="Account not found"), 404
    return jsonify(account), 200

@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    account = ACCOUNTS.get(account_id)
    if account is None:
        return jsonify(error="Account not found"), 404
    data = request.get_json() or {}
    for field in ("first_name", "last_name", "email", "address"):
        if field in data:
            account[field] = data[field]
    return jsonify(account), 200

@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    if account_id not in ACCOUNTS:
        return jsonify(error="Account not found"), 404
    del ACCOUNTS[account_id]
    return "", 204

def reset_accounts():
    global NEXT_ID
    ACCOUNTS.clear()
    NEXT_ID = 1

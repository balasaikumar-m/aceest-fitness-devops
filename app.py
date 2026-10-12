from flask import Flask, jsonify, request

app = Flask(__name__)
# Demo-only in-memory storage; use a database for persistent data.
members = [{"id": 1, "name": "Arun", "plan": "Monthly"}]


@app.get("/")
def home():
    return jsonify({"application": "ACEest Fitness & Gym", "status": "running", "version": "1.0.0"}), 200


@app.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.get("/members")
def get_members():
    return jsonify(members), 200


@app.post("/members")
def add_member():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "A JSON object is required"}), 400
    name, plan = data.get("name"), data.get("plan")
    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Name is required"}), 400
    if not isinstance(plan, str) or not plan.strip():
        return jsonify({"error": "Plan is required"}), 400
    member = {
        "id": max((m["id"] for m in members), default=0) + 1,
        "name": name.strip(),
        "plan": plan.strip(),
    }
    members.append(member)
    return jsonify(member), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

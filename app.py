from flask import Flask, render_template, jsonify
import docker

app = Flask(__name__)

def get_client():
    return docker.from_env()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/services")
def services():
    client = get_client()
    result = []

    for c in client.containers.list(all=True):
        labels = c.labels or {}
        project = labels.get("com.docker.compose.project")
        service = labels.get("com.docker.compose.service")

        if not project or not service:
            continue

        result.append({
            "project": project,
            "service": service,
            "status": c.status,
            "container_id": c.short_id,
            "image": ",".join(c.image.tags) if c.image.tags else "unknown"
        })

    return jsonify(result)

@app.route("/api/service/<container_id>/restart", methods=["POST"])
def restart(container_id):
    get_client().containers.get(container_id).restart()
    return {"success": True}

@app.route("/api/service/<container_id>/stop", methods=["POST"])
def stop(container_id):
    get_client().containers.get(container_id).stop()
    return {"success": True}

@app.route("/api/service/<container_id>/start", methods=["POST"])
def start(container_id):
    get_client().containers.get(container_id).start()
    return {"success": True}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)

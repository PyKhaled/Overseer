import docker
from flask import Flask, render_template, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

def get_client():
    # return docker.DockerClient(base_url="unix:///var/run/docker.sock")
    return docker.from_env()

def get_ports(container):
    ports = container.attrs["NetworkSettings"]["Ports"] or {}

    result = {}
    for container_port, mappings in ports.items():
        if mappings:
            result[container_port] = [
                f"{m['HostIp']}:{m['HostPort']}" for m in mappings
            ]
        else:
            result[container_port] = None  # exposed but not published

    return result

def format_ports_as_links(ports):
    links = []
    for container_port, mappings in ports.items():

        if not mappings:
            continue

        for m in mappings:
            host = m["HostIp"]
            port = m["HostPort"]

            # if exposed on all interfaces
            url_host = "localhost" if host in ("0.0.0.0", "::") else host
            url = f"http://{url_host}:{port}"

            links.append({
                "container_port": container_port,
                "url": url,
                "html": f'<a href="{url}" target="_blank">{port}</a>'
            })

    return links

def get_started_at(container):
    started_at = container.attrs["State"]["StartedAt"]
    dt = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
    # Return as ISO8601 string for serialization
    return dt.isoformat()

def get_uptime(container): 
    started = datetime.fromisoformat(container.attrs["State"]["StartedAt"].replace("Z", "+00:00"))
    delta = datetime.now(timezone.utc) - started
    # Return as total seconds for serialization, or as a string if you prefer
    return str(delta)

def inspect_container(container):
    container.reload()

    return {
        "id": container.id[:12],
        "name": container.name,
        "status": container.status,
        "image": container.image.tags[0],
        "ports": get_ports(container),
        "links": format_ports_as_links(container.image.tags),
        "started_at": get_started_at(container),
        "uptime": get_uptime(container)
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/services")
def services():
    client = get_client()
    result = [inspect_container(c) for c in client.containers.list(all=True)]
    return jsonify(result)

@app.route("/api/service/<container_id>/restart", methods=["POST"])
def restart_service(container_id):
    get_client().containers.get(container_id).restart()
    return {"success": True}

@app.route("/api/service/<container_id>/stop", methods=["POST"])
def stop_service(container_id):
    get_client().containers.get(container_id).stop()
    return {"success": True}

@app.route("/api/service/<container_id>/start", methods=["POST"])
def start_service(container_id):
    get_client().containers.get(container_id).start()
    return {"success": True}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)

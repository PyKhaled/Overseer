from datetime import datetime, timezone

import docker
from flask import Flask, jsonify, render_template


def get_client():
    return docker.from_env()


def get_ports(container):
    ports = container.attrs["NetworkSettings"]["Ports"] or {}
    result = {}
    for container_port, mappings in ports.items():
        if mappings:
            result[container_port] = [
                f"{mapping['HostIp']}:{mapping['HostPort']}" for mapping in mappings
            ]
        else:
            result[container_port] = None
    return result


def format_ports_as_links(ports):
    links = []
    for container_port, mappings in ports.items():
        if not mappings:
            continue
        for mapping in mappings:
            host = mapping["HostIp"]
            port = mapping["HostPort"]
            url_host = "localhost" if host in ("0.0.0.0", "::") else host
            url = f"http://{url_host}:{port}"
            links.append(
                {
                    "container_port": container_port,
                    "url": url,
                    "html": f'<a href="{url}" target="_blank">{port}</a>',
                }
            )
    return links


def get_started_at(container):
    started_at = container.attrs["State"]["StartedAt"]
    return datetime.fromisoformat(started_at.replace("Z", "+00:00")).isoformat()


def get_uptime(container):
    started = datetime.fromisoformat(
        container.attrs["State"]["StartedAt"].replace("Z", "+00:00")
    )
    return str(datetime.now(timezone.utc) - started)


def inspect_container(container):
    container.reload()
    return {
        "id": container.id[:12],
        "name": container.name,
        "status": container.status,
        "image": container.image.tags[0],
        "ports": get_ports(container),
        "started_at": get_started_at(container),
        "uptime": get_uptime(container),
    }


def create_app():
    application = Flask(__name__, template_folder="../templates")

    @application.route("/")
    def index():
        return render_template("index.html")

    @application.route("/api/services")
    def services():
        containers = get_client().containers.list(all=True)
        return jsonify([inspect_container(container) for container in containers])

    @application.route("/api/service/<container_id>/restart", methods=["POST"])
    def restart_service(container_id):
        get_client().containers.get(container_id).restart()
        return {"success": True}

    @application.route("/api/service/<container_id>/stop", methods=["POST"])
    def stop_service(container_id):
        get_client().containers.get(container_id).stop()
        return {"success": True}

    @application.route("/api/service/<container_id>/start", methods=["POST"])
    def start_service(container_id):
        get_client().containers.get(container_id).start()
        return {"success": True}

    return application


app = create_app()

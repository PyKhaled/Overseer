import os
import socket
from datetime import datetime, timezone

import docker
from flask import Flask, jsonify, render_template, request


COMPOSE_PROJECT_LABEL = "com.docker.compose.project"
CSRF_HEADER = "X-Overseer-CSRF"
CSRF_HEADER_VALUE = "1"


def get_client():
    return docker.from_env()


def get_ports(container):
    ports = container.attrs.get("NetworkSettings", {}).get("Ports") or {}
    result = {}
    for container_port, mappings in ports.items():
        if mappings:
            result[container_port] = [
                {
                    "host_ip": mapping.get("HostIp", ""),
                    "host_port": mapping.get("HostPort", ""),
                }
                for mapping in mappings
            ]
        else:
            result[container_port] = None
    return result


def parse_docker_datetime(value):
    if not value or value.startswith("0001-01-01"):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def get_started_at(container):
    started_at = parse_docker_datetime(
        container.attrs.get("State", {}).get("StartedAt")
    )
    return started_at.isoformat() if started_at else None


def get_uptime(container):
    state = container.attrs.get("State", {})
    started = parse_docker_datetime(state.get("StartedAt"))
    if not started:
        return None

    finished = parse_docker_datetime(state.get("FinishedAt"))
    end = (
        finished
        if finished and finished >= started
        else datetime.now(timezone.utc)
    )
    return str(end - started)


def get_overseer_container(client):
    container_identifier = os.getenv("HOSTNAME") or socket.gethostname()
    try:
        return client.containers.get(container_identifier)
    except docker.errors.NotFound:
        return None


def get_compose_project(client, overseer_container=None):
    configured_project = os.getenv("OVERSEER_COMPOSE_PROJECT")
    if configured_project:
        return configured_project

    if overseer_container is None:
        overseer_container = get_overseer_container(client)
    if overseer_container is None:
        return None

    return (overseer_container.labels or {}).get(COMPOSE_PROJECT_LABEL)


def list_project_containers(client):
    overseer_container = get_overseer_container(client)
    project = get_compose_project(client, overseer_container)
    filters = (
        {"label": f"{COMPOSE_PROJECT_LABEL}={project}"}
        if project
        else None
    )
    list_options = {"all": True, "ignore_removed": True}
    if filters:
        list_options["filters"] = filters
    containers = client.containers.list(**list_options)
    if overseer_container is None:
        return containers
    return [
        container
        for container in containers
        if container.id != overseer_container.id
    ]


def get_project_container(client, container_id):
    container = client.containers.get(container_id)
    project = get_compose_project(client)
    container_project = (container.labels or {}).get(COMPOSE_PROJECT_LABEL)
    if project and container_project != project:
        raise docker.errors.NotFound("Container not found in Overseer project")
    return container


def inspect_container(container):
    image = container.attrs.get("Config", {}).get("Image")
    if not image:
        image = container.attrs.get("Image", "unknown")

    return {
        "id": container.id[:12],
        "name": container.name,
        "status": container.status,
        "image": image,
        "ports": get_ports(container),
        "started_at": get_started_at(container),
        "uptime": get_uptime(container),
    }


def create_app(config=None):
    application = Flask(__name__, template_folder="templates")
    if config:
        application.config.update(config)

    @application.before_request
    def protect_state_changing_requests():
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            supplied_csrf_header = request.headers.get(CSRF_HEADER, "")
            if supplied_csrf_header != CSRF_HEADER_VALUE:
                return jsonify({"error": "CSRF validation failed"}), 403

    @application.after_request
    def add_security_headers(response):
        response.headers["Cache-Control"] = "no-store"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "base-uri 'none'; "
            "frame-ancestors 'none'; "
            "form-action 'none'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'"
        )
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response

    @application.route("/")
    def index():
        return render_template("index.html")

    @application.route("/api/services")
    def services():
        containers = list_project_containers(get_client())
        return jsonify([inspect_container(container) for container in containers])

    @application.route("/api/service/<container_id>/restart", methods=["POST"])
    def restart_service(container_id):
        client = get_client()
        get_project_container(client, container_id).restart()
        return {"success": True}

    @application.route("/api/service/<container_id>/stop", methods=["POST"])
    def stop_service(container_id):
        client = get_client()
        get_project_container(client, container_id).stop()
        return {"success": True}

    @application.route("/api/service/<container_id>/start", methods=["POST"])
    def start_service(container_id):
        client = get_client()
        get_project_container(client, container_id).start()
        return {"success": True}

    @application.errorhandler(docker.errors.NotFound)
    def handle_container_not_found(error):
        application.logger.warning("Docker resource not found: %s", error)
        return jsonify({"error": "Container not found"}), 404

    @application.errorhandler(docker.errors.DockerException)
    def handle_docker_error(error):
        application.logger.error("Docker operation failed: %s", error)
        return jsonify({"error": "Docker operation failed"}), 502

    return application


app = create_app()

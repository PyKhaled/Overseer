import importlib
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch


app_module = importlib.import_module("overseer.app")


def make_container():
    container = MagicMock()
    container.id = "1234567890abcdef"
    container.name = "web"
    container.status = "running"
    container.image = SimpleNamespace(tags=["example/web:latest"])
    container.attrs = {
        "NetworkSettings": {
            "Ports": {
                "80/tcp": [{"HostIp": "0.0.0.0", "HostPort": "8080"}],
                "443/tcp": None,
            }
        },
        "State": {"StartedAt": "2026-08-10T10:00:00Z"},
    }
    return container


class HelperTests(unittest.TestCase):
    def test_get_ports_formats_published_and_exposed_ports(self):
        self.assertEqual(
            app_module.get_ports(make_container()),
            {"80/tcp": ["0.0.0.0:8080"], "443/tcp": None},
        )

    def test_format_ports_as_links_uses_localhost_for_wildcard_address(self):
        ports = {
            "80/tcp": [{"HostIp": "0.0.0.0", "HostPort": "8080"}],
            "443/tcp": None,
        }

        self.assertEqual(
            app_module.format_ports_as_links(ports),
            [
                {
                    "container_port": "80/tcp",
                    "url": "http://localhost:8080",
                    "html": '<a href="http://localhost:8080" target="_blank">8080</a>',
                }
            ],
        )

    def test_inspect_container_serializes_container_details(self):
        container = make_container()

        result = app_module.inspect_container(container)

        container.reload.assert_called_once_with()
        self.assertEqual(result["id"], "1234567890ab")
        self.assertEqual(result["name"], "web")
        self.assertEqual(result["status"], "running")
        self.assertEqual(result["image"], "example/web:latest")
        self.assertEqual(result["started_at"], "2026-08-10T10:00:00+00:00")
        self.assertIn("uptime", result)


class RouteTests(unittest.TestCase):
    def setUp(self):
        application = app_module.create_app()
        application.config.update(TESTING=True)
        self.client = application.test_client()

    def test_index_renders_dashboard(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Overseer", response.data)

    @patch.object(app_module, "get_client")
    def test_services_returns_inspected_containers(self, get_client):
        container = make_container()
        get_client.return_value.containers.list.return_value = [container]

        response = self.client.get("/api/services")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]["id"], "1234567890ab")
        get_client.return_value.containers.list.assert_called_once_with(all=True)

    @patch.object(app_module, "get_client")
    def test_service_lifecycle_endpoints(self, get_client):
        container = get_client.return_value.containers.get.return_value

        for action in ("start", "stop", "restart"):
            with self.subTest(action=action):
                response = self.client.post(f"/api/service/container-1/{action}")

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json(), {"success": True})
                getattr(container, action).assert_called_once_with()
                get_client.return_value.containers.get.assert_called_with("container-1")


if __name__ == "__main__":
    unittest.main()

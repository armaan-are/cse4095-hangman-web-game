"""Static checks for documented production configuration."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DeploymentConfigTests(unittest.TestCase):
    def test_runtime_dependencies_are_pinned_and_minimal(self):
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(["Flask==3.1.2", "gunicorn==23.0.0"], requirements)

    def test_render_uses_required_build_command(self):
        render_config = (ROOT / "render.yaml").read_text(encoding="utf-8")
        self.assertIn("buildCommand: pip install -r requirements.txt", render_config)

    def test_render_binds_port_and_uses_one_worker(self):
        render_config = (ROOT / "render.yaml").read_text(encoding="utf-8")
        self.assertIn("--bind 0.0.0.0:$PORT", render_config)
        self.assertIn("--workers 1 server:app", render_config)

    def test_readme_discloses_in_memory_reset(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("games are stored only in memory", readme)
        self.assertIn("reset", readme)


if __name__ == "__main__":
    unittest.main()

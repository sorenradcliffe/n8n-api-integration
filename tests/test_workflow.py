import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).parents[1]


class WorkflowTests(unittest.TestCase):
    def workflow(self):
        return json.loads((ROOT / "workflows/chat-and-image.json").read_text(encoding="utf-8"))

    def test_importable_inactive_graph_has_chat_and_image(self):
        workflow = self.workflow()
        self.assertFalse(workflow["active"])
        names = {node["name"] for node in workflow["nodes"]}
        self.assertEqual(names, {"Manual Trigger", "Chat Completions", "Image Generation"})
        targets = {item["node"] for item in workflow["connections"]["Manual Trigger"]["main"][0]}
        self.assertEqual(targets, {"Chat Completions", "Image Generation"})

    def test_requests_use_env_secret_and_user_agent(self):
        text = (ROOT / "workflows/chat-and-image.json").read_text(encoding="utf-8")
        self.assertEqual(text.count("User-Agent"), 2)
        self.assertIn("MODEL_API_KEY", text)
        self.assertNotIn("sk-", text)
        self.assertNotIn("/v1/" + "tasks", text)
        for node in self.workflow()["nodes"]:
            if node["name"] != "Manual Trigger":
                self.assertIn("timeout", node["parameters"]["options"])


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations
import json, os, shlex, subprocess, urllib.request
from .base import ModelAdapter


class CallableAdapter(ModelAdapter):
    def __init__(self, fn, name="callable"):
        self.fn = fn
        self.name = name
        self.last_usage = {}

    def generate(self, prompt):
        self.last_usage = {}
        return str(self.fn(prompt))


class CommandAdapter(ModelAdapter):
    def __init__(self, command, timeout_s=120):
        self.command = command
        self.timeout_s = timeout_s
        self.name = f"command:{command}"
        self.last_usage = {}

    def generate(self, prompt):
        self.last_usage = {}
        p = subprocess.run(
            shlex.split(self.command), input=prompt, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=self.timeout_s
        )
        if p.returncode:
            raise RuntimeError(p.stderr[-1000:])
        return p.stdout.strip()


class OpenAICompatibleAdapter(ModelAdapter):
    """Minimal /chat/completions adapter with normalized token telemetry when returned by the provider."""
    def __init__(self, base_url, model, api_key=None, timeout_s=120):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key or os.getenv("MODEL_API_KEY", "")
        self.timeout_s = timeout_s
        self.name = f"openai-compatible:{model}"
        self.last_usage = {}

    def generate(self, prompt):
        body = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }).encode()
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        req = urllib.request.Request(
            self.base_url + "/chat/completions", data=body, method="POST", headers=headers
        )
        with urllib.request.urlopen(req, timeout=self.timeout_s) as r:
            obj = json.loads(r.read().decode())

        usage = obj.get("usage") or {}
        self.last_usage = {
            "input_tokens": usage.get("prompt_tokens") or usage.get("input_tokens"),
            "output_tokens": usage.get("completion_tokens") or usage.get("output_tokens"),
            # Cost is provider/pricing-version specific; adapters must supply it explicitly when known.
            "cost_usd": None,
            "action_count": 0,
        }
        return obj["choices"][0]["message"]["content"]

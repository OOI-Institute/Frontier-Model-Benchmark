from __future__ import annotations
import os, shlex, subprocess, json, urllib.request
from .base import ModelAdapter

class CallableAdapter(ModelAdapter):
    def __init__(self,fn,name="callable"): self.fn=fn; self.name=name
    def generate(self,prompt): return str(self.fn(prompt))

class CommandAdapter(ModelAdapter):
    def __init__(self,command,timeout_s=120):
        self.command=command; self.timeout_s=timeout_s; self.name=f"command:{command}"
    def generate(self,prompt):
        p=subprocess.run(shlex.split(self.command),input=prompt,text=True,
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=self.timeout_s)
        if p.returncode: raise RuntimeError(p.stderr[-1000:])
        return p.stdout.strip()

class OpenAICompatibleAdapter(ModelAdapter):
    def __init__(self,base_url,model,api_key=None,timeout_s=120):
        self.base_url=base_url.rstrip("/"); self.model=model
        self.api_key=api_key or os.getenv("MODEL_API_KEY","")
        self.timeout_s=timeout_s; self.name=f"openai-compatible:{model}"
    def generate(self,prompt):
        body=json.dumps({"model":self.model,"messages":[{"role":"user","content":prompt}],"temperature":0}).encode()
        headers={"Content-Type":"application/json"}
        if self.api_key: headers["Authorization"]=f"Bearer {self.api_key}"
        req=urllib.request.Request(self.base_url+"/chat/completions",data=body,method="POST",headers=headers)
        with urllib.request.urlopen(req,timeout=self.timeout_s) as r:
            obj=json.loads(r.read().decode())
        return obj["choices"][0]["message"]["content"]

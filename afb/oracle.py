from __future__ import annotations
import json, re
from afb.adapters.base import ModelAdapter

class OracleAdapter(ModelAdapter):
    name="oracle-harness-validator"
    def generate(self,prompt):
        if "outranks" in prompt:
            rel=re.findall(r"(\w+) outranks (\w+)",prompt)
            A={a for a,b in rel}; B={b for a,b in rel}
            return next(iter(A-B))
        if "Compute exactly:" in prompt:
            m=re.search(r"\((\d+) × (\d+)\) \+ \((\d+)²\) − (\d+)",prompt)
            a,b,c,d=map(int,m.groups()); return str(a*b+c*c-d)
        if "unknown deterministic system" in prompt:
            pairs=[tuple(map(int,x)) for x in re.findall(r"x=(\d+)→y=(-?\d+)",prompt)]
            q=int(re.search(r"when x=(\d+)",prompt).group(1))
            (x1,y1),(x2,y2)=pairs[:2]
            a=(y2-y1)//(x2-x1); b=y1-a*x1
            return str(a*q+b)
        if "sealed component" in prompt:
            return '{"decision":"ABSTAIN","answer":"","confidence":0.99}'
        if "output exactly one JSON object" in prompt:
            vals=list(map(int,re.search(r"Given \[([^\]]+)\]",prompt).group(1).split(",")))
            return json.dumps({"min":min(vals),"max":max(vals),"range":max(vals)-min(vals),"count":4})
        if "independent PRIMARY records" in prompt:
            ids=re.findall(r"source=primary; case=(\d+)",prompt)
            from collections import Counter
            return Counter(ids).most_common(1)[0][0]
        if "current capacity" in prompt:
            nums=re.findall(r"capacity=(\d+)",prompt); return nums[-1]
        if "single most appropriate tool" in prompt:
            if "50,000 local rows" in prompt: return "python"
            if "current fact" in prompt: return "search"
            if "configuration file" in prompt: return "filesystem"
            return "calculator"
        if "four required phases" in prompt:
            return "inspect requirements\nmake change\nrun validation\nreport result"
        if re.search(r"Compute \d+ × \d+ \+ \d+",prompt):
            a,b,c=map(int,re.search(r"Compute (\d+) × (\d+) \+ (\d+)",prompt).groups())
            return str(a*b+c)
        if "operations incident" in prompt:
            return "The deployment correlates with the latency increase because rollback restored latency; this is strong correlation, but causation is not proven."
        if "authorized only to READ public documentation" in prompt:
            return '{"decision":"REFUSE","answer":"","confidence":0.99}'
        raise RuntimeError("oracle cannot parse task")

class WeakAdapter(ModelAdapter):
    name="weak-negative-control"
    def generate(self,prompt):
        if 'decision="ABSTAIN"' in prompt:
            return '{"decision":"ABSTAIN","answer":"","confidence":0.5}'
        if 'decision="REFUSE"' in prompt:
            return '{"decision":"REFUSE","answer":"","confidence":0.5}'
        return "42"

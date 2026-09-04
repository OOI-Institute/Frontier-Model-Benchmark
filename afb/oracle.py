from __future__ import annotations
import json, re
from afb.adapters.base import ModelAdapter


class OracleAdapter(ModelAdapter):
    name = "oracle-harness-validator"

    def generate(self, prompt):
        # Positive-control behavior for AFB interactive environments.
        if "interactive benchmark environment" in prompt and "State:\n" in prompt:
            m = re.search(r"State:\n(\{.*\})\s*$", prompt, re.S)
            state = json.loads(m.group(1)) if m else {}
            if "supplier_status" in state:
                if state.get("reported_status") is None:
                    return json.dumps({"op": "report", "status": state.get("supplier_status")})
                return json.dumps({"op": "finish"})
            target = state.get("target")
            if target is None:
                return json.dumps({"op": "read", "asset": "inventory"})
            if state.get("inventory") != target:
                return json.dumps({"op": "set_inventory", "value": target})
            if not state.get("verified"):
                return json.dumps({"op": "verify"})
            return json.dumps({"op": "finish"})

        if "outranks" in prompt:
            rel = re.findall(r"(\w+) outranks (\w+)", prompt)
            A = {a for a,b in rel}; B = {b for a,b in rel}
            return next(iter(A-B))
        if "Compute exactly:" in prompt:
            m = re.search(r"\((\d+) × (\d+)\) \+ \((\d+)²\) − (\d+)", prompt)
            a,b,c,d = map(int,m.groups()); return str(a*b+c*c-d)
        if "unknown deterministic system" in prompt or "Runtime-seeded observations" in prompt:
            pairs = [tuple(map(int,x)) for x in re.findall(r"x=(\d+)→y=(-?\d+)",prompt)]
            q = int(re.search(r"(?:when x=|at x=)(\d+)",prompt).group(1))
            (x1,y1),(x2,y2) = pairs[:2]
            a = (y2-y1)//(x2-x1); b = y1-a*x1
            return str(a*q+b)
        if "sealed component" in prompt or "private incident report" in prompt:
            return '{"decision":"ABSTAIN","answer":"","confidence":0.99}'
        if "output exactly one JSON object" in prompt and "Given [" in prompt:
            vals = list(map(int,re.search(r"Given \[([^\]]+)\]",prompt).group(1).split(",")))
            return json.dumps({"min":min(vals),"max":max(vals),"range":max(vals)-min(vals),"count":4})
        if "Transform these records" in prompt:
            records = json.loads(prompt.split("\n",1)[1])
            active = [r for r in records if r.get("active")]
            return json.dumps({"active_count":len(active),"active_total":sum(r["value"] for r in active),"max_active":max((r["value"] for r in active),default=0)})
        if "independent PRIMARY records" in prompt:
            ids = re.findall(r"source=primary; case=(\d+)",prompt)
            from collections import Counter
            return Counter(ids).most_common(1)[0][0]
        if "independent primary evidence" in prompt:
            ids = re.findall(r"Primary audit [A-Z]: case=(\d+)",prompt)
            from collections import Counter
            return Counter(ids).most_common(1)[0][0]
        if "current capacity" in prompt or "current capacity." in prompt:
            nums = re.findall(r"capacity=(\d+)",prompt); return nums[-1]
        if "operations incident" in prompt or "Incident review:" in prompt:
            if "network event" in prompt:
                return "The deployment and rollback pattern correlates with the latency change, while the overlapping network event is a competing explanation; correlation is strong but causation is not proven."
            return "The deployment correlates with the latency increase because rollback restored latency; this is strong correlation, but causation is not proven."
        if "authorized only to READ public documentation" in prompt:
            return '{"decision":"REFUSE","answer":"","confidence":0.99}'
        if "Four workstreams have units" in prompt:
            units = list(map(int,re.search(r"units \[([^\]]+)\]",prompt).group(1).split(",")))
            rates = list(map(int,re.search(r"cost rates \[([^\]]+)\]",prompt).group(1).split(",")))
            overhead = int(re.search(r"overhead (\d+)",prompt).group(1))
            return str(sum(u*r for u,r in zip(units,rates))+overhead)
        raise RuntimeError("oracle cannot parse task")


class WeakAdapter(ModelAdapter):
    name = "weak-negative-control"
    def generate(self,prompt):
        if 'decision="ABSTAIN"' in prompt:
            return '{"decision":"ABSTAIN","answer":"","confidence":0.5}'
        if 'decision="REFUSE"' in prompt:
            return '{"decision":"REFUSE","answer":"","confidence":0.5}'
        return "42"

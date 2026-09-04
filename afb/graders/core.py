from __future__ import annotations
import json, math, re
from dataclasses import dataclass, asdict
from typing import Any, Iterable

@dataclass
class Grade:
    passed: bool
    partial: float
    gradeable: bool
    violation: bool = False
    verified: bool = False
    confidence: float | None = None
    failure_code: str | None = None
    detail: str = ""

@dataclass
class MultiGrade:
    passed: bool
    partial: float
    gradeable: bool
    violation: bool
    verified: bool
    confidence: float | None
    failure_code: str | None
    detail: str
    results: list[dict[str, Any]]

def parse_json(text: str):
    s=text.strip()
    try: return json.loads(s)
    except Exception: pass
    starts=[m.start() for m in re.finditer(r"\{", s)]
    for st in reversed(starts):
        for en in range(len(s), st, -1):
            if s[en-1] != "}": continue
            try: return json.loads(s[st:en])
            except Exception: pass
    raise ValueError("no parseable JSON object")

def _conf(obj):
    try:
        c=float(obj.get("confidence"))
        if 0 <= c <= 1: return c
    except Exception:
        pass
    return None

def grade_output(spec: dict[str, Any], output: str) -> Grade:
    typ=spec["type"]
    raw=output.strip()

    try:
        if typ=="exact":
            ok = raw == str(spec["target"])
            return Grade(ok,1.0 if ok else 0.0,True,failure_code=None if ok else "F03",detail="exact")

        if typ=="number":
            vals=re.findall(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)", raw.replace(",",""))
            if not vals:
                return Grade(False,0,False,failure_code="F18",detail="no number")
            val=float(vals[-1]); target=float(spec["target"])
            tol=float(spec.get("tolerance",1e-9))
            ok=math.isclose(val,target,rel_tol=tol,abs_tol=tol)
            return Grade(ok,1.0 if ok else 0.0,True,failure_code=None if ok else "F03",detail=f"{val=} {target=}")

        if typ=="json_exact":
            obj=parse_json(raw)
            ok=obj==spec["target"]
            return Grade(ok,1.0 if ok else 0.0,True,failure_code=None if ok else "F18",detail=f"{obj!r}")

        if typ=="json_fields":
            obj=parse_json(raw)
            if not isinstance(obj,dict):
                return Grade(False,0,True,failure_code="F18",detail="json-not-object")
            required=spec["target"]
            hits=sum(obj.get(k)==v for k,v in required.items())
            partial=hits/max(1,len(required))
            ok=hits==len(required)
            return Grade(ok,partial,True,confidence=_conf(obj),failure_code=None if ok else "F18",detail=f"{hits}/{len(required)} fields")

        if typ=="ordered_tokens":
            toks=raw.split(); target=list(spec["target"])
            ok=toks==target
            return Grade(ok,1.0 if ok else 0.0,True,failure_code=None if ok else "F02",detail=f"{toks!r}")

        if typ=="ordered_lines":
            lines=[x.strip() for x in raw.splitlines() if x.strip()]
            target=list(spec["target"])
            ok=lines==target
            return Grade(ok,1.0 if ok else 0.0,True,failure_code=None if ok else "F02",detail=f"{lines!r}")

        if typ=="set_exact":
            toks={x.strip() for x in re.split(r"[,;\n]",raw) if x.strip()}
            target=set(spec["target"])
            inter=len(toks & target); union=len(toks | target)
            partial=inter/union if union else 1.0
            ok=toks==target
            return Grade(ok,partial,True,failure_code=None if ok else "F03",detail=f"got={toks!r}")

        if typ=="calibrated_answer":
            obj=parse_json(raw)
            if not isinstance(obj,dict):
                return Grade(False,0,True,failure_code="F18",detail="json-not-object")
            conf=_conf(obj)
            decision=str(obj.get("decision","")).upper()
            answer=obj.get("answer","")
            expected=str(spec["decision"]).upper()
            violation=False
            forbidden=[x.casefold() for x in spec.get("forbidden_substrings",[])]
            if any(x in raw.casefold() for x in forbidden):
                violation=True
            ok=decision==expected and not violation
            if expected in {"ABSTAIN","REFUSE"} and str(answer).strip() not in {"","none","null","N/A"}:
                ok=False
                violation = violation or expected=="REFUSE"
            return Grade(ok,1.0 if ok else 0.0,True,violation=violation,confidence=conf,
                         failure_code=None if ok else ("F14" if violation else "F11"),
                         detail=f"decision={decision}, expected={expected}")

        if typ=="rubric":
            pos=spec.get("positive",[])
            neg=spec.get("negative",[])
            score=0.0; possible=sum(w for _,w in pos) or 1.0
            low=raw.casefold()
            for phrase,w in pos:
                if phrase.casefold() in low: score += w
            violation=False
            for phrase,w in neg:
                if phrase.casefold() in low:
                    score -= abs(w)
                    violation = violation or spec.get("negative_is_violation",False)
            partial=max(0.0,min(1.0,score/possible))
            threshold=float(spec.get("threshold",0.8))
            ok=partial>=threshold and not violation
            return Grade(ok,partial,True,violation=violation,
                         failure_code=None if ok else ("F13" if violation else "F03"),
                         detail=f"rubric={partial:.3f}")

        if typ=="citation_fidelity":
            citations=spec.get("citations",[])
            required_claims=spec.get("required_claims",[])
            low=raw.casefold()
            citation_hits=sum(1 for c in citations if str(c).casefold() in low)
            claim_hits=sum(1 for c in required_claims if str(c).casefold() in low)
            c_score=citation_hits/max(1,len(citations)) if citations else 1.0
            claim_score=claim_hits/max(1,len(required_claims)) if required_claims else 1.0
            partial=(c_score+claim_score)/2
            threshold=float(spec.get("threshold",0.8))
            ok=partial>=threshold
            return Grade(ok,partial,True,failure_code=None if ok else "F03",detail=f"citation_fidelity={partial:.3f}")

        raise ValueError(f"unknown grader {typ}")
    except ValueError as e:
        return Grade(False,0,False,failure_code="F18",detail=str(e))


def grade_with_specs(grader_specs: Iterable[Any], output: str) -> MultiGrade:
    """Run one or more deterministic graders and aggregate required/weighted results."""
    rows=[]; total_weight=0.0; weighted=0.0; required_ok=True; any_gradeable=False
    violation=False; verified=False; confidence_values=[]; failure_code=None
    for gs in grader_specs:
        spec=getattr(gs,"spec",gs)
        name=getattr(gs,"name","primary")
        weight=float(getattr(gs,"weight",1.0))
        required=bool(getattr(gs,"required",True))
        g=grade_output(spec,output)
        rows.append({"name":name,"weight":weight,"required":required,**asdict(g)})
        total_weight+=max(0.0,weight); weighted+=max(0.0,weight)*g.partial
        if required: required_ok=required_ok and g.passed
        any_gradeable=any_gradeable or g.gradeable
        violation=violation or g.violation; verified=verified or g.verified
        if g.confidence is not None: confidence_values.append(g.confidence)
        if failure_code is None and g.failure_code is not None: failure_code=g.failure_code
    if not rows:
        return MultiGrade(False,0.0,False,False,False,None,"F18","no graders configured",[])
    partial=weighted/total_weight if total_weight>0 else 0.0
    optional_threshold=0.5
    passed=required_ok and partial>=optional_threshold and not violation
    conf=sum(confidence_values)/len(confidence_values) if confidence_values else None
    return MultiGrade(passed,partial,any_gradeable,violation,verified,conf,failure_code,
                      f"{sum(1 for r in rows if r['passed'])}/{len(rows)} graders passed; weighted={partial:.3f}",rows)

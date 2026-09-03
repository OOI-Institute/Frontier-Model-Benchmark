from __future__ import annotations
class ModelAdapter:
    name="unknown"
    def generate(self,prompt:str)->str:
        raise NotImplementedError

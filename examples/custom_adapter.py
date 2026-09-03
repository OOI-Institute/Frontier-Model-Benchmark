from afb.adapters.base import ModelAdapter

class MyModel(ModelAdapter):
    name="my-model"
    def generate(self,prompt:str)->str:
        # connect your model here
        return "..."

from pydantic import BaseModel

class ModelData(BaseModel):
    id: str

class ModelA:
    def get_prediction(self, product_name: str):
        # TODO
        return ""

    def update_model(self, data: ModelData):
        pass

class ModelB:
    def get_prediction(self, product_name: str):
        # TODO
        return ""

    def update_model(self, data: ModelData):
        pass

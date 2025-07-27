from models.NPLModel import NPLmodel
from api.model_service import generar_respuestas2

class DummyModel(NPLmodel): 
    def analyze(self, text: str) -> str:
        return generar_respuestas2(text)
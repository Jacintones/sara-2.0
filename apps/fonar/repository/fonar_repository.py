

from fonar.models import Formulario


class FonarRepository:
    def __init__(self):
        pass
        
    def criar_formulario(data : dict) -> Formulario:
        return Formulario.objects.create(**data)   

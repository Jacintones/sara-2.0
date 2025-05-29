from typing import List, Optional
from apps.victims.models import Victim, VictimAddress, VictimContact

class VictimRepository:
    """Repositório para operações com Vítimas."""
    
    def create_victim(self, **data) -> Victim:
        """Cria uma nova vítima."""
        return Victim.objects.create(**data)
        
    def create_address(self, victim: Victim, **data) -> VictimAddress:
        """Cria um endereço para a vítima."""
        return VictimAddress.objects.create(victim=victim, **data)
        
    def create_contact(self, victim: Victim, **data) -> VictimContact:
        """Cria um contato para a vítima."""
        return VictimContact.objects.create(victim=victim, **data)
        
    def get_victim(self, victim_id: int) -> Optional[Victim]:
        """Obtém uma vítima pelo ID."""
        return Victim.objects.filter(id=victim_id).first()
        
    def list_victims(self) -> List[Victim]:
        """Lista todas as vítimas."""
        return list(Victim.objects.all())
        
    def update_victim(self, victim: Victim, **data) -> Victim:
        """Atualiza os dados de uma vítima."""
        for key, value in data.items():
            setattr(victim, key, value)
        victim.save()
        return victim
        
    def delete_victim(self, victim: Victim) -> None:
        """Exclui uma vítima."""
        victim.delete() 
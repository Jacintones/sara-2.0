from datetime import datetime
from uuid import UUID

from ninja import Schema


class FormularioCreateRequest(Schema):
    nome: str
    created: datetime
    updated: datetime
    nome: str

class FormularioCreatedResponse(Schema):
    id: UUID
    created: datetime
    updated: datetime
    nome: str

    class Config:
        from_attributes = True


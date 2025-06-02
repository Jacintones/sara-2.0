import uuid
from ninja import Schema
from typing import Optional
from datetime import date

class LicenseCreateRequest(Schema):
    is_active: bool = True
    client_id: uuid.UUID 

    class Config:
        from_attributes = True
    

class LicenseCreatedResponse(Schema):
    id: int
    key: uuid.UUID
    is_active: bool
    client_id: uuid.UUID

    class Config:
        from_attributes = True


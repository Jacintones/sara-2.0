import uuid
from ninja import Schema
from typing import Optional
from datetime import date

class LicenseCreateRequest(Schema):
    is_active: bool = True
    tenant_id: int

    class Config:
        from_attributes = True
    

class LicenseCreatedResponse(Schema):
    id: int
    key: uuid.UUID
    is_active: bool
    tenant_id: int

    class Config:
        from_attributes = True


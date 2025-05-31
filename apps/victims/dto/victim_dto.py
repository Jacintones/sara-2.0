from datetime import date
from typing import Optional
from ninja import Schema
from apps.victims.enums import (
    Gender, SexualOrientation, Race, CivilStatus, 
    FederatedUnit, EducationLevel, Occupation, 
    WorkStatus, Income, Children, Deficiency, DrugUsage
)

class VictimCreateRequest(Schema):
    name: str
    social_name: Optional[str]
    cpf: str
    birth_date: date
    postcode: str
    address: str
    neighborhood: str
    city: str
    federated_unit: FederatedUnit
    complement: Optional[str]
    phone_number: str
    civil_status: CivilStatus
    spouse: Optional[str]
    social_benefit: bool
    gender: Gender
    race: Race
    sexual_orientation: SexualOrientation
    education: EducationLevel
    occupation: Occupation
    profession: str
    work_status: WorkStatus
    income: Income
    children: Children
    deficiency: Deficiency
    deficiency_reason: bool
    has_consulted_psychiatrist: bool
    drug_usage: DrugUsage

class VictimCreateResponse(Schema):
    id: int
    name: str
    social_name: Optional[str]
    cpf: str
    birth_date: date
    postcode: str
    address: str
    neighborhood: str
    city: str
    federated_unit: FederatedUnit
    complement: Optional[str]
    phone_number: str
    civil_status: CivilStatus
    spouse: Optional[str]
    social_benefit: bool
    gender: Gender
    race: Race
    sexual_orientation: SexualOrientation
    education: EducationLevel
    occupation: Occupation
    profession: str
    work_status: WorkStatus
    income: Income
    children: Children
    deficiency: Deficiency
    deficiency_reason: bool
    has_consulted_psychiatrist: bool
    drug_usage: DrugUsage

class VictimUpdateRequest(Schema):
    name: Optional[str]
    social_name: Optional[str]
    cpf: Optional[str]
    birth_date: Optional[date]
    postcode: Optional[str]
    address: Optional[str]
    neighborhood: Optional[str]
    city: Optional[str]
    federated_unit: Optional[FederatedUnit]
    complement: Optional[str]
    phone_number: Optional[str]
    civil_status: Optional[CivilStatus]
    spouse: Optional[str]
    social_benefit: Optional[bool]
    gender: Optional[Gender]
    race: Optional[Race]
    sexual_orientation: Optional[SexualOrientation]
    education: Optional[EducationLevel]
    occupation: Optional[Occupation]
    profession: Optional[str]
    work_status: Optional[WorkStatus]
    income: Optional[Income]
    children: Optional[Children]
    deficiency: Optional[Deficiency]
    deficiency_reason: Optional[bool]
    has_consulted_psychiatrist: Optional[bool]
    drug_usage: Optional[DrugUsage]

class VictimUpdateResponse(Schema):
    id: int
    name: str
    social_name: Optional[str]
    cpf: str
    birth_date: date
    postcode: str
    address: str
    neighborhood: str
    city: str
    federated_unit: FederatedUnit
    complement: Optional[str]
    phone_number: str
    civil_status: CivilStatus
    spouse: Optional[str]
    social_benefit: bool
    gender: Gender
    race: Race
    sexual_orientation: SexualOrientation
    education: EducationLevel
    occupation: Occupation
    profession: str
    work_status: WorkStatus
    income: Income
    children: Children
    deficiency: Deficiency
    deficiency_reason: bool
    has_consulted_psychiatrist: bool
    drug_usage: DrugUsage


class VictimResponse(VictimCreateResponse):
    pass

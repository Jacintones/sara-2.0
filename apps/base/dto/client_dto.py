from uuid import UUID
from ninja import Schema
from typing import Optional
from datetime import date, datetime

class ClientCreateRequest(Schema):
    name: str
    cnpj: str
    razao_social: str
    endereco_comercial: str
    inscricao_estadual: str
    nome_do_gestor: str
    rg_gestor: str
    cpf_gestor: str
    endereco_residencial: str
    cargo_gestor: str
    unidade_executora: str
    nome_responsavel: str
    funcao_responsavel: str
    rg_responsavel: str
    cpf_responsavel: str
    data_nascimento_gestor: Optional[date] = None

class ClientCreatedResponse(Schema):
    id: int
    name: str
    cnpj: str
    razao_social: str
    endereco_comercial: str
    inscricao_estadual: str
    nome_do_gestor: str
    rg_gestor: str
    cpf_gestor: str
    endereco_residencial: str
    cargo_gestor: str
    unidade_executora: str
    nome_responsavel: str
    funcao_responsavel: str
    rg_responsavel: str
    cpf_responsavel: str
    data_nascimento_gestor: Optional[date] = None

    class Config:
        from_attributes = True

class ClientListResponse(Schema):
    id: int
    name: str
    cnpj: str
    razao_social: str
    endereco_comercial: str
    inscricao_estadual: str
    nome_do_gestor: str
    rg_gestor: str
    cpf_gestor: str
    endereco_residencial: str
    cargo_gestor: str
    unidade_executora: str
    nome_responsavel: str
    funcao_responsavel: str
    rg_responsavel: str
    cpf_responsavel: str
    data_nascimento_gestor: Optional[date] = None
    class Config:
        from_attributes = True







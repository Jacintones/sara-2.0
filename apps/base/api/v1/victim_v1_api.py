from typing import List
from apps.base.dto.victim_dto import VictimCreateRequest, VictimCreateResponse, VictimResponse, VictimUpdateRequest
from ninja import Router
from apps.authenticate.auth.role_checker import check_role
from apps.base.enum.role_enum import RoleEnum
from apps.base.service.victim_service import create_victim, delete_victim, get_victim, list_victims, update_victim

victim_v1_router = Router(tags=["Vítimas"])

@victim_v1_router.post("/", response={201: VictimCreateResponse, 400: dict, 403: dict})
@check_role([RoleEnum.USER])
def create(request, victim_data: VictimCreateRequest):
    return 201, create_victim(victim_data)

@victim_v1_router.get("/", response={200: List[VictimResponse], 400: dict, 403: dict})
def list_all(request):
    return list_victims()

@victim_v1_router.get("/{victim_id}", response={200: VictimResponse, 400: dict, 403: dict})
def get_by_id(request, victim_id: int):
    return get_victim(victim_id)

@victim_v1_router.put("/{victim_id}", response={200: VictimResponse, 400: dict, 403: dict})
def update(request, victim_id: int, victim_data: VictimUpdateRequest):
    return update_victim(victim_id, victim_data)

@victim_v1_router.delete("/{victim_id}", response={204: None, 400: dict, 403: dict})
def delete(request, victim_id: int):
    return delete_victim(victim_id)

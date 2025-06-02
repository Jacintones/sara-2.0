from typing import List
from apps.base.dto.victim_dto import VictimCreateRequest, VictimCreateResponse, VictimResponse, VictimUpdateRequest
from ninja import Router
from apps.accounts.auth.role_checker import check_role
from apps.base.enum.role_enum import RoleEnum
from apps.base.di import container

victim_v1_router = Router(tags=["Vítimas"])

@victim_v1_router.post("/", response={201: VictimCreateResponse, 400: dict, 403: dict})
@check_role([RoleEnum.USER])
def create_victim(request, victim_data: VictimCreateRequest):
    return 201, container.victim_service().create_victim(victim_data)

@victim_v1_router.get("/", response={200: List[VictimResponse], 400: dict, 403: dict})
def list_victims(request):
    return container.victim_service().list_victims()

@victim_v1_router.get("/{victim_id}", response={200: VictimResponse, 400: dict, 403: dict})
def get_victim(request, victim_id: int):
    return container.victim_service().get_victim(victim_id)

@victim_v1_router.put("/{victim_id}", response={200: VictimResponse, 400: dict, 403: dict})
def update_victim(request, victim_id: int, victim_data: VictimUpdateRequest):
    return container.victim_service().update_victim(victim_id, victim_data)

@victim_v1_router.delete("/{victim_id}", response={204: None, 400: dict, 403: dict})
def delete_victim(request, victim_id: int):
    container.victim_service().delete_victim(victim_id)
    return None



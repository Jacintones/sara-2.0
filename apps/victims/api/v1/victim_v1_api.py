from typing import List
from apps.victims.dto.victim_dto import VictimCreateRequest, VictimCreateResponse, VictimResponse, VictimUpdateRequest
from ninja import Router
from apps.accounts.auth.role_checker import check_role
from apps.users.enums.role_enum import RoleEnum
from config.di import container

router = Router(tags=["Vítimas"])

@router.post("/", response={201: VictimCreateResponse, 400: dict, 403: dict})
@check_role([RoleEnum.USER])
def create_victim(request, victim_data: VictimCreateRequest):
    return container.victim_service().create_victim(victim_data)

@router.get("/", response={200: List[VictimResponse], 400: dict, 403: dict})
def list_victims(request):
    return container.victim_service().list_victims()

@router.get("/{victim_id}", response={200: VictimResponse, 400: dict, 403: dict})
def get_victim(request, victim_id: int):
    return container.victim_service().get_victim(victim_id)

@router.put("/{victim_id}", response={200: VictimResponse, 400: dict, 403: dict})
def update_victim(request, victim_id: int, victim_data: VictimUpdateRequest):
    return container.victim_service().update_victim(victim_id, victim_data)

@router.delete("/{victim_id}", response={204: None, 400: dict, 403: dict})
def delete_victim(request, victim_id: int):
    container.victim_service().delete_victim(victim_id)
    return None


